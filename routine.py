"""
routine.py - the runnable two-speed routine (ROUTINE.md, as code).

  python routine.py daily  [--watchlist watchlist.txt] [--positions positions.json]
                           [--max-deep N] [--outdir out] [--live] [--no-news]
  python routine.py retro

DAILY (the full connected loop — every external seam is INJECTED by the orchestration layer
       and dry-runs/stubs by default, so it runs free today and goes live with no code change):
   1. positions  read-only holdings              (connectors.read_positions  <- Robinhood seam)
   2. universe   watchlist OR full IWM + churn   (universe.load_iwm_universe; held names always covered)
   3. firehose   one EDGAR daily-index pull       (the day's 8-K filers across the universe; a set lookup)
   4. scan       cheap two-speed scan of the slice + held, PLUS
                 - 8-K fast-track (material filers go straight to deep), AND
                 - SECTOR-EVENT propagation (a development logged in a vertical re-examines the
                   companies it touches) -> the prioritized deep queue (capped at max_deep)
   5. deep       engine.run on the queue          (synth_provider <- live Claude reasoning; else stub)
                 -> reverse DCF -> thesis -> recommendation; FEEDS the sector dossier + company news
   6. board      today's deep + held + accrued actionable recs (--iwm) / full book (watchlist)
   7. outputs    dashboard.html + email_brief.html (index-departure + membership churn surfaced)
   8. notify     email the brief when an action is flagged   (emailer           <- Gmail seam)
   9. mirror     journal tree -> Drive                       (drive_syncer      <- Drive seam)
  10. audit      commit store/ (journal + snapshots)         (journal_committer <- git seam)

RETRO (periodic): score matured theses, write per-thesis verdicts + the compounding
LESSONS file that future synthesis runs read back.

This is recommend-only. No trade is placed or suggested anywhere; there is no order
path. The synthesis provider and every connector default to safe stubs / dry-runs;
the orchestration layer (Claude Code / Cowork) injects the live callables — see
CONNECTING.md. --live uses the hand-authored synthesis in _live_synthesis.py for the
names it covers (others fall back to the deterministic stub).
"""
import argparse
import os

import config
import engine
import outputs
import scanner
import store
import connectors


# --------------------------------------------------------------------- universe
def load_universe(watchlist_path, held_tickers):
    """Watchlist file (one ticker per line, '#' comments) plus all held names."""
    names = []
    if watchlist_path and os.path.exists(watchlist_path):
        with open(watchlist_path) as f:
            for line in f:
                t = line.split("#", 1)[0].strip().upper()
                if t:
                    names.append(t)
    for t in held_tickers:           # always cover what you own
        names.append(t.upper())
    seen, uniq = set(), []
    for t in names:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def _live_provider():
    """The hand-authored live synthesis for known names; None elsewhere (-> stub)."""
    try:
        import _live_synthesis as ls
        return ls.provider
    except Exception:
        return None


# --------------------------------------------------------- full-book assembly
def _assemble_full_book(deep, universe, scan):
    """Show the whole book: today's DEEP-refreshed rows plus the last-known snapshot
    for every covered name the scan did NOT promote (tagged so it isn't read as fresh)."""
    rows = list(deep.get("rows", []))
    covered = {str(r.get("ticker", "")).upper() for r in rows}
    for t in universe:
        if t.upper() in covered:
            continue
        rec = store.load_by_ticker(t)
        snap = (rec or {}).get("latest")
        if snap:
            row = dict(snap)
            row["_stale"] = True       # last analysis, not re-run today
            rows.append(row)
    rows.sort(key=lambda r: r.get("rank_score", -1), reverse=True)
    out = dict(deep)
    out["rows"] = rows
    out.setdefault("paper_mode", config.PAPER_MODE)
    return out


def _assemble_recommendation_board(deep, held_tickers, top=60):
    """Cross-universe long/short board (for --iwm): today's freshly deep-analyzed rows, plus
    every held name, plus the best ACTIONABLE recommendations accumulated in the store over the
    rotation cycle (BUY*/ADD/SELL-TRIM/REVIEW, or a reliability-weighted gap past the bar).
    Capped at `top` so the dashboard is a readable feed, not a ~2,000-row dump. Stored rows are
    tagged _stale (last analysis; re-priced when their slice next comes up)."""
    rows = list(deep.get("rows", []))
    covered = {str(r.get("ticker", "")).upper() for r in rows if not r.get("error")}
    held_up = {t.upper() for t in held_tickers}
    held_rows, other = [], []
    for snap in store.all_latest():
        tk = str(snap.get("ticker", "")).upper()
        if not tk or tk in covered:
            continue
        rec = snap.get("recommendation") or {}
        action = rec.get("action", "")
        gap = (snap.get("our_view") or {}).get("gap_vs_price")
        actionable = (action.startswith("BUY") or action in ("ADD", "SELL/TRIM", "REVIEW")
                      or (gap is not None and abs(gap) >= config.BUY_GAP))
        if tk in held_up or actionable:
            row = dict(snap)
            row["_stale"] = True
            covered.add(tk)
            (held_rows if tk in held_up else other).append(row)
    other.sort(key=lambda r: r.get("rank_score", -1), reverse=True)
    rows = rows + held_rows + other[:max(0, top)]
    rows.sort(key=lambda r: r.get("rank_score", -1), reverse=True)
    out = dict(deep)
    out["rows"] = rows
    out.setdefault("paper_mode", config.PAPER_MODE)
    return out


