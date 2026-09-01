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


# --- the markdown renderer must not mangle the vocabulary these logs use ------
def test_markdown_renderer():
    import dashboard as D
    h = D.md_to_html("A <script>alert(1)</script> tag & an ampersand.")
    check("markdown escapes HTML", "<script>" not in h and "&lt;script&gt;" in h, h)

    # snake_case is everywhere in these files (no_edge, stock_comp_is_67%_of_fcff).
    # A naive _italic_ rule eats them, so the guard is a hard requirement, not a nicety.
    h = D.md_to_html("Verdict no_edge with stock_comp_is_67%_of_fcff flagged.")
    check("snake_case survives the italic pass", "<em>" not in h, h)
    check("word-boundary underscores still italicise",
          "<em>risk</em>" in D.md_to_html("_risk_ — a note"),
          D.md_to_html("_risk_ — a note"))

    h = D.md_to_html("**Base case.** Text with `code` and https://sec.gov/x_y_z here.")
    check("bold renders", "<strong>Base case.</strong>" in h, h)
    check("code renders", "<code>code</code>" in h, h)
    check("bare url becomes a link", 'href="https://sec.gov/x_y_z"' in h, h)
    check("a url with underscores is not italicised", "x_y_z</a>" in h, h)

    h = D.md_to_html("## Heading\n\n- one\n- two\n\n> quoted\n\n---\n\npara")
    for frag in ("<h2>Heading</h2>", "<li>one</li>", "<blockquote>", "<hr>", "<p>para</p>"):
        check(f"markdown renders {frag}", frag in h, h)

    check("empty input is safe", D.md_to_html("") == "" and D.md_to_html(None) == "")


def test_research_site_structure():
    import dashboard as D, brief
    check("sector slug is url-safe and stable",
          D.sector_slug("Consumer Discretionary") == "consumer-discretionary"
          and D.sector_slug("Health Care") == "health-care", D.sector_slug("Health Care"))

    md = ("## 2026-01-01 — OLD\n\n**Base case.** stale one.\n\n"
          "## 2026-08-31 — NEW\n\n**Base case.** the current one.\n\n**Verdict:** x\n")
    check("latest_section reads the NEWEST entry, not the first",
          D.latest_section(md, "Base case") == "the current one.",
          D.latest_section(md, "Base case"))
    check("a missing label returns None rather than a guess",
          D.latest_section(md, "Nonexistent") is None)

    # the tree must come off the filesystem: imported names have a log and no verdict json
    tree = D.research_tree()
    if tree:
        for sector, tickers in tree.items():
            check(f"{sector} log paths resolve",
                  all(brief.research_path(sector, t).exists() for t in tickers))


def test_site_build_writes_both_tabs():
    """The dashboard and every research page must be generated in one pass, and every
    root-absolute link on them must resolve to a file that exists — a dead Research tab
    would look fine locally and 404 on Vercel."""
    import tempfile, pathlib, re, dashboard as D
    sc = json.loads((config.DATA / "screen.json").read_text())
    vdir = config.DATA / "verdicts"
    verdicts = [json.loads(p.read_text()) for p in sorted(vdir.glob("*.json"))] \
        if vdir.exists() else []
    with tempfile.TemporaryDirectory() as td:
        out, written = D.build(sc, [], verdicts, out=pathlib.Path(td) / "index.html")
        root = pathlib.Path(td)
        check("build returns the index plus research pages", out.exists() and len(written) > 1,
              f"{len(written)} pages")
        check("research index is written", (root / "research" / "index.html").exists())
        idx = out.read_text()
        check("both tabs are in the nav",
              "/research/index.html" in idx and ">Dashboard<" in idx and ">Research<" in idx)
        check("hero is exactly two stats",
              idx.count("<div class='stat'>") == 2, idx.count("<div class='stat'>"))
        check("hero shows universe and screened",
              "Total universe" in idx and "Total screened" in idx)
        bad = []
        for p in root.rglob("*.html"):
            for href in re.findall(r'href="(/[^"#]+)"', p.read_text()):
                if not (root / href.lstrip("/")).exists():
                    bad.append(f"{p.name} -> {href}")
        check("no broken internal links", not bad, "; ".join(bad[:5]))


