"""
portfolio.py - portfolio-level construction, monitoring, and reweighting.

The engine analyzes names in isolation; this layer looks at the BOOK as a whole,
which is where the real risks of running money live:

  - Overexposure: a single name or sector too large (concentration risk). Winners grow
    into oversized positions WITHOUT a trade, so this is monitored continuously.
  - Hidden concentration: in an all-small-cap book everything shares the same size
    factor, and names cluster by sector — "20 names" can be far fewer real bets.
  - Correlation: effective diversification, not just the count of holdings.
  - Sizing: half-Kelly target weights (edge / variance), capped at the concentration
    limits, used to suggest add/trim — sized by PROCESS, not vibes.

Discipline carried over from the monitor: trim a winner only when it is BOTH overweight
AND its expected return has vanished (fair value reached). Never trim just because it
rose. If fair value INCREASED, a strengthened thesis can justify ADDING (subject to the cap).

All ADVISORY. The engine never trades. Rebalancing is a monthly-cadence activity, not a
daily one — interim price drift is expected on long-horizon theses.
"""
import math
import statistics as stats

import config
import data_sources as ds


# ----------------------------------------------------------- return series cache
def _returns(ticker):
    px = ds.get_prices(ticker, lookback_days=400)
    if not px or len(px[1]) < 40:
        return None, None
    dates, closes = px[0], px[1]
    rets = {dates[i]: (closes[i] / closes[i - 1] - 1) for i in range(1, len(closes))}
    vol = stats.pstdev(list(rets.values())) * math.sqrt(252) if len(rets) > 5 else None
    return rets, vol


def _avg_pairwise_corr(ret_by_ticker):
    tickers = [t for t, r in ret_by_ticker.items() if r]
    if len(tickers) < 2:
        return None, 0
    corrs = []
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            a, b = ret_by_ticker[tickers[i]], ret_by_ticker[tickers[j]]
            common = sorted(set(a) & set(b))
            if len(common) > 30:
                x = [a[d] for d in common]
                y = [b[d] for d in common]
                mx, my = sum(x) / len(x), sum(y) / len(y)
                cov = sum((x[k] - mx) * (y[k] - my) for k in range(len(x))) / len(x)
                sx = math.sqrt(sum((v - mx) ** 2 for v in x) / len(x))
                sy = math.sqrt(sum((v - my) ** 2 for v in y) / len(y))
                if sx > 0 and sy > 0:
                    corrs.append(cov / (sx * sy))
    return (stats.mean(corrs) if corrs else None), len(corrs)


# ----------------------------------------------------------- Kelly target weight
def _kelly_target(gap, horizon_months, vol_ann, rf):
    """Half-Kelly (configurable) single-asset weight: edge / variance, capped.
    Deliberately NOT the matrix-inversion multi-asset Kelly — correlation estimates
    for small-caps are too noisy, and inverting a noisy covariance matrix overfits.
    The robust choice is single-asset Kelly + concentration caps + a fractional scale."""
    if gap is None or vol_ann is None or vol_ann <= 0 or not horizon_months:
        return None
    # annualize the expected return to fair value over the thesis horizon
    exp_ret = (1 + gap) ** (12.0 / horizon_months) - 1
    excess = exp_ret - rf
    raw = excess / (vol_ann ** 2)
    sized = config.KELLY_FRACTION * raw
    return max(0.0, min(sized, config.MAX_SINGLE_NAME_WEIGHT))  # no shorts in sizing; cap


