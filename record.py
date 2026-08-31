"""Take the analyst's JSON, re-price it through the DCF, and commit it to memory.

This is the second DCF pass. The analyst supplies ONE number that moves money —
`final_growth` — and this module prices it. Everything else in their JSON is the audit
trail explaining why. If the JSON is malformed we record the failure; we never fill in a
plausible-looking number on the analyst's behalf.
"""
import json, re, datetime as dt
import config, edgar, valuation as V, brief

GROWTH_BOUNDS = (-0.30, 0.40)
VERDICTS = {"cheap", "fair", "rich", "no_model", "no_edge"}
CONVICTIONS = {"low", "medium", "high"}


def parse(raw):
    """Tolerate fenced blocks and stray prose; refuse to guess at missing judgment."""
    if isinstance(raw, dict):
        obj = raw
    else:
        text = raw.strip()
        m = re.search(r"```(?:json)?\s*(.+?)```", text, re.S)
        if m:
            text = m.group(1).strip()
        else:
            i, j = text.find("{"), text.rfind("}")
            if i >= 0 and j > i:
                text = text[i:j + 1]
        obj = json.loads(text)

    notes = []
    g = obj.get("final_growth", obj.get("base_case_growth"))
    if isinstance(g, str):
        try:
            g = float(g.strip().rstrip("%")) / (100 if "%" in g else 1)
        except ValueError:
            g = None
    if isinstance(g, (int, float)):
        if abs(g) > 1.0:                      # someone wrote 5 meaning 5%
            g = g / 100.0
            notes.append("final_growth looked like a percent; divided by 100")
        lo, hi = GROWTH_BOUNDS
        if g < lo or g > hi:
            notes.append(f"final_growth {g:+.1%} clamped into {lo:+.0%}..{hi:+.0%}")
            g = min(max(g, lo), hi)
    else:
        g = None
        notes.append("no usable final_growth")

    verdict = str(obj.get("verdict", "")).strip().lower()
    if verdict not in VERDICTS:
        notes.append(f"unrecognised verdict {verdict!r} -> no_edge")
        verdict = "no_edge"
    conviction = str(obj.get("conviction", "")).strip().lower()
    if conviction not in CONVICTIONS:
        conviction = "low"
        notes.append("conviction missing or invalid -> low")

    da = obj.get("devils_advocate") or {}
    if not isinstance(da, dict) or not da.get("strongest_counter"):
        notes.append("devil's advocate section missing or empty — verdict is UNCHALLENGED")

    obj.update(final_growth=g, verdict=verdict, conviction=conviction,
               _parse_notes=notes)
    return obj


def reprice(obj, screen_row, rf):
    """Price the analyst's own assumption. Returns the second half of the two-sided model."""
    if screen_row.get("method") != "fcff" or obj.get("final_growth") is None:
        return {"ok": False, "reason": "not a repriceable fcff name or no growth supplied"}
    cik = screen_row.get("cik")
    if not cik:
        return {"ok": False, "reason": "no cik"}
    # Use the committed extract, not a fresh companyfacts pull. The forward pass runs in the
    # analyst's runtime, which has no SEC egress; re-fetching raw XBRL here made every
    # reprice fail silently and left the dashboard with a screen and no second opinion.
    fund, fund_source = edgar.fundamentals_cached(cik)
    w = V.cost_of_capital(fund, screen_row["price"], screen_row.get("beta"),
                          None, rf)
    override = obj.get("fcff_base_override")
    fd = V.forward_dcf(fund, screen_row["price"], w, obj["final_growth"],
                       fcff_base=override if isinstance(override, (int, float)) else None)
    if not fd.get("ok"):
        return {"ok": False, "reason": ",".join(fd.get("flags", []))}
    implied = screen_row.get("implied_growth")
    return {
        "ok": True,
        "analyst_growth": obj["final_growth"],
        "market_implied_growth": implied,
        "growth_delta": (obj["final_growth"] - implied) if implied is not None else None,
        "fair_value": fd["fair_value"],
        "price": fd["price"],
        "gap": fd["gap"],
        "fair_value_band": fd["fair_value_band"],
        "fcff_base_used": fd["fcff_base_used"],
        "base_overridden": isinstance(override, (int, float)),
        "fundamentals_source": fund_source,
        "flags": fd.get("flags", []),
    }


def _pct(x):
    return "n/a" if x is None else f"{x*100:+.1f}%"


def _usd(x):
    if x is None:
        return "n/a"
    for u, d in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(x) >= d:
            return f"${x/d:,.1f}{u}"
    return f"${x:,.2f}"


