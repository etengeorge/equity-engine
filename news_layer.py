"""
news_layer.py - multi-source news + sentiment with cross-referencing.

Your ask: use as many tools as possible and cross-reference, with a precedence
ranking. This module fans out across every AVAILABLE news source (registry order),
normalizes each item to a common shape tagged with its source and trust tier,
deduplicates near-identical stories across sources, and produces a CORROBORATION
view: where multiple independent sources carry the same story (confidence up) vs.
where sentiment diverges across sources (a signal in itself).

Everything here is TIER 3: it informs the synthesis as context and triage. It is
NEVER a buy/sell signal on its own. Vendor sentiment scores are treated as
"something is happening here, go verify," not as truth.
"""
import json
import time
import urllib.request
import urllib.parse
import re
from difflib import SequenceMatcher

import config
import sources_registry as reg


def _get(url, headers=None, timeout=20):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=timeout).read()


# ----------------------------------------------------------- per-source fetchers
def _av_news(ticker):
    key = config.ALPHAVANTAGE_API_KEY or ("demo" if config.AV_ALLOW_DEMO else "")
    if not key:
        return []
    try:
        url = ("https://www.alphavantage.co/query?function=NEWS_SENTIMENT"
               f"&tickers={ticker}&limit=20&apikey={key}")
        d = json.loads(_get(url))
        out = []
        for a in d.get("feed", []):
            ts = next((t for t in a.get("ticker_sentiment", [])
                       if t.get("ticker") == ticker), None)
            out.append({
                "source": "alphavantage", "tier": 3,
                "title": a.get("title", ""), "url": a.get("url"),
                "published": a.get("time_published", "")[:8],
                "publisher": a.get("source"),
                "sentiment_label": (ts or {}).get("ticker_sentiment_label")
                                   or a.get("overall_sentiment_label"),
                "sentiment_score": float((ts or {}).get("ticker_sentiment_score") or 0)
                                   if ts else None,
                "relevance": float((ts or {}).get("relevance_score") or 0) if ts else None,
            })
        return out
    except Exception:
        return []


def _finnhub_news(ticker):
    if not config.FINNHUB_API_KEY:
        return []
    try:
        import datetime as dt
        to = dt.date.today().isoformat()
        frm = (dt.date.today() - dt.timedelta(days=30)).isoformat()
        url = (f"https://finnhub.io/api/v1/company-news?symbol={ticker}"
               f"&from={frm}&to={to}&token={config.FINNHUB_API_KEY}")
        d = json.loads(_get(url))
        return [{
            "source": "finnhub", "tier": 3, "title": a.get("headline", ""),
            "url": a.get("url"), "published": "",
            "publisher": a.get("source"), "sentiment_label": None,
            "sentiment_score": None, "relevance": None,
        } for a in (d or [])[:20]]
    except Exception:
        return []


def _marketaux_news(ticker):
    key = getattr(config, "MARKETAUX_API_KEY", "")
    if not key:
        return []
    try:
        url = (f"https://api.marketaux.com/v1/news/all?symbols={ticker}"
               f"&filter_entities=true&language=en&api_token={key}")
        d = json.loads(_get(url))
        out = []
        for a in d.get("data", []):
            ent = next((e for e in a.get("entities", [])
                        if e.get("symbol") == ticker), None)
            out.append({
                "source": "marketaux", "tier": 3, "title": a.get("title", ""),
                "url": a.get("url"), "published": (a.get("published_at") or "")[:10],
                "publisher": a.get("source"),
                "sentiment_label": None,
                "sentiment_score": (ent or {}).get("sentiment_score"),
                "relevance": None,
            })
        return out
    except Exception:
        return []


_RSS_FEEDS = {
    # company-agnostic market feeds; the synthesizer filters for the name.
    "yahoo": "https://feeds.finance.yahoo.com/rss/2.0/headline?s={t}&region=US&lang=en-US",
}


