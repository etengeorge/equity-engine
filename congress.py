"""
congress.py - congressional-trade sourcing (STOCK Act disclosures).

A FREE sourcing signal. Members of Congress must file a Periodic Transaction
Report (PTR) within 45 days of a securities trade over $1,000. A LARGE disclosed
trade is a reason to LOOK: promote that name to deep research and ask WHY (a
policy edge, a government contract, a sector tailwind the filer may have a read
on). It is NEVER a reason to ACT — the reverse-DCF still governs the
recommendation, and synthesis must EXPLAIN the trade, not copy it. (This is the
"sentiment triggers a LOOK, never an ACT" rule, applied to disclosures.)

SOURCES (free, no key, nothing paywalled — honors the free-sources hard rule):
  * House  — the OFFICIAL Clerk of the House disclosure feed, refreshed daily:
      index :  https://disclosures-clerk.house.gov/public_disc/financial-pdfs/<YEAR>FD.zip
               -> <YEAR>FD.xml lists every filing; FilingType "P" == PTR.
      detail:  https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/<YEAR>/<DocID>.pdf
      This is where Pelosi and the marquee names file. It is the anchor source.
  * Senate — best-effort only. efdsearch.senate.gov sits behind a consent wall
      (like the iShares CSV) and the old free JSON mirrors are dead, so Senate is
      opportunistic: skipped with a flag when unreachable. House alone covers the
      high-signal names.

Resilience contract: any network/parse failure returns whatever was gathered plus
a flag and NEVER raises into the run (the one-bad-name rule). PDF parsing uses
pypdf when installed; without it, House transaction-detail parsing is skipped and
a flag is set (the run still works, just without this signal).
"""
import io
import json
import os
import re
import time
import zipfile
import datetime as dt
import urllib.request
import xml.etree.ElementTree as ET

import config

_HEADERS = {"User-Agent": config.SEC_USER_AGENT}
_last_call = [0.0]

_HOUSE_ZIP = "https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.zip"
_HOUSE_PTR = "https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/{doc_id}.pdf"

try:                       # pypdf is optional; without it we skip PDF detail parsing
    import pypdf as _pypdf
    _HAVE_PYPDF = True
except Exception:          # pragma: no cover - environment dependent
    _pypdf = None
    _HAVE_PYPDF = False


# --------------------------------------------------------------------- helpers
def _today():
    return dt.date.today()


def _dir(*parts):
    d = os.path.join(config.STORE_DIR, "congress", *parts)
    os.makedirs(os.path.dirname(d) if os.path.splitext(d)[1] else d, exist_ok=True)
    return d


def _http_get(url, timeout=45):
    # Polite throttle; the Clerk site is a public government endpoint, not rate-limited
    # like SEC, but we keep a small gap to be a good citizen.
    gap = time.time() - _last_call[0]
    if gap < 0.3:
        time.sleep(0.3 - gap)
    req = urllib.request.Request(url, headers=_HEADERS)
    out = urllib.request.urlopen(req, timeout=timeout).read()
    _last_call[0] = time.time()
    return out


def _parse_date(s):
    s = (s or "").strip()
    for fmt in ("%m/%d/%Y", "%Y-%m-%d", "%m/%d/%y", "%-m/%-d/%Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    # last resort: M/D/YYYY with single-digit parts
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{2,4})", s)
    if m:
        mo, da, yr = (int(x) for x in m.groups())
        yr = yr + 2000 if yr < 100 else yr
        try:
            return dt.date(yr, mo, da)
        except ValueError:
            return None
    return None


# ------------------------------------------------------------- amount parsing
_AMOUNT_RE = re.compile(r"\$\s*([\d,]+)\s*[-–]\s*\$\s*([\d,]+)")


def _amount_low_high(text):
    """Disclosed amounts are RANGES (e.g. '$50,001 - $100,000'). Return (low, high) ints,
    or (0, 0) if no range is present. The lower bound drives the 'big trade' filter."""
    m = _AMOUNT_RE.search(text or "")
    if not m:
        return 0, 0
    try:
        return int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
    except ValueError:
        return 0, 0


# ------------------------------------------------------------- PTR text parser
# Tickers print inside parentheses after the asset name, e.g. "NVIDIA Corp (NVDA) [ST]".
_TICKER_RE = re.compile(r"\(([A-Z][A-Z.\-]{0,5})\)")
_DATE_IN_RE = re.compile(r"\d{1,2}/\d{1,2}/\d{2,4}")
# common non-equity codes that show up in parens and must NOT be treated as tickers
_NOT_TICKER = {"ST", "OP", "BO", "ET", "MF", "OL", "OT", "PE", "RP", "CT", "EF", "ID",
               "US", "USA", "IRA", "LLC", "INC", "ETF", "REIT", "N", "A", "S", "P", "E"}


