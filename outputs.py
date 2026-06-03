"""
outputs.py - dashboard + email, now showing the FULL rationale chain.

Every recommendation surfaces: action, fair value, gap, horizon, conviction, the
reasoning, the explicit deviation from what the market priced in, and the evidence
with receipts. Neither output can place a trade; both lead with the recommend-only
and paper-mode banners.
"""
import html
import datetime as dt


def _pct(x, dp=0):
    return "—" if x is None else f"{x*100:.{dp}f}%"


def _money(x):
    if x is None:
        return "—"
    if abs(x) >= 1e9:
        return f"${x/1e9:.2f}B"
    if abs(x) >= 1e6:
        return f"${x/1e6:.1f}M"
    return f"${x:,.0f}"


_AC = {"BUY": "#0F6E56", "ADD": "#0F6E56", "SELL/TRIM": "#A32D2D",
       "REVIEW": "#854F0B", "RESEARCH": "#185FA5", "HOLD": "#5F5E5A", "PASS": "#8C8B85"}


def _color(a):
    for k, v in _AC.items():
        if a.startswith(k):
            return v
    return "#5F5E5A"


def _banner(paper):
    tag = ("PAPER MODE — recommendations only, no capital committed. Validate edge on "
           "out-of-sample results before funding." if paper else
           "LIVE MODE — recommendations only.")
    return (f'<div style="background:#FCEBEB;border:1px solid #A32D2D;color:#791F1F;'
            f'padding:10px 14px;border-radius:8px;font-size:13px;margin-bottom:18px">'
            f'<b>This engine recommends. You decide and execute.</b><br>{tag}</div>')


def _churn_html(results):
    """Index-membership churn notice: prominent (red) when you HOLD a name that left the
    index; a quieter amber summary of entrants/departures otherwise."""
    c = results.get("universe_churn")
    if not c:
        return ""
    added, removed = c.get("added") or [], c.get("removed") or []
    held_left = c.get("held_left") or []
    if not (added or removed or held_left):
        return ""
    parts = []
    if held_left:
        since = f' since {html.escape(str(c.get("prior_asof")))}' if c.get("prior_asof") else ""
        parts.append(
            f'<div style="background:#FCEBEB;border:1px solid #A32D2D;color:#791F1F;'
            f'padding:10px 14px;border-radius:8px;font-size:13px;margin-bottom:10px">'
            f'<b>⚠ You hold {html.escape(", ".join(held_left))} — left the Russell 2000{since}.</b> '
            f'Still covered below, but a name leaving the index often signals a take-private, '
            f'merger, delisting, or distress. Review it directly.</div>')
    summ = ([f"+{len(added)} entered"] if added else []) + ([f"−{len(removed)} left"] if removed else [])
    if summ:
        ex_rem = (" · left: " + html.escape(", ".join(removed[:8])) + (" …" if len(removed) > 8 else "")) if removed else ""
        ex_add = (" · entered: " + html.escape(", ".join(added[:8])) + (" …" if len(added) > 8 else "")) if added else ""
        parts.append(
            f'<div style="background:#FBF6EC;border:1px solid #B8862B;color:#6B4E0B;'
            f'padding:8px 12px;border-radius:8px;font-size:12px;margin-bottom:18px">'
            f'<b>Index membership change ({" · ".join(summ)})</b>{ex_rem}{ex_add}</div>')
    return "".join(parts)


def _evidence_html(ev):
    if not ev:
        return '<span class="sub">(no evidence captured)</span>'
    out = []
    dircolor = {"supports_higher": "#0F6E56", "supports_lower": "#A32D2D", "risk": "#854F0B"}
    for e in ev:
        c = dircolor.get(e.get("direction"), "#5F5E5A")
        url = e.get("source_url") or ""
        link = (f' <a href="{html.escape(url)}" style="color:#185FA5">[source]</a>'
                if url else "")
        out.append(
            f'<li><span style="color:{c};font-weight:600">{html.escape(e.get("direction",""))}</span> '
            f'— {html.escape((e.get("claim","") or "")[:240])} '
            f'<span class="sub">[{html.escape(e.get("source_form",""))}, '
            f'{html.escape(e.get("source_date","") or "")}]</span>{link}</li>')
    return '<ul style="margin:4px 0;padding-left:18px">' + "".join(out) + "</ul>"


