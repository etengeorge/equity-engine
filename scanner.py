"""
scanner.py - the two-speed trigger layer.

Speed 1 (CHEAP, DAILY, whole universe): watch every name for whether something
MOVED — abnormal price move, volume spike, fresh news, sentiment spike — and re-price
the DCF gap against the stored target (pure arithmetic). This is feasible across all
~2,000 names because each check is light.

Speed 2 (EXPENSIVE, GATED): the deep synthesis + full DCF re-do (new assumptions ->
new target price). A name is promoted into this queue ONLY when the cheap scan finds
something material, OR it's due on cadence (twice a week), OR it's a held position
whose gap crossed a threshold. Plus a cold-tail rotation so no-signal names still get
a periodic deep refresh.

This resolves the tension: daily responsiveness to real events (news/social CAN move a
stock any day) WITHOUT trying to deep-analyze 2,000 names a day (infeasible + overkill
for 12-36 month theses). The scan widens what gets ATTENTION; the anti-overtrading and
no-edge logic downstream still govern what gets ACTED on.
"""
import datetime as dt
import math
import statistics as stats

import config
import data_sources as ds
import analytics as an


def _abnormal_move(ticker):
    """Cheap: latest 1-day return vs the stock's own daily vol, plus volume spike.
    Returns (signals, latest_price)."""
    px = ds.get_prices(ticker, lookback_days=60)
    if not px or len(px[1]) < 21:
        return [], (px[1][-1] if px and px[1] else None)
    dates, closes, vols = px[0], px[1], px[4]
    latest_price = closes[-1]
    rets = [closes[i] / closes[i - 1] - 1 for i in range(1, len(closes))]
    last_ret = rets[-1]
    daily_vol = stats.pstdev(rets[-21:]) if len(rets) >= 21 else stats.pstdev(rets)
    signals = []
    if daily_vol and daily_vol > 0:
        z = last_ret / daily_vol
        if abs(z) >= config.SCAN_ABNORMAL_RETURN_Z:
            signals.append(f"abnormal_move({last_ret:+.1%}, {z:+.1f}σ)")
    if abs(last_ret) >= config.SCAN_ABNORMAL_RETURN_FLOOR:
        signals.append(f"big_move({last_ret:+.1%})")
    if vols and len(vols) >= 21:
        avg_vol = stats.mean(vols[-21:-1]) if len(vols) > 21 else stats.mean(vols[:-1])
        if avg_vol and vols[-1] > config.SCAN_VOLUME_SPIKE_MULT * avg_vol:
            signals.append(f"volume_spike({vols[-1]/avg_vol:.1f}x)")
    return signals, latest_price


def _news_sentiment_signal(ticker):
    """Cheap-ish: fresh material events / news / sentiment. Separates SUBSTANTIVE events
    (facts that change the thesis) from sentiment (mood). Returns (signals, material_confirmed).
    Look, never act — the deep synthesis decides if it's thesis-changing."""
    if not (config.SCAN_NEWS_TRIGGER or config.SCAN_SENTIMENT_TRIGGER):
        return [], False
    try:
        import news_layer as nl
        b = nl.gather_news(ticker)
    except Exception:
        return [], False
    signals = []
    material_confirmed = False
    for ev in b.get("material_events", []):
        if ev["confidence"] == "confirmed":
            signals.append(f"material:{ev['category']}(confirmed)")
            material_confirmed = True
        else:
            signals.append(f"material:{ev['category']}(provisional)")
    if config.SCAN_NEWS_TRIGGER and not signals and b.get("conflicting_stories"):
        signals.append(f"news_conflict({len(b['conflicting_stories'])})")
    if config.SCAN_SENTIMENT_TRIGGER:
        st = b.get("stance_tally", {})
        tot = sum(st.values()) or 1
        if (st.get("bull", 0) / tot > 0.6 or st.get("bear", 0) / tot > 0.6) and tot >= 3:
            signals.append(f"sentiment_tilt({b.get('bull_bear_split')})")
    return signals, material_confirmed


