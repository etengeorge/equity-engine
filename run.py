#!/usr/bin/env python3
"""The only entry point. Six verbs, run in this order each morning.

    python run.py screen     # free: price + value all 1,956 names (no LLM, ~15 min)
    python run.py pick       # choose today's ten and write briefs/<TKR>.md
    python run.py record     # ingest synth/<TKR>.json -> research/ + data/verdicts/
    python run.py site       # rebuild public/index.html
    python run.py status     # what state is this repo in?
    python run.py daily      # screen + pick (the GitHub Action's job)

The agent's work sits between `pick` and `record`: read each brief, research, argue with
yourself, write synth/<TKR>.json. Nothing in this file does judgment, and nothing in this
repo can place an order.
"""
import argparse, json, sys, datetime as dt
import config


def _screen():
    p = config.DATA / "screen.json"
    if not p.exists():
        sys.exit("no data/screen.json — run `python run.py screen` first")
    return json.loads(p.read_text())


def _verdicts():
    d = config.DATA / "verdicts"
    if not d.exists():
        return []
    out = []
    for f in sorted(d.glob("*.json")):
        try:
            out.append(json.loads(f.read_text()))
        except json.JSONDecodeError:
            pass
    return out


def cmd_screen(args):
    import screen
    screen.run(limit=args.limit)


def _is_smoke(args):
    return bool(getattr(args, "limit", None))


def cmd_pick(args):
    import daily, brief, edgar
    sc = _screen()
    try:
        events = edgar.recent_8k_ciks(4)
        print(f"[pick] {len(events)} CIKs filed an 8-K in the last 4 sessions")
    except Exception as e:
        events = set()
        print(f"[pick] 8-K firehose unavailable ({type(e).__name__}) — "
              f"continuing without event boost")
    sel = daily.select(sc, events)
    picks = sel["picks"]
    if picks:
        picks[0]["_shocks"] = sel["shocks"]

    written = brief.write_all(picks, sc)
    daily._save("cursor.json", sel["cursor"])
    slim = [{k: v for k, v in p.items() if k != "row"} | {"row": p["row"]} for p in picks]
    daily._save("picks.json", {"date": dt.date.today().isoformat(),
                               "shocks": sel["shocks"], "picks": slim})

    print(f"\n[pick] today's {len(picks)} names:")
    for p in picks:
        r = p["row"]
        gap = f"{r['gap']:+.0%}" if r.get("gap") is not None else "n/a"
        why = "; ".join(p["why"][:2])[:70]
        print(f"  {p['ticker']:6s} {p['slot']:14s} gap={gap:>7s}  "
              f"{r['sector'][:16]:16s} {why}")
    if sel["shocks"]:
        print("\n[pick] sector moves:")
        for s, v in sel["shocks"].items():
            print(f"  {s:24s} median 5d {v['median']:+.1%} ({v['direction']}, n={v['n']})")
    print(f"\n[pick] briefs written to briefs/ "
          f"({sum(c for _, c in written):,} chars total, "
          f"max {max((c for _, c in written), default=0):,})")
    print("[pick] next: read each brief, then write synth/<TICKER>.json")


def cmd_record(args):
    import record, prices
    sc = _screen()
    by_ticker = {r["ticker"]: r for r in sc["rows"]}
    synth = config.ROOT / "synth"
    files = sorted(synth.glob("*.json")) if synth.exists() else []
    if not files:
        sys.exit("no synth/*.json to record — the analyst pass has not run")
    rf = sc.get("risk_free_rate") or prices.risk_free_rate()[0]
    ok = fail = 0
    for f in files:
        t = f.stem.upper()
        row = by_ticker.get(t)
        if not row:
            print(f"  {t}: not in the current screen — skipped")
            fail += 1
            continue
        try:
            v = record.record_one(t, f.read_text(), row, rf)
            pr = v.get("priced") or {}
            gap = f"{pr['gap']:+.0%}" if pr.get("ok") else "not repriced"
            print(f"  {t}: {v['verdict']:9s} conviction={v['conviction']:6s} gap={gap}"
                  + (f"  [{'; '.join(v['parse_notes'])}]" if v["parse_notes"] else ""))
            ok += 1
        except Exception as e:
            print(f"  {t}: FAILED to record — {type(e).__name__}: {e}")
            fail += 1
    print(f"\n[record] {ok} recorded, {fail} failed")
    if args.clean and ok:
        for f in files:
            f.unlink()
        print("[record] cleared synth/")
    if fail and not ok:
        sys.exit(2)


def cmd_site(args):
    import dashboard
    sc = _screen()
    p = config.DATA / "picks.json"
    picks = json.loads(p.read_text())["picks"] if p.exists() else []
    out = dashboard.build(sc, picks, _verdicts())
    print(f"[site] wrote {out} ({out.stat().st_size:,} bytes)")


def cmd_status(args):
    sc = config.DATA / "screen.json"
    print(f"universe          {sum(1 for _ in open(config.ROOT/'universe.csv')) - 1} names")
    if sc.exists():
        d = json.loads(sc.read_text())
        print(f"screen            {d['generated_utc']}  {d['counts']}")
    else:
        print("screen            (none)")
    v = _verdicts()
    print(f"researched        {len({x['ticker'] for x in v})} names, {len(v)} verdict files")
    cur = config.DATA / "cursor.json"
    if cur.exists():
        c = json.loads(cur.read_text())
        n = sum(1 for _ in open(config.ROOT / "universe.csv")) - 1
        print(f"rotation cursor   position {c.get('index')}/{n}, cycle {c.get('cycle')}")
        left = (n - len({x['ticker'] for x in v}))
        print(f"coverage          {left} names never researched "
              f"(~{left/max(config.ROTATION_SLOTS,1):.0f} sessions of rotation remaining)")
    b = list((config.ROOT / "briefs").glob("*.md")) if (config.ROOT/"briefs").exists() else []
    s = list((config.ROOT / "synth").glob("*.json")) if (config.ROOT/"synth").exists() else []
    print(f"pending           {len(b)} briefs written, {len(s)} analyst files waiting to record")


def cmd_daily(args):
    cmd_screen(args)
    if _is_smoke(args):
        # A limited run proves the pipeline works; it must not leave a limited screen,
        # a rewritten pick list or an advanced rotation cursor behind for the real run
        # (or the dashboard) to pick up.
        print(f"\n[daily] smoke test with --limit {args.limit}: selection skipped and no "
              f"state written. Re-run without --limit for a real screen.")
        return
    cmd_pick(args)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn, helptext in (
            ("screen", cmd_screen, "value every name in the universe (no LLM)"),
            ("pick", cmd_pick, "select today's ten and write their briefs"),
            ("record", cmd_record, "ingest analyst JSON into research + verdicts"),
            ("site", cmd_site, "rebuild the dashboard"),
            ("status", cmd_status, "show repo state"),
            ("daily", cmd_daily, "screen + pick")):
        p = sub.add_parser(name, help=helptext)
        p.set_defaults(func=fn)
        if name in ("screen", "daily"):
            p.add_argument("--limit", type=int,
                           help="SMOKE TEST: screen only the first N names, write to "
                                "data/screen.sample.json, and change no committed state")
        if name == "record":
            p.add_argument("--clean", action="store_true",
                           help="delete synth/*.json after a successful record")
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