# --- news layer --------------------------------------------------------------
def test_news_normalizes_both_yfinance_shapes():
    """yfinance has shipped two different news payloads. The 0.2.x form was flat with
    `uuid`/`link`/`providerPublishTime`; 1.x nests under `content`. requirements.txt
    pins a RANGE, so the Action can install either — reading only one shape would make
    the news layer silently return nothing after a routine dependency bump."""
    import news
    old = {"uuid": "abc", "title": "Old shape headline", "publisher": "Reuters",
           "link": "https://example.com/a", "providerPublishTime": 1756600000,
           "relatedTickers": ["BBW"]}
    new = {"id": "xyz", "content": {
        "title": "New shape headline", "summary": "A summary.",
        "pubDate": "2026-08-31T12:00:00Z",
        "provider": {"displayName": "Bloomberg"},
        "canonicalUrl": {"url": "https://example.com/b"}}}
    a, b = news._from_yf(old), news._from_yf(new, fallback_tickers=["STRT"])
    check("old yfinance shape parses", a and a["title"] == "Old shape headline", a)
    check("old shape keeps related tickers", a and "BBW" in a["tickers"], a)
    check("old shape epoch seconds become an ISO instant",
          a and a["ts"] == "2025-08-31T00:26:40+00:00", a and a["ts"])
    check("new yfinance shape parses", b and b["title"] == "New shape headline", b)
    check("new shape reads the nested publisher", b and b["publisher"] == "Bloomberg", b)
    check("new shape reads the canonical url",
          b and b["url"] == "https://example.com/b", b)
    check("a titleless article is dropped", news._from_yf({"id": "1"}) is None)


def test_news_store_dedupes_and_prunes():
    """The same wire story is returned every day it stays on Yahoo's page. Without an id
    check the store would grow by a full page per ticker per day instead of by what is
    actually new — which is the difference between a 5 MB store and a 200 MB one."""
    import news, tempfile, pathlib, datetime as _dt
    old_store = news.STORE
    with tempfile.TemporaryDirectory() as td:
        news.STORE = pathlib.Path(td)
        fresh = news._article("id1", _dt.datetime.now(_dt.timezone.utc).isoformat(),
                              "Fresh", "", "P", "u", ["T"], "test")
        stale = news._article("id2", (_dt.datetime.now(_dt.timezone.utc)
                                      - _dt.timedelta(days=200)).isoformat(),
                              "Stale", "", "P", "u", ["T"], "test")
        added, total = news.append("companies", "TEST", [fresh, stale, fresh])
        check("duplicate ids collapse on the way in", added == 2, added)
        check("an article past retention is dropped on write", total == 1, total)
        again, _ = news.append("companies", "TEST", [fresh])
        check("re-appending the same story adds nothing", again == 0, again)
        check("read honours the lookback window",
              len(news.read("companies", "TEST", days=90)) == 1)
        check("read of an unknown key is empty, not an error",
              news.read("companies", "NOSUCH") == [])
        news.STORE = old_store


def test_news_candidates_are_bounded_and_forced_picks_survive():
    """A company news pull is one HTTP round trip. The candidate set must stay inside its
    budget, and today's picks must never be crowded out of it by movers."""
    import news
    rows = [{"ticker": f"T{i}", "ret_5d": 0.5, "volume_ratio": 9.0} for i in range(900)]
    rows.append({"ticker": "QUIET", "ret_5d": 0.0})
    cands = news.candidates(rows, always=["PICK1", "PICK2"], max_names=50)
    check("candidate set respects max_names", len(cands) == 50, len(cands))
    check("forced picks are always included",
          {"PICK1", "PICK2"} <= set(cands), cands[:5])
    check("a name that did nothing is not fetched", "QUIET" not in cands)


def test_selection_falls_back_when_news_is_missing():
    """News is an enrichment, not a dependency. With an empty store every count must be
    zero and selection must behave exactly as it did before news existed — otherwise a
    throttled Yahoo silently changes which ten names get researched."""
    import daily, news, tempfile, pathlib
    old_store = news.STORE
    with tempfile.TemporaryDirectory() as td:
        news.STORE = pathlib.Path(td)
        rows = [{"ticker": "AAA", "sector": "Industrials", "cik": 1},
                {"ticker": "BBB", "sector": "Industrials", "cik": 2}]
        daily.attach_news(rows, event_ciks={1})
        check("filed_8k is stamped from the 8-K index", rows[0]["filed_8k"] is True)
        check("a non-filer is stamped false", rows[1]["filed_8k"] is False)
        check("news counts default to zero with an empty store",
              rows[0]["news_recent"] == 0 and rows[1]["news_recent"] == 0)
        check("no sector is hot with an empty store",
              not rows[0]["news_sector_hot"])
        news.STORE = old_store


def test_news_boost_cannot_select_on_its_own():
    """News is a MULTIPLIER on names that are already interesting on price, never a
    trigger. Coverage volume selects for what is already priced; this is a valuation
    screen, so a heavily covered name with no gap must still score at zero."""
    import daily
    covered = {"ticker": "LOUD", "sector": "Industrials", "news_recent": 6,
               "news_sector_hot": True, "gap": None, "cohort_pct": None}
    s, why = daily.urgency(covered, {}, set(), {})
    check("news alone cannot manufacture a score", s <= 0.5, f"score={s} why={why}")