def _due_for_full_revalue(stored_thesis, today):
    """Twice-a-week cadence: has it been >= interval days since the last full re-do?"""
    if not stored_thesis:
        return True
    last = stored_thesis.get("created")
    snap_last = None
    # prefer an explicit last_full_revalue if present on the snapshot
    last = stored_thesis.get("last_full_revalue") or last
    if not last:
        return True
    try:
        days = (dt.date.fromisoformat(today) - dt.date.fromisoformat(last)).days
        return days >= config.FULL_REVALUE_INTERVAL_DAYS
    except Exception:
        return True


def _material_event_signal(ticker, stored_thesis, today):
    """Confirmed material events fast-track to deep synthesis ahead of everything.
    Filing-backed (a new 8-K) is CONFIRMED by construction. News-based is confirmed
    only with >=2 sources, else provisional (reliability-first: await corroboration)."""
    signals = []
    confirmed = False
    provisional = False
    # 1) 8-K filings since the last full revalue (or recent) = confirmed material events
    try:
        last = (stored_thesis or {}).get("last_full_revalue") or (stored_thesis or {}).get("created")
        evs = ds.recent_material_events(ds.resolve_cik(ticker)[0], since_date=last)
        for e in evs:
            cats = [ev["category"] for ev in e["events"] if ev["category"] not in ("other", "reg_fd")]
            if cats:
                tag = "HIGH-IMPACT " if e["any_high_impact"] else ""
                signals.append(f"8K_{tag}event({','.join(cats[:3])})")
                confirmed = True
    except Exception:
        pass
    return signals, confirmed, provisional


def scan_name(ticker, stored_record=None, held=False, check_events=True,
              event_filer_ciks=None):
    """Run the cheap checks for one name. Returns trigger signals, re-priced gap, and
    whether to PROMOTE to deep synthesis. Material events (8-K / corroborated news)
    fast-track to top priority.

    event_filer_ciks: when provided (a full-universe scan), the set of CIKs that filed
    an 8-K recently (one firehose pull) — so the material-event check is a set lookup
    instead of a submissions call per name. When None (a hand-list scan), the detailed
    per-name 8-K check runs."""
    today = dt.date.today().isoformat()
    snap = (stored_record or {}).get("latest", {}) if stored_record else {}
    stored_thesis = snap.get("thesis")

    move_signals, price = _abnormal_move(ticker)

    # material events: a fresh 8-K fast-tracks regardless of price move.
    event_signals, ev_confirmed, ev_provisional = ([], False, False)
    if check_events:
        if event_filer_ciks is not None:
            cik = ds.resolve_cik(ticker)[0]
            if cik and cik in event_filer_ciks:
                event_signals, ev_confirmed = ["8K_filed(firehose)"], True
        else:
            event_signals, ev_confirmed, ev_provisional = _material_event_signal(
                ticker, stored_thesis, today)

    # news/sentiment: fetch when something already moved, an event fired, held, or uncovered
    need_news = bool(move_signals or event_signals or held or not stored_thesis)
    news_signals, news_material_confirmed = [], False
    if need_news:
        ns, nm = _news_sentiment_signal(ticker)
        news_signals = ns
        news_material_confirmed = nm
    revalue = an.quick_revalue(snap, price) if (snap and price) else None

    triggers = list(event_signals) + list(move_signals) + list(news_signals)
    if revalue and revalue.get("crossed_buy"):
        triggers.append(f"gap_crossed_buy({revalue['new_gap']:+.0%})")
    if held and revalue and revalue.get("crossed_sell"):
        triggers.append(f"gap_crossed_sell({revalue['new_gap']:+.0%})")
    # v2 short side: an UNHELD, liquid name whose re-priced gap crossed the short bar is a
    # reason to LOOK (deep-synthesize), never an automatic short.
    if (not held and revalue and revalue.get("new_gap") is not None
            and revalue["new_gap"] <= config.SCAN_GAP_SHORT
            and (snap.get("adv_usd") or 0) >= config.MIN_ADV_SHORT_USD):
        triggers.append(f"gap_crossed_short({revalue['new_gap']:+.0%})")

    # cadence: last_full_revalue lives on the SNAPSHOT (not the thesis); fall back to the
    # thesis 'created' date if absent (also tolerates a test fixture's thesis-level field).
    revalue_marker = {"last_full_revalue": snap.get("last_full_revalue")
                      or (stored_thesis or {}).get("last_full_revalue"),
                      "created": (stored_thesis or {}).get("created")}
    due = _due_for_full_revalue(revalue_marker, today)
    if due:
        triggers.append("cadence_due(twice_weekly)")

    promote = bool(triggers)
    # priority: confirmed material event tops everything (re-underwrite the thesis now)
    priority = 0
    if ev_confirmed or news_material_confirmed:
        priority = 4
    elif held and revalue and revalue.get("crossed_sell"):
        priority = 3
    elif any("gap_crossed_buy" in t for t in triggers):
        priority = 3
    elif move_signals or news_signals:
        priority = 2
    elif due:
        priority = 1

    return {
        "ticker": ticker, "price": price, "held": held,
        "triggers": triggers, "promote_to_deep_synthesis": promote,
        "priority": priority, "revalue": revalue,
        "material_event_confirmed": ev_confirmed or news_material_confirmed,
        "material_event_provisional": ev_provisional,
        "has_stored_thesis": bool(stored_thesis),
    }


