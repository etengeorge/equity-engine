"""Pick today's ten, and write each one a self-contained research brief.

Rotation guarantees eventual coverage of the whole index. Opportunism guarantees we are
not blind to a name that just halved while it waited its turn. Neither alone is enough:
pure rotation misses today's news, pure opportunism revisits the same volatile names
forever and never finishes the universe.

Every pick records WHY it was picked. A selector you cannot audit is a selector you
cannot correct.
"""
import json, math, statistics, datetime as dt
from collections import defaultdict
import config

BRIEFS = config.ROOT / "briefs"


# --- state -------------------------------------------------------------------
def _load(path, default):
    p = config.DATA / path
    if p.exists():
        try:
            return json.loads(p.read_text())
        except json.JSONDecodeError:
            return default
    return default


def _save(path, obj):
    config.DATA.mkdir(parents=True, exist_ok=True)
    import screen
    (config.DATA / path).write_text(
        json.dumps(screen._clean(obj), indent=2, allow_nan=False, default=float))


def days_since(iso, today=None):
    if not iso:
        return None
    try:
        return ((today or dt.date.today()) - dt.date.fromisoformat(iso[:10])).days
    except ValueError:
        return None


# --- sector shocks -----------------------------------------------------------
def sector_shocks(rows, window="ret_5d", threshold=-0.04):
    """Detect a sector-wide move from the tape itself, no news feed required.
    A 'massive tech selloff' shows up here as a deeply negative median return across
    a whole sector -- and then the names that moved MOST inside that sector are the
    ones worth looking at first."""
    by_sector = defaultdict(list)
    for r in rows:
        v = r.get(window)
        if v is not None and math.isfinite(v):
            by_sector[r["sector"]].append(v)
    out = {}
    for sec, vals in by_sector.items():
        if len(vals) < 10:
            continue
        med = statistics.median(vals)
        if abs(med) >= abs(threshold):
            out[sec] = {"median": med, "n": len(vals),
                        "direction": "selloff" if med < 0 else "melt_up"}
    return out


# --- urgency -----------------------------------------------------------------
def urgency(r, shocks, event_ciks, visits, today=None):
    """Score a name for an opportunistic slot. Components are returned alongside the
    total so the dashboard can show the reason in words."""
    why, score = [], 0.0

    # 1. how far from fair value, measured against its own cohort so my choice of
    #    equity-risk-premium cannot manufacture a whole sector of "opportunities".
    #    cohort_pct is the percentile of the GAP, so HIGH percentile = cheap. Getting
    #    this backwards silently ranks the most expensive names in the index first.
    pct = r.get("cohort_pct")
    gap = r.get("gap")
    if pct is not None and gap is not None:
        if pct >= 90:
            score += 3.0 * (pct - 90) / 10 + 1.5
            why.append(f"cheapest {100-pct:.0f}% of {r.get('cohort_n')} {r['sector']} peers "
                       f"({pct:.0f}th pct)")
        elif pct <= 10:
            score += config.RICH_WEIGHT * (2.0 * (10 - pct) / 10 + 1.0)
            why.append(f"richest {pct:.0f}% of its cohort")
    if gap is not None and math.isfinite(gap) and abs(gap) <= config.MAX_ABS_GAP:
        # asymmetric on purpose: this is a long-oriented screen. An overvalued name is
        # interesting, but a very negative gap is more often a broken input than a short.
        w = 1.5 if gap > 0 else 1.5 * config.RICH_WEIGHT
        score += min(abs(gap), 1.0) * w
        why.append(f"baseline gap {gap:+.0%}")

    # 1b. penalise the distortions we can measure, rather than pretending they are signal
    sbc = r.get("sbc_share_of_fcff")
    if sbc is not None and sbc > 0.20:
        score -= 1.5 * min(sbc, 0.5)
        why.append(f"discounted: stock comp is {sbc:.0%} of reported FCFF")
    if any("peak_cycle" in f for f in r.get("flags", [])):
        score -= 0.75
        why.append("discounted: cash-flow base may be a cycle peak")

    # 2. it moved. a large recent move against an unchanged business is the whole point
    for field, weight, label in (("ret_5d", 4.0, "5d"), ("ret_21d", 2.0, "21d")):
        v = r.get(field)
        if v is not None and math.isfinite(v) and abs(v) > 0.08:
            score += min(abs(v), 0.5) * weight
            why.append(f"{label} move {v:+.0%}")

    # 2b. abnormal volume. Unlike a return this has no direction and it usually moves
    #     BEFORE the story is written, so it catches a name on the day something
    #     happened rather than the day it was reported.
    vr = r.get("volume_ratio")
    if vr is not None and math.isfinite(vr) and vr > 2.0:
        score += min(vr, 6.0) * 0.30
        why.append(f"volume {vr:.1f}x its 60d average")

    # 3. it filed something material
    if r.get("cik") in event_ciks:
        score += 2.5
        why.append("filed an 8-K in the last few sessions")

    # 3b. it is actually in the news, and the news is recent.
    #     Deliberately a MULTIPLIER on names that are already interesting on price
    #     rather than a trigger of its own: news volume on its own selects for what is
    #     already priced, and this is a valuation screen. A name with heavy coverage and
    #     no gap still scores near zero here.
    #     Both terms are multiplicative and both are gated on an existing score. Written
    #     additively, "its sector is in the news" alone put a name with no valuation gap
    #     at 1.0 and into contention — which is the failure this comment exists to
    #     prevent, caught by test_news_boost_cannot_select_on_its_own.
    if score > 0:
        nz = r.get("news_recent") or 0
        if nz:
            score *= 1.0 + min(nz, 6) * 0.06
            why.append(f"{nz} news items in the last 5 days")
        if r.get("news_sector_hot"):
            score *= 1.10
            why.append(f"{r['sector']} is in the news")

    # 4. its whole sector moved, and it moved more than the sector did
    shock = shocks.get(r["sector"])
    if shock:
        own = r.get("ret_5d")
        score += 1.0
        why.append(f"{r['sector']} sector {shock['direction']} (median {shock['median']:+.1%})")
        if own is not None and math.isfinite(own) and abs(own) > abs(shock["median"]) * 1.5:
            score += 1.5
            why.append("moved harder than its sector")

    # 5. staleness of our own work: never looked at, or looked at long ago
    seen = days_since((visits.get(r["ticker"]) or {}).get("last_visit"), today)
    if seen is None:
        score += 0.5
        why.append("never researched")
    elif seen > 240:
        score += 0.75
        why.append(f"last researched {seen}d ago")

    return score, why


