"""The news layer: what happened, organized so the analyst can find it.

Three independent sources, because no single free feed covers a 1,956-name small-cap
index. Each one answers a different question and each degrades on its own without
taking the run down with it:

  COMPANY   yfinance, one request per ticker. Answers "what happened to THIS name".
            There is no bulk form, so this is the expensive source and it is spent
            only on names that already look interesting -- see `candidates()`.

  SECTOR    the eleven SPDR sector ETFs, whose holdings map 1:1 onto the GICS sectors
            in universe.csv, plus the Russell 2000 and the VIX. Eleven requests buy
            sector-level news for the entire universe, including for the ~1,500 names
            that never get a company pull. This is the cheapest information in the
            whole engine per request.

  MACRO     free government RSS/JSON with no API key: the Fed, the SEC, the BLS, and
            the Federal Register. These are the events that move a whole cohort at
            once -- a rate decision, a CPI print, a rule change in an agency that
            regulates a sector -- and they are the ones a price screen cannot see.

Everything is normalized to one article shape and deduped by a stable id, so the store
grows by genuinely new items rather than by re-recording the same wire story every day.
"""
import datetime as dt, json, re, time, urllib.error, urllib.request
import xml.etree.ElementTree as ET
import config

STORE = config.DATA / "news"
RETENTION_DAYS = 120          # 90-day lookback plus a month of margin


# --- the eleven sector ETFs, mapped onto universe.csv's GICS sector strings ----
# These are holdings-based proxies, not opinions: XLV's news IS health-care news.
SECTOR_ETF = {
    "Health Care": "XLV",
    "Financials": "XLF",
    "Industrials": "XLI",
    "Information Technology": "XLK",
    "Consumer Discretionary": "XLY",
    "Energy": "XLE",
    "Real Estate": "XLRE",
    "Materials": "XLB",
    "Communication": "XLC",
    "Consumer Staples": "XLP",
    "Utilities": "XLU",
}

# The tape's own context. ^RUT is the universe itself; ^VIX is whether the market is
# calm or not, which changes how much a 10% single-name move actually means.
MARKET_SYMBOLS = {"^RUT": "Russell 2000", "^GSPC": "S&P 500", "^VIX": "Volatility"}

# Free, keyless, and primary. A dead feed logs a warning and is skipped -- news
# sources change their URLs and that must never fail a run that also does the screen.
MACRO_FEEDS = [
    ("federal_reserve", "https://www.federalreserve.gov/feeds/press_all.xml"),
    ("sec", "https://www.sec.gov/news/pressreleases.rss"),
    ("bls", "https://www.bls.gov/feed/bls_latest.rss"),
]
# Federal Register is a JSON API rather than RSS, and it is the one that catches
# regulation aimed at a specific industry (FDA, EPA, FERC, Commerce/tariffs).
FEDERAL_REGISTER = (
    "https://www.federalregister.gov/api/v1/documents.json"
    "?per_page=40&order=newest"
    "&fields[]=title&fields[]=publication_date&fields[]=html_url"
    "&fields[]=agencies&fields[]=type"
    "&conditions[type][]=RULE&conditions[type][]=PRORULE"
)


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")


def _now():
    return dt.datetime.now(dt.timezone.utc)


def _iso(ts):
    """Coerce whatever a source hands back into an ISO-8601 UTC string, or None.
    Yahoo has used both epoch seconds and ISO strings for publish time across versions."""
    if ts is None or ts == "":
        return None
    if isinstance(ts, (int, float)):
        try:
            return dt.datetime.fromtimestamp(ts, dt.timezone.utc).isoformat(timespec="seconds")
        except (ValueError, OSError, OverflowError):
            return None
    s = str(ts).strip().replace("Z", "+00:00")
    for parse in (dt.datetime.fromisoformat,
                  lambda x: dt.datetime.strptime(x, "%a, %d %b %Y %H:%M:%S %z"),
                  lambda x: dt.datetime.strptime(x, "%Y-%m-%d")):
        try:
            d = parse(s)
            if d.tzinfo is None:
                d = d.replace(tzinfo=dt.timezone.utc)
            return d.astimezone(dt.timezone.utc).isoformat(timespec="seconds")
        except (ValueError, TypeError):
            continue
    return None


def _age_days(iso):
    d = _iso(iso)
    if not d:
        return None
    try:
        return (_now() - dt.datetime.fromisoformat(d)).days
    except ValueError:
        return None