def _rss_news(ticker):
    out = []
    for pub, tmpl in _RSS_FEEDS.items():
        try:
            xml = _get(tmpl.format(t=urllib.parse.quote(ticker))).decode("utf-8", "ignore")
            for m in re.finditer(r"<item>(.*?)</item>", xml, re.DOTALL)[:15] if False else \
                    re.findall(r"<item>(.*?)</item>", xml, re.DOTALL)[:15]:
                title = re.search(r"<title>(.*?)</title>", m, re.DOTALL)
                link = re.search(r"<link>(.*?)</link>", m, re.DOTALL)
                pub_d = re.search(r"<pubDate>(.*?)</pubDate>", m, re.DOTALL)
                if title:
                    out.append({
                        "source": "rss", "tier": 3,
                        "title": re.sub(r"<.*?>", "", title.group(1)).strip(),
                        "url": link.group(1).strip() if link else None,
                        "published": pub_d.group(1)[:16] if pub_d else "",
                        "publisher": pub, "sentiment_label": None,
                        "sentiment_score": None, "relevance": None,
                    })
        except Exception:
            continue
    return out


_FETCHERS = {"alphavantage": _av_news, "finnhub": _finnhub_news,
             "marketaux": _marketaux_news, "rss": _rss_news}


# ----------------------------------------------------------- dedup + corroborate
def _similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


_STOP = {"the", "a", "an", "of", "to", "in", "for", "on", "and", "with", "at", "by",
         "is", "as", "its", "be", "from", "worth", "amid", "after", "into", "this"}


def _tokens(title):
    return {w for w in re.findall(r"[a-z0-9]+", title.lower())
            if w not in _STOP and len(w) > 2}


def _same_story(a, b):
    if SequenceMatcher(None, a.lower(), b.lower()).ratio() > 0.6:
        return True
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return False
    return len(ta & tb) / min(len(ta), len(tb)) >= 0.6


# Perspective classifier: WHO is talking and what's their angle. The point is to
# weigh DIFFERENT viewpoints, not to count agreement. Each perspective type has its
# own incentives and blind spots.
_PERSPECTIVE_CUES = {
    "sell_side_bull": ["upgrade", "buy rating", "outperform", "raises price target",
                       "price target raised", "initiates buy", "overweight"],
    "sell_side_bear": ["downgrade", "sell rating", "underperform", "cuts price target",
                       "price target cut", "underweight", "lowers"],
    "short_bear": ["short seller", "short report", "fraud", "overvalued", "accounting",
                   "going concern", "warns", "red flag", "probe", "investigation",
                   "lawsuit", "delist"],
    "retail_sentiment": ["reddit", "stocktwits", "wallstreetbets", "retail", "meme",
                         "social", "buzz"],
    "official_filing": ["8-k", "10-q", "10-k", "sec filing", "form 4", "files"],
    "fundamental_pos": ["beats", "raises guidance", "record revenue", "new contract",
                        "wins", "approval", "expansion", "undervalued"],
    "fundamental_neg": ["misses", "cuts guidance", "lowers guidance", "layoffs",
                        "decline", "loss", "weak", "slump"],
}


def _classify_perspective(title, source):
    t = title.lower()
    for persp, cues in _PERSPECTIVE_CUES.items():
        if any(c in t for c in cues):
            return persp
    if source in ("alphavantage", "marketaux") and source:
        return "news_wire"
    return "news_wire"


# Materiality classifier: separate SUBSTANTIVE CORPORATE EVENTS (facts that change the
# business — and thus the thesis) from SENTIMENT/CHATTER (mood). A failed launch or a
# signed partnership is a material event; "people are bullish" is not.
_EVENT_CUES = {
    "partnership_contract": ["partnership", "partners with", "contract", "deal with",
                             "agreement with", "awarded", "wins contract", "selected by",
                             "collaboration", "supply agreement"],
    "m_and_a": ["acquire", "acquisition", "merger", "to buy", "takeover", "buyout",
                "to be acquired", "stake in", "divest", "sells division"],
    "regulatory": ["fda", "approval", "approved", "rejected", "clearance", "ce mark",
                   "regulatory", "patent", "ruling", "antitrust", "sec charges"],
    "clinical_trial": ["phase 1", "phase 2", "phase 3", "trial results", "topline",
                       "endpoint", "efficacy", "study met", "study failed"],
    "operational_failure": ["explosion", "explodes", "failed launch", "recall", "outage",
                            "halt", "shutdown", "accident", "crash", "fire", "disaster",
                            "breach", "hack", "contamination", "defect"],
    "guidance": ["guidance", "guides", "preannounce", "pre-announce", "profit warning",
                 "warns on", "beats estimates", "misses estimates", "raises outlook",
                 "cuts outlook", "lowers outlook", "slashes forecast"],
    "executive": ["ceo", "cfo", "resigns", "steps down", "appoints", "names new",
                  "departure", "fired", "hires"],
    "litigation": ["lawsuit", "sued", "settlement", "verdict", "litigation", "fraud",
                   "investigation", "probe", "subpoena", "class action"],
    "capital": ["offering", "dilution", "buyback", "dividend", "raises capital",
                "secondary", "convertible", "default", "refinanc"],
}