def _has_flagged_action(results):
    if (results.get("universe_churn") or {}).get("held_left"):
        return True                              # a held name leaving the index is worth surfacing
    for r in results.get("rows", []):
        if r.get("error") or r.get("_stale"):   # stale rows aren't today's fresh actions
            continue
        rec = r.get("recommendation") or {}
        action = rec.get("action", "")
        if r.get("held") and action in ("SELL/TRIM", "ADD", "REVIEW"):
            return True
        if not r.get("held") and action.startswith("BUY"):
            return True
    return False


def _print_recs(results):
    print(f"\nPAPER_MODE={config.PAPER_MODE}  (recommend-only; no trades placed or suggested)")
    for r in results.get("rows", []):
        if r.get("error"):
            print(f"  {r.get('ticker'):6} ERROR {r['error']}")
            continue
        ov = r.get("our_view") or {}
        gap = ov.get("gap_vs_price")
        stale = " [scan only]" if r.get("_stale") else ""
        print(f"  {r['ticker']:6} {r['recommendation']['action']:34} "
              f"gap={('%+.0f%%' % (gap*100)) if gap is not None else 'n/a':>6} "
              f"reliable={r.get('reliable')}{stale}")


# ------------------------------------------------------------------- daily run
def daily_routine(watchlist="watchlist.txt", positions_path="positions.json",
                  synth_provider=None, position_source=None, emailer=None,
                  drive_syncer=None, max_deep=None, outdir="out", gather_news=True,
                  persist=True, write_journal=True, iwm=False, limit=None,
                  refresh_universe=False, batch=None, journal_committer=None):
    positions = connectors.read_positions(source=position_source, fallback_path=positions_path)
    held = {p["ticker"].upper() for p in positions}

    # ---- build the universe (watchlist by default; full Russell 2000 with --iwm) ----
    event_filer_ciks = None
    churn = None
    if iwm:
        try:
            import universe as iwm_universe
            index_list = iwm_universe.load_iwm_universe(limit=limit, refresh=refresh_universe)

            # DYNAMIC membership: index constituents change (annual reconstitution, plus
            # intra-year M&A / take-privates / delistings / distress). Diff vs the last full
            # pull. Names that LEFT drop from the active scan automatically; HELD names that
            # left are kept in coverage and flagged. Skip the diff on --limit subsets (it
            # would read as false churn).
            if limit is None:
                # stable source category so a fresh-fetch day and a cache-hit day don't
                # reset the baseline (both are "faithful"); the SEC superset is its own baseline.
                src = "sec" if (iwm_universe.LAST_SOURCE or "").startswith("SEC") else "faithful"
                churn = iwm_universe.record_membership(index_list, source=src)
                if churn["added"] or churn["removed"]:
                    print(f"[universe] membership change since {churn['prior_asof']}: "
                          f"+{len(churn['added'])} entered, -{len(churn['removed'])} left")
                    if churn["removed"]:
                        print(f"  left index: {', '.join(churn['removed'][:12])}"
                              + (' ...' if len(churn['removed']) > 12 else ''))
                        held_left = [t for t in churn["removed"] if t in held]
                        if held_left:
                            print(f"  ⚠ YOU HOLD {', '.join(held_left)} which left the index — "
                                  "kept in coverage; review for delisting / take-private / distress")
                    if churn["added"]:
                        print(f"  entered (analyzed fresh as uncovered): {', '.join(churn['added'][:12])}"
                              + (' ...' if len(churn['added']) > 12 else ''))

            universe = index_list + [t for t in held if t not in {x.upper() for x in index_list}]
            if max_deep is None:
                max_deep = config.MAX_DEEP_PER_RUN
            try:    # one EDGAR daily-index pull -> 8-K detection across the universe is a set lookup
                import data_sources as ds
                event_filer_ciks = ds.recent_8k_filer_ciks()
                print(f"[universe] IWM: {len(universe)} names; 8-K firehose found "
                      f"{len(event_filer_ciks)} recent filer CIKs")
            except Exception as e:
                print(f"[universe] 8-K firehose unavailable ({type(e).__name__}); "
                      "per-name event check (slower at scale)")
        except Exception as e:
            print(f"[universe] IWM load failed ({type(e).__name__}: {e}); using watchlist")
            universe = load_universe(watchlist, held)
    else:
        universe = load_universe(watchlist, held)

    tag = f" [IWM universe, max_deep={max_deep}]" if iwm else ""
    print(f"universe: {len(universe)} names ({len(held)} held){tag}")
    if len(universe) <= 40:
        print("  " + ", ".join(universe))

    # ---- rotating batch (free full coverage over a cycle of runs) + event fast-track ----
    # Schedule 2-3 runs/day: a persisted cursor advances each run so the whole universe is
    # cheap-scanned over `cycle_runs` runs. Held names are scanned every run; recent 8-K filers
    # (firehose) are fast-tracked straight to deep regardless of the slice, so material events
    # drive timely recs without a universe-wide price pull.
    event_names, scan_set = [], universe
    if iwm and batch:
        import universe as iwm_universe
        import data_sources as ds
        if event_filer_ciks:
            _seen = set()
            for t in universe:
                c = ds.resolve_cik(t)[0]
                if c and c in event_filer_ciks and t.upper() not in _seen:
                    _seen.add(t.upper())
                    event_names.append(t)
        bi = iwm_universe.next_batch(universe, batch)
        slice_list = bi["batch"]
        scan_set = slice_list + [t for t in held if t not in {x.upper() for x in slice_list}]
        print(f"[batch] cheap-scan {len(slice_list)} (slice {bi['start']}-"
              f"{bi['start'] + len(slice_list)} of {len(universe)}; full sweep every "
              f"{bi['cycle_runs']} runs) + {len(held)} held; {len(event_names)} recent "
              f"8-K filers fast-tracked to deep")

    # SPEED 1 — cheap scan over the slice (+ held): promotes movers / cadence / cold-tail
    scan = scanner.scan_universe(scan_set, store, positions=positions, max_deep=max_deep,
                                 event_filer_ciks=event_filer_ciks)
    queue = [s["ticker"] for s in scan["queue"]]
    # event fast-track (8-K filers) jump to the front of the deep queue
    forced = [t for t in event_names if t not in set(queue)]
    # SECTOR-EVENT propagation: names whose vertical logged a fresh development (a regulator acting,
    # a commodity moving, a peer's move) get re-examined — this turns the sector dossier into ACTION,
    # not just synthesis context. (Closes the news -> recommendation loop.)
    import sectors as _sectors
    _uni_up = {x.upper() for x in universe}
    _already = set(forced) | set(queue)
    sector_evt = [t for t in _sectors.recent_event_tickers(days=config.FULL_REVALUE_INTERVAL_DAYS)
                  if t in _uni_up and t not in _already]
    deep_tickers, _seen = [], set()
    for t in forced + sector_evt + queue:
        if t not in _seen:
            _seen.add(t)
            deep_tickers.append(t)
    if max_deep:
        deep_tickers = deep_tickers[:max_deep]
    if sector_evt:
        print(f"[sector-event] re-examining on fresh vertical developments: {', '.join(sector_evt[:10])}")
    print(f"scan: {scan['scanned']} watched, {scan.get('skipped', 0)} skipped, "
          f"{len(deep_tickers)} to deep synthesis "
          f"({len(forced)} 8-K fast-track, {len(sector_evt)} sector-event)")
    print(f"scan summary: {scan['summary']}")
    print(f"deep ({len(deep_tickers)}): {', '.join(deep_tickers) or '(none)'}")

    # SPEED 2 — deep synthesis ONLY on the (capped) deep queue
    if deep_tickers:
        deep = engine.run(deep_tickers, llm_synth_provider=synth_provider, positions=positions,
                          gather_news=gather_news, persist=persist, write_journal=write_journal)
    else:
        deep = {"rows": [], "paper_mode": config.PAPER_MODE}

    # --iwm: a capped cross-universe long/short BOARD (today's deep + held + best stored recs
    # accumulated over the cycle). watchlist: the whole (small) book.
    results = (_assemble_recommendation_board(deep, held, top=config.MAX_BOARD_ROWS)
               if iwm else _assemble_full_book(deep, universe, scan))

    # surface index-membership churn in the outputs (esp. HELD names that left the index)
    if churn and (churn.get("removed") or churn.get("added")):
        held_left = [t for t in churn.get("removed", []) if t in held]
        results["universe_churn"] = {"added": churn.get("added", []),
                                     "removed": churn.get("removed", []),
                                     "held_left": held_left,
                                     "prior_asof": churn.get("prior_asof")}
        _hl = {t.upper() for t in held_left}
        present = set()
        for r in results["rows"]:
            tk = str(r.get("ticker", "")).upper()
            present.add(tk)
            if tk in _hl:
                r["left_index"] = True
        # a held name that left the index may have no fresh data (delisted / taken private):
        # still surface it as an explicit REVIEW row so it never silently drops off the book.
        for t in held_left:
            if t.upper() not in present:
                pos = next((p for p in positions if p["ticker"].upper() == t.upper()), None)
                results["rows"].append({
                    "ticker": t.upper(), "name": "", "sector": "", "held": pos,
                    "left_index": True, "price": None, "reliability_flags": ["left_index"],
                    "recommendation": {"action": "REVIEW", "sizing": None,
                                       "reason": "left the Russell 2000 — review for "
                                                 "delisting / take-private / distress"}})

    os.makedirs(outdir, exist_ok=True)
    dash = outputs.build_dashboard(results, os.path.join(outdir, "dashboard.html"))
    mail = outputs.build_email(results, os.path.join(outdir, "email_brief.html"))
    print("wrote", dash)
    print("wrote", mail)

    # connector seams (dry-run by default; orchestration layer injects live callables)
    if _has_flagged_action(results):
        connectors.send_brief_email(mail, sender=emailer)
    else:
        print("[connector] email: no flagged action on a holding and no new BUY — not sending")
    connectors.sync_journal_to_drive(syncer=drive_syncer)
    if persist:        # audit trail: commit store/ (journal + snapshots); dry-run unless a committer is injected
        connectors.commit_store(committer=journal_committer)

    _print_recs(results)
    return results