# --- normalization -----------------------------------------------------------
def _article(aid, ts, title, summary, publisher, url, tickers, source):
    """One shape for every source. `id` is what dedupes the store, so it must be stable
    across days -- a source's own id when it has one, otherwise a hash of the URL."""
    title = (title or "").strip()
    if not title:
        return None
    if not aid:
        aid = str(abs(hash(url or title)))
    return {"id": str(aid), "ts": _iso(ts), "title": title[:400],
            "summary": re.sub(r"\s+", " ", (summary or ""))[:900].strip(),
            "publisher": (publisher or "")[:120], "url": url or "",
            "tickers": sorted({t for t in (tickers or []) if t}), "source": source}


def _from_yf(raw, fallback_tickers=()):
    """yfinance has shipped two different news payloads. 0.2.x returned a flat dict with
    `uuid`/`link`/`providerPublishTime`; 1.x nests almost everything under `content`.
    Handle both rather than pinning a version -- the Action installs from a range."""
    if not isinstance(raw, dict):
        return None
    c = raw.get("content") if isinstance(raw.get("content"), dict) else raw
    prov = c.get("provider")
    publisher = prov.get("displayName") if isinstance(prov, dict) else (
        c.get("publisher") or raw.get("publisher"))
    url = ""
    for key in ("canonicalUrl", "clickThroughUrl"):
        v = c.get(key)
        if isinstance(v, dict) and v.get("url"):
            url = v["url"]
            break
    url = url or c.get("link") or raw.get("link") or ""
    rel = raw.get("relatedTickers") or c.get("relatedTickers") or []
    if isinstance(rel, str):
        rel = [rel]
    return _article(
        aid=raw.get("id") or raw.get("uuid") or c.get("id"),
        ts=c.get("pubDate") or c.get("displayTime") or raw.get("providerPublishTime"),
        title=c.get("title") or raw.get("title"),
        summary=c.get("summary") or c.get("description") or "",
        publisher=publisher, url=url,
        tickers=list(rel) + list(fallback_tickers), source="yfinance")


# --- source 1: per-company, via yfinance -------------------------------------
def yf_news(symbol, count=10, tab="all"):
    """One ticker. Raises on failure so the caller can decide whether to keep going."""
    import yfinance as yf
    raw = yf.Ticker(symbol).get_news(count=count, tab=tab) or []
    out = []
    for r in raw:
        a = _from_yf(r, fallback_tickers=[symbol] if not symbol.startswith("^") else [])
        if a:
            out.append(a)
    return out


def company_news(tickers, count=10, pause=0.25, budget_s=600, log=print):
    """News for a list of tickers. Yahoo has no bulk news endpoint, so this is one HTTP
    round trip per name -- the reason the caller passes a candidate set, not the universe.

    Never raises. A ticker that throttles or 404s is recorded as a miss and the sweep
    continues: a partial news pull is worth far more than a failed screen.
    """
    out, misses, t0 = {}, [], time.time()
    for i, t in enumerate(tickers, 1):
        if time.time() - t0 > budget_s:
            log(f"[news] budget of {budget_s}s reached at {i}/{len(tickers)} — stopping early")
            break
        try:
            arts = yf_news(t, count=count)
            if arts:
                out[t] = arts
        except Exception as e:
            misses.append(f"{t}:{type(e).__name__}")
        time.sleep(pause)
        if i % 100 == 0:
            log(f"[news]   company {i}/{len(tickers)}  ({time.time()-t0:.0f}s, "
                f"{len(out)} with news)")
    if misses:
        log(f"[news] {len(misses)} company pulls failed (first 5: {misses[:5]})")
    return out


# --- source 2: sector and market, via the SPDR sector ETFs --------------------
def sector_news(count=12, pause=0.25, log=print):
    """Sector-level news for the whole universe in eleven requests.

    This is what covers the ~1,500 names that never earn a company pull. A tariff on
    steel, an FDA panel, a rate move through the banks -- those arrive here whether or
    not any individual small cap made the wire.
    """
    out = {}
    for sector, etf in SECTOR_ETF.items():
        try:
            arts = yf_news(etf, count=count)
            for a in arts:
                a["sector"] = sector
                a["via"] = etf
            if arts:
                out[sector] = arts
        except Exception as e:
            log(f"[news] sector {sector} ({etf}) failed: {type(e).__name__}")
        time.sleep(pause)
    return out


