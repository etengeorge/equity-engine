"""
engine.py - orchestration: synthesis -> thesis -> valuation -> recommendation -> journal.

Per name, the full chain now runs:
  fundamentals -> prices -> gate -> risk stats -> WACC
  -> reverse DCF (market-implied growth)
  -> SYNTHESIS (research view: adjusted growth + full rationale, with receipts)
  -> reverse DCF priced at the variant growth (fair value + gap)
  -> THESIS object (rationale, deviation, catalyst, falsification, horizon, window)
  -> recommendation (reliability-weighted, liquidity-gated)
  -> JOURNAL (company doc + vertical notes; all verticals read together)

The synthesis is autonomous (it proposes the number). The reasoning and the
deviation-from-market are captured and surfaced everywhere.
"""
import config
import data_sources as ds
import analytics as an
import synthesis as syn
import thesis as th
import journal
import store
import sectors


def _hist_revenue_cagr(rev_series):
    s = [x for x in rev_series if x and x > 0]
    if len(s) < 2:
        return None
    try:
        return (s[0] / s[-1]) ** (1 / (len(s) - 1)) - 1
    except Exception:
        return None


def _sourcing_signal(implied, hist):
    if implied is None:
        return {"label": "no_valuation"}
    if hist is None:
        return {"label": "no_history", "implied_growth": implied}
    gap = implied - hist
    label = ("expectations_rich" if gap > 0.05 else
             "expectations_low" if gap < -0.05 else "expectations_inline")
    return {"label": label, "implied_growth": implied,
            "historical_cagr": hist, "implied_minus_historical": gap}


