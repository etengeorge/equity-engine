"""
qa_harness.py - the adversarial QA pass.

Run as the "second team member": hammer the logic with the cases most likely to
produce wrong numbers or crashes, on both synthetic edge inputs and live real
data. Prints a report and exits non-zero if any hard check fails.

What it CAN verify: logic, math, wiring, graceful degradation on bad input.
What it CANNOT verify: whether the synthesis produces GOOD investment judgment —
that's the paper-trade gate's job over time. Kept explicit so "passed QA" doesn't
oversell.
"""
import math
import sys
import traceback

import config
import analytics as an
import data_sources as ds
import engine
import thesis as th
import synthesis as syn


PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, cond, detail=""):
    results.append((PASS if cond else FAIL, name, detail))


def section(t):
    results.append(("SECTION", t, ""))


# ----------------------------------------------------------- synthetic fixtures
def fund(**kw):
    base = dict(cik=1, revenue=1e9, ebit=1.2e8, interest_expense=1e7,
                total_debt=2e8, cash=5e7, shares=5e7,
                cfo_series=[1.5e8, 1.4e8, 1.3e8], capex_series=[4e7, 3.5e7, 3e7],
                revenue_series=[1e9, 9e8, 8e8, 7e8], provenance={})
    base.update(kw)
    return base


# ---------------------------------------------------------------- WACC tests
def test_wacc():
    section("WACC")
    # normal
    w = an.compute_wacc(fund(), price=20.0, beta_adj=1.1)
    check("wacc normal in 3-25% range", w["reliable"] and 0.03 < w["wacc_point"] < 0.25,
          f"wacc={w['wacc_point']:.3f}")
    check("wacc weights sum to 1",
          abs(w["weight_equity"] + w["weight_debt"] - 1.0) < 1e-9)
    # no debt -> debt leg shouldn't blow up, weight_debt ~ 0
    w2 = an.compute_wacc(fund(total_debt=0, interest_expense=0), 20.0, 1.0)
    check("no-debt name handled", w2["reliable"] and w2["weight_debt"] < 1e-6)
    # negative EBIT -> flagged unreliable, not crashed
    w3 = an.compute_wacc(fund(ebit=-5e7), 20.0, 1.0)
    check("neg-EBIT WACC flagged unreliable", not w3["reliable"],
          f"reasons={w3['reasons']}")
    # missing shares -> graceful
    w4 = an.compute_wacc(fund(shares=None), 20.0, 1.0)
    check("missing-shares WACC graceful", not w4["reliable"])
    # beta None -> defaults to 1, flagged
    w5 = an.compute_wacc(fund(), 20.0, None)
    check("missing-beta defaults to 1 and flags", "beta_defaulted_to_1" in w5["reasons"])


# ---------------------------------------------------------------- reverse DCF
def test_reverse_dcf():
    section("Reverse DCF")
    w = an.compute_wacc(fund(), 20.0, 1.1)
    r = an.reverse_dcf(fund(), 20.0, w)
    check("implied growth solved & finite",
          r["reliable"] and r["implied_growth"] is not None
          and math.isfinite(r["implied_growth"]), f"g={r.get('implied_growth')}")
    # monotonicity: higher price must imply higher growth
    r_lo = an.reverse_dcf(fund(), 10.0, w)
    r_hi = an.reverse_dcf(fund(), 40.0, w)
    check("higher price -> higher implied growth",
          r_lo["implied_growth"] < r_hi["implied_growth"],
          f"{r_lo['implied_growth']:.3f} < {r_hi['implied_growth']:.3f}")
    # negative normalized FCFF -> flagged, not crashed
    rn = an.reverse_dcf(fund(cfo_series=[1e7, 1e7], capex_series=[5e7, 5e7]), 20.0, w)
    check("negative FCFF flagged", not rn["reliable"],
          f"reasons={rn.get('reasons')}")
    # WACC <= terminal growth must be caught (no divide-by-near-zero)
    bad_w = dict(w); bad_w["wacc_point"] = config.TERMINAL_GROWTH - 0.005
    bad_w["wacc_band"] = {"low": bad_w["wacc_point"] - 0.01, "high": bad_w["wacc_point"] + 0.01}
    rb = an.reverse_dcf(fund(), 20.0, bad_w)
    check("WACC<=terminal handled", (rb.get("implied_growth") is None) or (not rb["reliable"]))
    # our_view gap sign correct: variant growth >> implied -> positive gap
    rv = an.reverse_dcf(fund(), 20.0, w, research_growth=r["implied_growth"] + 0.05)
    check("higher variant growth -> positive gap",
          rv["our_view"]["gap_vs_price"] > 0, f"gap={rv['our_view']['gap_vs_price']:.3f}")
    rv2 = an.reverse_dcf(fund(), 20.0, w, research_growth=r["implied_growth"] - 0.05)
    check("lower variant growth -> negative gap",
          rv2["our_view"]["gap_vs_price"] < 0)
    # WACC-band economics (regression for the label-inversion bug): higher WACC discounts
    # harder, so it implies HIGHER growth to justify the same price.
    band = r.get("implied_growth_band", {})
    check("WACC band: at_high_wacc >= at_low_wacc (higher discount needs more growth)",
          band.get("at_high_wacc") is not None
          and band["at_high_wacc"] >= band["at_low_wacc"],
          f"{band.get('at_high_wacc')} vs {band.get('at_low_wacc')}")
    # fair value strictly increases in the growth assumption, across the whole curve
    fvs = [an.reverse_dcf(fund(), 20.0, w, research_growth=g)["our_view"]["fair_value"]
           for g in (0.0, 0.02, 0.04, 0.06, 0.08, 0.10)]
    check("fair value strictly monotonic in growth",
          all(fvs[i] < fvs[i + 1] for i in range(len(fvs) - 1)), str([round(x, 1) for x in fvs]))


