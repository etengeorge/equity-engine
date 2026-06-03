"""
store.py - the durable record. One JSON file per company.

In production this directory is a git repo: a scheduled run pulls it at the
start and commits+pushes at the end, so commit history IS the point-in-time
audit trail (the integrity discipline). Here we just read/write the files;
`git init` the directory and the history starts accruing for free.

Point-in-time rule: we stamp every write with the date the data was observed,
and the retrospective only ever scores a thesis against the record as it stood
at thesis-creation time. That keeps restated financials from handing the system
hindsight it never had.
"""
import json
import os
import datetime as dt

import config


def _path(cik):
    os.makedirs(os.path.join(config.STORE_DIR, "companies"), exist_ok=True)
    return os.path.join(config.STORE_DIR, "companies", f"{int(cik):010d}.json")


def load(cik):
    p = _path(cik)
    if os.path.exists(p):
        try:
            with open(p) as f:
                return json.load(f)
        except Exception:
            # a corrupt / half-written company file must not crash the whole run
            return None
    return None


def upsert(record):
    """Merge a fresh observation into the company record, append-only on history."""
    cik = record["cik"]
    existing = load(cik) or {"cik": cik, "observations": [], "theses": []}
    stamp = dt.date.today().isoformat()
    # snapshot the observable state, never overwriting prior snapshots
    existing["ticker"] = record.get("ticker")
    existing["name"] = record.get("name")
    existing["observations"].append({"date": stamp, "snapshot": record["snapshot"]})
    existing["latest"] = record["snapshot"]
    existing["latest_date"] = stamp
    with open(_path(cik), "w") as f:
        json.dump(existing, f, indent=2, default=str)
    return existing


def all_latest():
    """Every stored company's latest snapshot — for the cross-universe recommendation board
    (the accumulated long/short ideas across the rotation cycle). Cheap: local reads, no network."""
    import glob
    out = []
    for f in glob.glob(os.path.join(config.STORE_DIR, "companies", "*.json")):
        try:
            snap = json.load(open(f)).get("latest")
            if snap:
                out.append(snap)
        except Exception:
            continue
    return out


def all_latest_reports(limit=250):
    """Latest snapshot per company WITH its observation date + history depth — the research
    LIBRARY feeding the dashboard's Reports tab (every report produced, not just today's board).
    Newest first, then by reliability-weighted rank. Cheap: local reads, no network."""
    import glob
    out = []
    for f in glob.glob(os.path.join(config.STORE_DIR, "companies", "*.json")):
        try:
            with open(f) as fh:
                rec = json.load(fh)
            snap = rec.get("latest")
            if snap:
                out.append({"date": rec.get("latest_date"),
                            "n_observations": len(rec.get("observations") or []),
                            "snapshot": snap})
        except Exception:
            continue
    out.sort(key=lambda x: ((x.get("date") or ""),
                            (x["snapshot"].get("rank_score") if isinstance(x.get("snapshot"), dict) else -1) or -1),
             reverse=True)
    return out[:limit] if limit else out


def load_by_ticker(ticker):
    """Find a stored record by ticker (scans the store dir). Used by the scanner to
    re-price names against their last full analysis without re-pulling data."""
    import glob
    t = ticker.upper()
    for f in glob.glob(os.path.join(config.STORE_DIR, "companies", "*.json")):
        try:
            rec = json.load(open(f))
            if (rec.get("ticker") or rec.get("latest", {}).get("ticker", "")).upper() == t:
                return rec
        except Exception:
            continue
    return None
