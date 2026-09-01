"""The two-sided model.

Reverse DCF: what 5-year FCFF growth does today's PRICE already require?
Forward DCF: what is the business worth under MY assumptions?
The difference between those two numbers is the only thing this engine is looking for.

Nothing here narrates. If the inputs don't support a number, it returns None and a reason.
"""
import math
import config

# --- small helpers -----------------------------------------------------------
def _fin(*v):
    return all(x is not None and isinstance(x, (int, float)) and math.isfinite(x) for x in v)


def _mean(xs):
    xs = [x for x in xs if _fin(x)]
    return sum(xs) / len(xs) if xs else None


# --- cost of capital ---------------------------------------------------------
# Damodaran-style synthetic rating: interest coverage -> default spread.
_SPREAD = [(12.5, 0.0075), (9.5, 0.0100), (7.5, 0.0125), (6.0, 0.0150), (4.5, 0.0200),
           (3.5, 0.0250), (3.0, 0.0325), (2.5, 0.0425), (2.0, 0.0550), (1.5, 0.0750),
           (1.25, 0.0950), (0.8, 0.1200), (0.5, 0.1500)]


def _synthetic_spread(coverage):
    for threshold, spread in _SPREAD:
        if coverage >= threshold:
            return spread
    return 0.1800


def cost_of_capital(fund, price, beta, beta_note, rf, sector_beta=None):
    """WACC with an explicit reliability verdict. An unmeasurable beta falls back to the
    median of the name's own sector rather than to a flat 1.0, and says which it used.

    A flat 1.0 was wrong at both ends of this universe: utilities regress to a 0.44
    median and health care to 1.24, so the old default overstated a utility's cost of
    equity by roughly 300bp and understated a biotech's by 130bp. The sector median is
    measured on the same benchmark (IWM) and the same 104-week window as every other
    beta here, which is what makes it comparable; an externally sourced beta computed
    against a different index on monthly data would not be.
    """
    flags = []
    erp, tax = config.EQUITY_RISK_PREMIUM, config.MARGINAL_TAX_RATE
    beta_source = "regression"
    if not _fin(beta):
        if config.BETA_FALLBACK == "sector_median" and _fin(sector_beta):
            beta, beta_source = sector_beta, "sector_median"
            flags.append(f"beta_from_sector_median_{beta:.2f}({beta_note or 'missing'})")
        else:
            beta, beta_source = 1.0, "default_1.0"
            flags.append(f"beta_defaulted_to_1.0({beta_note or 'missing'})")
    coe = rf + beta * erp

    shares = fund.get("shares")
    if not _fin(shares) or shares <= 0:
        return {"reliable": False, "flags": ["no_share_count"]}
    mktcap = price * shares
    debt = fund.get("total_debt") or 0.0
    ebit, intex = fund.get("ebit"), fund.get("interest_expense") or 0.0

    speculative_credit = False
    if debt <= 0 or intex <= 0:
        spread, coverage, rating = _SPREAD[0][1], None, "no/low debt"
    elif not _fin(ebit) or ebit <= 0:
        # A loss-making year makes the synthetic rating a guess, so take the worst
        # spread on the table. Whether that guess MATTERS depends entirely on how much
        # debt there is: at a 5% debt weight, being wrong by 1,000bp moves WACC by 50bp,
        # which is inside the sensitivity band we already publish. Blocking every
        # loss-making company outright threw away real names (SLAB, FLR) for nothing.
        spread, coverage, rating = 0.13, None, "unrated (negative/absent EBIT)"
        speculative_credit = True
    else:
        coverage = ebit / intex
        spread, rating = _synthetic_spread(coverage), f"coverage {coverage:.1f}x"
    cod = rf + spread

    V = mktcap + debt
    wE, wD = mktcap / V, debt / V
    wacc = wE * coe + wD * cod * (1 - tax)

    if speculative_credit:
        if wD > 0.20:
            flags.append(f"speculative_cost_of_debt_at_{wD:.0%}_debt_weight_wacc_unreliable")
        else:
            flags.append(f"speculative_cost_of_debt_but_only_{wD:.0%}_debt_weight")
    if fund.get("ebit_derived"):
        flags.append("ebit_derived_from_pretax_plus_interest")
    if not _fin(wacc):
        flags.append("nonfinite_wacc")
    elif wacc <= config.TERMINAL_GROWTH:
        flags.append("wacc_below_terminal_growth_model_undefined")
    elif wacc > 0.40:
        flags.append("implausibly_high_wacc")

    blocking = {"nonfinite_wacc", "wacc_below_terminal_growth_model_undefined",
                "implausibly_high_wacc",
                f"speculative_cost_of_debt_at_{wD:.0%}_debt_weight_wacc_unreliable"}
    return {
        "reliable": not (blocking & set(flags)),
        "rf": rf, "erp": erp, "tax_rate": tax, "beta": beta,
        "beta_source": beta_source,
        "cost_of_equity": coe, "cost_of_debt": cod, "credit": rating,
        "interest_coverage": coverage,
        "weight_equity": wE, "weight_debt": wD,
        "wacc": wacc, "market_cap": mktcap, "flags": flags,
    }