def parse_ptr_text(text):
    """Pure parser: given the text extracted from a House PTR PDF, return a list of
    trade dicts. Heuristic but robust — anchors on each '(TICKER)' and reads the
    transaction type + amount range in the window around it. Returns [] on junk.
    Kept side-effect-free so it is unit-testable offline without a real PDF."""
    if not text:
        return []
    trades = []
    matches = list(_TICKER_RE.finditer(text))
    for i, m in enumerate(matches):
        ticker = m.group(1).upper().strip(".-")
        if not ticker or ticker in _NOT_TICKER or len(ticker) > 5:
            continue
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else min(len(text), start + 260)
        window = text[start:end]
        # asset name = a little text before the ticker (for display only)
        pre = text[max(0, m.start() - 80):m.start()]
        asset = re.split(r"[\n\r]", pre)[-1].strip(" .,-")[-70:]

        low, high = _amount_low_high(window)
        if low == 0 and high == 0:
            # amount sometimes sits just before the ticker on a wrapped row
            low, high = _amount_low_high(text[max(0, m.start() - 60):m.end() + 200])
        if low == 0 and high == 0:
            continue  # no amount range -> not a usable transaction row

        wl = window.lower()
        if "purchase" in wl:
            ttype = "buy"
        elif "exchange" in wl:
            ttype = "exchange"
        elif "sale" in wl or "sold" in wl:
            ttype = "sale"
        else:
            # fall back to the single-letter P/S/E code that precedes the date
            code = re.search(r"\b([PSE])\b", window)
            ttype = {"P": "buy", "S": "sale", "E": "exchange"}.get(
                code.group(1) if code else "", "")
        d = _DATE_IN_RE.search(window)
        tx_date = _parse_date(d.group(0)) if d else None
        trades.append({
            "ticker": ticker,
            "asset": asset,
            "type": ttype or "trade",
            "amount_low": low,
            "amount_high": high,
            "amount_str": f"${low:,} - ${high:,}" if high else f"${low:,}+",
            "transaction_date": tx_date.isoformat() if tx_date else None,
        })
    # de-dup identical rows: a ticker can print twice in the extracted text (header +
    # detail line), which would otherwise double-count one transaction.
    seen, uniq = set(), []
    for t in trades:
        key = (t["ticker"], t["type"], t["amount_low"], t["amount_high"], t["transaction_date"])
        if key not in seen:
            seen.add(key)
            uniq.append(t)
    return uniq


# ------------------------------------------------------------- House: index
def _house_xml_bytes(year):
    """Download (and cache for the day) the House Clerk annual FD.zip and return the
    inner <YEAR>FD.xml bytes. Cached at store/congress/<year>FD.xml; re-fetched when
    the cache is missing or older than today (the Clerk publishes a fresh ZIP daily)."""
    cache = _dir(f"{year}FD.xml")
    if os.path.exists(cache):
        age_date = dt.date.fromtimestamp(os.path.getmtime(cache))
        if age_date >= _today():
            with open(cache, "rb") as f:
                return f.read()
    raw = _http_get(_HOUSE_ZIP.format(year=year))
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        name = next((n for n in z.namelist() if n.lower().endswith(".xml")), None)
        if not name:
            raise ValueError("no XML in House FD.zip")
        data = z.read(name)
    with open(cache, "wb") as f:
        f.write(data)
    return data


def recent_house_ptrs(year=None, since_days=10):
    """Parse the House FD.xml index for Periodic Transaction Reports (FilingType 'P')
    filed within the window. Returns a list of {doc_id, name, last, filing_date, state}."""
    year = year or _today().year
    cutoff = _today() - dt.timedelta(days=since_days)
    data = _house_xml_bytes(year)
    root = ET.fromstring(data)
    out = []
    for mem in root.findall(".//Member"):
        def g(tag):
            el = mem.find(tag)
            return (el.text or "").strip() if el is not None and el.text else ""
        if g("FilingType").upper() != "P":
            continue
        doc_id = g("DocID")
        if not doc_id:
            continue
        fdate = _parse_date(g("FilingDate"))
        if fdate is None or fdate < cutoff:
            continue
        first, last = g("First"), g("Last")
        out.append({
            "doc_id": doc_id,
            "name": (f"{first} {last}").strip() or last,
            "last": last,
            "filing_date": fdate.isoformat(),
            "state": g("StateDst"),
            "year": year,
        })
    return out