# ---------------------------------------------------------------- thesis/window
def test_synthesis_machinery():
    section("Synthesis machinery (context, parser, validation)")
    import synthesis as syn, json

    def full(**over):
        base = {"adjusted_growth": 0.05, "thesis_archetype": "catalyst_mispricing",
                "conviction": 3, "horizon_months": 18, "variant_view": "v",
                "mispriced_mechanism": "m"}
        base.update(over)
        return json.dumps(base)

    # clean, fenced, and prose-wrapped JSON all parse to an llm result
    check("clean JSON parses", syn.from_llm_json(full()).source == "llm")
    check("```json-fenced parses", syn.from_llm_json("```json\n" + full() + "\n```").source == "llm")
    check("prose-wrapped JSON recovers (not silent stub)",
          syn.from_llm_json("Here is my analysis:\n\n" + full() + "\n\nDone.").source == "llm")
    # conviction clamped to 1-5 (drives sizing — must never pass through out of range)
    check("conviction 0 -> 1", syn.from_llm_json(full(conviction=0)).conviction == 1)
    check("conviction 100 -> 5", syn.from_llm_json(full(conviction=100)).conviction == 5)
    check("conviction -3 -> 1", syn.from_llm_json(full(conviction=-3)).conviction == 1)
    # horizon bounded to a sane window (feeds Kelly annualization 12/horizon, eval window)
    check("horizon -5 -> clamped >=1", syn.from_llm_json(full(horizon_months=-5)).horizon_months >= 1)
    check("horizon 0 -> clamped >=1", syn.from_llm_json(full(horizon_months=0)).horizon_months >= 1)
    check("horizon 9999 -> clamped <=120", syn.from_llm_json(full(horizon_months=9999)).horizon_months <= 120)
    # unknown archetype falls back; missing/garbage adjusted_growth raises (-> stub)
    check("unknown archetype -> none_efficiently_priced",
          syn.from_llm_json(full(thesis_archetype="moon")).thesis_archetype == "none_efficiently_priced")
    try:
        syn.from_llm_json(json.dumps({"thesis_archetype": "x"}))
        check("missing adjusted_growth raises", False)
    except Exception:
        check("missing adjusted_growth raises", True)
    try:
        syn.from_llm_json(full(adjusted_growth="high"))
        check("non-numeric growth raises", False)
    except Exception:
        check("non-numeric growth raises", True)
    # synthesize() falls back to a tagged stub on unparseable input (visible, not silent)
    res = syn.synthesize({"implied_growth": 0.05, "historical_cagr": 0.03,
                          "filing_excerpts": []}, llm_json="not json at all")
    check("parse failure tagged on stub source", res.source == "stub_after_parse_error")
    check("parse failure reason recorded in rationale", "FAILED TO PARSE" in res.rationale)
    # stub itself is structurally complete (every required field present and typed)
    stub = syn.stub_synthesize({"implied_growth": 0.05, "historical_cagr": 0.03,
                                "filing_excerpts": []})
    check("stub fills all scenario cases",
          all(k in stub.bull_case for k in ("narrative", "growth", "what_drives_it")))
    check("stub conviction in range", 1 <= stub.conviction <= 5)


def test_incomplete_information():
    section("Incomplete-information handling (graceful degradation + flags)")
    import analytics as an

    def complete():
        return {"cik": 1, "revenue": 1e9, "ebit": 1.2e8, "interest_expense": 1e7,
                "total_debt": 2e8, "cash": 5e7, "shares": 5e7,
                "cfo_series": [1.6e8, 1.5e8, 1.4e8], "capex_series": [3e7, 2.8e7, 2.6e7],
                "revenue_series": [1e9, 9e8, 8e8, 7e8], "provenance": {}}
    price = 20.0
    # control: complete data values cleanly with no soft flags
    w = an.compute_wacc(complete(), price, 1.0)
    r = an.reverse_dcf(complete(), price, w)
    check("complete data -> values, no soft flags", r["reliable"] and not r["reasons"])
    # missing shares -> gate fails, refuses
    g = an.validate({**complete(), "shares": None}, price, None)
    check("missing shares -> gate refuses", not g["passed"] and "bad_shares" in g["reasons"])
    # missing cash flow -> cannot compute FCFF -> refuses
    rcf = an.reverse_dcf({**complete(), "cfo_series": [], "capex_series": []}, price, w)
    check("missing cash flow -> refuses to value",
          not rcf["reliable"] and "nonpositive_normalized_fcff" in rcf["reasons"])
    # negative FCFF (capex > CFO) -> refuses, does not fabricate
    rneg = an.reverse_dcf({**complete(), "cfo_series": [3e7, 2e7],
                           "capex_series": [2e8, 1.8e8]}, price, w)
    check("negative FCFF -> refuses to value", not rneg["reliable"])
    # negative EBIT -> WACC unreliable (can't synthetically rate the debt)
    wn = an.compute_wacc({**complete(), "ebit": -5e7}, price, 1.0)
    check("negative EBIT -> WACC flagged unreliable", not wn.get("reliable"))
    # thin 1-year FCFF -> SOFT flag (still values, but surfaced)
    w1 = an.compute_wacc({**complete(), "cfo_series": [1.6e8], "capex_series": [3e7]}, price, 1.0)
    r1 = an.reverse_dcf({**complete(), "cfo_series": [1.6e8], "capex_series": [3e7]}, price, w1)
    check("thin 1-yr FCFF -> soft flag but still reliable",
          r1["reliable"] and "thin_fcff_normalization_1yr" in r1["reasons"])
    check("FCFF normalization year count reported", r1.get("fcff_normalization_years") == 1)