def _drift_html(r):
    d = r.get("thesis_drift_alert")
    if not d:
        return ""
    sev = d.get("severity", 0)
    color = "#A32D2D" if sev >= 3 else "#854F0B" if sev == 2 else "#185FA5"
    changes = "; ".join(d.get("changes", []))
    return (f'<div style="background:#FFF3F3;border-left:4px solid {color};padding:8px 10px;'
            f'margin:8px 0;border-radius:4px;font-size:12px">'
            f'<b style="color:{color}">⚠ THESIS CHANGED (held position):</b> {html.escape(changes)}'
            f'<br><b>→ {html.escape(d.get("recommended_action",""))}</b>'
            f'<br><span class="sub">Fact-driven alert — not a reaction to price movement.</span></div>')


def _news_line(r):
    ns = r.get("news_summary")
    pc = r.get("price_cross_check") or {}
    bits = []
    mat = (ns or {}).get("material_events") if ns else None
    if mat:
        for ev in mat[:2]:
            badge = "✓confirmed" if ev.get("confidence") == "confirmed" else "⊘provisional"
            bits.append(f'⚡ <b>material event</b>: {html.escape(str(ev.get("category")))} '
                        f'({badge})')
    if ns:
        srcs = ", ".join(ns.get("sources") or [])
        bits.append(f"📰 {ns.get('n_stories',0)} stories across [{html.escape(srcs)}]")
    if pc.get("checked"):
        agree = "✓ agrees" if pc.get("agree") else "⚠ DISAGREES"
        bits.append(f"price x-check vs {pc.get('alt_source')}: {agree}")
    if not bits:
        return ""
    return (f'<div class="sub" style="margin-top:4px;color:#6B6A65">'
            + " · ".join(bits) + "</div>")


def _band_range(band):
    """Render the implied-growth band as a readable low–high range regardless of which
    WACC bound produced which value."""
    lo, hi = band.get("at_low_wacc"), band.get("at_high_wacc")
    vals = [v for v in (lo, hi) if v is not None]
    if not vals:
        return "—"
    return f"{min(vals)*100:.1f}%–{max(vals)*100:.1f}%"


def _scenarios_html(t):
    def g(c):
        gr = c.get("growth")
        return f"{gr*100:.1f}%" if isinstance(gr, (int, float)) else "—"
    bull, base, bear = t.get("bull_case") or {}, t.get("base_case") or {}, t.get("bear_case") or {}
    return f"""
<div style="display:flex;gap:8px;margin:8px 0;flex-wrap:wrap">
  <div style="flex:1;min-width:170px;background:#E8F5EE;border:1px solid #0F6E56;border-radius:6px;padding:8px">
    <b style="color:#0F6E56">Bull · g {g(bull)}</b><br><span style="font-size:11px">{html.escape(bull.get('narrative',''))}<br><i>{html.escape(bull.get('what_drives_it',''))}</i></span></div>
  <div style="flex:1;min-width:170px;background:#F1EFE8;border:1px solid #5F5E5A;border-radius:6px;padding:8px">
    <b>Base · g {g(base)}</b><br><span style="font-size:11px">{html.escape(base.get('narrative',''))}<br><i>{html.escape(base.get('what_drives_it',''))}</i></span></div>
  <div style="flex:1;min-width:170px;background:#FCEBEB;border:1px solid #A32D2D;border-radius:6px;padding:8px">
    <b style="color:#A32D2D">Bear · g {g(bear)}</b><br><span style="font-size:11px">{html.escape(bear.get('narrative',''))}<br><i>{html.escape(bear.get('what_drives_it',''))}</i></span></div>
</div>"""