def parse_house_ptr(doc_id, year):
    """Fetch + parse one House PTR PDF into trade dicts. Cached per DocID (filings are
    immutable once posted) at store/congress/parsed/<doc_id>.json. Best-effort: returns
    [] on a missing/scanned/unparseable PDF or when pypdf is unavailable."""
    cache = _dir("parsed", f"{doc_id}.json")
    if os.path.exists(cache):
        try:
            with open(cache) as f:
                return json.load(f)
        except Exception:
            pass
    if not _HAVE_PYPDF:
        return []
    trades = []
    try:
        raw = _http_get(_HOUSE_PTR.format(year=year, doc_id=doc_id))
        reader = _pypdf.PdfReader(io.BytesIO(raw))
        text = "\n".join((p.extract_text() or "") for p in reader.pages)
        trades = parse_ptr_text(text)
    except Exception:
        trades = []
    try:
        with open(cache, "w") as f:
            json.dump(trades, f)
    except Exception:
        pass
    return trades


# --------------------------------------------------------- Senate (best-effort)
def recent_senate_trades(since_days=10):
    """Best-effort Senate pass. The official eFD portal requires accepting an agreement
    (a CSRF/consent wall, like the iShares CSV under headless fetch) and the old free
    JSON mirrors are dead, so this returns [] with a flag unless a reachable mirror is
    configured via CONGRESS_SENATE_JSON_URL. House alone covers the marquee filers."""
    url = os.environ.get("CONGRESS_SENATE_JSON_URL", "").strip()
    if not url:
        return [], ["senate_skipped_no_free_source"]
    try:
        data = json.loads(_http_get(url))
    except Exception as e:
        return [], [f"senate_unavailable:{type(e).__name__}"]
    cutoff = _today() - dt.timedelta(days=since_days)
    out = []
    for r in (data if isinstance(data, list) else data.get("transactions", [])):
        tk = (r.get("ticker") or "").upper().strip()
        if not tk or tk in ("--", "N/A"):
            continue
        low, high = _amount_low_high(r.get("amount", ""))
        tdate = _parse_date(r.get("transaction_date") or r.get("transactionDate") or "")
        ttype = (r.get("type") or "").lower()
        ttype = "buy" if "purchase" in ttype else "sale" if "sale" in ttype else ttype or "trade"
        out.append({
            "ticker": tk, "asset": r.get("asset_description") or "",
            "type": ttype, "amount_low": low, "amount_high": high,
            "amount_str": r.get("amount") or (f"${low:,} - ${high:,}" if high else ""),
            "transaction_date": tdate.isoformat() if tdate else None,
            "name": r.get("senator") or r.get("name") or "",
            "filing_date": r.get("disclosure_date") or "",
        })
    out = [t for t in out if not t["transaction_date"]
           or _parse_date(t["transaction_date"]) is None
           or _parse_date(t["transaction_date"]) >= cutoff]
    return out, []


# ------------------------------------------------------------- seen-doc memory
def _load_seen():
    p = _dir("seen.json")
    if os.path.exists(p):
        try:
            with open(p) as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_seen(seen):
    try:
        with open(_dir("seen.json"), "w") as f:
            json.dump(seen, f)
    except Exception:
        pass


def _is_high_signal(name):
    n = (name or "").lower()
    return any(h.lower() in n for h in config.CONGRESS_HIGH_SIGNAL_NAMES)