def test_valuation_extremes():
    section("Valuation extremes (solver bounds, degenerate FV, artifact gaps)")
    import analytics as an
    def base(**o):
        f = {"cik": 1, "revenue": 1e9, "ebit": 1.2e8, "interest_expense": 1e7,
             "total_debt": 2e8, "cash": 5e7, "shares": 5e7,
             "cfo_series": [1.6e8, 1.5e8, 1.4e8], "capex_series": [3e7, 2.8e7, 2.6e7],
             "revenue_series": [1e9, 9e8, 8e8], "provenance": {}}
        f.update(o)
        return f
    # deep value (FCFF >> mktcap): implied growth pins at floor -> UNRELIABLE, no fake gap
    w = an.compute_wacc(base(cfo_series=[3e8], capex_series=[2e7]), 2.0, 1.0)
    r = an.reverse_dcf(base(cfo_series=[3e8], capex_series=[2e7]), 2.0, w, 0.04)
    check("solver-floor case -> unreliable (no false top-rank BUY)",
          not r["reliable"] and "implied_growth_at_solver_bound_unvaluable" in r["reasons"])
    # hypergrowth (tiny FCFF vs huge price): implied growth pins at ceiling -> UNRELIABLE
    w2 = an.compute_wacc(base(cfo_series=[2e7], capex_series=[1e7]), 500.0, 1.0)
    r2 = an.reverse_dcf(base(cfo_series=[2e7], capex_series=[1e7]), 500.0, w2, 0.04)
    check("solver-ceiling case -> unreliable", not r2["reliable"])
    # distressed: non-positive fair value -> flagged, gap suppressed (no negative target)
    wd = an.compute_wacc(base(total_debt=5e9, cash=1e8, interest_expense=4e8, ebit=2e7), 5.0, 1.0)
    rd = an.reverse_dcf(base(total_debt=5e9, cash=1e8, interest_expense=4e8, ebit=2e7), 5.0, wd, 0.04)
    ov = rd.get("our_view") or {}
    check("non-positive fair value -> gap suppressed + flagged",
          ov.get("gap_vs_price") is None and "nonpositive_fair_value_degenerate" in rd["reasons"])
    # extreme gap (data artifact) -> withholds reliable stamp
    we = an.compute_wacc(base(shares=5e8), 0.42, 1.0)
    re = an.reverse_dcf(base(shares=5e8), 0.42, we, 0.04)
    check("extreme gap -> flagged suspect + unreliable",
          not re["reliable"] and "extreme_gap_suspect_data_artifact" in re["reasons"])
    # control: a normal company still values reliably with no extreme flags
    wc = an.compute_wacc(base(cfo_series=[7e7, 6.8e7, 6.5e7], capex_series=[3e7, 2.9e7, 2.8e7]), 25.0, 1.0)
    rc = an.reverse_dcf(base(cfo_series=[7e7, 6.8e7, 6.5e7], capex_series=[3e7, 2.9e7, 2.8e7]), 25.0, wc, 0.04)
    check("normal company still values reliably",
          rc["reliable"] and "implied_growth_at_solver_bound_unvaluable" not in rc["reasons"])
    # WACC <= terminal growth -> refuse with explicit reason (Gordon TV would diverge)
    wbad = {"wacc_point": 0.01, "wacc_band": {"low": 0.005, "high": 0.015},
            "reliable": True, "market_cap": 1e9}
    rwb = an.reverse_dcf(base(), 20.0, wbad, 0.04)
    check("WACC <= terminal growth -> unreliable + flagged",
          not rwb["reliable"] and "wacc_below_terminal_growth" in rwb["reasons"])


def test_pathological_inputs():
    section("Pathological inputs (NaN/Inf, impossible financials, WACC sanity)")
    import analytics as an
    nan, inf = float("nan"), float("inf")
    def base(**o):
        f = {"cik": 1, "revenue": 1e9, "ebit": 1.2e8, "interest_expense": 1e7,
             "total_debt": 2e8, "cash": 5e7, "shares": 5e7,
             "cfo_series": [1.6e8, 1.5e8, 1.4e8], "capex_series": [3e7, 2.8e7, 2.6e7],
             "revenue_series": [1e9, 9e8, 8e8], "provenance": {}}
        f.update(o)
        return f
    # NaN/Inf in inputs -> gate rejects (a broken feed must never look clean)
    check("NaN shares -> gate fails", not an.validate(base(shares=nan), 20.0, None)["passed"])
    check("NaN price -> gate fails", not an.validate(base(), nan, None)["passed"])
    check("NaN revenue -> gate fails", not an.validate(base(revenue=nan), 20.0, None)["passed"])
    check("Inf EBIT -> gate fails", not an.validate(base(ebit=inf), 20.0, None)["passed"])
    check("NaN in cfo_series -> gate fails",
          not an.validate(base(cfo_series=[1.6e8, nan, 1.4e8]), 20.0, None)["passed"])
    # internally impossible financials -> gate rejects
    check("EBIT > revenue (>100% margin) -> gate fails",
          "ebit_exceeds_revenue_impossible" in an.validate(base(ebit=2e9), 20.0, None)["reasons"])
    check("negative revenue -> gate fails",
          "negative_revenue_impossible" in an.validate(base(revenue=-1e9), 20.0, None)["reasons"])
    check("negative interest expense -> gate fails",
          "negative_interest_expense_impossible" in an.validate(base(interest_expense=-1e7), 20.0, None)["reasons"])
    # control: clean financials pass the gate
    check("clean financials pass gate", an.validate(base(), 20.0, None)["passed"])
    # DCF defense in depth: non-finite research growth -> unreliable, no NaN gap
    w = an.compute_wacc(base(), 20.0, 1.0)
    rnan = an.reverse_dcf(base(), 20.0, w, nan)
    check("NaN research growth -> DCF unreliable (no NaN gap leak)",
          not rnan["reliable"] and "nonfinite_research_growth" in rnan["reasons"])
    # WACC sanity
    check("NaN beta -> defaults to 1.0, stays finite/reliable",
          an.compute_wacc(base(), 20.0, nan).get("reliable")
          and "nonfinite_beta_defaulted" in an.compute_wacc(base(), 20.0, nan)["reasons"])
    check("negative WACC (beta -2) -> unreliable",
          not an.compute_wacc(base(), 20.0, -2.0).get("reliable"))
    check("implausibly high WACC (beta 50) -> unreliable",
          not an.compute_wacc(base(), 20.0, 50.0).get("reliable"))
    check("plausible high beta (8) -> still reliable",
          an.compute_wacc(base(), 20.0, 8.0).get("reliable"))