def market_news(count=12, pause=0.25, log=print):
    out = []
    for sym, label in MARKET_SYMBOLS.items():
        try:
            for a in yf_news(sym, count=count):
                a["via"] = label
                out.append(a)
        except Exception as e:
            log(f"[news] market {sym} failed: {type(e).__name__}")
        time.sleep(pause)
    return out


# --- source 3: macro and regulatory, via free government feeds ----------------
def _get(url, timeout=25):
    req = urllib.request.Request(url, headers={
        "User-Agent": config.SEC_USER_AGENT or "equity-engine",
        "Accept": "application/json, application/rss+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _rss(name, url):
    """Minimal RSS/Atom reader. Government feeds are well-formed and stable; the point
    of hand-parsing is to avoid a dependency for four feeds."""
    root = ET.fromstring(_get(url))
    out = []
    # RSS 2.0 <item> and Atom <entry> both, without a namespace map
    for el in root.iter():
        tag = el.tag.rsplit("}", 1)[-1]
        if tag not in ("item", "entry"):
            continue
        get = {}
        for child in el:
            ct = child.tag.rsplit("}", 1)[-1]
            if ct == "link" and not (child.text or "").strip():
                get["link"] = child.attrib.get("href", "")
            else:
                get.setdefault(ct, (child.text or "").strip())
        a = _article(
            aid=get.get("guid") or get.get("id") or get.get("link"),
            ts=get.get("pubDate") or get.get("updated") or get.get("published"),
            title=get.get("title"),
            summary=get.get("description") or get.get("summary") or "",
            publisher=name, url=get.get("link", ""), tickers=[], source=f"rss:{name}")
        if a:
            out.append(a)
    return out


def macro_news(log=print):
    """Rate decisions, economic releases, SEC actions, and proposed or final rules.
    Every one of these is free and keyless. A feed that has moved or died logs a line
    and is skipped -- never a run failure."""
    out = []
    for name, url in MACRO_FEEDS:
        try:
            got = _rss(name, url)
            out += got
            log(f"[news] macro {name}: {len(got)} items")
        except Exception as e:
            log(f"[news] macro {name} unavailable ({type(e).__name__}) — skipped")
    try:
        blob = json.loads(_get(FEDERAL_REGISTER))
        for d in blob.get("results", []):
            agencies = ", ".join(a.get("name", "") for a in (d.get("agencies") or [])[:3])
            a = _article(aid=d.get("html_url"), ts=d.get("publication_date"),
                         title=d.get("title"), summary=agencies,
                         publisher=f"Federal Register ({d.get('type','')})",
                         url=d.get("html_url"), tickers=[], source="federal_register")
            if a:
                out.append(a)
        log(f"[news] macro federal_register: {len(blob.get('results', []))} items")
    except Exception as e:
        log(f"[news] macro federal_register unavailable ({type(e).__name__}) — skipped")
    return out


# --- the store ---------------------------------------------------------------
def _path(kind, key):
    d = STORE / kind
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{_slug(key) if kind == 'sectors' else key}.json"


def append(kind, key, articles, retention=RETENTION_DAYS):
    """Merge new articles into a store file, dedupe by id, drop anything past retention.

    Deduping is what keeps this affordable: the same wire story is returned by Yahoo
    every day it stays on the page, so without an id check the store would grow by the
    full page size daily instead of by what is actually new.
    """
    p = _path(kind, key)
    try:
        existing = json.loads(p.read_text()) if p.exists() else []
    except json.JSONDecodeError:
        existing = []
    by_id = {a.get("id"): a for a in existing if isinstance(a, dict) and a.get("id")}
    added = 0
    for a in articles:
        if a and a.get("id") and a["id"] not in by_id:
            by_id[a["id"]] = a
            added += 1
    keep = [a for a in by_id.values()
            if (_age_days(a.get("ts")) is None or _age_days(a.get("ts")) <= retention)]
    keep.sort(key=lambda a: a.get("ts") or "", reverse=True)
    p.write_text(json.dumps(keep, indent=1))
    return added, len(keep)


def read(kind, key, days=90, limit=None):
    """Articles for one key within a lookback window, newest first.
    This is what the brief builder and the analyst's 90-day question both call."""
    p = _path(kind, key)
    if not p.exists():
        return []
    try:
        arts = json.loads(p.read_text())
    except json.JSONDecodeError:
        return []
    out = [a for a in arts
           if isinstance(a, dict)
           and (_age_days(a.get("ts")) is None or _age_days(a.get("ts")) <= days)]
    out.sort(key=lambda a: a.get("ts") or "", reverse=True)
    return out[:limit] if limit else out


# --- who gets an expensive company pull --------------------------------------
def candidates(rows, always=(), max_names=450):
    """Which tickers earn a per-company news request today.

    Deliberately not the whole universe. A company pull is one HTTP round trip and the
    store has to live in a git repo, so the budget goes where news actually is: names
    that moved, names trading abnormal volume, names that filed an 8-K, and today's
    picks. Everything else is covered by the sector feeds, which cost eleven requests
    for all 1,956 names.

    Volume is in here because it is the one signal that fires BEFORE the story is
    written: a small cap trading five times its normal dollar volume has news whether
    or not a wire has picked it up yet.
    """
    scored, forced = [], set(always)
    for r in rows:
        t = r.get("ticker")
        if not t or t in forced:
            continue
        s = 0.0
        for f, w in (("ret_5d", 1.0), ("ret_21d", 0.5)):
            v = r.get(f)
            if isinstance(v, (int, float)):
                if abs(v) > (0.05 if f == "ret_5d" else 0.15):
                    s += abs(v) * w
        vr = r.get("volume_ratio")
        if isinstance(vr, (int, float)) and vr > 2.0:
            s += min(vr, 6.0) * 0.15
        if r.get("filed_8k"):
            s += 0.30
        if s > 0:
            scored.append((s, t))
    scored.sort(key=lambda x: -x[0])
    room = max(0, max_names - len(forced))
    return list(forced) + [t for _, t in scored[:room]]


# --- the daily pass ----------------------------------------------------------
def run(rows, picks=(), log=print, company_count=10, max_names=450, budget_s=600):
    """Fetch every source, write the store, and return a summary the screen can embed.

    Order matters: sector and macro run FIRST because they are cheap and universally
    useful, so a company sweep that gets throttled halfway still leaves the run with
    complete sector coverage.
    """
    t0 = time.time()
    summary = {"generated_utc": _now().isoformat(timespec="seconds"),
               "sectors": {}, "macro": 0, "market": 0, "companies": 0, "articles_new": 0}

    log("[news] sector feeds (11 ETFs) …")
    sec = sector_news(log=log)
    for sector, arts in sec.items():
        added, total = append("sectors", sector, arts)
        summary["sectors"][sector] = {"new": added, "held": total, "etf": SECTOR_ETF[sector]}
        summary["articles_new"] += added

    log("[news] market context (^RUT, ^GSPC, ^VIX) …")
    mkt = market_news(log=log)
    added, _ = append("market", "market", mkt)
    summary["market"] = len(mkt)
    summary["articles_new"] += added

    log("[news] macro + regulatory feeds …")
    mac = macro_news(log=log)
    added, _ = append("market", "macro", mac)
    summary["macro"] = len(mac)
    summary["articles_new"] += added

    cands = candidates(rows, always=picks, max_names=max_names)
    log(f"[news] company sweep: {len(cands)} candidates "
        f"({len(picks)} forced, {len(cands)-len(picks)} scored in)")
    comp = company_news(cands, count=company_count, budget_s=budget_s, log=log)
    for t, arts in comp.items():
        added, _ = append("companies", t, arts)
        summary["articles_new"] += added
    summary["companies"] = len(comp)
    summary["candidates"] = len(cands)
    summary["elapsed_s"] = round(time.time() - t0, 1)

    (STORE).mkdir(parents=True, exist_ok=True)
    (STORE / "summary.json").write_text(json.dumps(summary, indent=2))
    log(f"[news] done in {summary['elapsed_s']:.0f}s — {summary['articles_new']} new "
        f"articles across {len(sec)} sectors and {summary['companies']} companies")
    return summary


def prune(retention=RETENTION_DAYS, log=print):
    """Drop everything past the retention window. Called by the daily run so the store
    reaches a steady state instead of growing without bound inside a git repository."""
    removed = 0
    for kind in ("companies", "sectors", "market"):
        d = STORE / kind
        if not d.exists():
            continue
        for p in d.glob("*.json"):
            try:
                arts = json.loads(p.read_text())
            except json.JSONDecodeError:
                continue
            keep = [a for a in arts if isinstance(a, dict)
                    and (_age_days(a.get("ts")) is None
                         or _age_days(a.get("ts")) <= retention)]
            if len(keep) != len(arts):
                removed += len(arts) - len(keep)
                if keep:
                    p.write_text(json.dumps(keep, indent=1))
                else:
                    p.unlink()
    if removed:
        log(f"[news] pruned {removed} articles older than {retention}d")
    return removed
