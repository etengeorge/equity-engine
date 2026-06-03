"""
Throwaway adversarial battery: degenerate / extreme inputs across the system, focused
on the new/changed code (charts, connectors, routine, journal, company_brief/charts
threading) and the robustness seams. Offline (no network). Isolated temp STORE_DIR.
"""
import os
import tempfile
import json as J

os.environ["STORE_DIR"] = tempfile.mkdtemp(prefix="ee_extreme_")
os.environ.setdefault("PRICE_PROVIDER", "yfinance")

import charts
import connectors
import synthesis as syn
import thesis as th
import engine
import outputs
import journal
import scanner
import routine
import store as _store

PASS = 0
FAIL = 0
FAILS = []


def ok(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        FAILS.append(name)
        print("  ✗", name)


def noraise(name, fn, want_not_none=False):
    global PASS, FAIL
    try:
        r = fn()
        if want_not_none and r is None:
            FAIL += 1
            FAILS.append(name)
            print("  ✗", name, "(returned None)")
        else:
            PASS += 1
    except Exception as e:
        FAIL += 1
        FAILS.append(name)
        print("  ✗", name, "RAISED", type(e).__name__, str(e)[:140])


def boom(*a, **k):
    raise RuntimeError("boom")


C = charts.render_chart_to_datauri
print("\n── charts.py extremes ──")
ok("empty dict -> None", C({}) is None)
ok("None -> None", C(None) is None)
ok("list (not dict) -> None", C([1, 2]) is None)
ok("missing series -> None", C({"x": ["a"]}) is None)
ok("empty series -> None", C({"x": ["a"], "series": []}) is None)
ok("missing x -> None", C({"series": [{"name": "a", "data": [1], "kind": "bar"}]}) is None)
noraise("mismatched data length no crash", lambda: C({"x": ["a", "b", "c"], "series": [{"name": "s", "data": [1, 2], "kind": "line"}]}))
noraise("single-point combo", lambda: C({"x": ["FY25"], "series": [{"name": "rev", "data": [100], "kind": "bar", "axis": "left"}, {"name": "m", "data": [10.0], "kind": "line", "axis": "right"}]}), want_not_none=True)
noraise("negative+zero values", lambda: C({"x": ["a", "b", "c"], "series": [{"name": "m", "data": [-30.0, 0.0, 45.0], "kind": "line"}]}), want_not_none=True)
noraise("huge values", lambda: C({"x": ["a", "b"], "series": [{"name": "r", "data": [1e12, 2e12], "kind": "bar"}]}), want_not_none=True)
noraise("string data no crash", lambda: C({"x": ["a", "b"], "series": [{"name": "r", "data": ["x", "y"], "kind": "bar"}]}))
noraise("NaN/inf data no crash", lambda: C({"x": ["a", "b"], "series": [{"name": "r", "data": [float("nan"), float("inf")], "kind": "line"}]}))
noraise("$ and unicode title", lambda: C({"title": "Margin $100M->$2B · café ±5%", "x": ["a", "b"], "series": [{"name": "m", "data": [1, 2], "kind": "line"}]}), want_not_none=True)
noraise("many series color cycle", lambda: C({"x": ["a", "b"], "series": [{"name": f"s{i}", "data": [i, i + 1], "kind": "line"} for i in range(8)]}), want_not_none=True)

print("\n── connectors.py extremes ──")
ok("read_positions no source/no file -> []", connectors.read_positions(source=None, fallback_path="/nonexistent.json") == [])
ok("source not-a-list -> []", connectors.read_positions(source=lambda: "garbage") == [])
ok("source list of non-dicts -> []", connectors.read_positions(source=lambda: [1, 2, 3]) == [])
ok("source dicts missing ticker -> []", connectors.read_positions(source=lambda: [{"shares": 5}]) == [])
ok("source good -> normalized upper", connectors.read_positions(source=lambda: [{"ticker": "shoo", "shares": 10, "avg_cost": 35}]) == [{"ticker": "SHOO", "shares": 10, "avg_cost": 35}])
_tmpf = tempfile.mktemp(suffix=".json")
open(_tmpf, "w").write('[{"ticker":"AAA","shares":1,"avg_cost":2}]')
ok("source raises -> file fallback", connectors.read_positions(source=boom, fallback_path=_tmpf) == [{"ticker": "AAA", "shares": 1, "avg_cost": 2}])
_badf = tempfile.mktemp(suffix=".json")
open(_badf, "w").write("{not valid json")
noraise("malformed positions.json no crash", lambda: connectors.read_positions(source=None, fallback_path=_badf))
ok("email missing file -> not sent", connectors.send_brief_email("/nonexistent.html")["sent"] is False)
_okf = tempfile.mktemp(suffix=".html")
open(_okf, "w").write("<p>hi</p>")
ok("email dry-run (no sender)", connectors.send_brief_email(_okf)["sent"] is False)
ok("email real sender -> sent", connectors.send_brief_email(_okf, sender=lambda to, s, h: None, to="x@y") ["sent"] is True)
ok("email sender raises -> handled", connectors.send_brief_email(_okf, sender=boom)["sent"] is False)
noraise("sync dry-run (empty journal)", lambda: connectors.sync_journal_to_drive())

print("\n── synthesis from_llm_json / synthesize extremes ──")
FULL = {"adjusted_growth": 0.1, "thesis_archetype": "fundamentals_divergence", "conviction": 3,
        "horizon_months": 24, "company_brief": "Co does X", "edge_source": "interpretation",
        "charts": [{"title": "t", "x": ["a"], "series": [{"name": "m", "data": [1], "kind": "line"}]}]}
ok("valid -> source llm", syn.from_llm_json(J.dumps(FULL)).source == "llm")
ok("brief threaded", syn.from_llm_json(J.dumps(FULL)).company_brief == "Co does X")
ok("charts threaded", len(syn.from_llm_json(J.dumps(FULL)).charts) == 1)
ok("prose preamble extracted", syn.from_llm_json("Answer:\n" + J.dumps(FULL) + "\nDone.").source == "llm")
ok("```json fences", syn.from_llm_json("```json\n" + J.dumps(FULL) + "\n```").adjusted_growth == 0.1)
ok("conviction 99 -> clamp 5", syn.from_llm_json(J.dumps({**FULL, "conviction": 99})).conviction == 5)
ok("conviction -3 -> clamp 1", syn.from_llm_json(J.dumps({**FULL, "conviction": -3})).conviction == 1)
ok("bad archetype -> none_eff", syn.from_llm_json(J.dumps({**FULL, "thesis_archetype": "bogus"})).thesis_archetype == "none_efficiently_priced")
ok("charts non-list -> []", syn.from_llm_json(J.dumps({**FULL, "charts": "nope"})).charts == [])
ok("missing brief -> ''", syn.from_llm_json(J.dumps({k: v for k, v in FULL.items() if k != "company_brief"})).company_brief == "")
ctx = {"implied_growth": 0.08, "historical_cagr": 0.05, "filing_excerpts": []}
ok("synthesize empty -> stub", syn.synthesize(ctx, llm_json="").source.startswith("stub"))
ok("synthesize garbage -> stub", syn.synthesize(ctx, llm_json="no json here").source.startswith("stub"))
ok("synthesize missing adjusted_growth -> stub", syn.synthesize(ctx, llm_json=J.dumps({k: v for k, v in FULL.items() if k != "adjusted_growth"})).source.startswith("stub"))
ok("synthesize non-numeric growth -> stub", syn.synthesize(ctx, llm_json=J.dumps({**FULL, "adjusted_growth": "abc"})).source.startswith("stub"))
ok("synthesize non-int conviction -> stub", syn.synthesize(ctx, llm_json=J.dumps({**FULL, "conviction": "high"})).source.startswith("stub"))
ok("synthesize None -> deterministic stub", syn.synthesize(ctx, llm_json=None).source == "stub")
noraise("stub both None", lambda: syn.stub_synthesize({"implied_growth": None, "historical_cagr": None, "filing_excerpts": []}))
noraise("stub implied only", lambda: syn.stub_synthesize({"implied_growth": 0.1, "historical_cagr": None, "filing_excerpts": []}))
noraise("stub hist only", lambda: syn.stub_synthesize({"implied_growth": None, "historical_cagr": 0.05, "filing_excerpts": []}))


def mk_synth(**over):
    base = dict(adjusted_growth=0.1, market_narrative="m", implied_view_interpretation="i",
                consensus_interrogation="c", perspective_spread="p", thesis_archetype="fundamentals_divergence",
                variant_view="v", mispriced_mechanism="mm", rationale="r", deviation_explanation="d",
                bull_case={}, base_case={}, bear_case={}, catalyst_path="cp", what_must_happen=[],
                evidence=[], cross_source_corroboration="x", disconfirming="dc", catalyst="cat",
                catalyst_date=None, falsification="f", conviction=3, horizon_months=24, edge_source="none",
                company_brief="b", charts=[])
    base.update(over)
    return syn.SynthesisResult(**base)


print("\n── thesis.build_thesis extremes (evidence robustness) ──")
OV = {"fair_value": 12.0, "gap_vs_price": 0.2, "sign_survives_fcff_band": True}
noraise("evidence missing keys", lambda: th.build_thesis("T", mk_synth(evidence=[{"claim": "x", "source_form": "8-K"}]), 0.05, OV))
noraise("evidence extra keys", lambda: th.build_thesis("T", mk_synth(evidence=[{"claim": "x", "source_form": "8-K", "source_url": "u", "source_date": "d", "direction": "risk", "EXTRA": "boom"}]), 0.05, OV))
noraise("evidence non-dict string", lambda: th.build_thesis("T", mk_synth(evidence=["a string", "another"]), 0.05, OV))
noraise("our_view None", lambda: th.build_thesis("T", mk_synth(), 0.05, None))
noraise("to_dict after messy evidence", lambda: th.build_thesis("T", mk_synth(evidence=[{"claim": "x"}, "str"]), 0.05, OV).to_dict())
ok("none_eff -> direction hold", th.build_thesis("T", mk_synth(thesis_archetype="none_efficiently_priced"), 0.05, OV).direction == "hold")
ok("negative gap -> avoid", th.build_thesis("T", mk_synth(), 0.05, {"gap_vs_price": -0.3}).direction == "avoid")

print("\n── engine pure-function extremes ──")
ok("hist_cagr empty -> None", engine._hist_revenue_cagr([]) is None)
ok("hist_cagr single -> None", engine._hist_revenue_cagr([100]) is None)
ok("hist_cagr zeros/neg/None -> None", engine._hist_revenue_cagr([0, -5, None]) is None)
noraise("hist_cagr normal", lambda: engine._hist_revenue_cagr([200, 100]))
ok("sourcing no_valuation", engine._sourcing_signal(None, None)["label"] == "no_valuation")
ok("sourcing no_history", engine._sourcing_signal(0.1, None)["label"] == "no_history")
ok("sourcing rich", engine._sourcing_signal(0.2, 0.05)["label"] == "expectations_rich")
ok("sourcing low", engine._sourcing_signal(0.01, 0.2)["label"] == "expectations_low")


def snap(**o):
    base = dict(our_view={"gap_vs_price": 0.3, "sign_survives_fcff_band": True}, adv_usd=5e6, reliable=True,
                thesis={"thesis_archetype": "fundamentals_divergence", "conviction": 4},
                sourcing_signal={"label": "neutral"})
    base.update(o)
    return base


ok("huge gap reliable conv4 -> full", engine._recommend_one(snap(our_view={"gap_vs_price": 0.6, "sign_survives_fcff_band": True}), False)["sizing"] == "full")
ok("BUY not held gap>=bar", engine._recommend_one(snap(), False)["action"].startswith("BUY"))
ok("ADD held gap>=bar", engine._recommend_one(snap(), True)["action"] == "ADD")
ok("no_edge not held -> PASS", engine._recommend_one(snap(thesis={"thesis_archetype": "none_efficiently_priced", "conviction": 2}), False)["action"] == "PASS")
ok("no_edge held -> HOLD", engine._recommend_one(snap(thesis={"thesis_archetype": "none_efficiently_priced", "conviction": 2}), True)["action"] == "HOLD")
ok("illiquid -> avoid_sizing", engine._recommend_one(snap(adv_usd=100), False)["sizing"] == "avoid_sizing")
ok("not reliable -> BUY watch", "watch" in engine._recommend_one(snap(reliable=False), False)["action"])
ok("held big neg gap -> SELL/TRIM", engine._recommend_one(snap(our_view={"gap_vs_price": -0.5, "sign_survives_fcff_band": True}), True)["action"] == "SELL/TRIM")
ok("ov None held -> HOLD/REVIEW", engine._recommend_one(snap(our_view=None), True)["action"] in ("HOLD", "REVIEW"))
ok("ov None not held -> PASS/RESEARCH", engine._recommend_one(snap(our_view=None), False)["action"] in ("PASS", "RESEARCH"))

print("\n── routine pure-function extremes ──")
ok("universe missing file + no held -> []", routine.load_universe("/nope.txt", set()) == [])
ok("universe held only", routine.load_universe("/nope.txt", {"shoo"}) == ["SHOO"])
_wl = tempfile.mktemp(suffix=".txt")
open(_wl, "w").write("# comment line\nAAA  # inline comment\n\nbbb\nAAA\n")
ok("universe dedup+upper+comments+held", routine.load_universe(_wl, {"ccc"}) == ["AAA", "BBB", "CCC"])
ok("flagged held ADD", routine._has_flagged_action({"rows": [{"held": True, "recommendation": {"action": "ADD"}}]}) is True)
ok("flagged new BUY", routine._has_flagged_action({"rows": [{"recommendation": {"action": "BUY"}}]}) is True)
ok("not flagged HOLD/PASS", routine._has_flagged_action({"rows": [{"held": True, "recommendation": {"action": "HOLD"}}, {"recommendation": {"action": "PASS"}}]}) is False)
ok("flagged ignores error rows", routine._has_flagged_action({"rows": [{"error": "x"}]}) is False)
_orig_lbt = _store.load_by_ticker
_store.load_by_ticker = lambda t: ({"latest": {"ticker": t, "rank_score": 0.1, "recommendation": {"action": "HOLD"}}} if t == "STALE" else None)
_res = routine._assemble_full_book({"rows": [{"ticker": "FRESH", "rank_score": 0.5}]}, ["FRESH", "STALE", "MISSING"], {"queue": []})
ok("assemble adds stale row", any(r.get("ticker") == "STALE" and r.get("_stale") for r in _res["rows"]))
ok("assemble keeps fresh", any(r.get("ticker") == "FRESH" for r in _res["rows"]))
ok("assemble skips missing", not any(r.get("ticker") == "MISSING" for r in _res["rows"]))
_store.load_by_ticker = _orig_lbt

print("\n── outputs.py extremes ──")
noraise("dashboard empty rows", lambda: outputs.build_dashboard({"rows": [], "paper_mode": True}, tempfile.mktemp(suffix=".html")), want_not_none=True)
noraise("email empty rows", lambda: outputs.build_email({"rows": [], "paper_mode": True}, tempfile.mktemp(suffix=".html")), want_not_none=True)
noraise("dashboard error row", lambda: outputs.build_dashboard({"rows": [{"ticker": "ERR", "error": "no_cik"}], "paper_mode": True}, tempfile.mktemp(suffix=".html")))
FULLROW = {"ticker": "ZZZ", "name": "Ztest", "sector": "Tech", "price": 10.0,
           "our_view": {"gap_vs_price": 0.3, "fair_value": 13.0}, "implied_growth": 0.05, "wacc": 0.08,
           "beta_adjusted": 1.1, "adv_usd": 5e6, "reliable": True, "reliability_flags": [], "held": None,
           "rank_score": 0.3, "recommendation": {"action": "BUY", "reason": "x", "sizing": "half"},
           "thesis": {"thesis_archetype": "fundamentals_divergence", "conviction": 3, "edge_source": "interpretation",
                      "company_brief": "Ztest makes <b>widgets</b> & sells to OEMs", "market_narrative": "mn",
                      "consensus_interrogation": "ci", "implied_view_interpretation": "iv", "perspective_spread": "ps",
                      "variant_view": "vv", "mispriced_mechanism": "mm", "deviation_explanation": "de", "rationale": "rat",
                      "cross_source_corroboration": "cs", "evidence": [], "disconfirming": "dc", "catalyst": "cat",
                      "catalyst_date": None, "catalyst_path": "cp", "what_must_happen": ["a"], "falsification": "f",
                      "variant_growth": 0.1, "bull_case": {"growth": 0.2}, "base_case": {"growth": 0.1}, "bear_case": {"growth": 0.0},
                      "charts": [{"title": "Margin $1M->$2M", "x": ["FY24", "FY25"], "series": [{"name": "m", "data": [10, 12], "kind": "line"}]}]}}
_pfull = outputs.build_dashboard({"rows": [FULLROW], "paper_mode": True}, tempfile.mktemp(suffix=".html"))
_hfull = open(_pfull).read()
ok("full row renders", "ZZZ" in _hfull)
ok("chart embedded", "data:image/png;base64," in _hfull)
ok("company_brief html-escaped", "&lt;b&gt;widgets&lt;/b&gt;" in _hfull)
_stale = dict(FULLROW)
_stale["_stale"] = True
ok("stale badge", "scan only, not re-analyzed today" in open(outputs.build_dashboard({"rows": [_stale], "paper_mode": True}, tempfile.mktemp(suffix=".html"))).read())
_churn_res = {"rows": [dict(FULLROW, ticker="SHOO", held={"ticker": "SHOO"}, left_index=True)],
              "paper_mode": True,
              "universe_churn": {"added": ["PLAB"], "removed": ["SHOO"], "held_left": ["SHOO"], "prior_asof": "2026-06-01"}}
_cdash = open(outputs.build_dashboard(_churn_res, tempfile.mktemp(suffix=".html"))).read()
ok("dashboard: held-departure notice", "left the Russell 2000" in _cdash and "SHOO" in _cdash)
ok("dashboard: LEFT INDEX row badge", "LEFT INDEX" in _cdash)
ok("dashboard: churn summary line", "Index membership change" in _cdash)
ok("email: index-departure note", "Index departure" in open(outputs.build_email(_churn_res, tempfile.mktemp(suffix=".html"))).read())

print("\n── journal extremes (temp store) ──")
noraise("journal missing fields", lambda: journal.append_company_entry("Tech", "AAA", {"thesis_archetype": "x"}, {"price": 1}))
noraise("journal unicode+None brief/charts", lambda: journal.append_company_entry("Tech", "BBB", {"company_brief": None, "market_narrative": "café ±", "charts": None, "evidence": [{"direction": "risk", "claim": "c"}]}, {"price": 2, "recommendation": {"action": "HOLD"}}))
_pj = journal.append_company_entry("Tech", "CCC", {"company_brief": "Brief here", "charts": [{"title": "T1"}], "thesis_archetype": "y", "evidence": []}, {"price": 3, "name": "C", "recommendation": {"action": "HOLD"}})
_jb = open(_pj).read()
ok("journal brief rendered", "What this company is" in _jb and "Brief here" in _jb)
ok("journal charts note", "T1" in _jb)

print("\n── scanner pure-function extremes ──")
import datetime as _dt
_today = _dt.date.today().isoformat()
ok("due when no thesis", scanner._due_for_full_revalue(None, _today) is True)
ok("not due created today", scanner._due_for_full_revalue({"created": _today}, _today) is False)
ok("due when old", scanner._due_for_full_revalue({"created": "2020-01-01"}, _today) is True)
ok("due when bad date", scanner._due_for_full_revalue({"created": "garbage"}, _today) is True)

print("\n── fixed-bug regression (H1 peak-cycle / M2 run isolation / M3 corrupt store) ──")
_peak = syn.stub_synthesize({"implied_growth": -0.30, "historical_cagr": 0.33, "filing_excerpts": []})
ok("H1 stub peak-cycle -> none_efficiently_priced", _peak.thesis_archetype == "none_efficiently_priced")
ok("H1 stub peak-cycle -> adj not positive", _peak.adjusted_growth <= 0)
ok("H1 peak-cycle huge gap not held -> PASS (no_edge wins)",
   engine._recommend_one(snap(our_view={"gap_vs_price": 2.4, "sign_survives_fcff_band": True},
                              thesis={"thesis_archetype": _peak.thesis_archetype, "conviction": _peak.conviction}), False)["action"] == "PASS")
_cf = os.path.join(os.environ["STORE_DIR"], "companies")
os.makedirs(_cf, exist_ok=True)
open(os.path.join(_cf, "0000000001.json"), "w").write("{corrupt json")
ok("M3 store.load corrupt -> None (no crash)", _store.load(1) is None)
_orig_at = engine.analyze_ticker


def _fake_at(t, **k):
    if t == "BOOM":
        raise RuntimeError("kaboom")
    return {"error": "no_cik"}


engine.analyze_ticker = _fake_at
try:
    _r = engine.run(["BOOM", "OKK"], persist=False, write_journal=False, gather_news=False)
    ok("M2 raising ticker -> analysis_failed error row", any(str(x.get("error", "")).startswith("analysis_failed") for x in _r["rows"]))
    ok("M2 run continues after raise (both rows present)", len(_r["rows"]) == 2)
finally:
    engine.analyze_ticker = _orig_at

print("\n── universe.py loader / firehose parsing extremes ──")
import universe as _u
_SAMPLE_CSV = ('iShares Russell 2000 ETF\nFund Holdings as of,"May 30, 2026"\n\n'
               'Ticker,Name,Sector,Asset Class,Weight (%)\n'
               'SHOO,"STEVEN MADDEN",Consumer Discretionary,Equity,"0.05"\n'
               'calm,"CAL-MAINE",Consumer Staples,Equity,"0.05"\n'
               'USD,"USD CASH","Cash and/or Derivatives",Cash,"0.0"\n'
               'SHOO,"dup row",X,Equity,"0.0"\n')
_parsed = _u.parse_holdings_csv(_SAMPLE_CSV)
ok("universe parse: equity tickers uppercased", _parsed == ["SHOO", "CALM"])
ok("universe parse: drops cash line + de-dups", "USD" not in _parsed and _parsed.count("SHOO") == 1)
ok("universe parse: HTML consent page -> [] (no silent universe)",
   _u.parse_holdings_csv("<!DOCTYPE html><html><head>...consent...</head></html>") == [])
ok("universe parse: no Ticker header -> []", _u.parse_holdings_csv("a,b\n1,2\n") == [])
ok("universe plain-list parse (comments/dups/blanks)",
   _u._parse_plain_list("# header\nAAA\nbbb # note\n\nAAA\n") == ["AAA", "BBB"])
import re as _re
_idxline = ("8-K              ACADIA PHARMACEUTICALS INC                       "
            "1070494     20260529    edgar/data/1070494/0001193125-26-248242.txt")
ok("firehose CIK extracted from idx path", _re.search(r"edgar/data/(\d+)/", _idxline).group(1) == "1070494")
# dynamic membership churn (MEMBERSHIP_PATH lives under the temp STORE_DIR set at top)
_c1 = _u.record_membership(["A", "B", "C"], source="test")        # baseline, no prior same-source
ok("membership baseline -> no churn", _c1["added"] == [] and _c1["removed"] == [])
_c2 = _u.record_membership(["B", "C", "D"], source="test")        # A left, D entered
ok("membership detects new entrant", _c2["added"] == ["D"])
ok("membership detects departure", _c2["removed"] == ["A"])
_c3 = _u.record_membership(["X", "Y"], source="other")            # source change -> baseline reset
ok("membership source change -> no false churn", _c3["added"] == [] and _c3["removed"] == [])
_c4 = _u.record_membership(["Y"], source="other")                # now same source: X left
ok("membership resumes churn after reset", _c4["removed"] == ["X"])
# rotating batch cursor (CURSOR_PATH under the temp STORE_DIR -> isolated)
_uni = [f"T{i}" for i in range(10)]
_b1 = _u.next_batch(_uni, 3)
ok("batch 1 = first slice", _b1["batch"] == ["T0", "T1", "T2"] and _b1["start"] == 0)
ok("batch cycle_runs = ceil(n/size)", _b1["cycle_runs"] == 4)
ok("batch 2 advances cursor", _u.next_batch(_uni, 3)["batch"] == ["T3", "T4", "T5"])
_u.next_batch(_uni, 3)                                            # T6,T7,T8 -> cursor 9
ok("batch wraps around", _u.next_batch(_uni, 3)["batch"] == ["T9", "T0", "T1"])
ok("batch_size >= n -> full universe", _u.next_batch(_uni, 99)["batch"] == _uni)
ok("batch_size falsy -> full universe", _u.next_batch(_uni, None)["batch"] == _uni)
# cross-universe recommendation board (monkeypatch store.all_latest)
import routine as _rt
_orig_all = _store.all_latest
_store.all_latest = lambda: [
    {"ticker": "AAA", "recommendation": {"action": "BUY"}, "our_view": {"gap_vs_price": 0.4}, "rank_score": 0.4},
    {"ticker": "BBB", "recommendation": {"action": "PASS"}, "our_view": {"gap_vs_price": 0.01}, "rank_score": 0.01},
    {"ticker": "HLD", "recommendation": {"action": "HOLD"}, "our_view": {"gap_vs_price": 0.0}, "rank_score": 0.0}]
_board = [r["ticker"] for r in _rt._assemble_recommendation_board({"rows": [{"ticker": "DEEP", "rank_score": 0.9}]}, {"HLD"}, top=10)["rows"]]
ok("board keeps today's deep row", "DEEP" in _board)
ok("board surfaces actionable BUY", "AAA" in _board)
ok("board surfaces held even if HOLD", "HLD" in _board)
ok("board excludes non-actionable PASS", "BBB" not in _board)
_store.all_latest = _orig_all

print("\n── sectors.py / folder-method (vertical folder + company files + propagation) ──")
import sectors as _sec
import journal as _jr
import os as _os2
# from_llm_json parses the new emit fields
_fj = syn.from_llm_json(J.dumps({**FULL, "relationships": [{"entity": "X", "type": "supplier"}],
                                 "sector_update": {"learning": "L"}, "company_news": "CN"}))
ok("from_llm_json parses relationships", len(_fj.relationships) == 1)
ok("from_llm_json parses sector_update", _fj.sector_update.get("learning") == "L")
ok("from_llm_json parses company_news", _fj.company_news == "CN")
# relationships -> sector entity graph (entity -> the tickers it touches)
_sec.record_relationships("TestSec", "AAA", [{"entity": "USDA", "type": "regulator", "tickers": ["BBB"]},
                                             {"entity": "corn feed", "type": "input"}])
_d = _sec.load("TestSec")
ok("relationship: entity recorded", "USDA" in _d["entities"])
ok("relationship: entity -> self + peer tickers", set(_d["entities"]["USDA"]["tickers"]) == {"AAA", "BBB"})
ok("relationship: member tracked", "AAA" in _d["members"])
# sector-wide learning -> event log + narrative (the propagation substrate)
_sec.record_sector_update("TestSec", {"learning": "HPAI resurgence reported", "drivers": ["HPAI"],
                                      "entities": ["USDA"], "affected_tickers": ["AAA", "BBB"]}, ticker="AAA")
_d2 = _sec.load("TestSec")
ok("sector update -> event logged", any("HPAI" in e["event"] for e in _d2["events"]))
ok("sector update -> narrative set", "HPAI" in _d2["narrative"])
ok("sector dossier md readable (sector->company propagation source)", "HPAI" in _jr.read_sector_dossier("TestSec"))
# event-entity -> affected universe tickers (news->company reverse lookup)
_hits = _sec.affected_tickers(["USDA"], sectors=["TestSec"])
ok("propagation: entity -> affected tickers", set(_hits.keys()) == {"AAA", "BBB"})
# company-specific news written SEPARATELY into the company file inside the vertical folder
_jr.append_company_news("TestSec", "AAA", [{"title": "AAA signs partnership with BBB", "source_label": "rss"}], name="AAA Inc")
ok("company news -> company file", "partnership" in _jr.read_company_history("TestSec", "AAA"))
ok("company file co-located IN the vertical folder", _os2.path.exists(_os2.path.join(_jr.sector_dir("TestSec"), "AAA.md")))
ok("sector dossier co-located IN the vertical folder", _os2.path.exists(_jr.sector_md_path("TestSec")))
ok("read_all_vertical_notes picks up the new sector dossier", "TestSec" in _jr.read_all_vertical_notes())
# CROSS-INDUSTRY routing: a Tech name's HEALTHCARE-tagged edge lands in the Healthcare dossier
_sec.record_relationships("Technology", "TECHCO", [
    {"entity": "CMS reimbursement", "type": "regulator", "sector": "Healthcare", "note": "drives demand"},
    {"entity": "AWS", "type": "supplier"}])
_tech, _hc = _sec.load("Technology"), _sec.load("Healthcare")
ok("cross-industry: home-sector edge stays home", "AWS" in _tech["entities"])
ok("cross-industry: healthcare-tagged edge routes to Healthcare", "CMS reimbursement" in _hc["entities"])
ok("cross-industry: tech name logged as cross-sector member of Healthcare", "TECHCO" in _hc["cross_sector_members"])
ok("cross-industry: tech name NOT a normal Healthcare member", "TECHCO" not in _hc["members"])
ok("cross-industry: healthcare entity propagates to the tech name", "TECHCO" in _sec.affected_tickers(["CMS reimbursement"]))
_sec.record_sector_update("Technology", {"learning": "CMS cut telehealth reimbursement",
                                          "sectors": ["Healthcare"], "affected_tickers": ["TECHCO"]}, ticker="TECHCO")
ok("cross-industry: learning logged into the Healthcare dossier too",
   any("telehealth" in e["event"] for e in _sec.load("Healthcare")["events"]))
# sector-event -> scan propagation (the news -> recommendation wiring)
import datetime as _dt2
_sec.record_event("PropSec", "Big regulatory shift", date=_dt2.date.today().isoformat(), affected_tickers=["AAA", "BBB"])
ok("recent_event_tickers returns the affected names to re-examine",
   set(_sec.recent_event_tickers(days=3, sectors=["PropSec"]).keys()) == {"AAA", "BBB"})
ok("recent_event_tickers respects the time window", _sec.recent_event_tickers(since_date="2099-01-01", sectors=["PropSec"]) == {})
# commit_store audit-trail seam
import connectors as _conn
ok("commit_store dry-runs by default (touches no git)", _conn.commit_store()["dry_run"] is True)
_cap = {}
_conn.commit_store(committer=lambda sd, m: _cap.update({"sd": sd, "m": m}))
ok("commit_store calls the injected committer", "sd" in _cap)
ok("commit_store survives a raising committer", _conn.commit_store(committer=boom).get("committed") is False)

# ---------------------------------------------------------------------------
print("\n── congress.py extremes (congressional-trade sourcing) ──")
import congress as _cng
_ptr_sample = ("Periodic Transaction Report\nName: Hon. Nancy Pelosi\n"
               "SP NVIDIA Corp (NVDA) [ST] P 01/14/2025 02/12/2025 $1,000,001 - $5,000,000\n"
               "JT Apple Inc. (AAPL) [ST] Sale (Partial) 12/31/2024 02/12/2025 $250,001 - $500,000\n"
               "Bond Fund (no ticker) [OL] P 01/01/2025 $1,001 - $15,000\n")
_tr = _cng.parse_ptr_text(_ptr_sample)
ok("congress: extracts exactly the two ticketed rows", len(_tr) == 2)
ok("congress: NVDA 'P' -> buy", any(x["ticker"] == "NVDA" and x["type"] == "buy" for x in _tr))
ok("congress: 'Sale (Partial)' -> sale", any(x["ticker"] == "AAPL" and x["type"] == "sale" for x in _tr))
ok("congress: amount lower bound captured", any(x["ticker"] == "NVDA" and x["amount_low"] == 1000001 for x in _tr))
ok("congress: asset-type codes are not treated as tickers", all(x["ticker"] not in ("ST", "OL", "OP") for x in _tr))
ok("congress: amount range parser", _cng._amount_low_high("$50,001 - $100,000") == (50001, 100000))
ok("congress: amount parser on junk -> (0,0)", _cng._amount_low_high("n/a") == (0, 0))
ok("congress: high-signal filer flagged", _cng._is_high_signal("Hon. Nancy Pelosi") and not _cng._is_high_signal("John Q. Doe"))
ok("congress: summarize empty -> ''", _cng.summarize_trades([]) == "")
ok("congress: summarize non-empty -> str", isinstance(_cng.summarize_trades(
    [{"politician": "X", "type": "buy", "amount_str": "$1-2", "transaction_date": "2025-01-01", "high_signal": False}]), str))
noraise("congress: parse_ptr_text('') no raise", lambda: _cng.parse_ptr_text(""))
noraise("congress: parse_ptr_text(junk) no raise", lambda: _cng.parse_ptr_text("plain prose with no tickers at all"))
ok("congress: parse_ptr_text(junk) -> []", _cng.parse_ptr_text("plain prose with no tickers at all") == [])
# disabled trigger short-circuits with no network
_cng_flag = _cng.config.CONGRESS_TRADES_TRIGGER
_cng.config.CONGRESS_TRADES_TRIGGER = False
try:
    _dis = _cng.recent_congressional_trades()
    ok("congress: disabled trigger -> empty + flag", _dis["by_ticker"] == {} and "disabled" in _dis["flags"])
finally:
    _cng.config.CONGRESS_TRADES_TRIGGER = _cng_flag
# parsed-cache path returns without network (offline-safe regardless of pypdf)
_pcache_dir = os.path.join(_cng.config.STORE_DIR, "congress", "parsed")
os.makedirs(_pcache_dir, exist_ok=True)
with open(os.path.join(_pcache_dir, "12345678.json"), "w") as _pf:
    J.dump([{"ticker": "CACH", "type": "buy", "amount_low": 60000, "amount_high": 100000,
             "amount_str": "$60,001 - $100,000", "transaction_date": "2025-01-01", "asset": ""}], _pf)
ok("congress: parse_house_ptr reads parsed cache (offline)",
   _cng.parse_house_ptr("12345678", 2025)[0]["ticker"] == "CACH")

# ---------------------------------------------------------------------------
print("\n── engine.run congress + progress_cb plumbing (monkeypatched, offline) ──")
_plumb = {"cb": 0, "congress_seen": "UNSET"}


def _fake_analyze(t, llm_synth_provider=None, vertical_notes_text=None, gather_news=True, congress_trades=None):
    _plumb["congress_seen"] = congress_trades
    return {"ticker": t, "cik": 424242, "name": t, "sector": "Tech",
            "snapshot": {"ticker": t, "name": t, "sector": "Tech", "price": 10.0,
                         "our_view": {"fair_value": 13.0, "gap_vs_price": 0.30, "sign_survives_fcff_band": True},
                         "thesis": None, "reliable": True, "adv_usd": 5e6, "reliability_flags": [],
                         "congressional_trades": congress_trades},
            "gate": {"passed": True, "reasons": []}}


_orig_analyze = engine.analyze_ticker
engine.analyze_ticker = _fake_analyze
try:
    _pres = engine.run(["ZZZZ"],
                       congress_trades={"ZZZZ": [{"politician": "Nancy Pelosi", "type": "buy",
                                                  "amount_str": "$1M-5M", "high_signal": True,
                                                  "disclosure_date": "2025-02-12", "doc_url": ""}]},
                       progress_cb=lambda rows: _plumb.__setitem__("cb", _plumb["cb"] + 1),
                       persist=False, write_journal=False)
    ok("engine.run threads congress_trades into analyze_ticker", _plumb["congress_seen"] is not None)
    ok("engine.run fires progress_cb once per name", _plumb["cb"] == 1)
    ok("engine.run keeps congress trades on the row", bool(_pres["rows"][0].get("congressional_trades")))
finally:
    engine.analyze_ticker = _orig_analyze

# ---------------------------------------------------------------------------
print("\n── outputs dashboard: two tabs, live reports, congress panel ──")
_store.upsert({"cik": 999001, "ticker": "RPTX", "name": "ReportCo", "snapshot": {
    "ticker": "RPTX", "name": "ReportCo", "sector": "Tech", "price": 5.0,
    "our_view": {"fair_value": 7.0, "gap_vs_price": 0.4}, "recommendation": {"action": "BUY", "reason": "cheap"},
    "thesis": {"thesis_archetype": "catalyst_mispricing", "variant_view": "v", "mispriced_mechanism": "m",
               "conviction": 3, "horizon_months": 12, "evidence": [], "bull_case": {}, "base_case": {},
               "bear_case": {}, "what_must_happen": [], "catalyst": "c", "rationale": "r"},
    "reliability_flags": [], "rank_score": 0.4}})
_dpath = os.path.join(tempfile.mkdtemp(), "d.html")
outputs.build_dashboard({"rows": [], "paper_mode": True}, _dpath)
_ddoc = open(_dpath).read()
ok("dashboard: two tab buttons", _ddoc.count('class="tabbtn') >= 2)
ok("dashboard: board + reports panes", 'id="pane-board"' in _ddoc and 'id="pane-reports"' in _ddoc)
ok("dashboard: reports tab pulls the stored report", "RPTX" in _ddoc and "ReportCo" in _ddoc)
ok("dashboard: auto-refresh script + toggle embedded", "location.reload()" in _ddoc and 'id="ee_auto"' in _ddoc)
ok("dashboard: tab survives reload via hash", "eeShow" in _ddoc and "location.hash" in _ddoc)
ok("dashboard: recommend-only banner present", "This engine recommends" in _ddoc)
outputs.build_dashboard({"rows": [], "paper_mode": True, "_in_progress": True, "_deep_total": 5}, _dpath)
ok("dashboard: live in-progress note when a run is mid-flight", "in progress" in open(_dpath).read())
_crow = {"ticker": "NVDA", "name": "NVIDIA", "sector": "Tech", "price": 1.0,
         "our_view": {"fair_value": 2.0, "gap_vs_price": 0.5}, "recommendation": {"action": "BUY", "reason": "x"},
         "reliability_flags": [], "congressional_trades": [{"politician": "Nancy Pelosi", "chamber": "house",
            "type": "buy", "amount_str": "$1M-5M", "transaction_date": "2025-01-14",
            "disclosure_date": "2025-02-12", "high_signal": True, "doc_url": ""}]}
outputs.build_dashboard({"rows": [_crow], "paper_mode": True}, _dpath)
_ddoc2 = open(_dpath).read()
ok("dashboard: congressional-trade panel renders", "Congressional trade" in _ddoc2 and "Pelosi" in _ddoc2)
ok("dashboard: congress framed as a LOOK, not a copy signal", "not a signal to copy" in _ddoc2)
noraise("dashboard: _report_block survives a thesis-less snapshot",
        lambda: outputs._report_block({"ticker": "NOTH", "recommendation": {"action": "PASS", "reason": "x"}}))

print(f"\n{'=' * 60}\n  {PASS} passed, {FAIL} failed")
if FAILS:
    print("  FAILURES:", FAILS)

import shutil
shutil.rmtree(os.environ["STORE_DIR"], ignore_errors=True)
