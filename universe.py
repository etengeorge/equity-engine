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
LAST_ASOF = None     # 'Fund Holdings as of' date parsed from a local holdings file (ISO str)
LAST_STALE = False   # True when the local file predates STALE_AFTER_DAYS (see _local_asof)

# The index reconstitutes annually each June, so a holdings file more than ~4 months old can
# be missing a whole reconstitution. v1's lesson was that a wrong universe must never look
# healthy: a stale drop-in still loads (the pipeline stays exercisable) but is labeled STALE
# in LAST_SOURCE, recorded in the run manifest, and flagged as a manifest problem.
STALE_AFTER_DAYS = 120
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


def _local_asof(raw, path):
    """The holdings file's as-of date, as (iso_str, age_days). iShares puts
    `Fund Holdings as of,"Aug 22, 2026"` in the preamble; fall back to the file's mtime when
    the header is absent (a plain universe.txt). Returns (None, None) if nothing parses."""
    for ln in raw.splitlines()[:40]:
        if ln.lower().lstrip('"').startswith("fund holdings as of"):
            val = ln.split(",", 1)[1].strip().strip('"') if "," in ln else ""
            for fmt in ("%b %d, %Y", "%d-%b-%Y", "%Y-%m-%d", "%m/%d/%Y"):
                try:
                    d = dt.datetime.strptime(val, fmt).date()
                    return d.isoformat(), (dt.date.today() - d).days
                except ValueError:
                    continue
            break
    try:
        d = dt.date.fromtimestamp(os.path.getmtime(path))
        return d.isoformat(), (dt.date.today() - d).days
    except Exception:
        return None, None


def _from_local_file():
    global LAST_ASOF, LAST_STALE
    for d in (".", config.STORE_DIR):
        for name in LOCAL_CANDIDATES:
            p = os.path.join(d, name)
            if os.path.exists(p):
                raw = open(p, encoding="utf-8", errors="ignore").read()
                tickers = (_parse_plain_list(raw) if name.endswith(".txt")
                           else parse_holdings_csv(raw))
                if tickers:
                    asof, age = _local_asof(raw, p)
                    LAST_ASOF = asof
                    LAST_STALE = age is not None and age > STALE_AFTER_DAYS
                    label = f"local file {p}"
                    if asof:
                        label += f" (as of {asof}"
                        label += f", STALE {age}d)" if LAST_STALE else ")"
                    return tickers, label
    return None, None


def _from_ishares():
    req = urllib.request.Request(config.IWM_HOLDINGS_URL, headers={"User-Agent": _UA})
    raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    tickers = parse_holdings_csv(raw)        # [] if HTML/consent wall
    return (tickers, "iShares IWM CSV") if tickers else (None, None)


VTWO_URL = ("https://investor.vanguard.com/investment-products/etfs/profile/api/VTWO/"
            "portfolio-holding/stock")


def _from_vanguard():
    """Vanguard Russell 2000 ETF (VTWO) holdings. Free, headless-friendly JSON (no consent
    wall), paged 500 at a time. Faithful R2000 constituent list; Vanguard refreshes monthly."""
    tickers, start, asof = [], 1, None
    while True:
        url = f"{VTWO_URL}?start={start}&count=500"
        req = urllib.request.Request(url, headers={"User-Agent": _UA, "Accept": "application/json",
                                                   "Referer": "https://investor.vanguard.com/"})
        d = json.loads(urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore"))
        ents = (d.get("fund") or {}).get("entity") or []
        for e in ents:
            t = (e.get("ticker") or "").strip().upper()
            if t and t not in ("-", "N/A"):
                tickers.append(t.replace(".", "-"))   # MOG.A -> MOG-A (EDGAR / yfinance style)
            asof = asof or e.get("asOfDate")
        if len(ents) < 500:
            break
        start += 500
    tickers = sorted(set(tickers))
    if len(tickers) < 1500:      # a faithful R2000 pull is ~1,900-2,000; anything less is a partial page
        return None, None
    return tickers, f"Vanguard VTWO holdings ({len(tickers)} tickers, as of {str(asof)[:10]})"


def _from_sec():
    import data_sources as ds
    tickers = sorted(ds._ticker_map().keys())
    return tickers, f"SEC company_tickers.json (ALL {len(tickers)} US filers — superset, NOT R2000)"


def _cache_fresh(path):
    try:
        return dt.date.fromtimestamp(os.path.getmtime(path)) == dt.date.today()
    except Exception:
        return False


# v2: the SEC all-filers superset (~10k names) is NOT the Russell 2000 and silently ran the
# old routine for weeks. It is now opt-in only (ALLOW_SEC_SUPERSET=1); "auto" stops at Vanguard.
_ALLOW_SUPERSET = os.environ.get("ALLOW_SEC_SUPERSET", "0") == "1"
_ORDER = {"auto": ["file", "ishares", "vanguard"] + (["sec"] if _ALLOW_SUPERSET else []),
          "file": ["file"], "ishares": ["ishares"], "vanguard": ["vanguard"], "sec": ["sec"]}
_FETCHERS = {"file": _from_local_file, "ishares": _from_ishares, "vanguard": _from_vanguard,
             "sec": _from_sec}


def load_iwm_universe(limit=None, refresh=False, source="auto", cache_path=RESOLVED_CACHE,
                      verbose=True):
    """Return the universe ticker list (see module docstring for source order)."""
    global LAST_SOURCE, LAST_ASOF, LAST_STALE
    LAST_ASOF, LAST_STALE = None, False
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
        raise RuntimeError("no faithful Russell 2000 source: no local IWM_holdings.csv, iShares "
                           "returned its consent wall, and the Vanguard VTWO API failed. Refusing "
                           "to fall back to the SEC all-filers superset (set ALLOW_SEC_SUPERSET=1 "
                           "to override). Drop IWM_holdings.csv in the project and retry.")
    if verbose:
        print(f"[universe] source: {used} -> {len(tickers)} tickers")
        if LAST_STALE:
            print(f"[universe] WARNING: holdings file is stale (as of {LAST_ASOF}, older than "
                  f"{STALE_AFTER_DAYS}d). The index reconstitutes each June — refresh "
                  "IWM_holdings.csv (README: 'Refreshing the universe').")
    LAST_SOURCE = used
    # cache only the FAITHFUL sources (don't sticky-cache the SEC superset so a later
    # drop-in IWM_holdings.csv takes effect immediately), and never cache a STALE file —
    # a day-cache would hide the staleness from the next run's manifest.
    if used and not used.startswith("SEC") and not LAST_STALE:
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
