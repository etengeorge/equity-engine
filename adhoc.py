"""On-demand fetching for the analyst runtime, which has no internet.

The two halves of this engine run in different places. The Action runner can reach the
SEC and Yahoo; the Claude session that does the reasoning cannot reach anything except
web search. On 2026-08-31 that gap capped every one of ten verdicts at low conviction
with the same sentence — "I could not open the primary filing" — while three names had
their entire valuation invalidated by a document sitting on EDGAR.

This module is the bridge. The analyst dispatches the `adhoc-fetch` workflow, a runner
with real network access executes what is below, commits the result, and the analyst
pulls it. Round trip is about ninety seconds.

Nothing here does judgment. It retrieves documents and writes them down.
"""
import datetime as dt, html, json, re, sys
import config

OUT = config.DATA / "adhoc"
MAX_DOC_CHARS = 400_000        # a 10-K runs to megabytes of HTML; keep the repo sane
RETENTION_DAYS = 14            # pulled documents are working material, not memory


# --- html -> readable text ----------------------------------------------------
_DROP = re.compile(r"<(script|style|head)[^>]*>.*?</\1>", re.S | re.I)
_BLOCK = re.compile(r"</?(p|div|tr|br|h[1-6]|li|table|section)[^>]*>", re.I)
_TAG = re.compile(r"<[^>]+>")


