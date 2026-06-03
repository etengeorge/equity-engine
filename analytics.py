"""
analytics.py - the quant core.

Four pieces, in the order the engine runs them:
  1. validate()      - the gate. Bad data is the #1 maker of fake opportunities.
  2. risk_stats()    - beta / vol / ATR / liquidity from adjusted prices.
  3. compute_wacc()  - CAPM cost of equity + synthetic-rating cost of debt, with a band.
  4. reverse_dcf()   - solve for the growth the MARKET implies, then price OUR view.

Everything carries a reliability flag. When inputs break (negative EBIT, thin
trading, WACC <= terminal growth) the name is flagged, not silently valued.
"""
import math
import statistics as stats

import config
import data_sources as ds

# Damodaran-style interest-coverage -> default-spread map (synthetic rating).
# Coverage is EBIT / interest expense. Higher coverage -> tighter spread.
_SPREAD_TABLE = [
    (8.50, 0.0075, "AAA/AA"), (6.50, 0.0100, "A"), (4.25, 0.0140, "A-/BBB"),
    (3.00, 0.0200, "BBB"),    (2.50, 0.0300, "BB"), (2.00, 0.0400, "BB-/B+"),
    (1.50, 0.0550, "B"),      (1.25, 0.0750, "B-"), (0.80, 0.0950, "CCC"),
    (-1e9, 0.1300, "CC/distressed"),
]


# ---------------------------------------------------------------- market cache
_MKT = {}

def _market_returns():
    """Daily returns of the S&P 500 proxy keyed by date, cached for the run."""
    if "ret_by_date" in _MKT:
        return _MKT["ret_by_date"]
    p = ds.get_prices("^GSPC", lookback_days=420)
    if not p:
        _MKT["ret_by_date"] = {}
        return {}
    dates, closes = p[0], p[1]
    # guard against bad ticks in the benchmark: only form a return when BOTH adjacent closes
    # are valid positive finite numbers (a single zero/NaN here would crash every beta calc).
    rbd = {}
    for i in range(1, len(closes)):
        a, b = closes[i - 1], closes[i]
        if (isinstance(a, (int, float)) and isinstance(b, (int, float))
                and math.isfinite(a) and math.isfinite(b) and a > 0):
            rbd[dates[i]] = (b / a - 1, dates[i - 1])
    _MKT["ret_by_date"] = rbd
    return rbd


