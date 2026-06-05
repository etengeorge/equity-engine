"""
orchestrate.py - the SINGLE entry point the scheduled routine invokes.

It wires the whole loop and fills the seams Python can fill itself (the git audit commit is
real here). Live per-name reasoning plugs in via a FILE-BASED synthesis provider, so no code
changes are needed to go live:

  pass 1   python orchestrate.py daily --iwm --batch 250 --emit-prompts
           -> writes each promoted name's synthesis prompt to  synth/prompts/<TICKER>.txt
  (agent)  read each prompt, do the 7-step analysis + web_search, write  synth/<TICKER>.json
           (the schema is synthesis.PROMPT_TEMPLATE; return ONLY that JSON)
  pass 2   python orchestrate.py daily --iwm --batch 250
           -> feeds synth/<TICKER>.json through the engine (names with no file fall back to the
              deterministic stub), builds the dashboard/email, FEEDS the sector dossiers, and
              commits store/ as the audit trail.

The Robinhood / Gmail / Drive seams stay AGENT-mediated (the agent pulls positions read-only,
emails the brief, syncs Drive around this script — see ROUTINE_PROMPT.md and CONNECTING.md).
Recommend-only. PAPER_MODE. There is no order path.

  python orchestrate.py daily [--iwm] [--batch N] [--limit N] [--max-deep N]
                              [--watchlist f] [--positions f] [--synth-dir synth]
                              [--emit-prompts] [--no-commit] [--outdir out]
  python orchestrate.py retro
"""
import argparse
import os
import re
import subprocess

import routine

_TICKER_RE = re.compile(r'"ticker":\s*"([A-Z0-9.\-]+)"')


# ----------------------------------------------------------- live synthesis seam
def file_synth_provider(synth_dir):
    """provider(prompt)->json_str: read synth_dir/<TICKER>.json for the prompt's ticker, else None
    (the engine then falls back to the stub). This is how the agent's live reasoning is injected."""
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


def combined_provider(synth_dir):
    """Prefer a per-ticker JSON the agent wrote; else the hand-authored _live_synthesis.provider
    (the 4 demo names); else None -> deterministic stub."""
    file_prov = file_synth_provider(synth_dir)
    try:
        import _live_synthesis as ls
        hand = ls.provider
    except Exception:
        hand = None

    def provider(prompt):
        return file_prov(prompt) or (hand(prompt) if hand else None)
    return provider


def capture_provider(captured):
    """Pass-1 provider: record each rendered prompt by ticker, return None (stub fallback)."""
    def provider(prompt):
        m = _TICKER_RE.search(prompt)
        if m:
            captured[m.group(1)] = prompt
        return None
    return provider


# ----------------------------------------------------------- git audit seam
def git_committer(store_dir, message):
    """Real git audit commit of store/ (+ push if an 'origin' remote exists). Best-effort:
    raises only on a genuine commit error so connectors.commit_store can log it."""
    # stage the audit trail + the published static dashboard (public/) so a push triggers
    # the Vercel deploy. Add each path only if present so a missing one never blocks the commit.
    for _p in (store_dir, "public", "vercel.json"):
        if os.path.exists(_p):
            subprocess.run(["git", "add", _p], check=False, capture_output=True)
    r = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
    if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
        raise RuntimeError((r.stderr or r.stdout)[:160])
    if subprocess.run(["git", "remote"], capture_output=True, text=True).stdout.strip():
        subprocess.run(["git", "push"], capture_output=True)


# ----------------------------------------------------------- modes
def _daily_kwargs(args):
    return dict(watchlist=args.watchlist, positions_path=args.positions, iwm=args.iwm,
                batch=args.batch, limit=args.limit, max_deep=args.max_deep, gather_news=True)


def emit_prompts(args):
    captured = {}
    routine.daily_routine(synth_provider=capture_provider(captured), persist=False,
                          write_journal=False, journal_committer=None,
                          outdir=os.path.join(args.outdir, "_emit"), **_daily_kwargs(args))
    pdir = os.path.join(args.synth_dir, "prompts")
    os.makedirs(pdir, exist_ok=True)
    for tk, prompt in captured.items():
        with open(os.path.join(pdir, f"{tk}.txt"), "w", encoding="utf-8") as f:
            f.write(prompt)
    print(f"\n[emit] wrote {len(captured)} synthesis prompts to {pdir}/")
    print(f"[emit] NEXT: analyze each and write {args.synth_dir}/<TICKER>.json (synthesis.PROMPT_TEMPLATE "
          "schema, JSON only), then re-run `orchestrate.py daily` to feed them.")


def run_daily(args):
    os.makedirs(args.synth_dir, exist_ok=True)
    routine.daily_routine(synth_provider=combined_provider(args.synth_dir),
                          journal_committer=(None if args.no_commit else git_committer),
                          outdir=args.outdir, persist=True, write_journal=True,
                          # Robinhood / Gmail / Drive stay agent-mediated (dry-run from Python):
                          position_source=None, emailer=None, drive_syncer=None,
                          **_daily_kwargs(args))


def main():
    ap = argparse.ArgumentParser(description="Equity Engine orchestrator (recommend-only; PAPER_MODE).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("daily", help="the full connected daily loop")
    d.add_argument("--iwm", action="store_true")
    d.add_argument("--batch", type=int, default=None)
    d.add_argument("--limit", type=int, default=None)
    d.add_argument("--max-deep", type=int, default=None)
    d.add_argument("--watchlist", default="watchlist.txt")
    d.add_argument("--positions", default="positions.json")
    d.add_argument("--synth-dir", default="synth")
    d.add_argument("--outdir", default="out")
    d.add_argument("--emit-prompts", action="store_true",
                   help="pass 1: write the promoted names' synthesis prompts for the agent to reason over")
    d.add_argument("--no-commit", action="store_true", help="skip the git audit commit")
    sub.add_parser("retro", help="score matured theses + refresh LESSONS")

    args = ap.parse_args()
    if args.cmd == "retro":
        routine.monthly_retrospective()
    elif args.emit_prompts:
        emit_prompts(args)
    else:
        run_daily(args)


if __name__ == "__main__":
    main()