# --- selection cooldown ------------------------------------------------------
def test_revisit_floor_blocks_a_same_day_repick():
    """On 2026-08-31 the material-event override re-picked BBW, STRT and WLFC hours after
    they were researched, taking three of four opportunistic slots. ret_21d barely moves
    day to day, so a name that fell 25% over three weeks satisfied the override EVERY day
    for three more weeks. A floor plus a freshness test is what stops that."""
    import daily
    visits = {"BBW": {"last_visit": dt_today()}}
    same_day = {"ticker": "BBW", "gap": 0.4, "flags": [], "ret_5d": -0.225,
                "ret_21d": -0.112}
    ok, why = daily.eligible_for_opportunistic(same_day, visits)
    check("a name researched today is not re-picked", not ok, why)
    check("the reason names the floor", "minimum" in (why or ""), why)

    stale_mover = {"ticker": "BBW", "gap": 0.4, "flags": [], "ret_5d": -0.01,
                   "ret_21d": -0.257}
    visits2 = {"BBW": {"last_visit": _days_ago(20)}}
    ok2, why2 = daily.eligible_for_opportunistic(stale_mover, visits2)
    check("an unchanged 21-day move no longer re-triggers the override", not ok2, why2)

    fresh_mover = {"ticker": "BBW", "gap": 0.4, "flags": [], "ret_5d": -0.25,
                   "ret_21d": -0.257}
    ok3, _ = daily.eligible_for_opportunistic(fresh_mover, visits2)
    check("a NEW 5-day move still overrides the cooldown", ok3)

    filer = {"ticker": "BBW", "gap": 0.4, "flags": [], "ret_5d": -0.01,
             "ret_21d": -0.01, "filed_8k": True}
    ok4, _ = daily.eligible_for_opportunistic(filer, visits2)
    check("a new 8-K still overrides the cooldown", ok4)


def dt_today():
    import datetime
    return datetime.date.today().isoformat()


def _days_ago(n):
    import datetime
    return (datetime.date.today() - datetime.timedelta(days=n)).isoformat()


# --- the two-runtime handshake -----------------------------------------------
def test_ready_marker_records_what_completed():
    """The analyst run is on its own schedule and cannot see whether the Action
    finished. It had been inferring that from a date stamp — which passed on a day the
    scheduled run fired 7h10m late. ready.json states what actually completed."""
    import screen as S, tempfile, pathlib, json as _json
    old = config.DATA
    with tempfile.TemporaryDirectory() as td:
        config.DATA = pathlib.Path(td)
        payload = {"generated_utc": "2026-09-01T11:30:00+00:00",
                   "price_asof": "2026-08-31",
                   "counts": {"modelled": 1082}, "rows": [{}] * 1956}
        S.write_ready(payload)
        doc = _json.loads((config.DATA / "ready.json").read_text())
        check("ready records the price session", doc["price_asof"] == "2026-08-31", doc)
        check("ready records coverage", doc["modelled"] == 1082, doc)
        check("ready computes a coverage percentage",
              50 < doc["modelled_pct"] < 60, doc["modelled_pct"])
        check("screen stage is stamped", "screen" in doc["stages"], doc)
        S.write_ready(payload, picks=["AAA"])
        doc2 = _json.loads((config.DATA / "ready.json").read_text())
        check("later stages accumulate rather than replacing",
              "screen" in doc2["stages"] and "pick" in doc2["stages"], doc2)
        check("picks are carried", doc2["picks"] == ["AAA"], doc2)
        config.DATA = old


# --- adhoc fetch -------------------------------------------------------------
def test_adhoc_html_to_text():
    """The analyst reads these, so script/style must not survive and block tags must
    become line breaks — otherwise a 10-K arrives as one unreadable paragraph."""
    import adhoc
    raw = ("<html><head><style>p{color:red}</style></head><body>"
           "<script>var x=1;</script><p>Revenue was &amp;nbsp;$1.2M</p>"
           "<div>Net income rose</div><table><tr><td>2025</td><td>100</td></tr></table>"
           "</body></html>")
    txt = adhoc.to_text(raw)
    check("script contents are removed", "var x" not in txt, txt)
    check("style contents are removed", "color:red" not in txt, txt)
    check("entities are decoded", "&amp;" not in txt, txt)
    check("block tags become newlines", "\n" in txt, repr(txt))
    check("visible text survives", "Net income rose" in txt, txt)


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