# ------------------------------------------------------------------ risk stats
def risk_stats(ticker, price_data):
    if not price_data:
        return {"reliable": False, "reasons": ["no_price_data"]}
    dates, closes, highs, lows, vols = price_data
    n = len(closes)
    reasons = []
    # price-series sanity FIRST: a zero, negative, or non-finite close breaks every return
    # calc (div-by-zero, NaN propagation). Keep only the clean leading run of valid prices;
    # if too little survives, refuse. Real feeds emit bad ticks, halts, and NaNs.
    clean_idx = [i for i, c in enumerate(closes)
                 if isinstance(c, (int, float)) and math.isfinite(c) and c > 0]
    if len(clean_idx) < n:
        reasons.append("bad_prices_in_series_filtered")
    if len(clean_idx) < 2:
        return {"reliable": False, "reasons": reasons + ["no_valid_prices"]}
    # rebuild parallel arrays from valid indices only
    dates = [dates[i] for i in clean_idx]
    closes = [closes[i] for i in clean_idx]
    highs = [highs[i] if isinstance(highs[i], (int, float)) and math.isfinite(highs[i]) else closes[k]
             for k, i in enumerate(clean_idx)]
    lows = [lows[i] if isinstance(lows[i], (int, float)) and math.isfinite(lows[i]) else closes[k]
            for k, i in enumerate(clean_idx)]
    vols = [vols[i] if (i < len(vols) and isinstance(vols[i], (int, float))
                        and math.isfinite(vols[i])) else 0 for i in clean_idx]
    n = len(closes)
    if n < config.MIN_PRICE_HISTORY_DAYS:
        reasons.append("thin_history")

    rets = [(closes[i] / closes[i - 1] - 1) for i in range(1, n)]
    # a single huge jump (e.g. >300% one-day move) usually signals a corporate action,
    # bad tick, or post-halt reopen rather than a real return — flag, don't silently use it.
    if any(abs(r) > 3.0 for r in rets):
        reasons.append("extreme_single_day_move_suspect")
    vol_ann = stats.pstdev(rets) * math.sqrt(252) if len(rets) > 5 else None
    vol_30 = stats.pstdev(rets[-30:]) * math.sqrt(252) if len(rets) >= 30 else None

    # ATR% : average true range over ~14d as a fraction of price
    trs = []
    for i in range(1, n):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]),
                 abs(lows[i] - closes[i - 1]))
        trs.append(tr)
    atr_pct = (sum(trs[-14:]) / 14) / closes[-1] if len(trs) >= 14 and closes[-1] else None

    # average daily dollar volume over ~30d -> executability gate input
    adv = (sum(closes[i] * vols[i] for i in range(max(0, n - 30), n))
           / min(30, n)) if vols else None

    # beta vs market: pair by SHARED DATES and exclude any return that spans a gap.
    # A return at day d is only valid if d-1 (the prior row) is present too; we pair
    # only days valid on BOTH axes, so neither side contributes a multi-day return.
    mkt_by_date = _market_returns()                    # {date: (ret, prev_date)}
    beta_raw, beta_adj, r2 = None, None, None
    stock_rbd = {dates[i]: (rets[i - 1], dates[i - 1]) for i in range(1, n)}
    common = []
    for d in sorted(set(stock_rbd) & set(mkt_by_date)):
        s_ret, s_prev = stock_rbd[d]
        m_ret, m_prev = mkt_by_date[d]
        if s_prev == m_prev:        # same prior trading day on both -> clean 1-step
            common.append((d, s_ret, m_ret))
    if len(common) > 30:
        y = [c[1] for c in common]
        x = [c[2] for c in common]
        m = len(common)
        mx, my = sum(x) / m, sum(y) / m
        cov = sum((x[i] - mx) * (y[i] - my) for i in range(m)) / m
        varx = sum((xi - mx) ** 2 for xi in x) / m
        vary = sum((yi - my) ** 2 for yi in y) / m
        if varx > 0:
            beta_raw = cov / varx
            beta_adj = 0.67 * beta_raw + 0.33  # Blume shrink toward 1.0
            r2 = (cov ** 2) / (varx * vary) if vary > 0 else 0.0
    else:
        reasons.append("insufficient_overlap_for_beta")
    if r2 is not None and r2 < config.MIN_BETA_R2:
        reasons.append("beta_low_r2")
    if adv is not None and adv < config.MIN_ADV_USD:
        reasons.append("illiquid")

    return {
        "as_of": dates[-1], "price": closes[-1],
        "beta_raw": beta_raw, "beta_adjusted": beta_adj, "beta_r2": r2,
        "beta_method": "blume" if beta_adj is not None else None,
        "vol_annualized": vol_ann, "vol_30d": vol_30, "atr_pct": atr_pct,
        "adv_usd": adv, "lookback_days": n,
        "reliable": len([r for r in reasons if r in ("thin_history", "beta_low_r2")]) == 0,
        "reasons": reasons,
    }


# ------------------------------------------------------------------------ WACC
def _synthetic_spread(coverage):
    for thresh, spread, rating in _SPREAD_TABLE:
        if coverage >= thresh:
            return spread, rating
    return _SPREAD_TABLE[-1][1], _SPREAD_TABLE[-1][2]


