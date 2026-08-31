#!/usr/bin/env python3
"""Offline regression tests. No network, no fixtures on disk, runs in under a second.

Every test here corresponds to a bug that actually shipped and produced a wrong number.
They are cheap to run and specific on purpose: the previous version of this project had
1,300 lines of monolithic network-dependent tests that nobody could run in a loop.

    python test_engine.py
"""
import json, sys, math
import config, valuation as V, daily, record, screen

FAILED, PASSED = [], 0


def check(name, cond, detail=""):
    global PASSED
    if cond:
        PASSED += 1
    else:
        FAILED.append(f"{name}: {detail}")


# --- 1. XBRL alias selection must prefer RECENT data over list order ----------
def test_alias_recency():
    import edgar
    facts = {"facts": {"us-gaap": {
        # listed later in _ALIASES but current -- must win
        "Revenues": {"units": {"USD": [
            {"fp": "FY", "form": "10-K", "fy": 2011, "end": "2011-08-31", "val": 7_918_430_000}]}},
        "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [
            {"fp": "FY", "form": "10-K", "fy": 2025, "end": "2025-08-31", "val": 7_798_000_000}]}},
    }}}
    vals, concept, end = edgar._series(facts, "revenue", 3)
    check("alias recency beats list order", end == "2025-08-31",
          f"picked {concept} ending {end} — a 2011 value would poison every downstream number")

    # and the reverse: when the FIRST-listed alias is the stale one
    facts2 = {"facts": {"us-gaap": {
        "RevenueFromContractWithCustomerExcludingAssessedTax": {"units": {"USD": [
            {"fp": "FY", "form": "10-K", "fy": 2012, "end": "2012-12-31", "val": 1}]}},
        "Revenues": {"units": {"USD": [
            {"fp": "FY", "form": "10-K", "fy": 2025, "end": "2025-12-31", "val": 99}]}},
    }}}
    vals2, _, end2 = edgar._series(facts2, "revenue", 3)
    check("alias recency, reversed", end2 == "2025-12-31" and vals2[0] == 99, f"{vals2} {end2}")


# --- 2. an acquisition mid-window must not corrupt price/tangible-book -------
def test_pb_acquisition():
    # book roughly doubles via acquisition; earnings scale with it, so the RETURN is flat
    # UMB Financial's real figures across the Heartland acquisition: book went
    # $3.47B -> $7.69B and goodwill $0.28B -> $2.33B, while the underlying return on
    # tangible equity barely moved. Averaging LEVELS reported 20.5% ROTCE and a 4.53x
    # P/TBV; the true current multiple is 2.05x.
    fund = {"net_income_series": [702e6, 441e6, 350e6],
            "equity_series": [7694e6, 3467e6, 3100e6],
            "goodwill_series": [2100e6, 240e6, 245e6],
            "intangibles_series": [235e6, 31e6, 32e6],
            "goodwill": 2100e6, "intangibles": 235e6, "shares": 75_960_675}
    w = {"cost_of_equity": 0.1065, "reliable": True}
    r = V.justified_pb(fund, 144.59, w)
    check("acquisition: model produces a result", r.get("ok"), str(r.get("flags")))
    if not r.get("ok"):
        return
    # per-year ROTCE must be stable despite book doubling — that is the whole point
    spread = max(r["rotce_by_year"]) - min(r["rotce_by_year"])
    check("acquisition: ROTCE stable across the deal", spread < 0.05,
          f"ratios {[f'{x:.1%}' for x in r['rotce_by_year']]} — averaging LEVELS gave 20.5%")
    # P/TBV must be priced off the LATEST book, not a three-year average of it
    tbvps = (7694e6 - 2100e6 - 235e6) / 75_960_675
    check("acquisition: P/TBV uses latest book",
          abs(r["actual_p_tbv"] - 144.59 / tbvps) < 1e-6,
          f"got {r['actual_p_tbv']:.2f}, averaging levels gave 4.53 vs the true 2.05")


# --- 3. a missing EBIT tag is not a loss -------------------------------------
def test_missing_ebit_not_a_loss():
    base = {"shares": 10e6, "total_debt": 0.0, "cash": 0.0, "short_term_investments": 0.0,
            "interest_expense": 0.0}
    w = V.cost_of_capital({**base, "ebit": None}, 20.0, 1.0, None, 0.045)
    check("no EBIT + no debt stays usable", w.get("reliable"),
          f"flags {w.get('flags')} — this used to blackball profitable companies")

    # but a genuine loss WITH heavy debt must be treated as unreliable
    heavy = {"shares": 10e6, "total_debt": 900e6, "cash": 0.0,
             "short_term_investments": 0.0, "interest_expense": 50e6, "ebit": -20e6}
    w2 = V.cost_of_capital(heavy, 5.0, 1.0, None, 0.045)
    check("loss-making AND leveraged is unreliable", not w2.get("reliable"),
          f"debt weight {w2.get('weight_debt'):.0%}, flags {w2.get('flags')}")