def _catalyst_html(t):
    wmh = t.get("what_must_happen") or []
    items = "".join(f"<li>{html.escape(str(w))}</li>" for w in wmh)
    return f"""
<div style="background:#FBF6EC;border-left:3px solid #854F0B;padding:8px 10px;margin:8px 0">
<b>Catalyst:</b> {html.escape(t.get('catalyst',''))} (≈ {html.escape(t.get('catalyst_date','') or '—')})
&nbsp;·&nbsp; <b>Horizon:</b> {t.get('horizon_months')}m
&nbsp;·&nbsp; <b>Window (pinned):</b> {html.escape(t.get('evaluation_window','') or '—')}
<p style="margin:6px 0 2px"><b>Catalyst pathway:</b> {html.escape(t.get('catalyst_path',''))}</p>
<p style="margin:6px 0 2px"><b>What must happen for the thesis to play out:</b></p>
<ul style="margin:2px 0;padding-left:18px;font-size:12px">{items or '<li>—</li>'}</ul>
</div>"""


def _charts_html(t):
    """Render any chart specs carried in the thesis as inline base64 images. Best-effort:
    a missing matplotlib or a malformed spec just yields no image, never an error."""
    specs = t.get("charts") or []
    if not specs:
        return ""
    try:
        import charts as _charts
    except Exception:
        return ""
    out = []
    for spec in specs:
        try:
            uri = _charts.render_chart_to_datauri(spec)
        except Exception:
            uri = None
        if uri:
            alt = html.escape(spec.get("title", "")) if isinstance(spec, dict) else ""
            out.append(f'<div style="margin:10px 0"><img src="{uri}" alt="{alt}" '
                       'style="max-width:100%;height:auto;border:1px solid #E8E6DE;border-radius:6px"/></div>')
    return "".join(out)


def _thesis_block(r):
    """The expandable full-rationale panel under each actionable row."""
    t = r.get("thesis")
    if not t:
        return ""
    band = r.get("implied_growth_band") or {}
    arch = t.get("thesis_archetype", "")
    arch_color = "#8C8B85" if arch == "none_efficiently_priced" else "#185FA5"
    brief = t.get("company_brief") or ""
    brief_html = (f'<p style="background:#F2F0E8;border-left:3px solid #5F5E5A;padding:8px 10px;'
                  f'margin:0 0 10px"><b>What this company is:</b> {html.escape(brief)}</p>'
                  if brief else "")
    return f"""
<details style="margin-top:6px">
<summary style="cursor:pointer;color:#185FA5;font-size:12px">show full thesis &amp; reasoning</summary>
<div style="background:#FAF9F5;border:1px solid #E8E6DE;border-radius:8px;padding:12px;margin-top:6px;font-size:12px;line-height:1.6">
<div style="margin-bottom:8px">
<span style="background:{arch_color};color:#fff;padding:2px 9px;border-radius:12px;font-size:11px">{html.escape(arch)}</span>
<span class="sub">&nbsp;edge: {html.escape(t.get('edge_source',''))} · conviction {t.get('conviction')}/5</span>
</div>
{brief_html}
<p><b>What the market believes (and why):</b> {html.escape(t.get('market_narrative',''))}</p>
<p><b>Interrogating the consensus:</b> {html.escape(t.get('consensus_interrogation',''))}</p>
<p style="color:#5F5E5A"><i>Implied view:</i> {html.escape(t.get('implied_view_interpretation',''))}
&nbsp;(<span class="sub">implied growth band {_band_range(band)} across WACC ±1%</span>)</p>
<p><b>Perspective spread (sell-side / short / retail / filings):</b> {html.escape(t.get('perspective_spread',''))}</p>
<p style="background:#EEF4FB;padding:8px;border-radius:6px"><b>Our differentiated view:</b> {html.escape(t.get('variant_view',''))}</p>
<p><b>What the market is mis-weighting (mechanism):</b> {html.escape(t.get('mispriced_mechanism',''))}</p>
{_charts_html(t)}
{_scenarios_html(t)}
<p><b>Why our number differs:</b> {html.escape(t.get('deviation_explanation',''))}
&nbsp;<span class="sub">(market implies {_pct(t.get('implied_growth'),1)} → our base {_pct(t.get('variant_growth'),1)})</span></p>
<p><b>Full rationale:</b> {html.escape(t.get('rationale',''))}</p>
{_catalyst_html(t)}
<p><b>Cross-source view:</b> {html.escape(t.get('cross_source_corroboration',''))}</p>
<p><b>Evidence (with receipts):</b></p>{_evidence_html(t.get('evidence'))}
<p><b>Disconfirming (bear case against our view):</b> {html.escape(t.get('disconfirming',''))}</p>
<p><b>Falsification:</b> {html.escape(t.get('falsification',''))}
&nbsp;·&nbsp; <span class="sub">synthesis: {html.escape(r.get('synthesis_source') or '')}</span></p>
</div></details>"""