def compute_wacc(fund, price, beta_adj):
    rf, rf_src = ds.risk_free_rate()
    erp = config.EQUITY_RISK_PREMIUM
    t = config.MARGINAL_TAX_RATE
    reasons = []

    beta = beta_adj if beta_adj is not None else 1.0
    if beta_adj is None:
        reasons.append("beta_defaulted_to_1")
    # a non-finite beta (from a degenerate regression on insane volatility) can't yield a
    # valid cost of capital — fall back to the neutral 1.0 and flag it, never compute on NaN.
    if not _finite(beta):
        beta = 1.0
        reasons.append("nonfinite_beta_defaulted")
    cost_equity = rf + beta * erp

    ebit = fund.get("ebit")
    intex = fund.get("interest_expense") or 0.0
    debt = fund.get("total_debt") or 0.0

    if debt <= 0 or intex <= 0:
        # negligible / no debt -> debt leg barely matters; use tightest spread.
        spread, rating, coverage = _SPREAD_TABLE[0][1], "no/low debt", None
    elif ebit is None or ebit <= 0:
        spread, rating, coverage = 0.13, "unrated(neg EBIT)", None
        reasons.append("neg_ebit_synthetic_rating_unreliable")
    else:
        coverage = ebit / intex
        spread, rating = _synthetic_spread(coverage)
    cost_debt = rf + spread

    mktcap = price * fund["shares"] if fund.get("shares") else None
    if not mktcap or not _finite(mktcap):
        return {"reliable": False, "reasons": ["no_shares_or_nonfinite_mktcap"]}
    V = mktcap + debt
    wE, wD = mktcap / V, debt / V
    wacc = wE * cost_equity + wD * cost_debt * (1 - t)

    # WACC sanity: a non-finite, negative, or implausibly high (>50%) cost of capital is not a
    # usable discount rate. Negative WACC is economically nonsensical for a going concern.
    if not _finite(wacc):
        reasons.append("nonfinite_wacc")
    elif wacc <= 0:
        reasons.append("nonpositive_wacc_nonsensical")
    elif wacc > 0.50:
        reasons.append("implausibly_high_wacc")

    reliable = not any(r in reasons for r in (
        "neg_ebit_synthetic_rating_unreliable", "nonfinite_wacc",
        "nonpositive_wacc_nonsensical", "implausibly_high_wacc"))
    return {
        "rf": rf, "rf_source": rf_src, "erp": erp, "tax_rate": t,
        "beta_used": beta, "cost_of_equity": cost_equity,
        "interest_coverage": coverage, "implied_rating": rating,
        "cost_of_debt": cost_debt, "weight_equity": wE, "weight_debt": wD,
        "wacc_point": wacc,
        "wacc_band": {"low": wacc - config.WACC_BAND, "high": wacc + config.WACC_BAND},
        "market_cap": mktcap, "reliable": reliable, "reasons": reasons,
    }


# ----------------------------------------------------------------- reverse DCF
def _normalized_fcff(fund, tax, return_years=False):
    """FCFF ~= avg(CFO - capex) + after-tax interest, over the normalization window.
    Honest simplifications: uses reported CFO (so SBC is left inside CFO as the
    company reports it), and a simple multi-year average to damp working-capital
    and capex lumpiness. Negative -> caller flags valuation_unreliable.
    With return_years=True, also returns how many years were averaged (1-year is a
    thin, lumpy normalization the caller should flag)."""
    cfo = fund.get("cfo_series") or []
    capex = fund.get("capex_series") or []
    k = min(len(cfo), len(capex))
    if k == 0:
        return (None, 0) if return_years else None
    base = [cfo[i] - capex[i] for i in range(k)]
    fcf = sum(base) / k
    intex = fund.get("interest_expense") or 0.0
    val = fcf + intex * (1 - tax)
    return (val, k) if return_years else val


def _ev_from_growth(fcff0, g, wacc, years, g_term):
    """PV of two-stage FCFF: explicit growth for `years`, then Gordon terminal."""
    if wacc <= g_term:
        return None
    pv, fcff = 0.0, fcff0
    for yr in range(1, years + 1):
        fcff *= (1 + g)
        pv += fcff / (1 + wacc) ** yr
    tv = fcff * (1 + g_term) / (wacc - g_term)
    pv += tv / (1 + wacc) ** years
    return pv