# --- 4. the DCF must invert exactly ------------------------------------------
def test_dcf_roundtrip():
    fcff, wacc = 100e6, 0.09
    for g in (-0.20, -0.05, 0.0, 0.06, 0.18, 0.35):
        ev = V.ev_from_growth(fcff, g, wacc)
        back, note = V.implied_growth(ev, fcff, wacc)
        check(f"reverse DCF inverts at g={g:+.0%}", back is not None and abs(back - g) < 1e-6,
              f"solved {back} vs {g} ({note})")
    # and it must refuse, not guess, when the model is undefined
    bad, note = V.implied_growth(1e9, 100e6, 0.02)     # wacc below terminal growth
    check("refuses when WACC <= terminal growth", bad is None, f"returned {bad}")
    neg, note = V.implied_growth(1e9, -5e6, 0.09)      # negative cash flow
    check("refuses on negative FCFF", neg is None, f"returned {neg}")


# --- 5. beta reliability, not a blanket clamp --------------------------------
def test_beta_gate():
    import pandas as pd, numpy as np, prices
    idx = pd.date_range("2024-01-05", periods=140, freq="W-FRI")
    rng = np.random.default_rng(7)
    bench = pd.Series(np.cumprod(1 + rng.normal(0.001, 0.02, 140)) * 100, index=idx)
    # a real low-beta name: correlated, slope 0.3
    br = bench.pct_change().fillna(0)
    low = pd.Series(np.cumprod(1 + 0.3 * br.values + rng.normal(0, 0.004, 140)) * 50, index=idx)
    b, r2, note = prices.beta(low, bench)
    check("real low beta survives", b is not None and 0.2 < b < 0.45,
          f"beta={b} r2={r2} note={note} — clamping this to 0.6 adds ~165bp to cost of equity")
    # pure noise: must be refused, not reported
    noise = pd.Series(np.cumprod(1 + rng.normal(0, 0.05, 140)) * 50, index=idx)
    b2, r22, note2 = prices.beta(noise, bench)
    check("uncorrelated noise is refused", b2 is None and note2.startswith("unreliable"),
          f"beta={b2} r2={r22} note={note2}")


# --- 6. cohort percentile direction: HIGH percentile means CHEAP --------------
def test_cohort_direction():
    rows = [{"ticker": f"T{i}", "sector": "Widgets", "method": "fcff",
             "gap": (i - 10) / 20.0, "flags": []} for i in range(21)]
    screen.add_cohort_ranks(rows)
    cheapest = max(rows, key=lambda r: r["gap"])
    richest = min(rows, key=lambda r: r["gap"])
    check("highest gap = highest percentile", cheapest["cohort_pct"] > 90,
          f"cheapest name got {cheapest['cohort_pct']}th pct")
    check("lowest gap = lowest percentile", richest["cohort_pct"] < 10,
          f"richest name got {richest['cohort_pct']}th pct")

    # and the selector must reward the cheap end, not the rich end
    empty = {}
    s_cheap, why_c = daily.urgency({**cheapest, "cik": 1}, {}, set(), empty)
    s_rich, why_r = daily.urgency({**richest, "cik": 2}, {}, set(), empty)
    check("selector ranks cheap above rich", s_cheap > s_rich,
          f"cheap={s_cheap:.2f} {why_c} vs rich={s_rich:.2f} {why_r} — "
          "inverted, this screens for the most expensive names in the index")


# --- 7. cyclical base detection ----------------------------------------------
def test_cycle_flags():
    peak = V.normalized_fcff({"cfo_series": [455e6, 338e6, 241e6],
                              "capex_series": [0, 0, 0], "interest_expense": 0})
    check("peak cycle flagged",
          any("peak_cycle" in f for f in peak["flags"]), str(peak["flags"]))
    trough = V.normalized_fcff({"cfo_series": [120e6, 172e6, 210e6],
                                "capex_series": [0, 0, 0], "interest_expense": 0})
    check("trough cycle flagged",
          any("trough_cycle" in f for f in trough["flags"]), str(trough["flags"]))
    steady = V.normalized_fcff({"cfo_series": [105e6, 100e6, 98e6],
                                "capex_series": [0, 0, 0], "interest_expense": 0})
    check("steady series not flagged as cyclical",
          not any("cycle" in f for f in steady["flags"]), str(steady["flags"]))
    neg = V.normalized_fcff({"cfo_series": [-50e6, -40e6], "capex_series": [10e6, 10e6],
                             "interest_expense": 0})
    check("negative FCFF refused, not valued",
          "nonpositive_normalized_fcff" in neg["flags"], str(neg["flags"]))