def analyze_ticker(ticker, llm_synth_provider=None, vertical_notes_text=None,
                   gather_news=True):
    """
    llm_synth_provider: optional callable(prompt:str)->json_str (live Claude synthesis,
      supplied by the orchestration layer). If None, the deterministic stub runs.
    vertical_notes_text: ALL vertical notes, read together (cross-sector context).
    """
    cik, name = ds.resolve_cik(ticker)
    if not cik:
        return {"ticker": ticker, "error": "no_cik"}
    fund = ds.extract_fundamentals(cik)
    px = ds.get_prices(ticker)
    if not px:
        return {"ticker": ticker, "cik": cik, "name": name, "error": "no_prices"}
    price = px[1][-1]

    gate = an.validate(fund, price, None)
    risk = an.risk_stats(ticker, px)
    wacc = an.compute_wacc(fund, price, risk.get("beta_adjusted"))

    # 1) market-implied growth (no research view yet)
    rdcf0 = (an.reverse_dcf(fund, price, wacc)
             if wacc.get("reliable") else {"reliable": False, "reasons": ["wacc_unreliable"]})
    implied = rdcf0.get("implied_growth")
    hist = _hist_revenue_cagr(fund.get("revenue_series", []))

    # 2) synthesis: read filings + history + ALL vertical notes -> variant growth
    meta = ds.company_meta(cik)
    sector = meta["sector"]
    if vertical_notes_text is None:
        vertical_notes_text = journal.read_all_vertical_notes()
    company_hist = journal.read_company_history(sector, ticker)
    this_sector_dossier = journal.read_sector_dossier(sector)   # sector learnings -> company rationale
    try:
        import retrospective as retro
        lessons = retro.read_lessons()
    except Exception:
        lessons = None
    synth = None
    news_bundle = None
    price_xcheck = None
    if rdcf0.get("reliable"):
        if gather_news:
            try:
                import news_layer as nl
                news_bundle = nl.gather_news(ticker)
                price_xcheck = nl.price_cross_check(ticker, price)
            except Exception:
                news_bundle = {"error": "news layer unavailable"}
        ctx = syn.build_context(ticker, cik, fund, implied, hist,
                                vertical_notes_text, company_hist,
                                news_bundle=news_bundle, price_xcheck=price_xcheck,
                                this_sector_dossier=this_sector_dossier)
        ctx["retrospective_lessons"] = lessons   # learn from past errors
        llm_json = llm_synth_provider(syn.render_prompt(ctx)) if llm_synth_provider else None
        synth = syn.synthesize(ctx, llm_json=llm_json)

    # 3) reverse DCF priced at the variant growth -> fair value + gap
    rdcf = (an.reverse_dcf(fund, price, wacc, synth.adjusted_growth)
            if (synth and wacc.get("reliable")) else rdcf0)
    our_view = rdcf.get("our_view")

    # 4) thesis object (full rationale chain)
    thesis_obj = th.build_thesis(ticker, synth, implied, our_view) if synth else None

    # 4b) thesis drift: if we hold this name AND have a prior stored thesis, compare the
    # fresh thesis to the stored one and flag MATERIAL (fact-driven) changes only.
    drift_alert = None
    if thesis_obj is not None:
        prior = store.load(cik)
        prior_thesis = (prior or {}).get("latest", {}).get("thesis") if prior else None
        if prior_thesis:
            try:
                import monitor
                drift_alert = monitor.detect_drift(prior_thesis, thesis_obj.to_dict(),
                                                   held=True)
            except Exception:
                drift_alert = None

    reliable = bool(gate["passed"] and wacc.get("reliable") and rdcf.get("reliable")
                    and risk.get("reliable"))
    reasons = (gate["reasons"] + wacc.get("reasons", []) + rdcf.get("reasons", [])
               + [r for r in risk.get("reasons", []) if r in ("thin_history", "beta_low_r2")])
    # SOFT flag: a valuation formed with no revenue history has no track record to anchor
    # the growth view against — surfaced so the thesis isn't over-trusted (does not kill it).
    if rdcf.get("reliable") and hist is None:
        reasons.append("no_historical_revenue_anchor")

    snapshot = {
        "ticker": ticker, "name": name, "sector": sector, "price": price,
        "market_cap": wacc.get("market_cap"), "wacc": wacc.get("wacc_point"),
        "wacc_band": wacc.get("wacc_band"), "implied_rating": wacc.get("implied_rating"),
        "beta_adjusted": risk.get("beta_adjusted"), "vol_annualized": risk.get("vol_annualized"),
        "adv_usd": risk.get("adv_usd"), "normalized_fcff": rdcf.get("normalized_fcff"),
        "_debt": fund.get("total_debt") or 0.0, "_cash": fund.get("cash") or 0.0,
        "last_full_revalue": __import__("datetime").date.today().isoformat(),
        "implied_growth": implied, "implied_growth_band": rdcf.get("implied_growth_band"),
        "historical_revenue_cagr": hist, "sourcing_signal": _sourcing_signal(implied, hist),
        "our_view": our_view, "thesis": thesis_obj.to_dict() if thesis_obj else None,
        "synthesis_source": synth.source if synth else None,
        "synthesis_relationships": synth.relationships if synth else [],
        "synthesis_sector_update": synth.sector_update if synth else {},
        "synthesis_company_news": synth.company_news if synth else "",
        "thesis_drift_alert": drift_alert,
        "news_summary": ({"sources": news_bundle.get("sources_queried"),
                          "n_stories": news_bundle.get("n_stories"),
                          "material_events": news_bundle.get("material_events", []),
                          "has_confirmed_material_event": news_bundle.get("has_confirmed_material_event"),
                          "top": news_bundle.get("all_stories", [])[:5]}
                         if isinstance(news_bundle, dict) and not news_bundle.get("error")
                         else None),
        "price_cross_check": price_xcheck,
        "reliable": reliable, "reliability_flags": reasons,
        "provenance": fund.get("provenance"),
    }
    return {"ticker": ticker, "cik": cik, "name": name, "sector": sector,
            "snapshot": snapshot, "gate": gate}


