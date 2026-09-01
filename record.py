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

    def _rate(value, label, bounds=GROWTH_BOUNDS):
        """Coerce one analyst-supplied rate. Tolerates '7.5%', '0.075' and 7.5, clamps
        into bounds, and records every coercion so the dashboard shows what was changed."""
        v = value
        if isinstance(v, str):
            try:
                v = float(v.strip().rstrip("%")) / (100 if "%" in v else 1)
            except ValueError:
                return None
        if not isinstance(v, (int, float)):
            return None
        if abs(v) > 1.0:                      # someone wrote 5 meaning 5%
            v = v / 100.0
            notes.append(f"{label} looked like a percent; divided by 100")
        lo, hi = bounds
        if v < lo or v > hi:
            notes.append(f"{label} {v:+.1%} clamped into {lo:+.0%}..{hi:+.0%}")
            v = min(max(v, lo), hi)
        return v

    g = _rate(obj.get("final_growth", obj.get("base_case_growth")), "final_growth")
    if g is None:
        notes.append("no usable final_growth")
    bear = _rate(obj.get("bear_growth"), "bear_growth")
    bull = _rate(obj.get("bull_growth"), "bull_growth")
    # Order bear and bull against EACH OTHER, never against the base case. `final_growth`
    # is the number that drives the headline valuation and the recorded verdict, so
    # silently moving it would rewrite the thesis; a mislabelled pair is just relabelled.
    if bear is not None and bull is not None and bear > bull:
        notes.append("bear_growth was above bull_growth — labels swapped")
        bear, bull = bull, bear
    if g is not None:
        if bear is not None and bear > g:
            notes.append(f"bear_growth {bear:+.1%} sits ABOVE the base case {g:+.1%} — "
                         "left as supplied; the scenario grid will read out of order")
        if bull is not None and bull < g:
            notes.append(f"bull_growth {bull:+.1%} sits BELOW the base case {g:+.1%} — "
                         "left as supplied; the scenario grid will read out of order")
    # A sustainable ROTCE is a return, not a growth rate: it can legitimately be 25% for
    # a good lender, so it gets its own wider bounds.
    rotce = _rate(obj.get("rotce_override"), "rotce_override", bounds=(-0.20, 0.60))
    obj["bear_growth"], obj["bull_growth"], obj["rotce_override"] = bear, bull, rotce

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
    """Price the analyst's own assumption. Returns the second half of the two-sided model.

    Three routes, one per method, because the old single route silently discarded work:
    it accepted only `fcff` names, so a financial could never be repriced no matter what
    the analyst supplied. VEL was recorded with final_growth 0.14 — a 14% sustainable
    ROTCE, exactly what the brief asks a financial's analyst to state — and the result
    was logged as "no growth supplied", which reads as though the question went
    unanswered. 400 Financials in this universe were unpriceable by construction.
    """
    cik = screen_row.get("cik")
    if not cik:
        return {"ok": False, "reason": "no cik"}
    # Use the committed extract, not a fresh companyfacts pull. The forward pass runs in the
    # analyst's runtime, which has no SEC egress; re-fetching raw XBRL here made every
    # reprice fail silently and left the dashboard with a screen and no second opinion.
    fund, fund_source = edgar.fundamentals_cached(cik)
    w = V.cost_of_capital(fund, screen_row["price"], screen_row.get("beta"),
                          None, rf, sector_beta=screen_row.get("sector_beta"))
    method = screen_row.get("method")
    price = screen_row["price"]

    # --- financials: the analyst supplies a sustainable ROTCE, not a growth rate ------
    if method == "book":
        rotce = obj.get("rotce_override")
        if not isinstance(rotce, (int, float)):
            # The brief tells a financial's analyst to state a sustainable ROTCE, and
            # `final_growth` is the only numeric field in the schema, so that is where it
            # lands. Reading it here is what stops the number being thrown away.
            rotce = obj.get("final_growth")
        if not isinstance(rotce, (int, float)):
            return {"ok": False, "reason": "book method needs rotce_override or final_growth"}
        b = V.justified_pb(fund, price, w, roe_override=rotce)
        if not b.get("ok"):
            return {"ok": False, "reason": ",".join(b.get("flags", []))}
        return {
            "ok": True, "method": "justified_p_tbv",
            "analyst_rotce": rotce,
            "screen_rotce": screen_row.get("rotce"),
            "justified_p_tbv": b["justified_p_tbv"],
            "actual_p_tbv": b["actual_p_tbv"],
            "tangible_book_per_share": b["tangible_book_per_share"],
            "fair_value": b["fair_value"], "price": price, "gap": b["gap"],
            "fundamentals_source": fund_source, "flags": b.get("flags", []),
        }

    if method != "fcff" or obj.get("final_growth") is None:
        return {"ok": False, "reason": "not a repriceable fcff name or no growth supplied"}

    override = obj.get("fcff_base_override")
    base_override = override if isinstance(override, (int, float)) else None
    fd = V.forward_dcf(fund, price, w, obj["final_growth"], fcff_base=base_override)
    if not fd.get("ok"):
        return {"ok": False, "reason": ",".join(fd.get("flags", []))}
    implied = screen_row.get("implied_growth")

    # Bear / base / bull crossed with the discount rate. `base` defaults to the analyst's
    # own final_growth so a scenario table exists even when only one number was supplied.
    cases = {"bear": obj.get("bear_growth"), "base": obj.get("final_growth"),
             "bull": obj.get("bull_growth")}
    scen = V.scenario_table(fund, price, w, cases, fcff_base=base_override)

    return {
        "ok": True,
        "method": "fcff",
        "analyst_growth": obj["final_growth"],
        "market_implied_growth": implied,
        "growth_delta": (obj["final_growth"] - implied) if implied is not None else None,
        "fair_value": fd["fair_value"],
        "price": fd["price"],
        "gap": fd["gap"],
        "fair_value_band": fd["fair_value_band"],
        "fcff_base_used": fd["fcff_base_used"],
        "base_overridden": base_override is not None,
        "scenarios": scen if scen.get("ok") else None,
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
    if priced.get("ok") and priced.get("method") == "justified_p_tbv":
        L.append(f"- **Sustainable ROTCE:** screen said {_pct(priced.get('screen_rotce'))}, "
                 f"analyst says {_pct(priced.get('analyst_rotce'))}")
        L.append(f"- **P/TBV:** justified {priced['justified_p_tbv']:.2f} vs actual "
                 f"{priced['actual_p_tbv']:.2f} on tangible book of "
                 f"{_usd(priced['tangible_book_per_share'])}/share")
    elif priced.get("ok"):
        L.append(f"- **Growth:** market implies {_pct(priced.get('market_implied_growth'))}, "
                 f"analyst says {_pct(priced.get('analyst_growth'))} "
                 f"(delta {_pct(priced.get('growth_delta'))})")
        if priced.get("base_overridden"):
            L.append(f"- **FCFF base overridden** by the analyst to "
                     f"{_usd(priced['fcff_base_used'])}")
    elif row.get("method") == "fcff":
        L.append(f"- **Not repriced:** {priced.get('reason')}")
    scen = (priced or {}).get("scenarios")
    if scen and scen.get("ok"):
        L += ["", "**Scenarios.** Fair value at each growth case, across the discount rate.",
              ""]
        header = "| case | growth | " + " | ".join(
            f"{(scen['wacc_point']+s)*100:.1f}%" for s in scen["wacc_steps"]) + " |"
        L.append(header)
        L.append("|---" * (2 + len(scen["wacc_steps"])) + "|")
        for r in scen["grid"]:
            cells = " | ".join(_usd(c["fair_value"]) for c in r["cells"])
            L.append(f"| {r['case']} | {_pct(r['growth'])} | {cells} |")
        L.append("")
        L.append(f"At the point WACC of {scen['wacc_point']*100:.1f}%: "
                 + ", ".join(f"{k} {_pct(v)}" for k, v in scen["summary"].items() if v is not None))
        L.append(f"Across the whole grid the gap ranges {_pct(scen.get('downside'))} "
                 f"to {_pct(scen.get('upside'))} — that spread is the honest precision "
                 f"of this model, not the point estimate.")
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
               "bear_growth": obj.get("bear_growth"),
               "bull_growth": obj.get("bull_growth"),
               "rotce_override": obj.get("rotce_override"),
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