# ----------------------------------------------------------- main analysis
def analyze_portfolio(positions, snapshots_by_ticker):
    """
    positions: [{"ticker","shares","avg_cost"}]
    snapshots_by_ticker: {TICKER: snapshot dict from engine} for current price/sector/
                         beta/vol/thesis. Names without a snapshot are valued on last price.
    Returns the full portfolio view: weights, concentration flags, diversification,
    reweighting suggestions, and harvest flags.
    """
    rf, _ = ds.risk_free_rate()
    held = []
    ret_by_ticker = {}
    import math as _math
    def _ok(x):
        return isinstance(x, (int, float)) and _math.isfinite(x)
    for p in positions:
        t = p["ticker"].upper()
        snap = snapshots_by_ticker.get(t, {})
        price = snap.get("price")
        if not _ok(price) or price <= 0:
            px = ds.get_prices(t, lookback_days=40)
            price = px[1][-1] if px else None
        shares = p.get("shares")
        # skip positions with a non-finite/bad price or share count — a NaN here would
        # poison the total value and make every weight NaN.
        if not _ok(price) or price <= 0 or not _ok(shares):
            continue
        mv = price * shares
        rets, vol = _returns(t)
        if rets:
            ret_by_ticker[t] = rets
        thesis = snap.get("thesis") or {}
        ov = snap.get("our_view") or {}
        held.append({
            "ticker": t, "shares": shares, "price": price,
            "market_value": mv, "avg_cost": p.get("avg_cost"),
            "sector": snap.get("sector", "Unknown"),
            "vol_ann": vol or snap.get("vol_annualized"),
            "gap": (ov.get("gap_vs_price") if _ok(ov.get("gap_vs_price")) else None),
            "horizon_months": thesis.get("horizon_months"),
            "conviction": thesis.get("conviction"),
            "direction": thesis.get("direction"),
            "archetype": thesis.get("thesis_archetype"),
            "fair_value": ov.get("fair_value"),
            "unrealized_pct": ((price / p["avg_cost"] - 1) if p.get("avg_cost") else None),
        })
    total = sum(h["market_value"] for h in held)
    if total <= 0:
        return {"error": "no valued positions"}

    # weights
    for h in held:
        h["weight"] = h["market_value"] / total

    # ---- single-name concentration
    name_flags = [{"ticker": h["ticker"], "weight": h["weight"],
                   "over_by": h["weight"] - config.MAX_SINGLE_NAME_WEIGHT}
                  for h in held if h["weight"] > config.MAX_SINGLE_NAME_WEIGHT]

    # ---- sector concentration
    sector_w = {}
    for h in held:
        sector_w[h["sector"]] = sector_w.get(h["sector"], 0) + h["weight"]
    sector_flags = [{"sector": s, "weight": w, "over_by": w - config.MAX_SECTOR_WEIGHT}
                    for s, w in sector_w.items() if w > config.MAX_SECTOR_WEIGHT]

    # ---- diversification (correlation-aware)
    avg_corr, n_pairs = _avg_pairwise_corr(ret_by_ticker)
    hhi = sum(h["weight"] ** 2 for h in held)
    naive_eff_n = (1 / hhi) if hhi > 0 else 0
    # correlation haircut: high avg correlation shrinks the EFFECTIVE number of bets
    corr_adj_eff_n = naive_eff_n
    if avg_corr is not None and avg_corr > 0:
        corr_adj_eff_n = naive_eff_n / (1 + avg_corr * (naive_eff_n - 1))

    # ---- target weights (half-Kelly, capped) + reweighting suggestions
    targets = {}
    for h in held:
        if h["direction"] == "avoid":
            targets[h["ticker"]] = 0.0   # thesis says exit
        else:
            targets[h["ticker"]] = _kelly_target(h["gap"], h["horizon_months"],
                                                  h["vol_ann"], rf)
    # normalize positive targets so they don't exceed 100% (remainder = cash)
    pos_sum = sum(v for v in targets.values() if v)
    if pos_sum and pos_sum > 1.0:
        for k in targets:
            if targets[k]:
                targets[k] /= pos_sum

    suggestions = []
    for h in held:
        tgt = targets.get(h["ticker"])
        if tgt is None:
            continue
        gap = h["gap"]
        at_fair_value = (gap is not None and gap < 0.05)  # upside mostly gone
        over_cap = h["weight"] > config.MAX_SINGLE_NAME_WEIGHT
        drift = h["weight"] - tgt
        action, harvest = "hold", False
        # HARD CAP first: over the single-name concentration cap ALWAYS trims, regardless
        # of where the Kelly target sits (a cap is a limit, not a suggestion). Trim back to
        # the cap, or to the Kelly target if that's lower.
        if over_cap:
            if at_fair_value:
                action, harvest = "TRIM (harvest)", True
            else:
                action = "TRIM (over cap)"
            # trim target is the cap (or the Kelly target if even lower)
            tgt = min(tgt, config.MAX_SINGLE_NAME_WEIGHT)
        # otherwise use Kelly-target drift
        elif drift > config.REBALANCE_DRIFT_TRIGGER:
            if at_fair_value:
                action = "TRIM (fair value reached)"
            else:
                # overweight target but thesis still has upside -> Kelly says let it run
                action = "hold (overweight but thesis intact — let winners run)"
        elif drift < -config.REBALANCE_DRIFT_TRIGGER and (h["gap"] or 0) > 0:
            action = "ADD (under target, thesis intact)"
        # approximate share delta to reach target
        target_mv = tgt * total
        delta_mv = target_mv - h["market_value"]
        delta_shares = (delta_mv / h["price"]) if h["price"] else 0
        if action != "hold" and not action.startswith("hold"):
            suggestions.append({
                "ticker": h["ticker"], "current_weight": round(h["weight"], 4),
                "target_weight": round(tgt, 4), "action": action,
                "approx_shares": round(delta_shares), "harvest": harvest,
                "unrealized_pct": h["unrealized_pct"], "gap": h["gap"],
                "conviction": h["conviction"]})

    # ---- structural / factor warning (all-small-cap book)
    warnings = []
    if avg_corr is not None and avg_corr > config.HIGH_AVG_CORRELATION:
        warnings.append(f"High average pairwise correlation ({avg_corr:.2f}): your "
                        f"{len(held)} holdings behave like ~{corr_adj_eff_n:.1f} independent "
                        "bets. Adding more correlated small-caps doesn't diversify much.")
    if len(sector_flags) == 0 and len(held) >= 3:
        top_sector = max(sector_w.items(), key=lambda kv: kv[1])
        if top_sector[1] > config.MAX_SECTOR_WEIGHT * 0.8:
            warnings.append(f"{top_sector[0]} is approaching the sector cap "
                            f"({top_sector[1]:.0%}). Watch it.")
    warnings.append("Structural note: an all-small-cap book is concentrated in the size "
                    "factor — in a small-cap drawdown the whole book falls together "
                    "regardless of name-level diversification.")

    return {
        "total_value": total, "n_positions": len(held),
        "positions": sorted(held, key=lambda h: -h["weight"]),
        "sector_weights": dict(sorted(sector_w.items(), key=lambda kv: -kv[1])),
        "single_name_overexposure": name_flags,
        "sector_overexposure": sector_flags,
        "diversification": {
            "naive_effective_positions": round(naive_eff_n, 1),
            "correlation_adjusted_effective_bets": round(corr_adj_eff_n, 1),
            "avg_pairwise_correlation": round(avg_corr, 3) if avg_corr is not None else None,
            "n_pairs_measured": n_pairs,
        },
        "reweighting_suggestions": suggestions,
        "warnings": warnings,
        "limits_used": {"max_name": config.MAX_SINGLE_NAME_WEIGHT,
                        "max_sector": config.MAX_SECTOR_WEIGHT,
                        "kelly_fraction": config.KELLY_FRACTION},
        "note": ("Advisory portfolio view. Trim suggestions fire only when overweight AND "
                 "(over cap OR fair value reached) — never just because a name rose. "
                 "Rebalance on a monthly cadence, not on daily price drift."),
    }