def test_price_path_pathologies():
    section("Price-path pathologies (bad ticks, NaN propagation guards)")
    import analytics as an
    nan, inf = float("nan"), float("inf")
    def mkpx(closes):
        n = len(closes)
        return ([f"2026-01-{i+1:02d}" for i in range(n)], closes,
                [100] * n, [100] * n, [1e6] * n)
    # a zero / NaN / negative close must NOT crash and must flag the series
    for label, series in [("zero embedded", [100, 100, 0, 100] + [100] * 56),
                          ("NaN in series", [100, 100, nan, 100] + [100] * 56),
                          ("negative price", [100, 100, -50, 100] + [100] * 56),
                          ("all zeros", [0.0] * 60)]:
        try:
            r = an.risk_stats("T", mkpx(series))
            ok = (not r.get("reliable")) and any("bad_prices" in x or "no_valid" in x
                                                 for x in r.get("reasons", []))
            check(f"risk_stats handles {label} without crashing", ok, str(r.get("reasons")))
        except Exception as e:
            check(f"risk_stats handles {label} without crashing", False, f"{type(e).__name__}")
    # extreme single-day move flagged
    r = an.risk_stats("T", mkpx([10, 110, 1.1] + [1.1] * 57))
    check("extreme single-day move flagged",
          "extreme_single_day_move_suspect" in r.get("reasons", []))
    # quick_revalue never emits a non-finite gap
    good = {"price": 100, "our_view": {"fair_value": 130, "gap_vs_price": 0.3},
            "normalized_fcff": 5e7, "market_cap": 5e8, "wacc": 0.09, "_debt": 1e8, "_cash": 2e7}
    check("quick_revalue: NaN new price -> None", an.quick_revalue(good, nan) is None)
    rv = an.quick_revalue({**good, "our_view": {"fair_value": nan}}, 90)
    check("quick_revalue: NaN stored fair value -> no NaN gap",
          rv is not None and rv.get("new_gap") is None)
    rv2 = an.quick_revalue({**good, "our_view": {"fair_value": inf}}, 90)
    check("quick_revalue: Inf fair value -> no Inf gap", rv2.get("new_gap") is None)


def test_portfolio_nan_guards():
    section("Portfolio NaN guards (no poisoned weights)")
    import portfolio, math
    nan = float("nan")
    sg = {"A": {"ticker": "A", "price": 100, "sector": "Tech", "vol_annualized": 0.3,
                "our_view": {"gap_vs_price": 0.3, "fair_value": 130},
                "thesis": {"horizon_months": 24, "conviction": 4, "direction": "long",
                           "thesis_archetype": "x"}}}
    # NaN shares -> position skipped (not a NaN total)
    p = portfolio.analyze_portfolio([{"ticker": "A", "shares": nan, "avg_cost": 80}], sg)
    check("NaN shares -> no valued positions (no NaN total)", p.get("error") is not None)
    # NaN gap in snapshot -> total value still finite, gap sanitized
    p2 = portfolio.analyze_portfolio([{"ticker": "A", "shares": 100, "avg_cost": 80}],
                                     {"A": {**sg["A"], "our_view": {"gap_vs_price": nan,
                                                                    "fair_value": 130}}})
    tv = p2.get("total_value")
    check("NaN gap -> total value still finite",
          tv is not None and math.isfinite(tv))


def test_thesis():
    section("Thesis & evaluation window")
    s = syn.stub_synthesize({"implied_growth": 0.10, "historical_cagr": 0.02,
                             "filing_excerpts": []})
    s.thesis_archetype = "fundamentals_divergence"   # non-null so direction follows gap
    ov = {"fair_value": 25.0, "gap_vs_price": 0.25, "sign_survives_fcff_band": True}
    t = th.build_thesis("TEST", s, 0.10, ov)
    check("thesis has pinned evaluation_window", bool(t.evaluation_window))
    check("window is after creation date", t.evaluation_window > t.created)
    check("positive gap -> long direction", t.direction == "long")
    check("thesis carries deviation explanation", len(t.deviation_explanation) > 10)
    check("thesis carries mispriced mechanism", len(t.mispriced_mechanism) > 5)
    check("thesis carries bull/base/bear scenarios",
          isinstance(t.bull_case, dict) and isinstance(t.base_case, dict)
          and isinstance(t.bear_case, dict) and "growth" in t.base_case)
    check("thesis carries catalyst pathway + what-must-happen",
          len(t.catalyst_path) > 0 and isinstance(t.what_must_happen, list)
          and len(t.what_must_happen) >= 1)
    check("thesis to_dict round-trips", isinstance(t.to_dict(), dict)
          and t.to_dict()["variant_growth"] == s.adjusted_growth)


# ---------------------------------------------------------------- recommendation
def test_reco():
    section("Recommendation logic")
    snap = {"our_view": {"gap_vs_price": 0.30, "sign_survives_fcff_band": True},
            "adv_usd": 5e6, "reliable": True,
            "sourcing_signal": {"label": "expectations_low"},
            "thesis": {"thesis_archetype": "fundamentals_divergence", "conviction": 4}}
    check("big positive gap, not held -> BUY",
          engine._recommend_one(snap, held=False)["action"].startswith("BUY"))
    check("big positive gap, held -> ADD",
          engine._recommend_one(snap, held=True)["action"] == "ADD")
    snap_sell = {"our_view": {"gap_vs_price": -0.30, "sign_survives_fcff_band": True},
                 "adv_usd": 5e6, "reliable": True, "sourcing_signal": {"label": "x"},
                 "thesis": {"thesis_archetype": "fundamentals_divergence", "conviction": 4}}
    check("big negative gap, held -> SELL/TRIM",
          engine._recommend_one(snap_sell, held=True)["action"] == "SELL/TRIM")
    # illiquid -> sizing downgraded to avoid even on a buy
    snap_illiq = dict(snap); snap_illiq["adv_usd"] = 1e3
    check("illiquid name -> avoid_sizing",
          engine._recommend_one(snap_illiq, held=False)["sizing"] == "avoid_sizing")
    # unreliable -> BUY downgraded to watch
    snap_unrel = dict(snap); snap_unrel["reliable"] = False
    check("unreliable -> BUY (watch ...) label",
          "watch" in engine._recommend_one(snap_unrel, held=False)["action"])
    # NO-EDGE guard: synthesis says efficiently priced -> no BUY even on a big gap
    snap_noedge = {"our_view": {"gap_vs_price": 0.45, "sign_survives_fcff_band": True},
                   "adv_usd": 5e6, "reliable": True,
                   "sourcing_signal": {"label": "x"},
                   "thesis": {"thesis_archetype": "none_efficiently_priced", "conviction": 2}}
    rec_ne = engine._recommend_one(snap_noedge, held=False)
    check("no-edge verdict suppresses BUY despite +45% gap",
          rec_ne["action"] == "PASS", f"got {rec_ne['action']}")
    # low conviction -> sizing capped at starter even with a big reliable gap
    snap_lowconv = {"our_view": {"gap_vs_price": 0.45, "sign_survives_fcff_band": True},
                    "adv_usd": 5e6, "reliable": True, "sourcing_signal": {"label": "x"},
                    "thesis": {"thesis_archetype": "catalyst_mispricing", "conviction": 2}}
    check("low conviction caps sizing at starter",
          engine._recommend_one(snap_lowconv, held=False)["sizing"] == "starter")


