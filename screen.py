"""The free daily pass: value all ~1,956 names with zero LLM tokens.

What this is NOT: a thesis. There is no judgment here. Every name gets a crude BASELINE
assumption (its own history), and the output is a ranked list of where price and history
disagree most loudly. That list decides which handful of names are worth spending real
reasoning on. The reasoning happens later, on ten names, not here on two thousand.

Two numbers per name:
  expectation_spread = implied_growth - baseline_growth
      what the price demands, minus what the business has actually delivered.
  baseline_gap = fair value under the baseline assumption / price - 1

And one guard: both are reported against their COHORT (same method, same sector).
Absolute gaps move with the equity-risk-premium and terminal-growth constants, which are
my choices, not facts -- so a whole sector can read "cheap" or "rich" purely because of
them. Cohort rank does not move with those constants, so it is the honest comparator.
"""
import csv, json, math, statistics, sys, time, datetime as dt
import config, edgar, prices, valuation as V


def load_universe(path=None):
    p = path or (config.ROOT / "universe.csv")
    with open(p) as fh:
        return list(csv.DictReader(fh))


def baseline_growth(fund):
    """A deliberately dumb forward assumption: what the top line actually did.
    Clamped, because a 5-year FCFF growth baseline outside this band is a bet, not a base."""
    rev = [r for r in (fund.get("revenue_series") or []) if V._fin(r) and r > 0]
    if len(rev) < 3:
        return None, "insufficient_revenue_history"
    newest, oldest = rev[0], rev[-1]
    yrs = len(rev) - 1
    cagr = (newest / oldest) ** (1 / yrs) - 1
    if not math.isfinite(cagr):
        return None, "nonfinite_cagr"
    clamped = min(max(cagr, -0.10), 0.25)
    note = f"{yrs}y revenue CAGR {cagr:+.1%}"
    if clamped != cagr:
        note += f" (clamped to {clamped:+.1%})"
    return clamped, note