# --- FCFF base ---------------------------------------------------------------
def normalized_fcff(fund, tax=config.MARGINAL_TAX_RATE):
    """FCFF ~= mean(CFO - capex) over the window + after-tax interest.

    Honest simplifications, stated so the red team can attack them:
      * uses reported CFO, so stock comp stays added back exactly as the company reports it
      * a multi-year mean damps working-capital and capex lumpiness but cannot fix a
        genuinely broken base year -- hence the dispersion flags
    """
    cfo, capex = fund.get("cfo_series") or [], fund.get("capex_series") or []
    n = min(len(cfo), len(capex))
    flags = []
    if n == 0:
        return {"value": None, "flags": ["no_cashflow_history"], "years": 0, "series": []}
    series = [cfo[i] - capex[i] for i in range(n)]
    base = _mean(series)
    intex = fund.get("interest_expense") or 0.0
    value = base + intex * (1 - tax) if _fin(base) else None

    if n == 1:
        flags.append("single_year_base_no_normalization")
    if any(x < 0 for x in series):
        flags.append("negative_fcf_year_in_window")
    if base and base != 0:
        spread = (max(series) - min(series)) / abs(base)
        if spread > 1.5:
            flags.append(f"lumpy_fcff_spread_{spread:.1f}x_of_mean")

    # Cycle guard. A three-year mean does not normalize a cyclical: apply ANY positive
    # growth to a peak base and the model reports a huge discount that is really just the
    # cycle. This is the single largest source of false "cheap" readings in this universe
    # (egg producers, E&P, rate-sensitive financial processors), so name it explicitly
    # and let the analyst attack it rather than discovering it downstream.
    if n >= 3 and all(x > 0 for x in series):
        newest, oldest = series[0], series[-1]
        if newest > 1.6 * oldest:
            flags.append(
                f"possible_peak_cycle_base_newest_fcf_{newest/oldest:.1f}x_oldest_"
                "growth_applied_to_a_peak_overstates_value")
        elif oldest > 1.6 * newest:
            flags.append(
                f"possible_trough_cycle_base_newest_fcf_{newest/oldest:.2f}x_oldest_"
                "growth_applied_to_a_trough_understates_value")
    # Stock compensation: reported CFO adds it back, so an FCFF built from CFO counts it
    # as free cash. It is not — it is a real transfer of ownership away from the holder.
    # We do NOT silently subtract it (that is a judgment call the analyst should make and
    # defend), but we always quantify it, because "cheap" on a software name is usually
    # this and nothing else.
    sbc_series = [x for x in (fund.get("sbc_series") or [])[:n] if _fin(x)]
    sbc = _mean(sbc_series)
    sbc_share = (sbc / base) if (sbc and base and base > 0) else None
    if sbc_share and sbc_share > 0.20:
        flags.append(f"stock_comp_is_{sbc_share:.0%}_of_fcff_reported_cash_flow_"
                     "treats_it_as_free")

    if all(x == 0 for x in (fund.get("capex_series") or [1])[:n]):
        # Zero reported capex alongside real operating cash flow usually means the capex
        # concept wasn't matched, not that the business is capital-free. FCFF is then just
        # CFO and is overstated — badly so for shipping, energy and utilities.
        flags.append("zero_capex_reported_fcff_likely_overstated")
    if value is not None and value <= 0:
        flags.append("nonpositive_normalized_fcff")
    return {"value": value, "flags": flags, "years": n, "series": series,
            "sbc": sbc, "sbc_share_of_fcff": sbc_share,
            "value_ex_sbc": (value - sbc) if (_fin(value, sbc)) else None}