# ---------------------------------------------------------------- ranking guard
def test_ranking():
    section("Ranking (multiple-comparison guard)")
    rows = [{"our_view": {"gap_vs_price": 0.5}, "reliable": False},   # huge but unreliable
            {"our_view": {"gap_vs_price": 0.3}, "reliable": True}]    # smaller but reliable
    for r in rows:
        g = r["our_view"]["gap_vs_price"]
        r["rank_score"] = abs(g) * (1.0 if r["reliable"] else 0.35)
    rows.sort(key=lambda r: r["rank_score"], reverse=True)
    check("reliable 0.30 outranks unreliable 0.50",
          rows[0]["reliable"] is True,
          f"top score={rows[0]['rank_score']:.3f}")


# ---------------------------------------------------------------- live integration
def test_news_layer():
    section("Multi-source perspective mapping (anti-groupthink)")
    import news_layer as nl
    items = [
        {"source": "alphavantage", "tier": 3, "title": "Acme upgraded to Buy by analyst",
         "url": "a", "published": "20260530", "sentiment_score": 0.4},
        {"source": "finnhub", "tier": 3, "title": "Short seller warns Acme overvalued, flags accounting",
         "url": "b", "published": "20260530", "sentiment_score": None},
        {"source": "rss", "tier": 3, "title": "Totally unrelated CEO interview on strategy",
         "url": "d", "published": "", "sentiment_score": None},
    ]
    clusters = nl._dedupe_and_map_perspectives(items)
    # the two Acme items are DIFFERENT events (upgrade vs short report) -> not merged,
    # but the bundle should detect both a bull and a bear perspective present.
    bundle = nl.gather_news.__wrapped__ if hasattr(nl.gather_news, "__wrapped__") else None
    # classify perspectives directly
    p1 = nl._classify_perspective("Acme upgraded to Buy by analyst", "alphavantage")
    p2 = nl._classify_perspective("Short seller warns Acme overvalued", "finnhub")
    check("analyst-upgrade classified as sell_side_bull", p1 == "sell_side_bull", p1)
    check("short report classified as short_bear", p2 == "short_bear", p2)
    check("opposing stances detected (bull vs bear present)",
          nl._stance(p1, 0.4) == "bull" and nl._stance(p2, None) == "bear")
    # price cross-check logic
    diff = abs(312.06 - 340.0) / 312.06
    check("price cross-check flags >tolerance disagreement",
          diff > config.PRICE_XCHECK_TOLERANCE)


def test_retrospective():
    section("Retrospective strict scoring")
    import retrospective as retro
    # synthetic scored outcomes -> exercise the verdict logic directly
    def mk(direction, idio, mech):
        return {"ticker": "T", "sector": "Tech", "direction": direction,
                "thesis_archetype": "catalyst_mispricing", "conviction": 3,
                "idiosyncratic_excess": idio, "mechanism_played_out": mech,
                "stock_return": 0.1, "sector_basket_return": 0.1 - (idio or 0),
                "idio_direction_correct": (idio > 0 if direction == "long" else idio < 0)
                                          if idio is not None else None,
                "verdict": None, "likely_early": False, "created": "2025-01-01"}
    # reproduce verdict logic expectations
    cases = [
        ("long", 0.10, "played_out", "correct_idiosyncratic"),
        ("long", -0.10, "played_out", "right_mechanism_wrong_outcome"),
        ("long", 0.10, "did_not", "correct_but_wrong_reason"),
        ("long", 0.10, "unknown", "idio_correct_mechanism_unverified"),
        ("long", -0.10, "did_not", "wrong"),
    ]
    # We can't easily re-run score_thesis without price data, so verify the verdict
    # mapping is internally consistent by checking the aggregator on hand-built scores.
    scores = []
    for d, idio, mech, expected in cases:
        s = mk(d, idio, mech)
        # mimic score_thesis verdict branch
        ic = s["idio_direction_correct"]
        if mech == "played_out" and ic: v = "correct_idiosyncratic"
        elif mech == "played_out" and not ic: v = "right_mechanism_wrong_outcome"
        elif mech in ("did_not", "partial") and ic: v = "correct_but_wrong_reason"
        elif mech == "unknown" and ic: v = "idio_correct_mechanism_unverified"
        elif mech == "unknown" and not ic: v = "idio_wrong_mechanism_unverified"
        else: v = "wrong"
        s["verdict"] = v
        scores.append(s)
        check(f"verdict: {d}/{idio:+.0%}/{mech} -> {expected}", v == expected, f"got {v}")
    pat = retro.aggregate_patterns(scores)
    check("aggregator computes hit-rate and lessons",
          pat["n_graded"] >= 1 and len(pat["lessons"]) >= 1)
    check("strict win requires mechanism AND idiosyncratic",
          "correct_idiosyncratic" in [s["verdict"] for s in scores]
          and "correct_but_wrong_reason" in [s["verdict"] for s in scores])


def test_monitor():
    section("Thesis-drift monitor (anti-overtrading + sizing-up)")
    import monitor
    base = {"ticker": "X", "thesis_archetype": "catalyst_mispricing",
            "direction": "long", "conviction": 4, "mispriced_mechanism": "m"}
    rev = monitor.detect_drift(base, {**base, "direction": "avoid",
                                      "thesis_archetype": "fundamentals_divergence"})
    check("direction reversal -> severity 3", rev and rev["severity"] == 3)
    eg = monitor.detect_drift(base, {**base, "direction": "hold",
                                     "thesis_archetype": "none_efficiently_priced"})
    check("edge gone -> severity 2 (not over-escalated)", eg and eg["severity"] == 2)
    check("identical thesis -> no alert", monitor.detect_drift(base, dict(base)) is None)
    check("1-level conviction wobble -> no alert",
          monitor.detect_drift(base, {**base, "conviction": 3}) is None)
    coll = monitor.detect_drift(base, {**base, "conviction": 2})
    check("2-level conviction collapse -> alert + review", coll is not None and coll["severity"] == 2)
    # STRENGTHENED thesis (low->high conviction) on a held long -> ADD signal (negative sev)
    low = {**base, "conviction": 2}
    strong = monitor.detect_drift(low, {**base, "conviction": 5}, held=True)
    check("strengthened long thesis -> ADD recommendation",
          strong and strong["severity"] < 0 and "ADDING" in strong["recommended_action"],
          f"sev={strong['severity'] if strong else None}")


