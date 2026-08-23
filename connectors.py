"""
connectors.py - the orchestration seams, with SAFE no-credential defaults.

Design (CONNECTING.md): the Python holds NO credentials. The orchestration layer
(a Claude Code routine / Cowork task) injects real callables for the live services;
this module provides their STRUCTURE plus dry-run defaults that only LOG what they
would do, so routine.py runs end-to-end with or without connections.

HARD RULE: Robinhood access is READ-ONLY. There is no order-placement function in
this module — or anywhere in the project — and there must never be one. read_positions
only ever READS holdings for context.
"""
import json
import os
import datetime as dt


def _log(msg):
    print(f"[connector] {msg}")


def _normalize_positions(raw):
    out = []
    for p in (raw or []):
        if not isinstance(p, dict) or "ticker" not in p:
            continue
        out.append({"ticker": str(p["ticker"]).upper(),
                    "shares": p.get("shares"), "avg_cost": p.get("avg_cost")})
    return out


def read_positions(source=None, fallback_path="positions.json"):
    """Return current holdings as [{"ticker","shares","avg_cost"}].

    source: optional READ-ONLY callable injected by the orchestration layer (e.g. a
            Robinhood get_equity_positions read) returning that list. It must NEVER be
            an order call. Falls back to the local positions.json when absent or failing.
    """
    if callable(source):
        try:
            pos = _normalize_positions(source())
            _log(f"positions: pulled {len(pos)} holdings from injected read-only source")
            return pos
        except Exception as e:
            _log(f"positions: injected source failed ({type(e).__name__}: {e}); "
                 f"falling back to {fallback_path}")
    if os.path.exists(fallback_path):
        try:
            pos = _normalize_positions(json.load(open(fallback_path)))
        except Exception as e:
            _log(f"positions: {fallback_path} unreadable ({type(e).__name__}: {e}); running unheld")
            return []
        _log(f"positions: loaded {len(pos)} holdings from {fallback_path}")
        return pos
    _log("positions: none found (no source, no file) — running unheld")
    return []


def send_brief_email(html_path, sender=None, to=None, subject=None, dry_run=None):
    """Email the brief. sender: optional callable(to, subject, html_str) injected by the
    orchestration layer (e.g. a Gmail connector). Default is DRY-RUN: log intent, send
    nothing. dry_run=None means 'dry-run unless a real sender was supplied'."""
    if not os.path.exists(html_path):
        _log(f"email: {html_path} missing — nothing to send")
        return {"sent": False, "reason": "missing_file"}
    html = open(html_path).read()
    subject = subject or f"Equity Engine brief — {dt.date.today().isoformat()}"
    dry = (sender is None) if dry_run is None else dry_run
    if dry or not callable(sender):
        _log(f"[DRY-RUN] would email '{subject}' to {to or 'you'} "
             f"({len(html)} bytes from {html_path})")
        return {"sent": False, "dry_run": True, "subject": subject, "bytes": len(html)}
    try:
        sender(to, subject, html)
        _log(f"email: sent '{subject}' to {to}")
        return {"sent": True, "subject": subject}
    except Exception as e:
        _log(f"email: send failed ({type(e).__name__}: {e})")
        return {"sent": False, "error": str(e)}


def sync_journal_to_drive(syncer=None, journal_root=None, dry_run=None):
    """Mirror the journal tree to Drive. Delegates to journal.push_to_gdoc, which walks
    the tree and either calls the injected syncer(relpath, content) per file or returns a
    dry-run manifest of what WOULD sync. syncer is injected by the orchestration layer."""
    import journal
    dry = (syncer is None) if dry_run is None else dry_run
    manifest = journal.push_to_gdoc(syncer=syncer, journal_root=journal_root, dry_run=dry)
    if dry:
        _log(f"[DRY-RUN] would sync {len(manifest)} journal docs to Drive")
    else:
        _log(f"journal: synced {len(manifest)} docs to Drive")
    return manifest


def commit_store(committer=None, message=None, store_dir=None, dry_run=None):
    """Audit-trail seam (ROUTINE.md step 6): commit store/ — the journal + snapshots — so the git
    history IS the point-in-time record the retrospective scores against. The orchestration layer
    injects committer(store_dir, message) to do the real commit/push; with none it DRY-RUNS (logs
    what it would commit) and never touches git. Side-effect-free and recommend-only by default."""
    import config
    sd = store_dir or config.STORE_DIR
    msg = message or f"engine run {dt.date.today().isoformat()}"
    dry = (committer is None) if dry_run is None else dry_run
    n = sum(len(fs) for _, _, fs in os.walk(sd)) if os.path.isdir(sd) else 0
    if dry or not callable(committer):
        _log(f"[DRY-RUN] would commit {n} files under {sd}/ as the audit trail — '{msg}'")
        return {"committed": False, "dry_run": True, "files": n, "message": msg}
    try:
        committer(sd, msg)
        _log(f"audit trail: committed {n} files under {sd}/ — '{msg}'")
        return {"committed": True, "files": n, "message": msg}
    except Exception as e:
        _log(f"audit commit failed ({type(e).__name__}: {e})")
        return {"committed": False, "error": str(e)[:100]}


# ----------------------------------------------------------- v2 seams (all read-only, file-based)
# The routine (holding the connectors) writes small JSON files; Python reads them. No credentials
# in Python, and every seam degrades to None when the file is absent.
CONSENSUS_DIR = os.environ.get("CONSENSUS_DIR", os.path.join("synth", "consensus"))
REDTEAM_DIR = os.environ.get("REDTEAM_DIR", os.path.join("synth", "redteam"))


def _read_json_file(path):
    if not os.path.exists(path):
        return None
    try:
        d = json.load(open(path, encoding="utf-8"))
        return d if isinstance(d, dict) else None
    except Exception as e:
        _log(f"{path} unreadable ({type(e).__name__}); ignoring")
        return None


def read_street_consensus(ticker, consensus_dir=None):
    """Street consensus snapshot for a promoted name: synth/consensus/<TKR>.json.

    Written by the routine from S&P Capital IQ (S&P Global connector) when that connector works,
    else from a web-sourced fallback (source = "web:<site>"). Shape: see CONNECTING.md §5. Files
    older than 7 days are returned with stale=True so the synthesizer knows to refresh by search.
    """
    snap = _read_json_file(os.path.join(consensus_dir or CONSENSUS_DIR, f"{str(ticker).upper()}.json"))
    if not snap:
        return None
    try:
        age = (dt.date.today() - dt.date.fromisoformat(str(snap.get("as_of", ""))[:10])).days
        snap["stale"] = age > 7
    except Exception:
        snap["stale"] = True
    return snap


def file_red_team_provider(redteam_dir=None):
    """provider(prompt)->json_str for engine.run(red_team_provider=...): reads
    synth/redteam/<TKR>.json written by the agent after its devil's-advocate pass. None when absent
    (the thesis then stands un-red-teamed and is flagged as such on the dashboard)."""
    import re as _re
    d = redteam_dir or REDTEAM_DIR
    pat = _re.compile(r'"ticker":\s*"([A-Z0-9.\-]+)"')

    def provider(prompt):
        m = pat.search(prompt)
        if not m:
            return None
        p = os.path.join(d, f"{m.group(1)}.json")
        try:
            return open(p, encoding="utf-8").read() if os.path.exists(p) else None
        except Exception:
            return None
    return provider