def to_markdown(obj, row, priced, today):
    da = obj.get("devils_advocate") or {}
    L = [f"\n## {today} — {obj.get('verdict','?').upper()}"
         f" (conviction: {obj.get('conviction','?')})", ""]
    L.append(f"- **Verdict:** {obj.get('verdict')} · price {_usd(row.get('price'))}"
             + (f" · fair value {_usd(priced['fair_value'])} · gap {_pct(priced['gap'])}"
                if priced.get("ok") else ""))
    if priced.get("ok"):
        L.append(f"- **Growth:** market implies {_pct(priced['market_implied_growth'])}, "
                 f"analyst says {_pct(priced['analyst_growth'])} "
                 f"(delta {_pct(priced['growth_delta'])})")
        if priced.get("base_overridden"):
            L.append(f"- **FCFF base overridden** by the analyst to "
                     f"{_usd(priced['fcff_base_used'])}")
    elif row.get("method") == "fcff":
        L.append(f"- **Not repriced:** {priced.get('reason')}")
    L += ["", f"**The case for the price.** {obj.get('consensus_case','—')}", "",
          f"**What changed.** {obj.get('what_changed','—')}", "",
          f"**Base case.** {obj.get('base_case_rationale','—')}", "",
          "**Devil's advocate.**",
          f"- Strongest counter: {da.get('strongest_counter','— NOT ARGUED —')}",
          f"- What would prove it: {da.get('what_would_prove_it','—')}",
          f"- Already visible today: {da.get('already_visible','—')}",
          f"- Left unresolved: {da.get('unresolved','—')}", ""]
    if obj.get("key_risks"):
        L.append("**Key risks.** " + "; ".join(str(x) for x in obj["key_risks"]))
    if obj.get("watch_for"):
        L.append("**Watch for.** " + "; ".join(str(x) for x in obj["watch_for"]))
    if obj.get("data_quality_note"):
        L.append(f"\n**Data quality.** {obj['data_quality_note']}")
    if obj.get("horizon_months"):
        L.append(f"\n*Horizon: {obj['horizon_months']} months — "
                 f"re-evaluate no earlier than that unless something on the watch list fires.*")
    if obj.get("sources"):
        L.append("\n**Sources.**")
        L += [f"- {s}" for s in obj["sources"]]
    if obj.get("_parse_notes"):
        L.append("\n**Ingestion notes.** " + "; ".join(obj["_parse_notes"]))
    return "\n".join(L) + "\n"


def record_one(ticker, raw, screen_row, rf, today=None):
    today = today or dt.date.today().isoformat()
    obj = parse(raw)
    obj["ticker"] = ticker
    try:
        priced = reprice(obj, screen_row, rf)
    except Exception as e:
        priced = {"ok": False, "reason": f"{type(e).__name__}: {e}"}

    path = brief.research_path(screen_row["sector"], ticker)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# {ticker} — {screen_row.get('name','')}\n"
                        f"*{screen_row['sector']} · Russell 2000*\n\n"
                        f"Append-only research log. Newest entries at the bottom.\n")
    with path.open("a") as fh:
        fh.write(to_markdown(obj, screen_row, priced, today))

    verdict = {"ticker": ticker, "date": today, "sector": screen_row["sector"],
               "name": screen_row.get("name"), "method": screen_row.get("method"),
               "verdict": obj["verdict"], "conviction": obj["conviction"],
               "final_growth": obj["final_growth"],
               "horizon_months": obj.get("horizon_months"),
               "price_at_verdict": screen_row.get("price"),
               "market_implied_growth": screen_row.get("implied_growth"),
               "cohort_pct": screen_row.get("cohort_pct"),
               "priced": priced, "parse_notes": obj["_parse_notes"],
               "devils_advocate": obj.get("devils_advocate"),
               "what_changed": obj.get("what_changed"),
               "consensus_case": obj.get("consensus_case"),
               # the actual argument for the number. It was only ever written to the
               # markdown log, so the machine-readable verdict — the thing the dashboard
               # and the retrospective read — carried everything EXCEPT the reasoning.
               "base_case_rationale": obj.get("base_case_rationale"),
               "key_risks": obj.get("key_risks"), "watch_for": obj.get("watch_for"),
               "sources": obj.get("sources"), "flags": screen_row.get("flags", [])}
    vdir = config.DATA / "verdicts"
    vdir.mkdir(parents=True, exist_ok=True)
    (vdir / f"{ticker}.json").write_text(json.dumps(verdict, indent=2, default=float))

    vp = config.DATA / "visits.json"
    visits = json.loads(vp.read_text()) if vp.exists() else {}
    visits[ticker] = {"last_visit": today, "verdict": obj["verdict"],
                      "conviction": obj["conviction"]}
    vp.write_text(json.dumps(visits, indent=2, sort_keys=True))
    return verdict