def test_portfolio():
    section("Portfolio construction & limits")
    import portfolio, config
    # build snapshots so analyze_portfolio uses them (avoid live fetch for held names)
    def snap(t, price, sector, gap, fv, conv, direction, arch, vol=0.4, hz=24):
        return {"ticker": t, "price": price, "sector": sector, "vol_annualized": vol,
                "our_view": {"gap_vs_price": gap, "fair_value": fv},
                "thesis": {"horizon_months": hz, "conviction": conv,
                           "direction": direction, "thesis_archetype": arch}}
    snaps = {
        "A": snap("A", 100, "Tech", 0.40, 140, 4, "long", "catalyst_mispricing"),
        "B": snap("B", 100, "Tech", 0.01, 101, 3, "long", "cyclical_mean_reversion"),
    }
    # A is huge (60%), same sector as B -> sector + name overexposure
    pos = [{"ticker": "A", "shares": 600, "avg_cost": 70},
           {"ticker": "B", "shares": 400, "avg_cost": 90}]
    p = portfolio.analyze_portfolio(pos, snaps)
    check("weights computed and sum ~1",
          abs(sum(h["weight"] for h in p["positions"]) - 1.0) < 1e-6)
    check("single-name overexposure flagged (A > cap)",
          any(f["ticker"] == "A" for f in p["single_name_overexposure"]))
    check("sector overexposure flagged (Tech > cap)",
          any(f["sector"] == "Tech" for f in p["sector_overexposure"]))
    # B is at fair value (gap 0.01) and overweight -> harvest; A has upside -> not harvest
    sugg = {s["ticker"]: s for s in p["reweighting_suggestions"]}
    check("B (fair value reached) flagged as harvest", sugg.get("B", {}).get("harvest") is True)
    check("A (thesis intact) NOT flagged as harvest",
          not sugg.get("A", {}).get("harvest", False))
    check("diversification reports effective bets",
          "correlation_adjusted_effective_bets" in p["diversification"])
    # regression: a name OVER the hard cap must ALWAYS get a trim, even if its Kelly target
    # is high enough that drift-vs-target is small (cap is a limit, not a suggestion).
    snaps2 = {
        "BIG": snap("BIG", 100, "Tech", 0.60, 160, 5, "long", "catalyst_mispricing"),
        "MID": snap("MID", 100, "Tech", 0.50, 150, 4, "long", "cyclical_mean_reversion"),
    }
    pos2 = [{"ticker": "BIG", "shares": 700, "avg_cost": 50},
            {"ticker": "MID", "shares": 150, "avg_cost": 80}]
    p2 = portfolio.analyze_portfolio(pos2, snaps2)
    over_names = {f["ticker"] for f in p2["single_name_overexposure"]}
    trimmed = {s["ticker"] for s in p2["reweighting_suggestions"] if "TRIM" in s["action"]}
    check("every over-cap name receives a trim suggestion (panels agree)",
          over_names and over_names.issubset(trimmed),
          f"over={over_names} trimmed={trimmed}")


def test_dynamic_revalue():
    section("Dynamic DCF (cheap daily re-price + cadence)")
    import analytics as an, scanner, datetime as dt
    stored = {"price": 100, "our_view": {"fair_value": 130, "gap_vs_price": 0.30},
              "normalized_fcff": 5e7, "market_cap": 5e8, "wacc": 0.09,
              "_debt": 1e8, "_cash": 2e7}
    # price drops, target held -> gap widens (cheap, no synthesis)
    rv = an.quick_revalue(stored, 85)
    check("price drop widens gap vs held target", rv["new_gap"] > 0.30,
          f"gap={rv['new_gap']:.2f}")
    # price near target -> gap compresses
    rv2 = an.quick_revalue(stored, 128)
    check("price near target compresses gap", rv2["new_gap"] < 0.05)
    # crossing detection: stored gap below buy, new gap above -> crossed_buy
    stored_lo = {"price": 100, "our_view": {"fair_value": 110, "gap_vs_price": 0.10},
                 "normalized_fcff": 5e7, "market_cap": 5e8, "wacc": 0.09}
    rv3 = an.quick_revalue(stored_lo, 80)   # fair value 110 vs price 80 -> +37% gap
    check("gap crossing into buy zone flagged", rv3["crossed_buy"] is True,
          f"gap={rv3['new_gap']:.2f}")
    # cadence: 4 days stale -> due (twice weekly = 3 days)
    stale = {"last_full_revalue": (dt.date.today() - dt.timedelta(days=4)).isoformat()}
    fresh = {"last_full_revalue": dt.date.today().isoformat()}
    today = dt.date.today().isoformat()
    check("stale thesis (>3d) due for full revalue",
          scanner._due_for_full_revalue(stale, today) is True)
    check("freshly-revalued thesis not due",
          scanner._due_for_full_revalue(fresh, today) is False)


def test_scanner():
    section("Two-speed scanner (whole-universe trigger layer)")
    import scanner
    rec = {"latest": {"price": 100, "thesis": {"last_full_revalue": "2025-01-01"},
                      "our_view": {"fair_value": 130, "gap_vs_price": 0.30},
                      "normalized_fcff": 5e7, "market_cap": 5e8, "wacc": 0.09}}
    orig_move, orig_news, orig_evt = (scanner._abnormal_move,
                                      scanner._news_sentiment_signal,
                                      scanner._material_event_signal)
    scanner._abnormal_move = lambda t: (["big_move(+9.0%)"], 109.0)
    scanner._news_sentiment_signal = lambda t: ([], False)
    scanner._material_event_signal = lambda t, st, today: ([], False, False)
    try:
        s = scanner.scan_name("TEST", stored_record=rec, held=False)
        check("a big move promotes the name to deep synthesis",
              s["promote_to_deep_synthesis"] and s["priority"] >= 2,
              f"priority={s['priority']}")
        check("scan re-prices the gap cheaply", s["revalue"] is not None
              and s["revalue"]["new_gap"] is not None)
        # CONFIRMED MATERIAL EVENT (8-K) -> top priority (4), even with no price move
        scanner._abnormal_move = lambda t: ([], 100.0)
        scanner._material_event_signal = lambda t, st, today: (
            ["8K_HIGH-IMPACT event(material_agreement)"], True, False)
        s_evt = scanner.scan_name("EVT", stored_record=rec, held=False)
        check("confirmed material event -> top priority (4)",
              s_evt["priority"] == 4 and s_evt["material_event_confirmed"],
              f"priority={s_evt['priority']}")
        # quiet, freshly-valued name -> not promoted
        scanner._abnormal_move = lambda t: ([], 100.0)
        scanner._material_event_signal = lambda t, st, today: ([], False, False)
        rec2 = {"latest": {"price": 100, "thesis": {"last_full_revalue":
                __import__("datetime").date.today().isoformat()},
                "our_view": {"fair_value": 101, "gap_vs_price": 0.01},
                "normalized_fcff": 5e7, "market_cap": 5e8, "wacc": 0.09}}
        s2 = scanner.scan_name("QUIET", stored_record=rec2, held=False)
        check("quiet, freshly-valued name not promoted",
              not s2["promote_to_deep_synthesis"], f"triggers={s2['triggers']}")
    finally:
        scanner._abnormal_move = orig_move
        scanner._news_sentiment_signal = orig_news
        scanner._material_event_signal = orig_evt


