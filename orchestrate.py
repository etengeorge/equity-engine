"""
orchestrate.py (v2) - the SINGLE entry point the scheduled routine invokes.

Three passes per research run, each a separate command so the agent's reasoning sits between them:

  pass 1  python orchestrate.py <mode> --emit-prompts
          -> synth/prompts/<TKR>.txt for every promoted name
  (agent) 7-step synthesis + web_search per prompt -> synth/<TKR>.json  (JSON only)
  pass 2  python orchestrate.py <mode> --emit-redteam
          -> feeds synth/<TKR>.json, builds the thesis, and writes synth/redteam/prompts/<TKR>.txt
             ONLY for names that cleared the action bar (BUY/ADD/SELL/SHORT CANDIDATE) or are held
  (agent) devil's-advocate pass per prompt -> synth/redteam/<TKR>.json  (JSON only)
  pass 3  python orchestrate.py <mode>
          -> final run with both providers, dashboard/email, journal (LIVE theses only), git audit
             commit + push (loud), and store/runs/<date>_<mode>.json manifest. Non-zero exit on
             silent-failure conditions (see _check_manifest).

Modes:
  daily   held names + 8-K filers + movers + sector events; small deep cap (monitor)
  sweep   the rotating universe slice on top of daily; larger deep cap (research)
  retro   score matured theses -> LESSONS.md

Why v2 exists: the v1 routine reported 27 green runs while (a) git push failed silently in a fresh
clone every run, (b) the universe was the 10k SEC superset, (c) the prompt was cut at 90k chars so
the memory layer never reached the analyst, (d) stub output polluted the journal. Every one of those
now either fails loudly or cannot happen.

Recommend-only. PAPER_MODE. There is no order path.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

import config
import routine
import connectors
import synthesis as syn

_TICKER_RE = re.compile(r'"ticker":\s*"([A-Z0-9.\-]+)"')
ACTION_BAR = ("BUY", "ADD", "SELL/TRIM", "SHORT CANDIDATE", "REVIEW")
MODE_DEFAULTS = {
    "daily": dict(iwm=True, batch=0, max_deep=8),      # batch=0: no rotation slice, monitor only
    "sweep": dict(iwm=True, batch=300, max_deep=25),
}


# ----------------------------------------------------------- providers
def file_synth_provider(synth_dir):
    def provider(prompt):
        m = _TICKER_RE.search(prompt)
        if not m:
            return None
        p = os.path.join(synth_dir, f"{m.group(1)}.json")
        try:
            return open(p, encoding="utf-8").read() if os.path.exists(p) else None
        except Exception:
            return None
    return provider


def capture_provider(captured):
    """Record each rendered prompt by ticker, return None (stub fallback)."""
    def provider(prompt):
        m = _TICKER_RE.search(prompt)
        if m:
            captured[m.group(1)] = prompt
        return None
    return provider


# ----------------------------------------------------------- git audit seam (loud)
def git_committer(store_dir, message):
    """Commit store/ + public/ and push. Returns a dict with the push result; RAISES on a genuine
    commit error. A failed push is recorded, printed loudly, and surfaced in the manifest so a run
    that does not persist is never mistaken for success (this is how v1 lost 27 runs)."""
    for _p in (store_dir, "public", "vercel.json", "LESSONS.md"):
        if os.path.exists(_p):
            subprocess.run(["git", "add", _p], check=False, capture_output=True)
    # a fresh cloud clone has no git identity; never let that block the audit trail
    ident = ["-c", "user.name=equity-engine-routine", "-c", "user.email=routine@equity-engine"]
    r = subprocess.run(["git", *ident, "commit", "-m", message], capture_output=True, text=True)
    committed = r.returncode == 0
    if not committed and "nothing to commit" not in (r.stdout + r.stderr):
        raise RuntimeError((r.stderr or r.stdout)[:200])
    out = {"committed": committed, "pushed": False, "push_error": None,
           "head": subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True,
                                  text=True).stdout.strip()}
    if subprocess.run(["git", "remote"], capture_output=True, text=True).stdout.strip():
        # push the CURRENT branch to its upstream name (or to the branch's own name) explicitly:
        # a fresh clone on `main` pushes main; a local v2 tracking origin/main pushes to main.
        up = subprocess.run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
                            capture_output=True, text=True).stdout.strip()   # e.g. origin/main
        target = up.split("/", 1)[1] if "/" in up else subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()
        pr = subprocess.run(["git", "push", "origin", f"HEAD:{target}"], capture_output=True, text=True)
        out["pushed"] = pr.returncode == 0
        if not out["pushed"]:
            out["push_error"] = (pr.stderr or pr.stdout).strip()[:300]
            print(f"\n!!! AUDIT PUSH FAILED: {out['push_error']}\n!!! This run will NOT persist "
                  "in a fresh clone. Fix the remote/credential before the next run.\n")
        else:
            print(f"[audit] pushed {out['head']}")
    else:
        out["push_error"] = "no remote configured"
        print("[audit] no git remote; committed locally only")
    git_committer.last = out
    return out


git_committer.last = None


# ----------------------------------------------------------- manifest
def _write_manifest(results, mode, outdir, extra=None):
    run = dict(results.get("_run") or {})
    rows = [r for r in results.get("rows", []) if not r.get("error")]
    deep = [r for r in rows if not r.get("_stale")]
    live = [r for r in deep if r.get("synthesis_source") == "llm"]
    stub = [r for r in deep if r.get("synthesis_source") == "stub"]
    red = [r for r in live if isinstance(r.get("red_team"), dict) and r["red_team"].get("verdict")]
    verdicts = {}
    for r in red:
        v = r["red_team"]["verdict"]
        verdicts[v] = verdicts.get(v, 0) + 1
    actions = {}
    for r in rows:
        a = (r.get("recommendation") or {}).get("action", "?")
        actions[a] = actions.get(a, 0) + 1
    errors = [{"ticker": r.get("ticker"), "error": r.get("error")}
              for r in results.get("rows", []) if r.get("error")]
    commit = run.get("commit") or {}
    push = git_committer.last or {}
    manifest = {
        "date": dt.date.today().isoformat(),
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "mode": mode,
        "universe_source": run.get("universe_source"), "universe_size": run.get("universe_size"),
        "scanned": run.get("scanned"), "promoted": run.get("promoted"),
        "deep_tickers": run.get("deep_tickers"),
        "live_synthesis": len(live), "stub_synthesis": len(stub),
        "red_teamed": len(red), "red_team_verdicts": verdicts,
        "not_red_teamed_but_actionable": [
            r["ticker"] for r in live
            if (r.get("recommendation") or {}).get("action", "").startswith(ACTION_BAR)
            and not (isinstance(r.get("red_team"), dict) and r["red_team"].get("verdict"))],
        "actions": actions, "errors": errors,
        "held": run.get("held"),
        "commit": {"committed": commit.get("committed"), "files": commit.get("files"),
                   "error": commit.get("error"),
                   "head": push.get("head"), "pushed": push.get("pushed"),
                   "push_error": push.get("push_error")},
        "context_hard_cap": syn.CONTEXT_BUDGET["hard_cap"],
        "paper_mode": config.PAPER_MODE,
    }
    if extra:
        manifest.update(extra)
    d = os.path.join(config.STORE_DIR, "runs")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, f"{manifest['date']}_{mode}.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, default=str)
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=1, default=str)
    return manifest, p


def _check_manifest(m, final=True):
    """Silent-failure conditions. Return a list of problems; the caller exits non-zero on any."""
    problems = []
    if str(m.get("universe_source") or "").startswith("SEC"):
        problems.append("universe is the SEC all-filers superset, not the Russell 2000")
    if m.get("mode") in MODE_DEFAULTS and not m.get("universe_size"):
        problems.append("universe is empty")
    if m.get("promoted") == 0 and m.get("mode") == "sweep":
        problems.append("sweep promoted 0 names (scanner or price provider broken?)")
    if final:
        if (m.get("promoted") or 0) > 0 and m.get("live_synthesis", 0) == 0:
            problems.append("0 live theses on a run that promoted names (agent did not write synth/*.json)")
        if m.get("not_red_teamed_but_actionable"):
            problems.append("actionable names without a red-team verdict: "
                            + ", ".join(m["not_red_teamed_but_actionable"]))
        c = m.get("commit") or {}
        if c.get("error"):
            problems.append(f"audit commit FAILED: {c.get('error')}")
        if c.get("committed") and c.get("pushed") is False:
            problems.append(f"audit commit not pushed: {c.get('push_error')}")
    return problems


# ----------------------------------------------------------- modes
def _kwargs(args):
    d = dict(MODE_DEFAULTS.get(args.mode, {}))
    if args.batch is not None:
        d["batch"] = args.batch
    if args.max_deep is not None:
        d["max_deep"] = args.max_deep
    if args.watchlist_only:
        d["iwm"] = False
    return dict(watchlist=args.watchlist, positions_path=args.positions, iwm=d.get("iwm", False),
                batch=(d.get("batch") or None), limit=args.limit, max_deep=d.get("max_deep"),
                gather_news=not args.no_news, mode=args.mode)


def _clear_txt(pdir):
    os.makedirs(pdir, exist_ok=True)
    for f in os.listdir(pdir):
        if f.endswith(".txt"):
            os.remove(os.path.join(pdir, f))


def emit_prompts(args):
    captured = {}
    res = routine.daily_routine(synth_provider=capture_provider(captured), persist=False,
                                write_journal=False, journal_committer=None,
                                outdir=os.path.join(args.outdir, "_emit"), **_kwargs(args))
    pdir = os.path.join(args.synth_dir, "prompts")
    _clear_txt(pdir)
    for tk, prompt in captured.items():
        with open(os.path.join(pdir, f"{tk}.txt"), "w", encoding="utf-8") as f:
            f.write(prompt)
    m, p = _write_manifest(res, args.mode, args.outdir,
                           extra={"pass": "emit-prompts", "prompts_written": sorted(captured)})
    sizes = [os.path.getsize(os.path.join(pdir, f"{t}.txt")) for t in captured]
    print(f"\n[emit] wrote {len(captured)} synthesis prompts to {pdir}/ "
          f"(avg {int(sum(sizes) / len(sizes)) if sizes else 0} chars; context hard cap "
          f"{syn.CONTEXT_BUDGET['hard_cap']})")
    print(f"[emit] NEXT: write {args.synth_dir}/<TKR>.json per prompt, then "
          f"`python orchestrate.py {args.mode} --emit-redteam`")
    _finish(_check_manifest(m, final=False), p)


def emit_redteam(args):
    captured = {}
    res = routine.daily_routine(synth_provider=file_synth_provider(args.synth_dir),
                                red_team_provider=capture_provider(captured),
                                persist=False, write_journal=False, journal_committer=None,
                                outdir=os.path.join(args.outdir, "_emit"), **_kwargs(args))
    held = set((res.get("_run") or {}).get("held") or [])
    need = []
    for r in res.get("rows", []):
        if r.get("error") or r.get("_stale") or r.get("synthesis_source") != "llm":
            continue
        act = (r.get("recommendation") or {}).get("action", "")
        if r["ticker"].upper() in held or act.startswith(ACTION_BAR):
            need.append(r["ticker"].upper())
    pdir = os.path.join(args.synth_dir, "redteam", "prompts")
    _clear_txt(pdir)
    written = []
    for tk in need:
        if tk in captured:
            with open(os.path.join(pdir, f"{tk}.txt"), "w", encoding="utf-8") as f:
                f.write(captured[tk])
            written.append(tk)
    m, p = _write_manifest(res, args.mode, args.outdir,
                           extra={"pass": "emit-redteam", "redteam_prompts_written": written})
    print(f"\n[redteam] {len(written)} name(s) cleared the action bar or are held -> {pdir}/: "
          f"{', '.join(written) or '(none)'}")
    print(f"[redteam] NEXT: write {args.synth_dir}/redteam/<TKR>.json per prompt, then "
          f"`python orchestrate.py {args.mode}`")
    _finish([], p)


def run_final(args):
    os.makedirs(args.synth_dir, exist_ok=True)
    res = routine.daily_routine(synth_provider=file_synth_provider(args.synth_dir),
                                red_team_provider=connectors.file_red_team_provider(
                                    os.path.join(args.synth_dir, "redteam")),
                                journal_committer=(None if args.no_commit else git_committer),
                                outdir=args.outdir, persist=True, write_journal=True,
                                position_source=None, emailer=None, drive_syncer=None,
                                **_kwargs(args))
    m, p = _write_manifest(res, args.mode, args.outdir, extra={"pass": "final"})
    # the manifest is itself part of the audit trail: commit it on the same (loud) push path
    if not args.no_commit:
        try:
            git_committer(config.STORE_DIR, f"run manifest {m['date']} {args.mode}")
            m["commit"]["pushed"] = (git_committer.last or {}).get("pushed")
            m["commit"]["push_error"] = (git_committer.last or {}).get("push_error")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(m, f, indent=1, default=str)
        except Exception as e:
            print(f"[audit] manifest commit failed: {e}")
    _finish(_check_manifest(m, final=True), p)


def _finish(problems, manifest_path):
    print(f"[manifest] {manifest_path}")
    if problems:
        print("\n!!! RUN FLAGGED (exit 2). Problems:")
        for pr in problems:
            print(f"  - {pr}")
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="Equity Engine v2 orchestrator (recommend-only; PAPER_MODE).")
    sub = ap.add_subparsers(dest="mode", required=True)
    for mode, helptxt in (("daily", "monitor: held + 8-K + movers + sector events (small deep cap)"),
                          ("sweep", "research: daily + the rotating universe slice (larger deep cap)")):
        d = sub.add_parser(mode, help=helptxt)
        d.add_argument("--batch", type=int, default=None)
        d.add_argument("--limit", type=int, default=None)
        d.add_argument("--max-deep", type=int, default=None)
        d.add_argument("--watchlist", default="watchlist.txt")
        d.add_argument("--watchlist-only", action="store_true", help="ignore the index; scan watchlist.txt")
        d.add_argument("--positions", default="positions.json")
        d.add_argument("--synth-dir", default="synth")
        d.add_argument("--outdir", default="out")
        d.add_argument("--no-news", action="store_true")
        g = d.add_mutually_exclusive_group()
        g.add_argument("--emit-prompts", action="store_true", help="pass 1")
        g.add_argument("--emit-redteam", action="store_true", help="pass 2")
        d.add_argument("--no-commit", action="store_true", help="skip the git audit commit")
    sub.add_parser("retro", help="score matured theses + refresh LESSONS.md")

    args = ap.parse_args()
    if args.mode == "retro":
        routine.monthly_retrospective()
    elif args.emit_prompts:
        emit_prompts(args)
    elif args.emit_redteam:
        emit_redteam(args)
    else:
        run_final(args)


if __name__ == "__main__":
    main()