def to_text(raw):
    """Strip a filing down to something readable without pulling in a parser.

    Deliberately crude: filings are structurally simple and the analyst needs the words,
    not the layout. Table cells collapse onto lines, which is imperfect for a balance
    sheet but keeps the numbers adjacent to their labels.
    """
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8", "replace")
    s = _DROP.sub(" ", raw)
    s = _BLOCK.sub("\n", s)
    s = _TAG.sub(" ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    s = re.sub(r"\n\s*\n\s*\n+", "\n\n", s)
    return s.strip()


def _write(ticker, name, text, meta):
    d = OUT / ticker.upper()
    d.mkdir(parents=True, exist_ok=True)
    truncated = len(text) > MAX_DOC_CHARS
    if truncated:
        text = text[:MAX_DOC_CHARS] + (
            f"\n\n[TRUNCATED at {MAX_DOC_CHARS:,} characters — "
            f"the full document is at {meta.get('url','the source URL')}]")
    (d / name).write_text(text)
    meta = {**meta, "file": name, "chars": len(text), "truncated": truncated}
    return meta


def _safe(s, ext=".txt"):
    return re.sub(r"[^A-Za-z0-9._-]+", "-", str(s)).strip("-")[:80] + ext


# --- what can be fetched ------------------------------------------------------
def fetch_filings(ticker, days_back=180, max_docs=8):
    """Recent 10-K / 10-Q / 8-K primary documents plus their EX-99 exhibits, as text.

    This is the one that matters most. Every 'I could not read the 10-Q' in a research
    note is this function not having been called.
    """
    import edgar
    cik = edgar.cik_for(ticker)
    if cik is None:
        return {"ticker": ticker, "error": "no CIK for ticker"}
    got, seen = [], set()
    for f in edgar.recent_filings(cik, forms=("10-K", "10-Q", "8-K"), limit=max_docs):
        if f["url"] in seen:
            continue
        seen.add(f["url"])
        try:
            body = edgar._get(f["url"])
        except Exception as e:
            got.append({"form": f["form"], "filed": f["filed"], "url": f["url"],
                        "error": f"{type(e).__name__}"})
            continue
        got.append(_write(ticker, _safe(f"{f['filed']}-{f['form']}-{f['doc']}"),
                          to_text(body),
                          {"form": f["form"], "filed": f["filed"],
                           "items": f.get("items"), "url": f["url"]}))
        if len(got) >= max_docs:
            break
    try:
        for e in edgar.exhibits_for(cik, days_back=days_back)[:6]:
            if e["url"] in seen or e["url"].lower().endswith(".pdf"):
                # PDFs are left as links: they are usually the slide deck, and this
                # module has no PDF parser. The URL is what the analyst needs.
                got.append({**e, "note": "PDF not converted — open the URL"})
                continue
            seen.add(e["url"])
            got.append(_write(ticker, _safe(f"{e['filed']}-{e['exhibit']}"),
                              to_text(edgar._get(e["url"])), e))
    except Exception as e:
        got.append({"error": f"exhibits: {type(e).__name__}"})
    return {"ticker": ticker, "cik": cik, "documents": got}


def fetch_news(ticker, count=40):
    """Everything Yahoo will give for one name — deeper than the daily sweep's 10."""
    import news
    try:
        arts = news.yf_news(ticker, count=count, tab="all")
    except Exception as e:
        return {"ticker": ticker, "error": f"{type(e).__name__}: {e}"}
    news.append("companies", ticker.upper(), arts)
    return {"ticker": ticker, "articles": len(arts), "items": arts}


def fetch_url(ticker, url):
    """One arbitrary page. For an investor-relations deck, a transcript, a regulator's
    notice — anything the analyst found a link to but cannot open."""
    import urllib.request
    req = urllib.request.Request(url, headers={
        "User-Agent": config.SEC_USER_AGENT or "equity-engine",
        "Accept": "text/html,application/xhtml+xml,application/pdf,*/*",
    })
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read()
            ctype = r.headers.get("Content-Type", "")
    except Exception as e:
        return {"url": url, "error": f"{type(e).__name__}: {e}"}
    if "pdf" in ctype.lower() or url.lower().endswith(".pdf"):
        d = OUT / ticker.upper()
        d.mkdir(parents=True, exist_ok=True)
        name = _safe(url.rsplit("/", 1)[-1], ".pdf")
        (d / name).write_bytes(raw)
        return {"url": url, "file": name, "bytes": len(raw),
                "note": "PDF saved verbatim — this module does not extract PDF text"}
    return _write(ticker, _safe(url.rsplit("/", 1)[-1] or "page"), to_text(raw),
                  {"url": url, "content_type": ctype})


def prune(retention=RETENTION_DAYS, log=print):
    """Ad-hoc pulls are scratch, not memory. Anything the analyst wanted to keep is
    quoted in the research note; the raw documents age out so the repo does not."""
    if not OUT.exists():
        return 0
    cutoff = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=retention))
    removed = 0
    for d in OUT.iterdir():
        if not d.is_dir():
            continue
        idx = d / "index.json"
        try:
            when = dt.datetime.fromisoformat(json.loads(idx.read_text())["fetched_utc"])
        except Exception:
            continue
        if when < cutoff:
            for f in d.iterdir():
                f.unlink()
            d.rmdir()
            removed += 1
    if removed:
        log(f"[adhoc] pruned {removed} expired pulls")
    return removed


def run(tickers, what="filings", url=None, log=print):
    OUT.mkdir(parents=True, exist_ok=True)
    results = {}
    for t in [x.strip().upper() for x in tickers if x.strip()]:
        res = {"fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
               "requested": what}
        if what in ("filings", "all"):
            log(f"[adhoc] {t}: filings")
            res["filings"] = fetch_filings(t)
        if what in ("news", "all"):
            log(f"[adhoc] {t}: news")
            res["news"] = fetch_news(t)
        if what == "url" and url:
            log(f"[adhoc] {t}: {url}")
            res["url"] = fetch_url(t, url)
        d = OUT / t
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.json").write_text(json.dumps(res, indent=2, default=str))
        results[t] = res
        log(f"[adhoc] {t}: wrote {len(list(d.iterdir()))} files to {d}")
    return results


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tickers", required=True, help="comma-separated")
    ap.add_argument("--what", default="filings",
                    choices=["filings", "news", "url", "all"])
    ap.add_argument("--url", default=None)
    a = ap.parse_args()
    out = run(a.tickers.split(","), a.what, a.url)
    if not out:
        sys.exit("no tickers requested")
    prune()
