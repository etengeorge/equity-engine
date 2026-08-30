"""Build the static dashboard Vercel serves. One self-contained file, no dependencies."""
import json, html, datetime as dt
import config

CSS = """
:root{--bg:#fbfbfa;--panel:#fff;--ink:#1a1a19;--dim:#6b6b66;--line:#e5e4e0;
--pos:#0f7b4f;--neg:#b3261e;--warn:#8a6100;--accent:#2f5fd0;--chip:#f0efec}
@media(prefers-color-scheme:dark){:root{--bg:#141413;--panel:#1c1c1a;--ink:#eeeeec;
--dim:#9a9a94;--line:#2e2e2b;--pos:#4ec38a;--neg:#f08279;--warn:#d9a441;
--accent:#7aa2f7;--chip:#262623}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.55 ui-sans-serif,-apple-system,"Segoe UI",Inter,system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 80px}
h1{font-size:23px;margin:0 0 4px;letter-spacing:-.02em}
h2{font-size:16px;margin:38px 0 10px;letter-spacing:-.01em}
h2 .n{color:var(--dim);font-weight:400}
.sub{color:var(--dim);font-size:13px;margin:0}
.banner{background:var(--chip);border:1px solid var(--line);border-left:3px solid var(--accent);
padding:11px 14px;border-radius:7px;margin:18px 0;font-size:13.5px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(158px,1fr));gap:10px;margin:16px 0}
.card{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:12px 14px}
.card .k{color:var(--dim);font-size:11.5px;text-transform:uppercase;letter-spacing:.05em}
.card .v{font-size:22px;font-weight:600;letter-spacing:-.02em;margin-top:3px}
.card .s{color:var(--dim);font-size:12px;margin-top:2px}
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:9px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:8px 11px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
th{background:var(--chip);font-weight:600;font-size:12px;color:var(--dim);
text-transform:uppercase;letter-spacing:.04em;position:sticky;top:0;cursor:pointer;user-select:none}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--chip)}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.pos{color:var(--pos)}.neg{color:var(--neg)}.dim{color:var(--dim)}
.tick{font-weight:650}
.chip{display:inline-block;background:var(--chip);border:1px solid var(--line);
border-radius:20px;padding:1px 9px;font-size:11.5px;color:var(--dim);margin:0 3px 3px 0}
.chip.warn{color:var(--warn);border-color:var(--warn)}
.v-cheap{color:var(--pos);font-weight:600}.v-rich{color:var(--neg);font-weight:600}
.v-fair,.v-no_edge,.v-no_model{color:var(--dim)}
.bar{height:7px;background:var(--chip);border-radius:4px;overflow:hidden;margin-top:7px}
.bar>i{display:block;height:100%;background:var(--accent)}
details{margin-top:10px}summary{cursor:pointer;color:var(--dim);font-size:13px}
.why{color:var(--dim);font-size:12.5px;white-space:normal;max-width:430px}
footer{margin-top:48px;padding-top:18px;border-top:1px solid var(--line);
color:var(--dim);font-size:12.5px}
code{background:var(--chip);padding:1px 5px;border-radius:4px;font-size:12px}
"""

JS = """
document.querySelectorAll('table').forEach(function(t){
  t.querySelectorAll('th').forEach(function(th,i){
    th.addEventListener('click',function(){
      var tb=t.tBodies[0],rows=[].slice.call(tb.rows),asc=th.dataset.asc!=='1';
      t.querySelectorAll('th').forEach(function(x){x.dataset.asc=''});
      th.dataset.asc=asc?'1':'0';
      rows.sort(function(a,b){
        var x=a.cells[i].dataset.v,y=b.cells[i].dataset.v;
        var nx=parseFloat(x),ny=parseFloat(y);
        if(!isNaN(nx)&&!isNaN(ny))return asc?nx-ny:ny-nx;
        x=(x||a.cells[i].textContent).trim();y=(y||b.cells[i].textContent).trim();
        return asc?x.localeCompare(y):y.localeCompare(x);
      });
      rows.forEach(function(r){tb.appendChild(r)});
    });
  });
});
"""