_IMPLIED_GROWTH_FLOOR = -0.50
_IMPLIED_GROWTH_CEILING = 1.00


def _solve_implied_growth(target_ev, fcff0, wacc, years, g_term):
    """Bisection: find g so PV(FCFF) == target_ev (current enterprise value)."""
    if fcff0 is None or fcff0 <= 0 or wacc <= g_term:
        return None
    lo, hi = _IMPLIED_GROWTH_FLOOR, _IMPLIED_GROWTH_CEILING
    f = lambda g: (_ev_from_growth(fcff0, g, wacc, years, g_term) or -1e18) - target_ev
    flo, fhi = f(lo), f(hi)
    if flo > 0:        # even at -50% growth the model values it above price
        return lo
    if fhi < 0:        # even at +100% growth the model can't reach the price
        return hi
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def reverse_dcf(fund, price, wacc_block, research_growth=None):
    """
    Returns implied-growth (what the market prices) at the central WACC and across
    the WACC band, plus, if a research_growth is supplied, OUR fair value and the gap.
    research_growth is the human/synthesis input: the growth YOUR research supports.
    """
    tax = config.MARGINAL_TAX_RATE
    fcff0, fcff_years = _normalized_fcff(fund, tax, return_years=True)
    shares = fund.get("shares")
    debt = fund.get("total_debt") or 0.0
    cash = fund.get("cash") or 0.0
    years, g_term = config.HIGH_GROWTH_YEARS, config.TERMINAL_GROWTH

    # WACC must exceed terminal growth or the Gordon terminal value diverges (division by
    # (wacc - g) -> 0 or negative). The math returns None in that case, but flag it explicitly
    # so a caller never sees reliable=True with a missing value and no reason.
    wacc_point = wacc_block.get("wacc_point")
    if not _finite(wacc_point) or wacc_point <= g_term:
        return {"reliable": False, "reasons": ["wacc_below_terminal_growth"],
                "normalized_fcff": None}

    # defense in depth: a non-finite or bad share count can never produce a valid value.
    if not _finite(shares) or shares <= 0:
        return {"reliable": False, "reasons": ["nonfinite_or_bad_shares"],
                "normalized_fcff": fcff0}
    # missing or non-positive FCFF (None, NaN, Inf, or <=0) -> cannot value.
    if fcff0 is None or not math.isfinite(fcff0) or fcff0 <= 0:
        return {"reliable": False, "reasons": ["nonpositive_normalized_fcff"],
                "normalized_fcff": fcff0}

    # SOFT flag: a 1-year FCFF base is lumpy (no averaging to damp capex/working-capital).
    # The valuation still runs, but the caller surfaces this so the view isn't over-trusted.
    soft_reasons = []
    if fcff_years < 2:
        soft_reasons.append("thin_fcff_normalization_1yr")

    mktcap = price * shares
    current_ev = mktcap + debt - cash
    wacc = wacc_block["wacc_point"]

    implied = _solve_implied_growth(current_ev, fcff0, wacc, years, g_term)
    # CRITICAL: if the solver pins at its floor/ceiling, the market price is OUTSIDE what the
    # reverse-DCF can explain within [-50%, +100%] growth. The implied number and any gap are
    # then meaningless (e.g. a +9000% gap that would falsely rank #1). Treat as UNRELIABLE so
    # it cannot produce a confident recommendation — the model simply can't value this name.
    at_bound = (implied is not None and
                (implied <= _IMPLIED_GROWTH_FLOOR + 1e-9 or implied >= _IMPLIED_GROWTH_CEILING - 1e-9))
    if at_bound:
        return {"reliable": False,
                "reasons": ["implied_growth_at_solver_bound_unvaluable"],
                "normalized_fcff": fcff0, "implied_growth": implied,
                "note": ("market price implies growth outside [-50%, +100%]; reverse-DCF "
                         "cannot pin a meaningful value or gap for this name")}
    # Higher WACC discounts harder, so it implies HIGHER growth to justify the same price;
    # lower WACC implies LOWER growth. Label by the WACC each is computed at (no lies).
    implied_at_high_wacc = _solve_implied_growth(current_ev, fcff0, wacc_block["wacc_band"]["high"], years, g_term)
    implied_at_low_wacc = _solve_implied_growth(current_ev, fcff0, wacc_block["wacc_band"]["low"], years, g_term)

    out = {
        "reliable": True, "reasons": list(soft_reasons),
        "normalized_fcff": fcff0, "fcff_normalization_years": fcff_years,
        "current_ev": current_ev,
        "implied_growth": implied,
        "implied_growth_band": {"at_high_wacc": implied_at_high_wacc,
                                "at_low_wacc": implied_at_low_wacc},
        "assumptions": {"high_growth_years": years, "terminal_growth": g_term,
                        "wacc_used": wacc},
        "our_view": None,
    }

    if research_growth is not None:
        if not _finite(research_growth):
            out["reasons"] = list(out.get("reasons", [])) + ["nonfinite_research_growth"]
            out["reliable"] = False
            return out
        # fair value at OUR growth, plus FCFF sensitivity band
        def fair(fcff_mult):
            ev = _ev_from_growth(fcff0 * fcff_mult, research_growth, wacc, years, g_term)
            if ev is None:
                return None
            eq = ev - debt + cash
            return eq / shares
        fv = fair(1.0)
        fv_lo = fair(1 - config.FCFF_BAND_PCT)
        fv_hi = fair(1 + config.FCFF_BAND_PCT)
        # A non-positive fair value is degenerate (equity can't be worth < 0); don't report a
        # negative price target or a gap off it. Flag and suppress the gap.
        if fv is not None and fv <= 0:
            out["reasons"] = list(out.get("reasons", [])) + ["nonpositive_fair_value_degenerate"]
            out["our_view"] = {
                "research_growth": research_growth, "fair_value": fv,
                "fair_value_band": {"low": fv_lo, "high": fv_hi},
                "gap_vs_price": None, "sign_survives_fcff_band": None,
                "note": "implied equity value <= 0 (distressed/negative-equity); gap suppressed",
            }
            return out
        gap = (fv - price) / price if fv else None
        # does the sign of the call survive the FCFF band?
        survives = None
        if fv_lo and fv_hi:
            survives = ((fv_lo - price) * (fv_hi - price)) > 0  # same side of price
        extra = []
        # An implausibly large gap (>5x or <-95%) is almost always a data artifact (stale
        # price, wrong share count, one-off FCFF), not a real edge. Flag as suspect so it
        # doesn't silently rank #1; the recommendation layer down-weights unreliable names.
        if gap is not None and (gap > 5.0 or gap < -0.95):
            extra.append("extreme_gap_suspect_data_artifact")
        out["reasons"] = list(out.get("reasons", [])) + extra
        out["our_view"] = {
            "research_growth": research_growth, "fair_value": fv,
            "fair_value_band": {"low": fv_lo, "high": fv_hi},
            "gap_vs_price": gap, "sign_survives_fcff_band": survives,
        }
        # an extreme gap is suspect enough to withhold the reliable stamp
        if "extreme_gap_suspect_data_artifact" in extra:
            out["reliable"] = False
    return out