def value_one(row, quote, rf):
    """Returns a flat dict per ticker. Never raises for a single bad name."""
    t = row["ticker"]
    out = {"ticker": t, "name": row["name"], "sector": row["sector"],
           "method_intended": row["method"], "weight_pct": float(row["weight_pct"]),
           "status": "ok", "flags": [], "gap": None, "expectation_spread": None}

    if quote is None or quote.get("status") == "no_data" or not V._fin(quote.get("price")):
        out.update(status="no_price", flags=["no_price_data"])
        return out
    price = float(quote["price"])
    out.update(price=price, ret_5d=quote.get("ret_5d"), ret_21d=quote.get("ret_21d"),
               ret_63d=quote.get("ret_63d"), ret_252d=quote.get("ret_252d"),
               dollar_volume_60d=quote.get("dollar_volume_60d"),
               beta=quote.get("beta"), beta_r2=quote.get("beta_r2"))
    if quote.get("status") == "stale":
        out["flags"].append(f"stale_price_{quote.get('stale_days')}d")

    cik = edgar.cik_for(t)
    if cik is None and quote.get("yahoo_symbol") and quote["yahoo_symbol"] != t:
        cik = edgar.cik_for(quote["yahoo_symbol"])   # EDGAR knows MOOG as MOG-A too
    if cik is None:
        out.update(status="no_cik", flags=out["flags"] + ["ticker_not_in_edgar_map"])
        return out
    out["cik"] = cik
    try:
        fund, src = edgar.fundamentals_cached(cik)
        out["fundamentals_source"] = src
        if src == "store_stale":
            out["flags"].append("edgar_unreachable_using_cached_extract")
    except FileNotFoundError:
        out.update(status="no_facts", flags=out["flags"] + ["no_xbrl_facts_filed"])
        return out
    except Exception as e:
        out.update(status="fetch_error", flags=out["flags"] + [f"edgar_error:{type(e).__name__}"])
        return out

    out["entity"] = fund.get("entity")
    out["fy_end"] = fund.get("fy_end")
    if fund.get("fy_end"):
        try:
            age = (dt.date.today() - dt.date.fromisoformat(fund["fy_end"])).days
            out["fundamentals_age_days"] = age
            if age > 500:
                out["flags"].append(f"last_10k_{age}d_old")
        except ValueError:
            pass

    if fund.get("shares_asof"):
        try:
            sage = (dt.date.today() - dt.date.fromisoformat(fund["shares_asof"])).days
            out["shares_asof"] = fund["shares_asof"]
            if sage > 400:
                # market cap = current price x a share count this old is a real error,
                # not a rounding one, once buybacks or a raise have happened
                out["flags"].append(f"share_count_{sage}d_stale_market_cap_unreliable")
        except ValueError:
            pass

    w = V.cost_of_capital(fund, price, quote.get("beta"), quote.get("beta_note"), rf)
    out["wacc"] = w.get("wacc")
    out["cost_of_equity"] = w.get("cost_of_equity")
    out["flags"] += w.get("flags", [])

    # liquidity + size gates: a gap you cannot trade is not an opportunity
    mktcap = w.get("market_cap")
    out["market_cap"] = mktcap
    if V._fin(mktcap) and mktcap < config.MIN_MARKET_CAP:
        out["flags"].append("below_min_market_cap")
    dv = quote.get("dollar_volume_60d")
    if V._fin(dv) and dv < config.MIN_DOLLAR_VOLUME:
        out["flags"].append("illiquid_below_min_dollar_volume")

    method = row["method"]
    if method == "none":
        out.update(status="not_modelled", method="none")
        out["flags"].append("sector_has_no_defensible_free_model")
        return out

    if method == "book":
        # NOTE: the book method never uses WACC, only cost of equity -- so an unreliable
        # WACC (banks rarely tag OperatingIncomeLoss) must not disqualify it.
        b = V.justified_pb(fund, price, w)
        out["method"] = "book"
        out["flags"] += b.get("flags", [])
        if not b.get("ok"):
            out.update(status="model_failed")
            return out
        out.update(rotce=b["rotce"], justified_p_tbv=b["justified_p_tbv"],
                   actual_p_tbv=b["actual_p_tbv"], tangible_book_per_share=b["tangible_book_per_share"],
                   fair_value=b["fair_value"], gap=b["gap"])
        return out

    # --- fcff ---------------------------------------------------------------
    out["method"] = "fcff"
    rd = V.reverse_dcf(fund, price, w)
    out["flags"] += rd.get("flags", [])
    if not rd.get("ok"):
        out.update(status="model_failed")
        if rd.get("note"):
            out["model_note"] = rd["note"]
        return out
    out.update(enterprise_value=rd["enterprise_value"], fcff_base=rd["fcff_base"],
               fcff_series=rd["fcff_series"], fcff_yield=rd["fcff_yield"],
               implied_growth=rd["implied_growth"],
               implied_growth_note=rd.get("implied_growth_note"),
               sbc=rd.get("sbc"), sbc_share_of_fcff=rd.get("sbc_share_of_fcff"),
               fcff_ex_sbc=rd.get("fcff_ex_sbc"),
               implied_growth_ex_sbc=rd.get("implied_growth_ex_sbc"),
               implied_growth_low_wacc=rd["sensitivity"]["low"]["implied_growth"],
               implied_growth_high_wacc=rd["sensitivity"]["high"]["implied_growth"])

    g, gnote = baseline_growth(fund)
    out["baseline_growth"] = g
    out["baseline_growth_note"] = gnote
    if g is None:
        out["flags"].append("no_baseline_growth")
        return out
    fd = V.forward_dcf(fund, price, w, g)
    out["flags"] += fd.get("flags", [])
    if fd.get("ok"):
        out.update(fair_value=fd["fair_value"], gap=fd["gap"])
    if V._fin(rd["implied_growth"], g):
        out["expectation_spread"] = rd["implied_growth"] - g
    return out