def _portfolio_html(results):
    p = results.get("portfolio")
    if not p or p.get("error"):
        return ""
    div = p.get("diversification", {})
    name_over = p.get("single_name_overexposure", [])
    sec_over = p.get("sector_overexposure", [])
    sugg = p.get("reweighting_suggestions", [])

    over_rows = ""
    for f in name_over:
        over_rows += (f'<li style="color:#A32D2D">⚠ <b>{html.escape(f["ticker"])}</b> is '
                      f'{f["weight"]*100:.0f}% of the book (cap {p["limits_used"]["max_name"]*100:.0f}%) '
                      f'— over by {f["over_by"]*100:.0f}pp</li>')
    for f in sec_over:
        over_rows += (f'<li style="color:#A32D2D">⚠ <b>{html.escape(f["sector"])}</b> sector is '
                      f'{f["weight"]*100:.0f}% (cap {p["limits_used"]["max_sector"]*100:.0f}%) '
                      f'— over by {f["over_by"]*100:.0f}pp</li>')
    if not over_rows:
        over_rows = '<li style="color:#0F6E56">No concentration limits breached.</li>'

    sugg_rows = ""
    for s in sugg:
        col = "#A32D2D" if "TRIM" in s["action"] else "#0F6E56" if "ADD" in s["action"] else "#5F5E5A"
        harvest = " 🌾 harvest" if s.get("harvest") else ""
        sugg_rows += (f'<tr><td><b>{html.escape(s["ticker"])}</b></td>'
                      f'<td style="color:{col}">{html.escape(s["action"])}{harvest}</td>'
                      f'<td>{s["current_weight"]*100:.0f}% → {s["target_weight"]*100:.0f}%</td>'
                      f'<td>{s["approx_shares"]:+d} sh</td>'
                      f'<td>{(s["gap"]*100):.0f}% gap</td></tr>')
    sugg_table = (f'<table style="width:100%;border-collapse:collapse;font-size:12px;margin-top:6px">'
                  f'<tr><th style="text-align:left">Name</th><th style="text-align:left">Action</th>'
                  f'<th>Weight→Target</th><th>Δ</th><th>Upside</th></tr>{sugg_rows}</table>'
                  if sugg_rows else '<p class="sub">No reweighting suggested — weights near targets.</p>')

    warn_html = "".join(f'<li>{html.escape(w)}</li>' for w in p.get("warnings", []))
    secw = " · ".join(f"{html.escape(s)} {w*100:.0f}%" for s, w in
                      list(p.get("sector_weights", {}).items())[:6])

    return f"""
<div style="background:#fff;border:2px solid #185FA5;border-radius:12px;padding:16px;margin:18px 0">
<h2 style="margin:0 0 8px;font-size:17px">Portfolio overview</h2>
<div style="font-size:13px;color:#5F5E5A;margin-bottom:8px">
Total value ${p['total_value']:,.0f} · {p['n_positions']} positions ·
<b>{div.get('correlation_adjusted_effective_bets','—')} effective bets</b>
(naive {div.get('naive_effective_positions','—')}, avg corr {div.get('avg_pairwise_correlation','—')})</div>
<div style="font-size:12px;margin-bottom:8px"><b>Sectors:</b> {secw}</div>
<p style="margin:8px 0 4px"><b>Concentration:</b></p>
<ul style="margin:2px 0;padding-left:18px;font-size:12px">{over_rows}</ul>
<p style="margin:8px 0 4px"><b>Reweighting (monthly cadence — not for daily price drift):</b></p>
{sugg_table}
<p style="margin:10px 0 4px"><b>Structural watch:</b></p>
<ul style="margin:2px 0;padding-left:18px;font-size:11px;color:#7A7972">{warn_html}</ul>
<div class="sub" style="margin-top:6px">{html.escape(p.get('note',''))}</div>
</div>"""