# --------------------------------------------------------------- quick revalue
def quick_revalue(stored_snapshot, new_price):
    """CHEAP daily re-price: given a name's last full analysis (stored fair value,
    variant growth, FCFF base, WACC) and a NEW price, recompute the gap and the
    market-implied growth WITHOUT re-pulling financials or re-running synthesis.
    Runs on the whole universe daily. The TARGET (fair value) is held fixed from the
    last full re-do; only the gap moves with price."""
    if not stored_snapshot or not _finite(new_price) or new_price <= 0:
        return None
    ov = stored_snapshot.get("our_view") or {}
    fair_value = ov.get("fair_value")
    if fair_value is not None and not _finite(fair_value):
        fair_value = None       # corrupt stored target -> no gap, don't propagate NaN/Inf
    stored_price = stored_snapshot.get("price")
    fcff0 = stored_snapshot.get("normalized_fcff")
    shares = (stored_snapshot.get("market_cap") / stored_price
              if (stored_snapshot.get("market_cap") and _finite(stored_price)
                  and stored_price > 0) else None)
    wacc = stored_snapshot.get("wacc")
    gap = ((fair_value - new_price) / new_price) if fair_value else None
    if gap is not None and not _finite(gap):
        gap = None
    implied = None
    if _finite(fcff0) and fcff0 > 0 and shares and _finite(wacc):
        debt = stored_snapshot.get("_debt") or 0.0
        cash = stored_snapshot.get("_cash") or 0.0
        ev = new_price * shares + debt - cash
        implied = _solve_implied_growth(ev, fcff0, wacc, config.HIGH_GROWTH_YEARS,
                                        config.TERMINAL_GROWTH)
    prior_gap = ov.get("gap_vs_price")
    return {
        "new_price": new_price, "fair_value_held": fair_value,
        "new_gap": gap, "prior_gap": prior_gap, "new_implied_growth": implied,
        "crossed_buy": (gap is not None and gap >= config.SCAN_GAP_BUY
                        and (prior_gap is None or prior_gap < config.SCAN_GAP_BUY)),
        "crossed_sell": (gap is not None and gap <= config.SCAN_GAP_SELL
                         and (prior_gap is None or prior_gap > config.SCAN_GAP_SELL)),
        "note": "Gap re-priced against the stored target; target unchanged until the "
                "next full re-do (twice/week or news-triggered).",
    }