# --- the DCF itself ----------------------------------------------------------
def ev_from_growth(fcff0, g, wacc, years=config.EXPLICIT_YEARS,
                   g_term=config.TERMINAL_GROWTH):
    """PV of a two-stage FCFF stream: `years` of growth at g, then Gordon terminal."""
    if not _fin(fcff0, g, wacc) or wacc <= g_term:
        return None
    pv, fcff = 0.0, fcff0
    for yr in range(1, years + 1):
        fcff *= (1 + g)
        pv += fcff / (1 + wacc) ** yr
    tv = fcff * (1 + g_term) / (wacc - g_term)
    return pv + tv / (1 + wacc) ** years


def implied_growth(target_ev, fcff0, wacc, years=config.EXPLICIT_YEARS,
                   g_term=config.TERMINAL_GROWTH):
    """Bisection for the g that makes the model reproduce today's enterprise value.
    Returns (growth, note); the note says when the answer hit a bound."""
    if not _fin(target_ev, fcff0, wacc) or fcff0 <= 0 or wacc <= g_term:
        return None, "undefined_inputs"
    lo, hi = config.IMPLIED_GROWTH_BOUNDS
    f = lambda g: (ev_from_growth(fcff0, g, wacc, years, g_term) or -1e18) - target_ev
    if f(lo) > 0:
        return lo, "at_floor_market_prices_below_liquidation_of_declining_cashflows"
    if f(hi) < 0:
        return hi, "at_ceiling_price_unreachable_by_any_plausible_growth"
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2, None


def enterprise_value(fund, price):
    """EV = market cap + debt + preferred + minority interest - cash and equivalents.

    Operating leases are deliberately NOT capitalized into debt: their payments already
    flow through CFO, so adding the liability here without also adding those payments
    back to FCFF would double-count. The liability is reported separately and flagged
    when it is large enough that the other treatment would change the answer.
    """
    shares = fund.get("shares")
    if not _fin(shares, price):
        return None, None
    mktcap = price * shares
    net_cash = (fund.get("cash") or 0.0) + (fund.get("short_term_investments") or 0.0)
    ev = (mktcap + (fund.get("total_debt") or 0.0) + (fund.get("preferred") or 0.0)
          + (fund.get("minority_interest") or 0.0) - net_cash)
    return ev, mktcap


def equity_value_per_share(ev, fund):
    """Inverse of enterprise_value: strip out the same claims that were added in."""
    shares = fund.get("shares")
    if not _fin(ev, shares) or shares <= 0:
        return None
    net_cash = (fund.get("cash") or 0.0) + (fund.get("short_term_investments") or 0.0)
    return (ev - (fund.get("total_debt") or 0.0) - (fund.get("preferred") or 0.0)
            - (fund.get("minority_interest") or 0.0) + net_cash) / shares