def build_dashboard(results, path):
    rows = results["rows"]
    generated = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    cards = []
    for r in rows:
        if r.get("error"):
            cards.append(f'<div class="row"><b>{html.escape(r["ticker"])}</b> '
                         f'<span style="color:#A32D2D">error: {r["error"]}</span></div>')
            continue
        rec = r["recommendation"]
        ov = r.get("our_view") or {}
        gap = ov.get("gap_vs_price")
        ac = _color(rec["action"])
        flags = ", ".join(r.get("reliability_flags") or []) or "clean"
        held = " 📌" if r.get("held") else ""
        fv = ov.get("fair_value")
        gapcol = "#0F6E56" if (gap or 0) > 0 else "#A32D2D" if gap else "#5F5E5A"
        cb = (r.get("thesis") or {}).get("company_brief", "") or ""
        brief_row = (f'<div class="sub" style="margin:3px 0 6px;font-style:italic">'
                     f'{html.escape(cb[:185])}{"…" if len(cb) > 185 else ""}</div>') if cb else ""
        cards.append(f"""
<div class="row">
  <div class="rowhead">
    <div><span class="tk">{html.escape(r['ticker'])}</span>{held}{'<span style="background:#A32D2D;color:#fff;padding:1px 7px;border-radius:10px;font-size:10px;margin-left:6px">⚠ LEFT INDEX</span>' if r.get('left_index') else ''}
      <span class="sub">{html.escape((r['name'] or '')[:30])} · {html.escape(r.get('sector',''))}</span>{'<span class="sub" style="color:#9a7b00">&nbsp;· scan only, not re-analyzed today</span>' if r.get('_stale') else ''}</div>
    <span class="pill" style="background:{ac}">{html.escape(rec['action'])}</span>
  </div>
  {brief_row}
  <div class="metrics">
    <span>Price <b>{('$%.2f' % r['price']) if r.get('price') is not None else '—'}</b></span>
    <span>Fair value <b>{_money(fv) if fv else '—'}</b></span>
    <span>Gap <b style="color:{gapcol}">{_pct(gap) if gap is not None else '—'}</b></span>
    <span>Implied g <b>{_pct(r.get('implied_growth'),1)}</b></span>
    <span>Our g <b>{_pct((r.get('thesis') or {}).get('variant_growth'),1)}</b></span>
    <span>WACC <b>{_pct(r.get('wacc'),1)}</b></span>
    <span>Beta <b>{('%.2f'%r['beta_adjusted']) if r.get('beta_adjusted') else '—'}</b></span>
    <span>Liquidity <b>{_money(r.get('adv_usd'))}/d</b></span>
    <span class="sub">{html.escape(flags)}</span>
  </div>
  <div class="sub">{html.escape(rec['reason'])}{' · size: '+rec['sizing'] if rec.get('sizing') else ''}</div>
  {_drift_html(r)}
  {_news_line(r)}
  {_thesis_block(r)}
</div>""")

    doc = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Equity Engine — Recommendations</title><style>