# --------------------------------------------------------------- the gate
def _finite(*vals):
    """True only if every supplied value is a finite number (rejects NaN/Inf/None)."""
    for v in vals:
        if v is None or not isinstance(v, (int, float)) or not math.isfinite(v):
            return False
    return True


def validate(fund, price, risk):
    reasons = []
    # 0) non-finite / corrupt inputs (NaN, Inf) — a broken data feed must never look clean.
    if price is not None and not (isinstance(price, (int, float)) and math.isfinite(price)):
        reasons.append("nonfinite_price")
    for key in ("revenue", "ebit", "shares", "total_debt", "cash", "interest_expense"):
        v = fund.get(key)
        if v is not None and not (isinstance(v, (int, float)) and math.isfinite(v)):
            reasons.append(f"nonfinite_{key}")
    for seriesname in ("cfo_series", "capex_series", "revenue_series"):
        s = fund.get(seriesname) or []
        if any(not (isinstance(x, (int, float)) and math.isfinite(x)) for x in s):
            reasons.append(f"nonfinite_{seriesname}")
    # 1) basic presence / sign sanity
    if not fund.get("shares") or not (isinstance(fund.get("shares"), (int, float))
                                      and fund["shares"] > 0):
        reasons.append("bad_shares")
    if price is None or not (isinstance(price, (int, float)) and price > 0):
        reasons.append("bad_price")
    if fund.get("ebit") is None:
        reasons.append("missing_ebit")
    if (fund.get("total_debt") or 0) < 0:
        reasons.append("negative_debt")
    if not fund.get("cfo_series"):
        reasons.append("missing_cashflow")
    # 2) internally IMPOSSIBLE financials — corrupt data that would otherwise value cleanly.
    rev = fund.get("revenue")
    ebit = fund.get("ebit")
    if _finite(rev) and rev < 0:
        reasons.append("negative_revenue_impossible")
    if _finite(rev, ebit) and rev > 0 and ebit > rev:
        reasons.append("ebit_exceeds_revenue_impossible")   # >100% operating margin
    if _finite(fund.get("interest_expense")) and (fund.get("interest_expense") or 0) < 0:
        reasons.append("negative_interest_expense_impossible")
    if _finite(fund.get("cash")) and (fund.get("cash") or 0) < 0:
        reasons.append("negative_cash_impossible")
    return {"passed": len(reasons) == 0, "reasons": reasons}