def scan_universe(tickers, store_module, positions=None, cold_tail_fraction=None,
                  max_deep=None, event_filer_ciks=None):
    """Cheap scan across a batch of the universe. Returns the prioritized deep-synthesis
    queue plus the full scan log. cold_tail_fraction rotates some no-signal names in so
    quiet stocks still get periodic deep refreshes.

    For a true full-2000 daily scan, pass event_filer_ciks (one EDGAR daily-index
    firehose pull, see data_sources.recent_8k_filer_ciks) so 8-K detection is a set
    lookup, not a call per name. news/sentiment is still gated to names that already
    moved / are held / are uncovered, and any single name that errors is skipped
    rather than failing the whole batch (SCALING Step 4)."""
    held = {p["ticker"].upper() for p in (positions or [])}
    cold_tail_fraction = (cold_tail_fraction if cold_tail_fraction is not None
                          else config.COLD_TAIL_REFRESH_FRACTION)
    scanned, queue, skipped = [], [], 0
    for t in tickers:
        try:
            rec = store_module.load_by_ticker(t) if hasattr(store_module, "load_by_ticker") else None
            s = scan_name(t, stored_record=rec, held=(t.upper() in held),
                          event_filer_ciks=event_filer_ciks)
        except Exception as e:
            skipped += 1
            s = {"ticker": t, "price": None, "held": (t.upper() in held), "triggers": [],
                 "promote_to_deep_synthesis": False, "priority": 0, "revalue": None,
                 "material_event_confirmed": False, "material_event_provisional": False,
                 "has_stored_thesis": False, "scan_error": type(e).__name__}
        scanned.append(s)
        if s["promote_to_deep_synthesis"]:
            queue.append(s)

    # cold-tail rotation: names with NO trigger still get refreshed on a rotating slice
    no_signal = [s for s in scanned if not s["promote_to_deep_synthesis"]]
    if cold_tail_fraction and no_signal:
        n = max(1, int(len(no_signal) * cold_tail_fraction))
        # deterministic rotation by day-of-year so the slice advances each run
        doy = dt.date.today().timetuple().tm_yday
        start = (doy * n) % len(no_signal)
        rotated = (no_signal + no_signal)[start:start + n]
        for s in rotated:
            s = dict(s); s["triggers"] = ["cold_tail_rotation"]; s["priority"] = 0
            queue.append(s)

    queue.sort(key=lambda s: s["priority"], reverse=True)
    if max_deep:
        queue = queue[:max_deep]
    return {
        "scanned": len(scanned),
        "promoted": len(queue),
        "skipped": skipped,
        "queue": queue,
        "summary": _scan_summary(scanned, queue),
    }


def _scan_summary(scanned, queue):
    by_reason = {}
    for s in queue:
        for t in s["triggers"]:
            key = t.split("(")[0]
            by_reason[key] = by_reason.get(key, 0) + 1
    return {"universe_scanned": len(scanned), "promoted_to_deep": len(queue),
            "promotion_reasons": dict(sorted(by_reason.items(), key=lambda kv: -kv[1]))}
