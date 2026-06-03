"""
universe.py - load the investable universe (the Russell 2000) so the routine can scan
the whole index instead of a hand-list.

DATA-ACCESS REALITY: the iShares IWM holdings CSV (`config.IWM_HOLDINGS_URL`) is now
gated behind a browser consent wall — a headless fetch returns a 3 MB HTML page, not
CSV. So this loader is source-robust and tries, in order (source="auto"):

  1. LOCAL holdings file you (or the orchestration browser/Chrome connector) dropped in
     the project or STORE_DIR: IWM_holdings.csv / russell2000.csv (iShares CSV format),
     or universe.txt (one ticker per line). THIS is the faithful, blessed path: download
     the holdings CSV from ishares.com in a browser (consent handled there) and drop it
     in — exactly the engine's "Python holds no connections; the orchestration layer
     feeds it files" design (see CONNECTING.md).
  2. The iShares CSV URL — used only if it actually returns CSV (HTML is rejected, not
     silently parsed to an empty list).
  3. The SEC company_tickers.json (all ~10k US filers) — a labeled SUPERSET so the engine
     is never dead-in-the-water. Not the Russell 2000, but the reliability/liquidity gates
     and the scan's prioritization still apply; use it to exercise the pipeline.

Resolved lists from the faithful sources (1, 2) are cached per-day under STORE_DIR so
repeat runs are instant. limit= truncates for staged rollout / testing.
"""
import csv
import datetime as dt
import json
import os
import urllib.request

import config

RESOLVED_CACHE = os.path.join(config.STORE_DIR, "universe_resolved.txt")
MEMBERSHIP_PATH = os.path.join(config.STORE_DIR, "universe_membership.json")
CURSOR_PATH = os.path.join(config.STORE_DIR, "universe_cursor.json")
LOCAL_CANDIDATES = ["IWM_holdings.csv", "russell2000.csv", "universe.txt"]
LAST_SOURCE = None   # set by load_iwm_universe() to the source actually used (for churn gating)
_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
       "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
_NON_TICKERS = {"CASH", "USD", "MARGIN_USD", "-", "--", ""}


def parse_holdings_csv(raw):
    """iShares holdings CSV text -> ordered, de-duped equity tickers. Returns [] if the
    text is HTML (consent wall) or has no 'Ticker' header — the caller treats [] as a
    failed source, never as 'an empty universe'."""
    head = raw[:400].lower()
    if "<!doctype" in head or "<html" in head:
        return []
    lines = raw.splitlines()
    start = next((i for i, ln in enumerate(lines)
                  if ln.lstrip('"').upper().startswith("TICKER")), None)
    if start is None:
        return []
    seen, out = set(), []
    for r in csv.DictReader(lines[start:]):
        tk = (r.get("Ticker") or "").strip().strip('"').upper()
        asset = (r.get("Asset Class") or "Equity").strip().strip('"')
        if not tk or tk in _NON_TICKERS or asset != "Equity" or " " in tk:
            continue
        if tk not in seen:
            seen.add(tk)
            out.append(tk)
    return out


def _parse_plain_list(raw):
    seen, out = set(), []
    for ln in raw.splitlines():
        t = ln.split("#", 1)[0].strip().upper()
        if t and t not in seen:
            seen.add(t)
            out.append(t)
    return out


def _from_local_file():
    for d in (".", config.STORE_DIR):
        for name in LOCAL_CANDIDATES:
            p = os.path.join(d, name)
            if os.path.exists(p):
                raw = open(p, encoding="utf-8", errors="ignore").read()
                tickers = (_parse_plain_list(raw) if name.endswith(".txt")
                           else parse_holdings_csv(raw))
                if tickers:
                    return tickers, f"local file {p}"
    return None, None


def _from_ishares():
    req = urllib.request.Request(config.IWM_HOLDINGS_URL, headers={"User-Agent": _UA})
    raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    tickers = parse_holdings_csv(raw)        # [] if HTML/consent wall
    return (tickers, "iShares IWM CSV") if tickers else (None, None)


def _from_sec():
    import data_sources as ds
    tickers = sorted(ds._ticker_map().keys())
    return tickers, f"SEC company_tickers.json (ALL {len(tickers)} US filers — superset, NOT R2000)"


def _cache_fresh(path):
    try:
        return dt.date.fromtimestamp(os.path.getmtime(path)) == dt.date.today()
    except Exception:
        return False


_ORDER = {"auto": ["file", "ishares", "sec"], "file": ["file"],
          "ishares": ["ishares"], "sec": ["sec"]}
_FETCHERS = {"file": _from_local_file, "ishares": _from_ishares, "sec": _from_sec}