# ------------------------------------------------------------- retrospective
def monthly_retrospective(judge_provider=None):
    """Score matured theses and refresh the LESSONS file. judge_provider is an
    orchestration-layer llm provider for the live mechanism judge (optional)."""
    import retrospective as retro
    res = retro.run_retrospective(llm_provider=judge_provider)
    scores = res.get("scores", [])
    patterns = res.get("patterns", {})
    graded = patterns.get("n_graded", 0)
    print(f"retrospective: examined {len(scores)} stored theses, {graded} matured/graded")
    if graded == 0:
        print("  (no theses have passed their pinned evaluation_window yet — expected for "
              "fresh, long-horizon theses; re-run after they mature)")
    for L in patterns.get("lessons", []):
        print("  lesson:", L)
    print("wrote", retro.LESSONS_PATH)
    return res


# ---------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="Equity Engine two-speed routine (recommend-only).")
    sub = ap.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("daily", help="two-speed daily run: scan -> deep synth on promoted -> outputs")
    d.add_argument("--watchlist", default="watchlist.txt")
    d.add_argument("--positions", default="positions.json")
    d.add_argument("--iwm", action="store_true",
                   help="scan the full Russell 2000 (iShares IWM holdings) instead of the watchlist")
    d.add_argument("--limit", type=int, default=None,
                   help="cap the universe size (staged rollout / testing)")
    d.add_argument("--refresh-universe", action="store_true",
                   help="force a fresh IWM holdings fetch (ignore today's cache)")
    d.add_argument("--batch", type=int, default=None,
                   help="rotating cheap-scan slice size per run (with --iwm). Schedule 2-3 runs/"
                        "day to cycle the full universe for free; held names + recent 8-K filers "
                        "are covered every run regardless of the slice.")
    d.add_argument("--max-deep", type=int, default=None, help="cap deep synthesis per run")
    d.add_argument("--outdir", default="out")
    d.add_argument("--live", action="store_true",
                   help="use hand-authored live synthesis (_live_synthesis.provider) where available")
    d.add_argument("--no-news", action="store_true", help="skip the news layer (faster)")
    d.add_argument("--dry", action="store_true",
                   help="preview: build outputs but do NOT persist to store/ or the journal")

    sub.add_parser("retro", help="score matured theses and refresh the LESSONS file")

    args = ap.parse_args()
    if args.cmd == "daily":
        provider = _live_provider() if args.live else None
        if args.live and provider is None:
            print("note: --live requested but _live_synthesis.provider unavailable; using stub")
        daily_routine(watchlist=args.watchlist, positions_path=args.positions,
                      synth_provider=provider, max_deep=args.max_deep,
                      outdir=args.outdir, gather_news=not args.no_news,
                      persist=not args.dry, write_journal=not args.dry,
                      iwm=args.iwm, limit=args.limit, refresh_universe=args.refresh_universe,
                      batch=args.batch)
    elif args.cmd == "retro":
        monthly_retrospective()


if __name__ == "__main__":
    main()