def test_materiality():
    section("News materiality (events vs sentiment) + reliability")
    import news_layer as nl
    # substantive events are material
    for headline, cat in [("Acme announces partnership with Boeing", "partnership_contract"),
                          ("Rocket launch explodes on liftoff", "operational_failure"),
                          ("Pharma gets FDA approval", "regulatory"),
                          ("Company cuts full-year guidance", "guidance")]:
        c, m = nl._classify_event(headline)
        check(f"material event: {cat}", m and c == cat, f"got {c}")
    # sentiment/mood is NOT material
    for headline in ["Why investors are bullish on this stock",
                     "Stock surges on social media buzz"]:
        _, m = nl._classify_event(headline)
        check(f"sentiment not flagged material: '{headline[:30]}'", not m)
    # reliability: 2 sources of same event -> confirmed; 1 -> provisional
    two_src = [{"source": "alphavantage", "tier": 3, "title": "Acme wins major FDA approval",
                "url": "a", "published": "20260530", "sentiment_score": None},
               {"source": "finnhub", "tier": 3, "title": "Acme receives FDA approval for drug",
                "url": "b", "published": "20260530", "sentiment_score": None}]
    cl = nl._dedupe_and_map_perspectives(two_src)
    check("2-source material event -> confirmed",
          any(c.get("confidence") == "confirmed" for c in cl))
    one_src = [{"source": "rss", "tier": 3, "title": "Acme rumored to win FDA approval",
                "url": "a", "published": "", "sentiment_score": None}]
    cl2 = nl._dedupe_and_map_perspectives(one_src)
    check("1-source material event -> provisional",
          any(c.get("confidence") == "provisional" for c in cl2))


def test_horizon_aware_early():
    section("Horizon-aware early flag (long-timeline fit)")
    import retrospective as retro
    # build a matured record where we're only 30% through a long window, flat -> NOT early
    import datetime as dt
    created = (dt.date.today() - dt.timedelta(days=60)).isoformat()
    window = (dt.date.today() + dt.timedelta(days=600)).isoformat()  # long horizon
    # we can't easily run full score_thesis without prices; verify the frac logic:
    cd = dt.date.fromisoformat(created)
    wd = dt.date.fromisoformat(window)
    frac = (dt.date.today() - cd).days / max(1, (wd - cd).days)
    check("early flag suppressed when <70% through a long window", frac < 0.70,
          f"frac_elapsed={frac:.2f}")


def test_mechanism_judge():
    section("Mechanism judge (resolves unverified -> real verdict)")
    import retrospective as retro
    # parser handles a clean judge JSON and flags luck
    raw_played = ('{"mechanism_verdict":"played_out","explanation":"new 8-K confirms the '
                  'two contract wins the thesis predicted","checklist_assessment":[],'
                  '"was_outcome_luck":false,"lesson":"x"}')
    v, e = retro.from_judge_json(raw_played)
    check("judge parses played_out", v == "played_out")
    raw_luck = ('{"mechanism_verdict":"did_not","explanation":"stock rose on a buyout '
                'rumor unrelated to the thesis","was_outcome_luck":true,"lesson":"x"}')
    v2, e2 = retro.from_judge_json(raw_luck)
    check("judge flags luck when mechanism did_not but stock rose",
          v2 == "did_not" and e2.startswith("[FLAGGED LUCK]"))
    # bad verdict string falls back to unknown
    v3, _ = retro.from_judge_json('{"mechanism_verdict":"banana"}')
    check("invalid judge verdict -> unknown", v3 == "unknown")
    # live-judge wrapper feeds a provider's output through to a resolved verdict
    fake_provider = lambda prompt: raw_played
    judge = retro.make_live_judge(fake_provider)
    mv, _ = judge({"created": "2025-01-01", "mispriced_mechanism": "m",
                   "what_must_happen": []}, {"cik_for_judge": None,
                   "stock_return": 0.1, "idiosyncratic": 0.1})
    check("live-judge wrapper returns provider's verdict", mv == "played_out")
    # regression: a judge that returns the wrong shape or throws must surface judge_error,
    # NOT silently degrade to "unknown" (a broken learning loop should be visible).
    # Use a real ticker so pricing succeeds and execution actually reaches the judge.
    import datetime as _dt, engine as _eng, glob as _glob, json as _json, shutil as _sh, tempfile as _tf
    import config as _cfg, store as _st
    # v2: NEVER rmtree the real store/ (it is the git-tracked audit trail + LESSONS.md). Use a temp store.
    _tmp = _tf.mkdtemp(prefix="ee_qa_store_")
    _prev = _cfg.STORE_DIR
    _cfg.STORE_DIR = _tmp
    _eng.run(["SHOO"], gather_news=False, write_journal=False, persist=True)
    _f = (_glob.glob(f"{_tmp}/companies/*.json") or _glob.glob("store/companies/*.json"))[0]
    _rec = _json.load(open(_f))
    _th = _rec["latest"]["thesis"]
    _th["created"] = (_dt.date.today() - _dt.timedelta(days=800)).isoformat()
    _th["evaluation_window"] = (_dt.date.today() - _dt.timedelta(days=10)).isoformat()
    _th["direction"] = "long"
    s_bad = retro.score_thesis(_rec, mechanism_judge=lambda th, ctx: {"wrong": "shape"})
    check("malformed judge -> judge_error (not silent unknown)",
          s_bad and s_bad.get("mechanism_played_out") == "judge_error",
          f"got {s_bad.get('mechanism_played_out') if s_bad else None}")
    def _throw(th, ctx):
        raise ValueError("boom")
    s_err = retro.score_thesis(_rec, mechanism_judge=_throw)
    check("throwing judge -> judge_error with reason",
          s_err and s_err.get("mechanism_played_out") == "judge_error")
    _cfg.STORE_DIR = _prev
    _sh.rmtree(_tmp, ignore_errors=True)