def eligible_for_opportunistic(r, visits, today=None):
    """Cooldown and tradability. A gap you cannot buy is not an opportunity, and
    re-underwriting a name we did last week burns a slot -- unless it moved or filed."""
    blocking = {"below_min_market_cap", "illiquid_below_min_dollar_volume",
                "ticker_not_in_edgar_map", "no_price_data"}
    if blocking & set(r.get("flags", [])):
        return False, "fails size/liquidity/data gate"
    if any(f.startswith("extreme_gap_") for f in r.get("flags", [])):
        return False, "extreme gap — suspected data error, not an opportunity"
    # Reported cash flow adds stock comp back, so a name whose SBC exceeds half its FCFF
    # looks cheap for a reason that is not cheapness. BOX screened +147% on reported
    # numbers; expensing stock comp flips its implied growth from -11% to +12%. Ranking
    # those ahead of genuinely cheap names would waste the scarce research slots.
    sbc = r.get("sbc_share_of_fcff")
    if sbc is not None and sbc > 0.50:
        return False, f"stock comp is {sbc:.0%} of FCFF — the gap is an accounting artifact"
    if r.get("gap") is None:
        return False, "no model output"
    seen = days_since((visits.get(r["ticker"]) or {}).get("last_visit"), today)
    if seen is not None and seen < config.REVISIT_COOLDOWN_DAYS:
        # The override exists to catch a name that halved while it waited its turn. It
        # had no floor, and ret_21d barely changes from one day to the next, so a name
        # that fell 25% over three weeks satisfied it EVERY day for the next three weeks
        # and kept beating fresh names to a slot. On 2026-08-31 it cost three of the four
        # opportunistic slots to names researched nine hours earlier. Two conditions now:
        # enough time must have passed to have learned anything, and the trigger must be
        # something NEW -- a fresh 5-day move, a new filing, or abnormal volume today --
        # not a stale 21-day number that has not changed since the last look.
        if seen < config.MIN_REVISIT_DAYS:
            return False, (f"researched {seen}d ago (minimum {config.MIN_REVISIT_DAYS}d "
                           f"before any revisit)")
        fresh = (abs(r.get("ret_5d") or 0) > 0.20
                 or (r.get("volume_ratio") or 0) > 3.0
                 or bool(r.get("filed_8k")))
        if not (config.MATERIAL_EVENT_OVERRIDE and fresh):
            return False, f"researched {seen}d ago (cooldown {config.REVISIT_COOLDOWN_DAYS}d)"
    return True, None