body{{margin:0;background:#F5F4EF;color:#2C2C2A;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}}
.wrap{{max-width:920px;margin:0 auto;padding:28px 18px 60px}}
h1{{font-size:22px;font-weight:600;margin:0 0 2px}}
.meta{{color:#5F5E5A;font-size:13px;margin:0 0 18px}}
.row{{background:#fff;border:1px solid #E0DED5;border-radius:12px;padding:14px 16px;margin-bottom:12px}}
.rowhead{{display:flex;justify-content:space-between;align-items:flex-start}}
.tk{{font-size:17px;font-weight:700}}
.sub{{color:#7A7972;font-size:11px}}
.pill{{color:#fff;padding:4px 11px;border-radius:20px;font-size:12px;font-weight:600;white-space:nowrap}}
.metrics{{display:flex;flex-wrap:wrap;gap:14px;margin:10px 0 6px;font-size:13px}}
.metrics span{{color:#5F5E5A}}
details summary::-webkit-details-marker{{display:none}}
</style></head><body><div class="wrap">
<h1>Equity Engine — Recommendations</h1>
<div class="meta">Russell 2000 universe · generated {generated} · ranked by reliability-weighted gap</div>
{_banner(results.get('paper_mode', True))}
{_churn_html(results)}
{_portfolio_html(results)}
{''.join(cards)}
<div class="sub" style="margin-top:16px;line-height:1.7">
📌 = position you hold · <b>Implied g</b> = growth the market's price requires (reverse DCF) ·
<b>Our g</b> = growth our synthesis supports · <b>Gap</b> = fair value vs price.
Every action expands to its full reasoning, deviation from the market, and evidence with sources.
Sizing buckets are suggestions, not orders.
</div></div></body></html>"""
    with open(path, "w") as f:
        f.write(doc)
    return path


def build_email(results, path):
    rows = results["rows"]
    holds = [r for r in rows if not r.get("error") and not r.get("_stale") and r.get("held")
             and r["recommendation"]["action"] in ("SELL/TRIM", "ADD", "REVIEW")]
    buys = [r for r in rows if not r.get("error") and not r.get("_stale") and not r.get("held")
            and r["recommendation"]["action"].startswith("BUY")][:5]

    def block(r):
        rec = r["recommendation"]
        t = r.get("thesis") or {}
        ac = _color(rec["action"])
        cb = (t.get("company_brief") or "")
        brief_line = (f'<div style="font-size:12px;color:#6b6a64;margin:4px 0">'
                      f'{html.escape(cb[:200])}{"…" if len(cb) > 200 else ""}</div>') if cb else ""
        return f"""<div style="border:1px solid #E0DED5;border-radius:8px;padding:12px;margin-bottom:10px">
<div><b>{html.escape(r['ticker'])}</b> <span style="color:#7A7972;font-size:12px">{html.escape((r['name'] or '')[:30])}</span>
&nbsp;<span style="background:{ac};color:#fff;padding:2px 9px;border-radius:12px;font-size:12px">{html.escape(rec['action'])}</span></div>
{brief_line}
<div style="font-size:13px;margin:6px 0">{('$%.2f' % r['price']) if r.get('price') is not None else '—'} → fair value {_money(t.get('fair_value'))} ({_pct(t.get('gap_vs_price'))}) · {html.escape(rec['reason'])}</div>
<div style="font-size:12px;color:#444;line-height:1.5"><b>Thesis:</b> {html.escape(t.get('thesis_archetype',''))} · {html.escape(t.get('variant_view','')[:200])}</div>
<div style="font-size:12px;color:#444;margin-top:4px"><b>Market mis-weighting:</b> {html.escape(t.get('mispriced_mechanism','')[:240])}</div>
<div style="font-size:12px;color:#444;margin-top:4px"><b>Catalyst:</b> {html.escape(t.get('catalyst',''))} · <b>horizon</b> {t.get('horizon_months')}m · <b>conviction</b> {t.get('conviction')}/5</div>
</div>"""

    sec = ""
    if holds:
        sec += '<h3 style="margin:18px 0 6px">Your positions — action flagged</h3>' + "".join(block(r) for r in holds)
    if buys:
        sec += '<h3 style="margin:18px 0 6px">New buy candidates</h3>' + "".join(block(r) for r in buys)
    if not sec:
        sec = ('<p style="color:#5F5E5A">No actions flagged on holdings and no new buy '
               'candidates cleared the bar this run. Full detail in the dashboard.</p>')

    _hl = (results.get("universe_churn") or {}).get("held_left") or []
    churn_note = ((f'<div style="border:1px solid #A32D2D;background:#FCEBEB;color:#791F1F;'
                   f'border-radius:8px;padding:10px;margin-bottom:10px;font-size:13px">'
                   f'<b>⚠ Index departure:</b> you hold {html.escape(", ".join(_hl))}, which left '
                   f'the Russell 2000 — review for take-private / delisting / distress.</div>')
                  if _hl else "")

    doc = f"""<div style="font-family:-apple-system,Arial,sans-serif;max-width:660px;margin:0 auto;color:#2C2C2A">
<h2 style="margin:0 0 2px">Equity Engine brief</h2>
<div style="color:#5F5E5A;font-size:13px;margin-bottom:14px">{dt.datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
{_banner(results.get('paper_mode', True))}{churn_note}{sec}
<p style="color:#7A7972;font-size:12px;margin-top:20px">Recommendations only. Open Robinhood and place any trades yourself. Not investment advice.</p></div>"""
    with open(path, "w") as f:
        f.write(doc)
    return path