# ----------------------------------------------------------------- public API
def recent_congressional_trades(days_back=None, min_amount=None, universe=None,
                                max_ptrs=None, mark_seen=True):
    """The sourcing entry point. Returns:
        {
          "by_ticker": {TICKER: [trade, ...]},   # FRESH (newly disclosed) big trades to promote
          "trades":    [trade, ...],             # the same, flat, newest first
          "flags":     [str, ...],               # degradation notes (never an exception)
          "scanned":   int,                      # PTR filings inspected this run
        }
    A trade dict: {ticker, politician, chamber, type, amount_low, amount_high,
                   amount_str, transaction_date, disclosure_date, doc_url, high_signal}.
    Only NEW filings (DocID not seen before) drive promotion, so a name is surfaced once
    rather than re-promoted every run for the whole disclosure window. NEVER raises."""
    if not config.CONGRESS_TRADES_TRIGGER:
        return {"by_ticker": {}, "trades": [], "flags": ["disabled"], "scanned": 0}
    days_back = days_back if days_back is not None else config.CONGRESS_LOOKBACK_DAYS
    min_amount = min_amount if min_amount is not None else config.CONGRESS_MIN_AMOUNT
    max_ptrs = max_ptrs if max_ptrs is not None else config.CONGRESS_MAX_PTRS_PER_RUN
    uni = {t.upper() for t in universe} if universe else None

    flags = []
    if not _HAVE_PYPDF:
        flags.append("pypdf_missing_house_detail_skipped")
    seen = _load_seen()
    fresh = []

    # ---- House (official, daily) -------------------------------------------
    ptrs = []
    try:
        ptrs = recent_house_ptrs(since_days=days_back)
        # early January: also sweep the prior year's tail
        if _today().month == 1:
            try:
                ptrs += recent_house_ptrs(year=_today().year - 1, since_days=days_back)
            except Exception:
                pass
    except Exception as e:
        flags.append(f"house_index_unavailable:{type(e).__name__}")

    # newest filings first; parse only the unseen ones, capped
    ptrs.sort(key=lambda p: p.get("filing_date", ""), reverse=True)
    parsed_count = 0
    for ptr in ptrs:
        doc_id = ptr["doc_id"]
        already = doc_id in seen
        if already:
            continue
        if parsed_count >= max_ptrs:
            flags.append("house_ptr_cap_reached")
            break
        parsed_count += 1
        rows = parse_house_ptr(doc_id, ptr["year"])
        if mark_seen:
            seen[doc_id] = ptr["filing_date"]
        for tr in rows:
            if tr["type"] not in ("buy", "sale"):
                continue
            if tr["amount_low"] < min_amount:
                continue
            tk = tr["ticker"]
            if uni is not None and tk not in uni:
                continue
            fresh.append({
                "ticker": tk,
                "politician": ptr["name"],
                "chamber": "house",
                "type": tr["type"],
                "amount_low": tr["amount_low"],
                "amount_high": tr["amount_high"],
                "amount_str": tr["amount_str"],
                "asset": tr.get("asset", ""),
                "transaction_date": tr.get("transaction_date"),
                "disclosure_date": ptr["filing_date"],
                "doc_url": _HOUSE_PTR.format(year=ptr["year"], doc_id=doc_id),
                "high_signal": _is_high_signal(ptr["name"]),
            })

    # ---- Senate (best-effort) ----------------------------------------------
    try:
        sen, sflags = recent_senate_trades(since_days=days_back)
        flags += sflags
        for tr in sen:
            if tr["type"] not in ("buy", "sale") or tr["amount_low"] < min_amount:
                continue
            tk = tr["ticker"]
            if uni is not None and tk not in uni:
                continue
            key = f"S:{tk}:{tr.get('transaction_date')}:{tr.get('name')}"
            if key in seen:
                continue
            if mark_seen:
                seen[key] = tr.get("filing_date") or _today().isoformat()
            fresh.append({
                "ticker": tk, "politician": tr.get("name", ""), "chamber": "senate",
                "type": tr["type"], "amount_low": tr["amount_low"],
                "amount_high": tr["amount_high"], "amount_str": tr["amount_str"],
                "asset": tr.get("asset", ""), "transaction_date": tr.get("transaction_date"),
                "disclosure_date": tr.get("filing_date", ""), "doc_url": "",
                "high_signal": _is_high_signal(tr.get("name", "")),
            })
    except Exception as e:
        flags.append(f"senate_error:{type(e).__name__}")

    if mark_seen:
        # keep the seen-doc memory from growing without bound
        if len(seen) > 8000:
            seen = dict(list(seen.items())[-6000:])
        _save_seen(seen)

    # high-signal names first, then by amount
    fresh.sort(key=lambda t: (t["high_signal"], t["amount_low"]), reverse=True)
    by_ticker = {}
    for t in fresh:
        by_ticker.setdefault(t["ticker"], []).append(t)

    # persist a recent flat list for the dashboard / debugging (best-effort)
    try:
        with open(_dir("trades.json"), "w") as f:
            json.dump({"generated": _today().isoformat(), "trades": fresh[:300]}, f, indent=2)
    except Exception:
        pass

    return {"by_ticker": by_ticker, "trades": fresh, "flags": flags, "scanned": parsed_count}


def summarize_trades(trades):
    """One-line human summary of a name's congressional trades (for prompts/notes)."""
    if not trades:
        return ""
    bits = []
    for t in trades[:4]:
        verb = {"buy": "bought", "sale": "sold"}.get(t["type"], t["type"])
        when = t.get("transaction_date") or t.get("disclosure_date") or ""
        sig = " ★" if t.get("high_signal") else ""
        bits.append(f"{t.get('politician','?')}{sig} {verb} {t['amount_str']} on {when}")
    extra = f" (+{len(trades)-4} more)" if len(trades) > 4 else ""
    return "; ".join(bits) + extra