# --- 8. analyst JSON ingestion is tolerant but never invents judgment ---------
def test_parse():
    o = record.parse('```json\n{"final_growth": 0.07, "verdict": "cheap", '
                     '"conviction": "high", "devils_advocate": {"strongest_counter": "x"}}\n```')
    check("parses fenced json", o["final_growth"] == 0.07 and o["verdict"] == "cheap", str(o))

    o2 = record.parse('Here is my answer:\n{"final_growth": 8, "verdict": "cheap", '
                      '"conviction": "high", "devils_advocate": {"strongest_counter": "x"}}')
    check("percent-as-integer corrected", abs(o2["final_growth"] - 0.08) < 1e-9,
          f"got {o2['final_growth']}")

    o3 = record.parse('{"final_growth": 0.95, "verdict": "cheap", "conviction": "high"}')
    check("absurd growth clamped", o3["final_growth"] == record.GROWTH_BOUNDS[1],
          f"got {o3['final_growth']}")
    check("missing devil's advocate is called out",
          any("UNCHALLENGED" in n for n in o3["_parse_notes"]), str(o3["_parse_notes"]))

    o4 = record.parse('{"verdict": "moon", "conviction": "extreme"}')
    check("unknown verdict falls back to no_edge", o4["verdict"] == "no_edge", str(o4))
    check("unknown conviction falls back to low", o4["conviction"] == "low", str(o4))
    check("missing growth is not invented", o4["final_growth"] is None, str(o4))


# --- 9. hard rule: there is no order path anywhere ---------------------------
def test_no_order_path():
    import pathlib, re
    banned = re.compile(r"\b(place_order|submit_order|buy_market|sell_market|"
                        r"create_order|place_crypto_order|execute_trade)\b")
    hits = []
    for p in pathlib.Path(".").glob("*.py"):
        if p.name == "test_engine.py":
            continue                      # this file names the patterns in order to ban them
        for i, line in enumerate(p.read_text().splitlines(), 1):
            if banned.search(line):
                hits.append(f"{p}:{i}  {line.strip()[:60]}")
    check("no order-placement code path exists", not hits, str(hits))


def test_selection_shape():
    rows = [{"ticker": f"T{i}", "name": f"N{i}", "sector": "Widgets", "method": "fcff",
             "gap": (i % 30 - 15) / 30.0, "cik": i, "flags": [],
             "ret_5d": 0.01, "ret_21d": 0.02, "price": 10.0,
             "dollar_volume_60d": 5e6, "market_cap": 5e8} for i in range(200)]
    screen.add_cohort_ranks(rows)
    sel = daily.select({"rows": rows}, event_ciks=set())
    picks = sel["picks"]
    check("selects the configured number", len(picks) == config.DAILY_SLOTS, str(len(picks)))
    check("no duplicate picks", len({p["ticker"] for p in picks}) == len(picks), "duplicates")
    check("rotation slots honoured",
          sum(1 for p in picks if p["slot"] == "rotation") == config.ROTATION_SLOTS,
          str([p["slot"] for p in picks]))
    check("every pick states a reason", all(p["why"] for p in picks), "a pick had no rationale")
    check("cursor advances", sel["cursor"]["index"] > 0, str(sel["cursor"]))


def test_limit_never_clobbers_the_real_screen():
    """A limited run is a smoke test. It once overwrote the committed 1,956-row screen
    with 40 rows and pushed it, leaving the live dashboard reporting a 40-name universe
    as though that were the Russell 2000."""
    import inspect, screen as S, run as R
    src = inspect.getsource(S.run)
    check("limited screen writes to a separate file",
          "screen.sample.json" in src and "sample = out_path is None" in src,
          "screen.run has no sample-path guard")
    check("the real screen path is only the default",
          'out_path = out_path or (config.DATA / "screen.json")' in src,
          "screen.run still writes screen.json unconditionally")
    dsrc = inspect.getsource(R.cmd_daily)
    check("a limited daily run skips selection",
          "_is_smoke(args)" in dsrc and "return" in dsrc,
          "cmd_daily still advances the cursor and rewrites picks on a smoke test")


# --- % of 52-week high must degrade, not lie, on an older screen -------------
def test_pct_of_52w_high():
    """The column reads off high_252d, which screens written before that field existed do
    not carry. A missing high must render as em-dash, never as 100% of a missing high."""
    import dashboard as D
    check("a real high renders as a percentage of it",
          '>67%<' in D._pct_of_high(67.0, 100.0),
          D._pct_of_high(67.0, 100.0))
    check("at the high reads 100%", '>100%<' in D._pct_of_high(100.0, 100.0),
          D._pct_of_high(100.0, 100.0))
    for price, high in ((50.0, None), (None, 100.0), (50.0, 0.0), (None, None)):
        check(f"missing/degenerate high ({price},{high}) renders em-dash",
              "—" in D._pct_of_high(price, high) and "%" not in D._pct_of_high(price, high),
              D._pct_of_high(price, high))
    # the screen must actually carry the field forward, or the column is dead on arrival
    import inspect
    src = inspect.getsource(screen.value_one)
    check("screen.value_one carries high_252d into the row",
          "high_252d=quote.get(\"high_252d\")" in src,
          "the dashboard column would be permanently em-dash")


def main():
    for fn in sorted([v for k, v in globals().items() if k.startswith("test_")],
                     key=lambda f: f.__name__):
        try:
            fn()
        except Exception as e:
            FAILED.append(f"{fn.__name__} raised {type(e).__name__}: {e}")
    print(f"\n{PASSED} passed, {len(FAILED)} failed")
    for f in FAILED:
        print(f"  FAIL  {f}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