# --- selection ---------------------------------------------------------------
def attach_news(rows, event_ciks=(), today=None):
    """Stamp each row with what the news layer already collected.

    Reads the store rather than fetching, so selection stays offline-safe and testable:
    if the news pull was skipped or throttled, every count is zero and selection falls
    back to exactly the price-driven behaviour it had before.
    """
    try:
        import news
    except Exception:
        return {}
    event_ciks = set(event_ciks)
    hot = set()
    for sector in {r.get("sector") for r in rows if r.get("sector")}:
        recent = news.read("sectors", sector, days=config.NEWS_RECENT_DAYS)
        if len(recent) >= config.NEWS_SECTOR_HOT_ITEMS:
            hot.add(sector)
    for r in rows:
        r["filed_8k"] = r.get("cik") in event_ciks
        r["news_sector_hot"] = r.get("sector") in hot
        r["news_recent"] = len(news.read("companies", r["ticker"],
                                         days=config.NEWS_RECENT_DAYS))
    return {"sectors_hot": sorted(hot)}


def select(screen, event_ciks=(), today=None):
    rows = screen["rows"]
    by_ticker = {r["ticker"]: r for r in rows}
    order = [r["ticker"] for r in rows]            # universe.csv order = index weight desc
    visits = _load("visits.json", {})
    cursor = _load("cursor.json", {"index": 0, "cycle": 1})
    event_ciks = set(event_ciks)
    news_meta = attach_news(rows, event_ciks, today)
    shocks = sector_shocks(rows)

    picks, chosen = [], set()

    # --- rotation: the blind sweep that guarantees the universe gets covered
    i, wrapped = cursor.get("index", 0) % len(order), 0
    cycle = cursor.get("cycle", 1)
    while len([p for p in picks if p["slot"] == "rotation"]) < config.ROTATION_SLOTS and wrapped <= len(order):
        t = order[i]
        i = (i + 1) % len(order)
        wrapped += 1
        if i == 0:
            cycle += 1
        if t in chosen:
            continue
        r = by_ticker[t]
        # A name with no price or no EDGAR identity cannot be researched at all — it has
        # usually been acquired or delisted since the universe was frozen. Burn the cursor
        # past it rather than a research slot on it.
        if r.get("status") in ("no_price", "no_cik"):
            continue
        seen = days_since((visits.get(t) or {}).get("last_visit"), today)
        if seen is not None and seen < config.REVISIT_COOLDOWN_DAYS:
            continue                               # already covered recently; keep sweeping
        chosen.add(t)
        picks.append({"ticker": t, "slot": "rotation", "score": None,
                      "why": [f"rotation position {order.index(t)+1}/{len(order)}"],
                      "row": r})

    # --- opportunistic: whatever today actually demands
    scored = []
    for r in rows:
        if r["ticker"] in chosen:
            continue
        ok, reason = eligible_for_opportunistic(r, visits, today)
        if not ok:
            continue
        s, why = urgency(r, shocks, event_ciks, visits, today)
        if s > 0:
            scored.append((s, why, r))
    scored.sort(key=lambda x: -x[0])
    for s, why, r in scored[:config.OPPORTUNISTIC_SLOTS]:
        chosen.add(r["ticker"])
        picks.append({"ticker": r["ticker"], "slot": "opportunistic",
                      "score": round(s, 2), "why": why, "row": r})

    # --- backfill: if cooldowns starved rotation, top up from the ranked list
    for s, why, r in scored[config.OPPORTUNISTIC_SLOTS:]:
        if len(picks) >= config.DAILY_SLOTS:
            break
        if r["ticker"] in chosen:
            continue
        chosen.add(r["ticker"])
        picks.append({"ticker": r["ticker"], "slot": "backfill", "score": round(s, 2),
                      "why": why + ["backfilled: rotation exhausted by cooldowns"], "row": r})

    cursor = {"index": i, "cycle": cycle,
              "covered": len([t for t, v in visits.items() if v.get("last_visit")])}
    return {"picks": picks, "cursor": cursor, "shocks": shocks,
            "news": news_meta, "universe_size": len(order)}