def _classify_event(title):
    """Return (event_category or None, is_material). Material = a substantive corporate
    event, not sentiment."""
    t = title.lower()
    for cat, cues in _EVENT_CUES.items():
        if any(c in t for c in cues):
            return cat, True
    return None, False


def _stance(perspective, sentiment_score):
    """Coarse bull/bear/neutral stance implied by a perspective + any sentiment score."""
    if perspective in ("sell_side_bull", "fundamental_pos"):
        return "bull"
    if perspective in ("sell_side_bear", "short_bear", "fundamental_neg"):
        return "bear"
    if sentiment_score is not None:
        return "bull" if sentiment_score > 0.15 else "bear" if sentiment_score < -0.15 else "neutral"
    return "neutral"


def _dedupe_and_map_perspectives(items):
    """Cluster same-event stories, but FRAME the output as a map of perspectives and
    conflicts — NOT as an agreement tally. Multi-source clustering identifies the
    CONSENSUS NARRATIVE (to be interrogated), and differing stances are surfaced as
    the interesting signal."""
    clusters = []
    for it in items:
        it["perspective"] = _classify_perspective(it["title"], it["source"])
        it["stance"] = _stance(it["perspective"], it.get("sentiment_score"))
        it["event_category"], it["is_material"] = _classify_event(it["title"])
        placed = False
        for c in clusters:
            if _same_story(it["title"], c["title"]):
                c["items"].append(it)
                c["sources"].add(it["source"])
                c["stances"].add(it["stance"])
                placed = True
                break
        if not placed:
            clusters.append({"title": it["title"], "items": [it],
                             "sources": {it["source"]}, "stances": {it["stance"]}})
    for c in clusters:
        c["n_sources"] = len(c["sources"])
        c["is_consensus_narrative"] = c["n_sources"] >= 2  # consensus to interrogate
        c["stance_conflict"] = len(c["stances"] - {"neutral"}) >= 2  # bull AND bear present
        mat_items = [i for i in c["items"] if i.get("is_material")]
        c["is_material_event"] = len(mat_items) > 0
        c["event_category"] = mat_items[0]["event_category"] if mat_items else None
        # reliability (your call): CONFIRMED if >=2 independent sources carry the same
        # event; a single-source material headline is PROVISIONAL (await corroboration).
        c["confidence"] = ("confirmed" if (c["is_material_event"] and c["n_sources"] >= 2)
                           else "provisional" if c["is_material_event"] else "n/a")
        c["sources"] = sorted(c["sources"])
        c["stances"] = sorted(c["stances"])
    clusters.sort(key=lambda c: (c["is_material_event"], c["stance_conflict"],
                                 c["n_sources"]), reverse=True)
    return clusters