def reverse_dcf(fund, price, wacc_block):
    """What growth is baked into the price -- reported at three discount rates, because
    implied growth is far more sensitive to WACC than to anything else in the model.
    A single point estimate here would be false precision."""
    if not wacc_block.get("reliable"):
        return {"ok": False, "flags": wacc_block.get("flags", [])}
    base = normalized_fcff(fund)
    ev, mktcap = enterprise_value(fund, price)
    if base["value"] is None or not _fin(ev):
        return {"ok": False, "flags": base["flags"] + ["no_enterprise_value"]}
    if base["value"] <= 0:
        return {"ok": False, "flags": base["flags"],
                "note": "negative normalized FCFF — a DCF cannot value this; not a cheap stock"}
    if ev <= 0:
        return {"ok": False, "flags": base["flags"] + ["negative_enterprise_value_net_cash_exceeds_mktcap"]}

    lease = fund.get("operating_lease_liability") or 0.0
    lease_flag = []
    if lease > 0.25 * ev:
        lease_flag = [f"operating_leases_{lease/ev:.0%}_of_EV_kept_as_opex_not_debt_"
                      "capitalizing_them_would_materially_change_this"]

    w = wacc_block["wacc"]
    out = {}
    for label, rate in (("low", w - config.WACC_BAND), ("point", w), ("high", w + config.WACC_BAND)):
        g, note = implied_growth(ev, base["value"], rate)
        out[label] = {"wacc": rate, "implied_growth": g, "note": note}
    # the same reverse DCF run on cash flow that expenses stock comp, when it is material
    ex = base.get("value_ex_sbc")
    ig_ex = None
    if _fin(ex) and ex > 0 and (base.get("sbc_share_of_fcff") or 0) > 0.10:
        ig_ex, _ = implied_growth(ev, ex, w)

    return {
        "ok": True, "enterprise_value": ev, "market_cap": mktcap,
        "sbc": base.get("sbc"), "sbc_share_of_fcff": base.get("sbc_share_of_fcff"),
        "fcff_ex_sbc": ex, "implied_growth_ex_sbc": ig_ex,
        "fcff_base": base["value"], "fcff_series": base["series"],
        "fcff_years": base["years"], "flags": base["flags"] + lease_flag,
        "operating_lease_liability": lease,
        "implied_growth": out["point"]["implied_growth"],
        "implied_growth_note": out["point"]["note"],
        "sensitivity": out,
        "fcff_yield": base["value"] / ev if ev else None,
    }


def forward_dcf(fund, price, wacc_block, growth, years=config.EXPLICIT_YEARS,
                g_term=config.TERMINAL_GROWTH, fcff_base=None):
    """Price the analyst's own assumption. `growth` is the 5-year FCFF CAGR.
    Optional fcff_base lets the analyst override a base year they judge unrepresentative."""
    if not wacc_block.get("reliable"):
        return {"ok": False, "flags": wacc_block.get("flags", [])}
    base = fcff_base if _fin(fcff_base) else normalized_fcff(fund)["value"]
    if not _fin(base) or base <= 0:
        return {"ok": False, "flags": ["nonpositive_fcff_base"]}
    w = wacc_block["wacc"]
    ev = ev_from_growth(base, growth, w, years, g_term)
    fv = equity_value_per_share(ev, fund)
    if not _fin(fv, price) or price <= 0:
        return {"ok": False, "flags": ["no_fair_value"]}
    band = {}
    for label, rate in (("low", w + config.WACC_BAND), ("point", w), ("high", w - config.WACC_BAND)):
        v = equity_value_per_share(ev_from_growth(base, growth, rate, years, g_term), fund)
        band[label] = v
    gap = fv / price - 1.0
    flags = []
    if abs(gap) > config.MAX_ABS_GAP:
        flags.append(f"extreme_gap_{gap:+.0%}_treat_as_suspected_data_error")
    return {"ok": True, "growth_used": growth, "fcff_base_used": base,
            "enterprise_value": ev, "fair_value": fv, "price": price,
            "gap": gap, "fair_value_band": band, "flags": flags}