def add_cohort_ranks(rows):
    """Percentile of each name's gap within its own (method, sector) cohort.
    This is the comparator that survives my choice of ERP and terminal growth."""
    cohorts = {}
    for r in rows:
        if r.get("gap") is None or not math.isfinite(r["gap"]):
            continue
        if abs(r["gap"]) > config.MAX_ABS_GAP:
            continue                      # excluded from the cohort so outliers can't skew it
        cohorts.setdefault((r.get("method"), r["sector"]), []).append(r["gap"])
    stats = {}
    for k, gaps in cohorts.items():
        if len(gaps) < 8:                 # too thin to define a distribution honestly
            continue
        stats[k] = {"n": len(gaps), "median": statistics.median(gaps),
                    "sorted": sorted(gaps)}
    for r in rows:
        key = (r.get("method"), r.get("sector"))
        st = stats.get(key)
        r["cohort_n"] = st["n"] if st else None
        if not st or r.get("gap") is None or not math.isfinite(r["gap"]):
            r["cohort_pct"] = None
            r["gap_vs_cohort"] = None
            continue
        s = st["sorted"]
        below = sum(1 for x in s if x < r["gap"])
        r["cohort_pct"] = round(100.0 * below / len(s), 1)
        r["gap_vs_cohort"] = r["gap"] - st["median"]
    return stats


def run(limit=None, universe_path=None):
    uni = load_universe(universe_path)
    if limit:
        uni = uni[:limit]
    tickers = [r["ticker"] for r in uni]
    t0 = time.time()
    print(f"[screen] pricing {len(tickers)} tickers …", flush=True)
    quotes_df, _ = prices.build_quotes(tickers, {r["ticker"]: r["name"] for r in uni})
    quotes = {r["ticker"]: r for r in quotes_df.to_dict("records")}
    rf, rf_src = prices.risk_free_rate()
    print(f"[screen] rf={rf:.3%} ({rf_src}); valuing …", flush=True)

    rows = []
    for i, row in enumerate(uni, 1):
        try:
            rows.append(value_one(row, quotes.get(row["ticker"]), rf))
        except Exception as e:
            rows.append({"ticker": row["ticker"], "name": row["name"],
                         "sector": row["sector"], "status": "error",
                         "flags": [f"unhandled:{type(e).__name__}:{e}"], "gap": None})
        if i % 100 == 0:
            print(f"[screen]   {i}/{len(uni)}  ({time.time()-t0:.0f}s)", flush=True)

    for r in rows:
        r["flags"] = list(dict.fromkeys(r.get("flags", [])))
    edgar.save_store()
    cohorts = add_cohort_ranks(rows)
    payload = {
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "risk_free_rate": rf, "risk_free_source": rf_src,
        "assumptions": {"equity_risk_premium": config.EQUITY_RISK_PREMIUM,
                        "terminal_growth": config.TERMINAL_GROWTH,
                        "explicit_years": config.EXPLICIT_YEARS,
                        "marginal_tax_rate": config.MARGINAL_TAX_RATE,
                        "note": "absolute gaps move with these; cohort rank does not"},
        "counts": _counts(rows),
        "cohorts": {f"{m}|{s}": {"n": v["n"], "median_gap": v["median"]}
                    for (m, s), v in cohorts.items()},
        "rows": rows,
    }
    config.DATA.mkdir(parents=True, exist_ok=True)
    payload = _clean(payload)
    (config.DATA / "screen.json").write_text(json.dumps(payload, allow_nan=False, default=float))
    print(f"[screen] done in {time.time()-t0:.0f}s -> data/screen.json")
    for k, v in payload["counts"].items():
        print(f"          {k:16s} {v}")
    return payload


def _clean(obj):
    """NaN/Infinity are not valid JSON. pandas hands back NaN wherever a value was
    missing, and json.dumps writes it as a bare `NaN` token that Python happens to accept
    but strict parsers (including every JavaScript consumer) reject outright."""
    if isinstance(obj, dict):
        return {k: _clean(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_clean(v) for v in obj]
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if obj is not None and hasattr(obj, "item"):     # numpy scalars
        try:
            return _clean(obj.item())
        except Exception:
            return None
    return obj


def _counts(rows):
    from collections import Counter
    c = Counter(r.get("status", "?") for r in rows)
    c["modelled"] = sum(1 for r in rows if r.get("gap") is not None)
    return dict(c)


if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    run(limit=lim)