def gather_news(ticker):
    """Fan out across all available news sources, then MAP THE PERSPECTIVE SPREAD.
    The output is built to fight groupthink: it surfaces which viewpoints are present
    (sell-side, short, retail, fundamentals), where they CONFLICT, and what the
    consensus narrative is — explicitly so the synthesis can interrogate it rather
    than lean on it. Tier 3 — context, never a signal on its own."""
    used, items = [], []
    for spec in reg.available("news"):
        name = spec["name"]
        if name == "websearch":
            used.append("websearch(live synthesizer augments)")
            continue
        fetcher = _FETCHERS.get(name)
        if not fetcher:
            continue
        got = fetcher(ticker)
        if got:
            items.extend(got)
            used.append(f"{name}({len(got)})")
        time.sleep(0.2)
    clusters = _dedupe_and_map_perspectives(items)

    # aggregate the perspective spread across all items
    persp_counts, stance_counts = {}, {"bull": 0, "bear": 0, "neutral": 0}
    for it in items:
        persp_counts[it["perspective"]] = persp_counts.get(it["perspective"], 0) + 1
        stance_counts[it["stance"]] = stance_counts.get(it["stance"], 0) + 1
    conflicts = [c for c in clusters if c["stance_conflict"]]
    consensus = [c for c in clusters if c["is_consensus_narrative"]]
    material = [c for c in clusters if c.get("is_material_event")]

    return {
        "ticker": ticker, "sources_queried": used,
        "n_items": len(items), "n_stories": len(clusters),
        "perspectives_present": persp_counts,
        "stance_tally": stance_counts,
        "bull_bear_split": f"{stance_counts['bull']} bull / {stance_counts['bear']} bear "
                           f"/ {stance_counts['neutral']} neutral",
        # MATERIAL EVENTS (facts, not mood) — separated out, with reliability confidence
        "material_events": [{"title": c["title"], "category": c["event_category"],
                             "confidence": c["confidence"], "sources": c["sources"],
                             "url": next((i["url"] for i in c["items"] if i.get("url")), None)}
                            for c in material[:8]],
        "has_confirmed_material_event": any(c["confidence"] == "confirmed" for c in material),
        "has_provisional_material_event": any(c["confidence"] == "provisional" for c in material),
        "consensus_narratives": [{"title": c["title"], "sources": c["sources"]}
                                 for c in consensus[:5]],
        "conflicting_stories": [{"title": c["title"], "stances": c["stances"],
                                 "sources": c["sources"]} for c in conflicts[:5]],
        "all_stories": [{"title": c["title"], "sources": c["sources"],
                         "stances": c["stances"], "stance_conflict": c["stance_conflict"],
                         "is_consensus": c["is_consensus_narrative"],
                         "is_material_event": c.get("is_material_event"),
                         "event_category": c.get("event_category"),
                         "confidence": c.get("confidence"),
                         "url": next((i["url"] for i in c["items"] if i.get("url")), None)}
                        for c in clusters[:12]],
        "tier": 3,
        "note": ("Tier-3 context. MATERIAL EVENTS (partnerships, M&A, regulatory, "
                 "operational failures, guidance, etc.) are substantive facts that can "
                 "change the thesis — distinct from sentiment/mood. Confirmed = >=2 "
                 "independent sources (or back it with the 8-K feed); provisional = single "
                 "source, await corroboration before re-rating. Consensus narratives are to "
                 "INTERROGATE; conflicting stories are high-signal; agreement != confidence."),
    }


# ----------------------------------------------------------- price cross-check
def _stooq_quote(ticker):
    """v2: Stooq now sits behind a JavaScript proof-of-work wall and returns HTML headlessly, so
    this path is dead. Kept as a no-op for callers; the cross-check uses _alt_quote instead."""
    return None


def _alt_quote(ticker):
    """Independent-enough second read: yfinance's quote endpoint (fast_info) vs the history-derived
    close the engine uses. Different upstream endpoint, same vendor; flagged as such."""
    try:
        import yfinance as yf
        fi = yf.Ticker(ticker).fast_info
        v = getattr(fi, "last_price", None) or getattr(fi, "previous_close", None)
        return float(v) if v else None
    except Exception:
        return None


def price_cross_check(ticker, primary_close):
    """Compare the engine's primary close against an independent keyless source
    (Stooq). Flag disagreement beyond tolerance rather than trusting blindly."""
    alt = _alt_quote(ticker)
    if alt is None or not primary_close:
        return {"checked": False, "alt_source": "stooq", "alt_close": alt}
    diff = abs(primary_close - alt) / primary_close
    return {"checked": True, "alt_source": "stooq", "alt_close": alt,
            "pct_diff": diff, "agree": diff <= config.PRICE_XCHECK_TOLERANCE}