def _pct(x, cls=True):
    if x is None:
        return '<td class="num dim" data-v="">—</td>'
    c = "pos" if x > 0 else ("neg" if x < 0 else "dim")
    return f'<td class="num {c if cls else ""}" data-v="{x}">{x*100:+.1f}%</td>'


def _usd(x, nd=2):
    if x is None:
        return '<td class="num dim" data-v="">—</td>'
    return f'<td class="num" data-v="{x}">${x:,.{nd}f}</td>'


def _cap(x):
    if x is None:
        return '<td class="num dim" data-v="">—</td>'
    for u, d in (("B", 1e9), ("M", 1e6)):
        if abs(x) >= d:
            return f'<td class="num" data-v="{x}">${x/d:,.1f}{u}</td>'
    return f'<td class="num" data-v="{x}">${x:,.0f}</td>'


def _e(s):
    return html.escape(str(s if s is not None else ""))


def _table(rows, cols):
    h = "".join(f"<th>{c}</th>" for c in cols)
    return (f'<div class="scroll"><table><thead><tr>{h}</tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def build(screen, picks=None, verdicts=None, out=None):
    picks = picks or []
    verdicts = verdicts or []
    gen = screen.get("generated_utc", "")
    a = screen["assumptions"]
    rows = screen["rows"]
    modelled = [r for r in rows
                if r.get("gap") is not None
                and abs(r["gap"]) <= config.MAX_ABS_GAP
                and "illiquid_below_min_dollar_volume" not in (r.get("flags") or [])
                and "below_min_market_cap" not in (r.get("flags") or [])]
    covered = len({v["ticker"] for v in verdicts})
    n = len(rows)

    P = []
    A = P.append
    A(f"<h1>Equity Engine</h1><p class='sub'>Russell 2000 · screen generated {_e(gen)} UTC · "
      f"risk-free {screen.get('risk_free_rate',0)*100:.2f}% ({_e(screen.get('risk_free_source'))})</p>")
    A("<div class='banner'><strong>This engine screens and recommends. "
      "You decide and you execute.</strong> Nothing here is a trade instruction, and no "
      "part of this system can place one. Every number below is a starting point for your "
      "own research, not a conclusion.</div>")

    # --- headline numbers
    cheap = sorted([r for r in modelled if r["gap"] > 0], key=lambda r: -r["gap"])
    rich = sorted([r for r in modelled if r["gap"] < 0], key=lambda r: r["gap"])
    A("<div class='grid'>")
    A(f"<div class='card'><div class='k'>Universe</div><div class='v'>{n:,}</div>"
      f"<div class='s'>fixed constituents</div></div>")
    all_modelled = sum(1 for r in rows if r.get("gap") is not None)
    A(f"<div class='card'><div class='k'>Priced &amp; tradable</div><div class='v'>{len(modelled):,}</div>"
      f"<div class='s'>{all_modelled:,} priced, minus illiquid and sub-scale; "
      f"{n-all_modelled:,} refused a number</div></div>")
    A(f"<div class='card'><div class='k'>Researched</div><div class='v'>{covered:,}</div>"
      f"<div class='s'>{covered/n*100:.1f}% of the index</div>"
      f"<div class='bar'><i style='width:{min(100,covered/n*100):.1f}%'></i></div></div>")
    A(f"<div class='card'><div class='k'>Screened cheap</div><div class='v pos'>{len(cheap):,}</div>"
      f"<div class='s'>baseline fair value &gt; price</div></div>")
    A(f"<div class='card'><div class='k'>Screened rich</div><div class='v neg'>{len(rich):,}</div>"
      f"<div class='s'>baseline fair value &lt; price</div></div>")
    A("</div>")

    # --- sector shocks
    shocks = (picks[0] or {}).get("_shocks") if picks else None
    if shocks:
        A("<h2>Sector moves driving today's priorities</h2>")
        A("<p class='sub'>Detected from the tape, not from a news feed: a sector whose "
          "median 5-day return has moved hard pulls its worst-hit names forward in the queue.</p>")
        for sec, s in sorted(shocks.items(), key=lambda kv: kv[1]["median"]):
            cls = "neg" if s["median"] < 0 else "pos"
            A(f"<span class='chip'>{_e(sec)} <b class='{cls}'>{s['median']*100:+.1f}%</b> "
              f"median 5d ({s['n']} names)</span>")

    # --- today's ten
    if picks:
        A(f"<h2>Today's ten <span class='n'>· {len(picks)} names selected for deep research</span></h2>")
        vmap = {v["ticker"]: v for v in verdicts}
        tr = []
        for p in picks:
            r = p["row"]
            v = vmap.get(p["ticker"], {})
            pr = v.get("priced") or {}
            verdict = v.get("verdict")
            vc = (f"<td class='v-{verdict}' data-v='{verdict}'>{_e(verdict)}</td>"
                  if verdict else "<td class='dim' data-v=''>pending</td>")
            tr.append(
                f"<tr><td class='tick' data-v='{_e(p['ticker'])}'>{_e(p['ticker'])}</td>"
                f"<td data-v='{_e(r.get('name'))}'>{_e(r.get('name'))}</td>"
                f"<td data-v='{_e(r['sector'])}'>{_e(r['sector'])}</td>"
                f"<td data-v='{_e(p['slot'])}'><span class='chip'>{_e(p['slot'])}</span></td>"
                + _usd(r.get("price")) + _pct(r.get("ret_21d"))
                + _pct(r.get("implied_growth")) + _pct(r.get("gap"))
                + (_pct(pr.get("gap")) if pr.get("ok") else "<td class='num dim' data-v=''>—</td>")
                + vc
                + f"<td class='why' data-v=''>{_e('; '.join(p['why'][:3]))}</td></tr>")
        A(_table(tr, ["Ticker", "Name", "Sector", "Slot", "Price", "21d",
                      "Mkt implied g", "Baseline gap", "Analyst gap", "Verdict",
                      "Why selected"]))

    # --- researched leaderboard
    if verdicts:
        A(f"<h2>Researched names <span class='n'>· {len(verdicts)} with a written thesis</span></h2>")
        A("<p class='sub'>These have been through the full loop: news, own assumptions, "
          "and an adversarial pass. Sorted by the analyst's gap, not the screen's.</p>")
        vs = sorted(verdicts,
                    key=lambda v: -((v.get("priced") or {}).get("gap") or -9))
        tr = []
        for v in vs[:80]:
            pr = v.get("priced") or {}
            tr.append(
                f"<tr><td class='tick' data-v='{_e(v['ticker'])}'>{_e(v['ticker'])}</td>"
                f"<td data-v='{_e(v.get('name'))}'>{_e(v.get('name'))}</td>"
                f"<td data-v='{_e(v['sector'])}'>{_e(v['sector'])}</td>"
                f"<td class='v-{v['verdict']}' data-v='{v['verdict']}'>{_e(v['verdict'])}</td>"
                f"<td data-v='{_e(v.get('conviction'))}'>{_e(v.get('conviction'))}</td>"
                + _usd(v.get("price_at_verdict"))
                + _pct(v.get("market_implied_growth")) + _pct(v.get("final_growth"))
                + (_pct(pr.get("gap")) if pr.get("ok") else "<td class='num dim' data-v=''>—</td>")
                + f"<td class='dim' data-v='{_e(v['date'])}'>{_e(v['date'])}</td></tr>")
        A(_table(tr, ["Ticker", "Name", "Sector", "Verdict", "Conviction", "Price",
                      "Mkt implied g", "Analyst g", "Analyst gap", "Dated"]))

    # --- raw screen
    A(f"<h2>Screen — widest baseline gaps <span class='n'>· mechanical, no judgment applied</span></h2>")
    A("<p class='sub'>Every name priced off its own history, nothing more. This ranks "
      "candidates for research; it is not a view. Illiquid and sub-scale names are excluded, "
      "and gaps beyond ±300% are treated as data errors and dropped.</p>")
    tr = []
    for r in (cheap[:60] + rich[:25]):
        fl = "".join(f"<span class='chip warn'>{_e(f.split('(')[0][:26])}</span>"
                     for f in (r.get("flags") or [])[:2])
        tr.append(
            f"<tr><td class='tick' data-v='{_e(r['ticker'])}'>{_e(r['ticker'])}</td>"
            f"<td data-v='{_e(r.get('name'))}'>{_e(r.get('name'))}</td>"
            f"<td data-v='{_e(r['sector'])}'>{_e(r['sector'])}</td>"
            f"<td data-v='{_e(r.get('method'))}'>{_e(r.get('method'))}</td>"
            + _usd(r.get("price")) + _cap(r.get("market_cap"))
            + _pct(r.get("implied_growth")) + _pct(r.get("baseline_growth"))
            + _pct(r.get("gap"))
            + f"<td class='num' data-v='{r.get('cohort_pct') if r.get('cohort_pct') is not None else ''}'>"
              f"{r.get('cohort_pct') if r.get('cohort_pct') is not None else '—'}</td>"
            + f"<td data-v=''>{fl}</td></tr>")
    A(_table(tr, ["Ticker", "Name", "Sector", "Method", "Price", "Mkt cap",
                  "Mkt implied g", "Baseline g", "Gap", "Cohort %ile", "Flags"]))

    # --- method + honesty
    counts = screen.get("counts", {})
    A("<h2>How to read this, and where it is weak</h2>")
    A("<details open><summary>Method</summary><p class='sub'>"
      "Each name is priced twice with the same two-stage model. <b>Reverse DCF:</b> solve for "
      "the 5-year free-cash-flow growth that makes the model reproduce today's enterprise "
      "value — that is what the market is assuming. <b>Forward DCF:</b> price an assumption "
      "of our own and compare. On this page the forward number is a mechanical baseline "
      "(the company's own revenue history), which is why it carries no judgment. The ten "
      "researched names each day replace that baseline with a real one.<br><br>"
      "Financials get justified price-to-tangible-book from sustainable return on tangible "
      "equity instead — free cash flow to the firm is meaningless when debt is raw material. "
      "REITs and companies with negative normalized cash flow get no number at all.</p></details>")
    A(f"<details><summary>Assumptions that move every number on this page</summary>"
      f"<p class='sub'>Equity risk premium <code>{a['equity_risk_premium']:.1%}</code> · "
      f"terminal growth <code>{a['terminal_growth']:.1%}</code> · "
      f"explicit forecast <code>{a['explicit_years']}y</code> · "
      f"tax <code>{a['marginal_tax_rate']:.0%}</code>. "
      "These are choices, not facts, and they shift every absolute gap in the same direction. "
      "That is exactly why the cohort percentile column exists: it compares a name to its own "
      "sector under identical assumptions, so a whole sector cannot look cheap because of a "
      "constant chosen here. Implied growth is also reported at ±1pt of WACC on each brief, "
      "because it is far more sensitive to the discount rate than to anything else.</p></details>")
    A("<details><summary>What this screen cannot do</summary><p class='sub'>"
      "It cannot value pre-revenue biotech, bitcoin miners, or anything with negative "
      "normalized free cash flow — those are refused rather than guessed at. It cannot see "
      "off-balance-sheet obligations, segment detail, or anything not tagged in XBRL. "
      "A single lumpy year still distorts a three-year cash-flow base, which is why briefs "
      "carry dispersion flags. Prices are end-of-day. Fundamentals are as of the last annual "
      "filing and can be up to a year stale.</p></details>")
    A(f"<details><summary>Coverage detail</summary><p class='sub'>"
      + " · ".join(f"<code>{_e(k)}</code> {v}" for k, v in counts.items())
      + "</p></details>")

    A(f"<footer>Built from free sources only: SEC EDGAR XBRL company facts and end-of-day "
      f"prices. No paid data, no paywalled sources, no order-placement path anywhere in this "
      f"system.<br>Universe frozen from the iShares Russell 2000 holdings file; index "
      f"membership drifts between reconstitutions.</footer>")

    doc = (f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
           f"<meta name='viewport' content='width=device-width,initial-scale=1'>"
           f"<title>Equity Engine — Russell 2000 screen</title>"
           f"<style>{CSS}</style></head><body><div class='wrap'>"
           + "".join(P) + f"</div><script>{JS}</script></body></html>")
    out = out or (config.PUBLIC / "index.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    return out