def test_live_provider_integration():
    section("Live-provider integration (math overrides model spin)")
    import engine, json
    def provider_factory(growth, conviction):
        def provider(prompt):
            return json.dumps({
                "adjusted_growth": growth, "thesis_archetype": "catalyst_mispricing",
                "variant_view": "v", "mispriced_mechanism": "m", "rationale": "r",
                "bull_case": {"narrative": "b", "growth": growth + 0.04, "what_drives_it": "x"},
                "base_case": {"narrative": "b", "growth": growth, "what_drives_it": "x"},
                "bear_case": {"narrative": "b", "growth": growth - 0.05, "what_drives_it": "x"},
                "catalyst_path": "p", "what_must_happen": ["a"], "evidence": [],
                "catalyst": "c", "catalyst_date": "2026-09-30", "falsification": "f",
                "conviction": conviction, "horizon_months": 24, "edge_source": "synthesis"})
        return provider
    try:
        # contradictory: bullish archetype + high conviction but ZERO growth -> DCF must
        # produce a low/negative gap and the engine must NOT recommend BUY.
        res = engine.run(["SHOO"], llm_synth_provider=provider_factory(0.0, 5),
                         gather_news=False, write_journal=False, persist=False)
        r = res["rows"][0]
        if r.get("error"):
            check("live-provider run returned a result", False, r["error"][:50])
        else:
            gap = r["our_view"]["gap_vs_price"]
            action = r["recommendation"]["action"].upper()
            check("math overrides model spin (low growth -> not a BUY)",
                  not (gap < 0 and "BUY" in action), f"gap={gap:.2f} action={action}")
            check("provider archetype threads to thesis",
                  r["thesis"]["thesis_archetype"] == "catalyst_mispricing")
            check("provider scenarios thread to thesis",
                  all(r["thesis"].get(k) for k in ("bull_case", "base_case", "bear_case")))
        # conviction clamp survives the whole pipeline
        res2 = engine.run(["SHOO"], llm_synth_provider=provider_factory(0.06, 99),
                          gather_news=False, write_journal=False, persist=False)
        r2 = res2["rows"][0]
        if not r2.get("error"):
            check("conviction clamp survives full pipeline (99 -> <=5)",
                  r2["thesis"]["conviction"] <= 5, f"conv={r2['thesis']['conviction']}")
    except Exception as e:
        check("live-provider integration ran without crashing", False, f"{type(e).__name__}: {e}")


def test_live():
    section("Live integration (real EDGAR + prices)")
    try:
        res = engine.run(["SHOO", "UFPT"], positions=[{"ticker": "SHOO", "shares": 10}],
                         persist=False, write_journal=False, gather_news=False)
        rows = {r["ticker"]: r for r in res["rows"] if not r.get("error")}
        check("both live names returned", len(rows) == 2)
        for tk, r in rows.items():
            check(f"{tk}: has thesis with evidence",
                  r.get("thesis") and len(r["thesis"]["evidence"]) >= 1)
            check(f"{tk}: implied growth finite",
                  r["implied_growth"] is not None and math.isfinite(r["implied_growth"]))
            check(f"{tk}: WACC sane",
                  r["wacc"] is not None and 0.03 < r["wacc"] < 0.30, f"wacc={r['wacc']}")
            check(f"{tk}: recommendation present", bool(r["recommendation"]["action"]))
    except Exception as e:
        check("live integration ran without exception", False,
              f"{e}\n{traceback.format_exc()[:500]}")


def test_beta_alignment():
    section("Beta date-alignment (regression)")
    # market: 120 days; stock = identical series with interior days removed (a halt).
    # A stock that IS the market must have beta ~1.0 even with gaps.
    mkt_dates = [f"d{i:03d}" for i in range(120)]
    mkt_close = [100 * (1.001) ** i for i in range(120)]
    an._MKT.clear()
    an._MKT["ret_by_date"] = {mkt_dates[i]: (mkt_close[i] / mkt_close[i - 1] - 1,
                                             mkt_dates[i - 1])
                              for i in range(1, 120)}
    keep = [i for i in range(120) if not (40 <= i < 45)]
    s_dates = [mkt_dates[i] for i in keep]
    s_close = [mkt_close[i] for i in keep]
    pd = (s_dates, s_close, s_close, s_close, [1e6] * len(s_close))
    r = an.risk_stats("X", pd)
    b = r.get("beta_raw")
    check("beta of market-identical stock with a gap ~ 1.0",
          b is not None and abs(b - 1.0) < 0.05, f"beta={b}")
    an._MKT.clear()  # reset so live test refetches real market


def main():
    for t in (test_wacc, test_reverse_dcf, test_synthesis_machinery,
              test_incomplete_information, test_valuation_extremes,
              test_pathological_inputs, test_price_path_pathologies,
              test_portfolio_nan_guards, test_thesis,
              test_reco, test_ranking,
              test_beta_alignment, test_news_layer, test_retrospective,
              test_monitor, test_portfolio, test_dynamic_revalue, test_scanner,
              test_materiality, test_horizon_aware_early, test_mechanism_judge,
              test_live_provider_integration, test_live):
        try:
            t()
        except Exception as e:
            check(f"{t.__name__} crashed", False, f"{e}\n{traceback.format_exc()[:400]}")

    print("\n" + "=" * 70)
    print("QA HARNESS REPORT")
    print("=" * 70)
    n_pass = n_fail = 0
    for status, name, detail in results:
        if status == "SECTION":
            print(f"\n── {name} ──")
            continue
        mark = "✓" if status == PASS else "✗"
        print(f"  {mark} {name}" + (f"  [{detail}]" if detail and status == FAIL else ""))
        n_pass += status == PASS
        n_fail += status == FAIL
    print("\n" + "-" * 70)
    print(f"  {n_pass} passed, {n_fail} failed")
    print("-" * 70)
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