# --- multiples: the second opinion, and the only one for cash-burning names ---
def multiple_inputs(fund):
    """The denominators a comparables valuation needs, from the same committed extract.

    EBITDA is built as EBIT + D&A rather than taken from a tag, because almost nobody
    tags EBITDA -- it is a non-GAAP construction and the SEC does not require it.
    """
    ebit = fund.get("ebit")
    da_s = fund.get("dep_amort_series") or []
    da = da_s[0] if da_s else fund.get("dep_amort")
    ebitda = (ebit + da) if _fin(ebit, da) else None
    rev_s = fund.get("revenue_series") or []
    rev = rev_s[0] if rev_s else None
    gp_s = fund.get("gross_profit_series") or []
    gp = gp_s[0] if gp_s else None
    eq = fund.get("equity_now")
    if not _fin(eq):
        eq_s = fund.get("equity_series") or []
        eq = eq_s[0] if eq_s else None
    tce = None
    if _fin(eq):
        tce = (eq - (fund.get("goodwill") or 0.0) - (fund.get("intangibles") or 0.0)
               - (fund.get("preferred") or 0.0) - (fund.get("minority_interest") or 0.0))
    return {"ebitda": ebitda, "revenue": rev, "gross_profit": gp,
            "tangible_common_equity": tce, "dep_amort": da}


def observed_multiples(fund, price):
    """What this name actually trades at today. Negative denominators return None: a
    negative EV/EBITDA is not a cheap multiple, it is an undefined one."""
    ev, mktcap = enterprise_value(fund, price)
    m = multiple_inputs(fund)
    out = {"enterprise_value": ev, "market_cap": mktcap, **m}
    def _r(num, den):
        return (num / den) if (_fin(num, den) and den > 0) else None
    out["ev_ebitda"] = _r(ev, m["ebitda"])
    out["ev_sales"] = _r(ev, m["revenue"])
    out["ev_gross_profit"] = _r(ev, m["gross_profit"])
    out["p_tbv"] = _r(mktcap, m["tangible_common_equity"])
    return out


def _quartiles(xs):
    xs = sorted(x for x in xs if _fin(x) and x > 0)
    if len(xs) < config.MULTIPLE_MIN_COHORT:
        return None
    def q(p):
        i = p * (len(xs) - 1)
        lo, hi = int(math.floor(i)), int(math.ceil(i))
        return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)
    return {"n": len(xs), "p25": q(0.25), "median": q(0.50), "p75": q(0.75)}


def multiple_valuation(fund, price, cohort_multiples):
    """Value a name against what its own sector cohort actually pays.

    This exists because "a DCF cannot value this" and "this is worthless" are different
    claims, and the engine was collapsing them. A company burning cash while it builds
    something -- a clinical-stage biotech, a data-centre developer -- has a real value
    that the market expresses as a multiple of revenue, gross profit or capacity. The
    honest output is a RANGE across the cohort's interquartile spread, never a point
    estimate: a comparables valuation is a statement about the cohort, and reporting a
    single number from it would claim a precision it does not have.

    `cohort_multiples` is {metric: [observed values from the same (method, sector)]}.
    """
    obs = observed_multiples(fund, price)
    shares = fund.get("shares")
    if not _fin(shares, price) or shares <= 0 or price <= 0:
        return {"ok": False, "flags": ["no_share_count_or_price"]}
    net_debt = ((fund.get("total_debt") or 0.0) + (fund.get("preferred") or 0.0)
                + (fund.get("minority_interest") or 0.0)
                - (fund.get("cash") or 0.0) - (fund.get("short_term_investments") or 0.0))

    rows, flags = [], []
    for metric in config.MULTIPLE_METRICS:
        stats = _quartiles(cohort_multiples.get(metric) or [])
        if not stats:
            continue
        den = {"ev_ebitda": obs["ebitda"], "ev_sales": obs["revenue"],
               "ev_gross_profit": obs["gross_profit"],
               "p_tbv": obs["tangible_common_equity"]}[metric]
        if not _fin(den) or den <= 0:
            continue
        vals = {}
        for label in ("p25", "median", "p75"):
            if metric == "p_tbv":
                vals[label] = stats[label] * den / shares          # equity multiple
            else:
                vals[label] = (stats[label] * den - net_debt) / shares
        # A negative implied equity value is information, not an error: it says the
        # cohort multiple applied to this denominator does not cover the debt.
        rows.append({"metric": metric, "cohort_n": stats["n"],
                     "cohort_p25": stats["p25"], "cohort_median": stats["median"],
                     "cohort_p75": stats["p75"],
                     "own_multiple": obs.get(metric), "denominator": den,
                     "value_low": vals["p25"], "value_mid": vals["median"],
                     "value_high": vals["p75"],
                     "gap_at_median": (vals["median"] / price - 1.0) if price else None})
    if not rows:
        return {"ok": False, "flags": ["no_usable_multiple_for_this_name"],
                "observed": obs}
    mids = [r["value_mid"] for r in rows if _fin(r["value_mid"])]
    blended = _mean(mids)
    if any(r["denominator"] and r["metric"] == "ev_sales" for r in rows) and len(rows) == 1:
        flags.append("only_ev_sales_available_widest_and_least_reliable_multiple")
    if _fin(obs.get("ebitda")) and obs["ebitda"] <= 0:
        flags.append("negative_ebitda_valued_on_revenue_or_gross_profit_only")
    return {"ok": True, "method": "multiples", "rows": rows,
            "blended_value": blended, "price": price,
            "gap": (blended / price - 1.0) if (blended and price) else None,
            "observed": obs, "flags": flags}