def _recommend_one(snap, held):
    ov = snap.get("our_view")
    liquid = (snap.get("adv_usd") or 0) >= config.MIN_ADV_USD
    reliable = snap.get("reliable")
    thesis = snap.get("thesis") or {}
    archetype = thesis.get("thesis_archetype")
    conviction = thesis.get("conviction") or 0

    # If the synthesis itself found no edge, do not issue a BUY/SELL off a mechanical
    # gap — the analyst explicitly said the market looks right. This is the guard against
    # the engine manufacturing conviction the research doesn't support.
    no_edge = archetype == "none_efficiently_priced"

    if not ov or ov.get("gap_vs_price") is None:
        if held and snap["sourcing_signal"].get("label") == "expectations_rich":
            return {"action": "REVIEW", "reason": "you hold this; market now prices "
                    "growth above its track record", "sizing": None}
        if held:
            return {"action": "HOLD", "reason": "no actionable gap", "sizing": None}
        if snap["sourcing_signal"].get("label") == "expectations_low":
            return {"action": "RESEARCH", "reason": "priced below its growth history; "
                    "candidate for a deep dive", "sizing": None}
        return {"action": "PASS", "reason": "no edge flagged", "sizing": None}

    gap = ov["gap_vs_price"]
    survives = ov.get("sign_survives_fcff_band")
    if no_edge:
        return {"action": "HOLD" if held else "PASS",
                "reason": "synthesis found no differentiated edge; market looks fairly "
                f"priced (mechanical gap {gap:+.0%} not backed by a thesis)", "sizing": None}
    if not reliable or not liquid:
        size = "avoid_sizing"
    elif abs(gap) > 0.40 and survives and conviction >= 4:
        size = "full"
    elif abs(gap) > 0.25 and conviction >= 3:
        size = "half"
    else:
        size = "starter"

    if gap >= config.BUY_GAP and not held:
        action = "BUY" if (reliable and liquid) else "BUY (watch: low reliability/liquidity)"
        return {"action": action, "reason": f"fair value {gap:+.0%} vs price", "sizing": size}
    if held and gap <= config.SELL_GAP:
        return {"action": "SELL/TRIM", "reason": f"fair value {gap:+.0%} vs price", "sizing": size}
    if held and gap >= config.BUY_GAP:
        return {"action": "ADD", "reason": f"you hold this; fair value {gap:+.0%} vs price",
                "sizing": size}
    if held:
        return {"action": "HOLD", "reason": f"fair value {gap:+.0%} vs price", "sizing": None}
    return {"action": "PASS", "reason": f"fair value {gap:+.0%} vs price; below buy bar",
            "sizing": None}


def run(tickers, llm_synth_provider=None, positions=None, persist=True,
        write_journal=True, gather_news=True):
    held = {p["ticker"].upper(): p for p in (positions or [])}
    vertical_notes = journal.read_all_vertical_notes()   # read ALL verticals together
    rows = []
    for t in tickers:
        try:
            res = analyze_ticker(t, llm_synth_provider=llm_synth_provider,
                                 vertical_notes_text=vertical_notes, gather_news=gather_news)
            if res.get("error"):
                rows.append({"ticker": t, "error": res["error"]})
                continue
            snap = res["snapshot"]
            rec = _recommend_one(snap, t.upper() in held)
            snap["held"] = held.get(t.upper())
            snap["recommendation"] = rec
            ov = snap.get("our_view") or {}
            gap = ov.get("gap_vs_price")
            snap["rank_score"] = (abs(gap) * (1.0 if snap.get("reliable") else 0.35)
                                  if gap is not None else -1)
            rows.append(snap)
            if persist:
                store.upsert({"cik": res["cik"], "ticker": t, "name": res["name"],
                              "snapshot": snap})
            if write_journal and snap.get("thesis"):
                sec = res["sector"]
                journal.append_company_entry(sec, t, snap["thesis"], snap)
                # folder-method: log company-specific news + FEED the sector dossier, so a
                # sector-wide learning flows into every other name in the sector next run.
                ns = snap.get("news_summary") or {}
                news_items = [{"title": s.get("title"), "url": s.get("url"),
                               "source_label": ("/".join(s["sources"]) if isinstance(s.get("sources"), list)
                                                else s.get("sources")),
                               "date": s.get("date") or s.get("source_date")}
                              for s in (ns.get("top") or [])[:5]]
                if snap.get("synthesis_company_news"):
                    news_items.append(snap["synthesis_company_news"])
                journal.append_company_news(sec, t, news_items, name=res.get("name"))
                sectors.record_relationships(sec, t, snap.get("synthesis_relationships") or [])
                sectors.record_sector_update(sec, snap.get("synthesis_sector_update") or {}, ticker=t)
        except Exception as e:
            # one bad name never kills the whole run (ROUTINE.md / CONNECTING.md contract)
            rows.append({"ticker": t,
                         "error": f"analysis_failed: {type(e).__name__}: {str(e)[:120]}"})
            continue
    rows.sort(key=lambda r: r.get("rank_score", -1), reverse=True)
    result = {"rows": rows, "paper_mode": config.PAPER_MODE}

    # portfolio-level analysis (concentration, diversification, reweighting) when held
    if held:
        try:
            import portfolio
            snaps = {r["ticker"]: r for r in rows if not r.get("error")}
            # include held names even if not in this run's ticker list (value them)
            result["portfolio"] = portfolio.analyze_portfolio(list(held.values()), snaps)
        except Exception as e:
            result["portfolio"] = {"error": f"portfolio analysis failed: {e}"}
    return result