def load_iwm_universe(limit=None, refresh=False, source="auto", cache_path=RESOLVED_CACHE,
                      verbose=True):
    """Return the universe ticker list (see module docstring for source order)."""
    global LAST_SOURCE
    if not refresh and source == "auto" and _cache_fresh(cache_path):
        try:
            cached = _parse_plain_list(open(cache_path, encoding="utf-8").read())
            if cached:
                LAST_SOURCE = "local cache"
                if verbose:
                    print(f"[universe] using today's cache ({len(cached)} tickers) — "
                          "--refresh-universe to re-pull")
                return cached[:limit] if limit else cached
        except Exception:
            pass

    tickers, used = None, None
    for s in _ORDER[source]:
        try:
            tickers, used = _FETCHERS[s]()
        except Exception:
            tickers, used = None, None
        if tickers:
            break
    if not tickers:
        raise RuntimeError("no universe source available: no local holdings file found, "
                           "iShares returned non-CSV (consent wall), and the SEC fallback "
                           "failed. Drop IWM_holdings.csv in the project and retry.")
    if verbose:
        print(f"[universe] source: {used} -> {len(tickers)} tickers")
    LAST_SOURCE = used
    # cache only the FAITHFUL sources (don't sticky-cache the SEC superset so a later
    # drop-in IWM_holdings.csv takes effect immediately)
    if used and not used.startswith("SEC"):
        try:
            os.makedirs(os.path.dirname(cache_path) or ".", exist_ok=True)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write("\n".join(tickers))
        except Exception:
            pass
    return tickers[:limit] if limit else tickers


def load_membership():
    """The last recorded universe membership: {'asof','source','tickers'} or None."""
    try:
        with open(MEMBERSHIP_PATH, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def record_membership(tickers, source="", asof=None):
    """Dynamic membership tracking: diff the current universe against the last recorded
    membership FROM THE SAME SOURCE, persist the new membership, and return the churn:
      {'asof', 'prior_asof', 'added', 'removed'}.
    'added'   = names that ENTERED the index (new holdings) — deep-analyzed as uncovered.
    'removed' = names that LEFT (annual reconstitution, M&A / take-private, delisting,
                distress). A source change (e.g. the SEC superset -> a dropped-in IWM file)
                resets the baseline so it doesn't read as false churn. Called only on FULL
                pulls (the routine skips it on --limit subsets)."""
    asof = asof or dt.date.today().isoformat()
    cur = {t.upper() for t in tickers}
    prior = load_membership()
    if prior and prior.get("source") == source:
        prev = set(prior.get("tickers", []))
        added, removed, prior_asof = sorted(cur - prev), sorted(prev - cur), prior.get("asof")
    else:
        added, removed, prior_asof = [], [], (prior or {}).get("asof")
    try:
        os.makedirs(os.path.dirname(MEMBERSHIP_PATH) or ".", exist_ok=True)
        with open(MEMBERSHIP_PATH, "w", encoding="utf-8") as f:
            json.dump({"asof": asof, "source": source, "tickers": sorted(cur)}, f)
    except Exception:
        pass
    return {"asof": asof, "prior_asof": prior_asof, "added": added, "removed": removed}


def next_batch(tickers, batch_size, cursor_path=CURSOR_PATH):
    """Rotating slice for free, multi-run-per-day coverage. Returns
    {'batch', 'start', 'cycle_runs'} and advances a PERSISTED cursor by batch_size each call,
    so consecutive runs sweep different slices and the whole universe completes one cheap-scan
    cycle every cycle_runs runs (wraps around). batch_size falsy / >= len -> the full universe."""
    import math
    n = len(tickers)
    if not batch_size or batch_size <= 0 or batch_size >= n:
        return {"batch": list(tickers), "start": 0, "cycle_runs": 1}
    cur = 0
    try:
        with open(cursor_path, encoding="utf-8") as f:
            cur = int(json.load(f).get("cursor", 0)) % n
    except Exception:
        cur = 0
    batch = (list(tickers) + list(tickers))[cur:cur + batch_size]
    try:
        os.makedirs(os.path.dirname(cursor_path) or ".", exist_ok=True)
        with open(cursor_path, "w", encoding="utf-8") as f:
            json.dump({"cursor": (cur + batch_size) % n, "size": n, "batch": batch_size}, f)
    except Exception:
        pass
    return {"batch": batch, "start": cur, "cycle_runs": math.ceil(n / batch_size)}


if __name__ == "__main__":
    import sys
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    u = load_iwm_universe(limit=lim)
    print(f"universe: {len(u)} tickers")
    print(", ".join(u[:40]) + (" ..." if len(u) > 40 else ""))