# --- scenarios: the same thesis priced three ways, across the discount rate ---
def scenario_table(fund, price, wacc_block, cases, fcff_base=None,
                   wacc_steps=config.SCENARIO_WACC_STEPS):
    """Bear / base / bull growth crossed with a range of discount rates.

    Two variables move a DCF far more than anything else: the growth you assume and the
    rate you discount at. Reporting one cell of that grid as "fair value" hides how much
    of the answer is the assumption. This returns the whole surface, so the output is a
    range of outcomes with named drivers rather than a single number.

    `cases` is {"bear": g, "base": g, "bull": g}; any may be None and is skipped.
    """
    if not wacc_block.get("reliable"):
        return {"ok": False, "flags": wacc_block.get("flags", [])}
    base_fcff = fcff_base if _fin(fcff_base) else normalized_fcff(fund)["value"]
    if not _fin(base_fcff) or base_fcff <= 0 or not _fin(price) or price <= 0:
        return {"ok": False, "flags": ["nonpositive_fcff_base_or_price"]}
    w0 = wacc_block["wacc"]
    grid, summary = [], {}
    for case in ("bear", "base", "bull"):
        g = cases.get(case)
        if not _fin(g):
            continue
        row = {"case": case, "growth": g, "cells": []}
        for step in wacc_steps:
            w = w0 + step
            if w <= config.TERMINAL_GROWTH:
                row["cells"].append({"wacc": w, "fair_value": None, "gap": None,
                                     "note": "wacc_at_or_below_terminal_growth"})
                continue
            fv = equity_value_per_share(ev_from_growth(base_fcff, g, w), fund)
            row["cells"].append({"wacc": w, "fair_value": fv,
                                 "gap": (fv / price - 1.0) if _fin(fv) else None})
        at_point = next((c for c in row["cells"] if abs(c["wacc"] - w0) < 1e-9), None)
        row["fair_value_at_point_wacc"] = at_point["fair_value"] if at_point else None
        row["gap_at_point_wacc"] = at_point["gap"] if at_point else None
        summary[case] = row["gap_at_point_wacc"]
        grid.append(row)
    if not grid:
        return {"ok": False, "flags": ["no_scenario_growth_rates_supplied"]}
    finite = [c["gap"] for r in grid for c in r["cells"] if _fin(c.get("gap"))]
    return {"ok": True, "wacc_point": w0, "wacc_steps": list(wacc_steps),
            "fcff_base_used": base_fcff, "price": price, "grid": grid,
            "summary": summary,
            "downside": min(finite) if finite else None,
            "upside": max(finite) if finite else None}


# --- financials: residual income instead of FCFF -----------------------------
def justified_pb(fund, price, wacc_block, roe_override=None,
                 g=config.TERMINAL_GROWTH):
    """Banks, insurers and capital-markets firms have no meaningful FCFF: debt is raw
    material, not financing. The honest analogue is justified price/tangible-book from
    sustainable ROTCE:  P/TBV* = (ROTCE - g) / (COE - g).

    Two things this gets right that the naive version does not:
      * the P/TBV denominator is the LATEST tangible book against the LATEST share count.
        Averaging book levels across an acquisition (UMBF's book went 3.5B -> 7.7B) prices
        the bank against a company that no longer exists.
      * sustainable ROTCE averages the per-year RATIOS, not the levels, so a mid-window
        acquisition changes the scale of both numerator and denominator together and
        cancels out instead of manufacturing a gap.
    """
    flags = []
    ni_s = fund.get("net_income_series") or []
    eq_s = fund.get("equity_series") or []
    gw_s = fund.get("goodwill_series") or []
    int_s = fund.get("intangibles_series") or []
    shares, price_ok = fund.get("shares"), _fin(price) and price > 0
    if not ni_s or not eq_s or not _fin(shares) or shares <= 0 or not price_ok:
        return {"ok": False, "flags": ["insufficient_book_or_earnings_history"]}

    def _tce_at(i):
        if i >= len(eq_s) or eq_s[i] is None:
            return None
        gw = gw_s[i] if i < len(gw_s) and gw_s[i] is not None else 0.0
        it = int_s[i] if i < len(int_s) and int_s[i] is not None else 0.0
        return eq_s[i] - gw - it

    # sustainable return: mean of per-year ROTCE ratios
    ratios = []
    for i in range(min(len(ni_s), len(eq_s), 3)):
        tce_i = _tce_at(i)
        if tce_i and tce_i > 0 and _fin(ni_s[i]):
            ratios.append(ni_s[i] / tce_i)
    if not ratios:
        return {"ok": False, "flags": ["no_usable_return_on_tangible_equity"]}
    rotce = roe_override if _fin(roe_override) else _mean(ratios)

    tce_now = _tce_at(0)
    if tce_now is None or tce_now <= 0:
        return {"ok": False, "flags": ["negative_tangible_common_equity"]}
    intangibles_now = (fund.get("goodwill") or 0.0) + (fund.get("intangibles") or 0.0)
    if intangibles_now > 0.25 * (eq_s[0] or 1):
        flags.append(f"goodwill_and_intangibles_{intangibles_now/eq_s[0]:.0%}_of_book")
    if len(ratios) > 1 and (max(ratios) - min(ratios)) > 0.5 * abs(_mean(ratios) or 1):
        flags.append(f"unstable_rotce_{min(ratios):.1%}_to_{max(ratios):.1%}")
    if any(x <= 0 for x in ni_s[:len(ratios)]):
        flags.append("loss_year_in_window")
    if rotce > 0.30:
        # GICS "Financials" bundles balance-sheet lenders with asset-light businesses
        # (exchanges, asset managers, brokers) that legitimately earn 40%+ on almost no
        # tangible capital and legitimately trade at many times book. Justified P/TBV is
        # the wrong lens for those, and the tell is an ROTCE this high. Say so rather
        # than reporting a confident gap from a model that does not apply.
        flags.append(f"rotce_{rotce:.0%}_suggests_asset_light_financial_"
                     "p_tbv_may_be_the_wrong_model_here")

    coe = wacc_block.get("cost_of_equity")
    if not _fin(coe) or coe <= g:
        return {"ok": False, "flags": flags + ["cost_of_equity_below_terminal_growth"]}

    justified = (rotce - g) / (coe - g)
    tbvps = tce_now / shares
    actual = price / tbvps
    fv = justified * tbvps
    gap = fv / price - 1.0
    if abs(gap) > config.MAX_ABS_GAP:
        flags.append(f"extreme_gap_{gap:+.0%}_treat_as_suspected_data_error")
    return {"ok": True, "method": "justified_p_tbv", "rotce": rotce,
            "rotce_by_year": ratios, "cost_of_equity": coe,
            "tangible_book": tce_now, "tangible_book_per_share": tbvps,
            "justified_p_tbv": justified, "actual_p_tbv": actual,
            "fair_value": fv, "price": price, "gap": gap, "flags": flags}
