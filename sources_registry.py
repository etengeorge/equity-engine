"""
sources_registry.py - the control center for multi-source cross-referencing.

Every external source is declared here with: its ROLE (price / fundamentals / news /
sentiment / macro), its TRUST TIER, a PRECEDENCE rank (lower = tried first), and
whether it needs a key. The engine fans out across all available sources for a role,
then cross-references — corroboration raises confidence, disagreement is flagged.

TRUST TIERS (the firewall from earlier in the design):
  1 = official structured data you ACT ON         (EDGAR, FRED)
  2 = market-data vendors, used with cross-check   (Tiingo, Stooq, Polygon, yfinance)
  3 = news/sentiment — VERIFY, never act directly  (AlphaVantage, Finnhub, Marketaux, RSS)

PRECEDENCE: for a given role, sources are ranked. The top available one is primary;
the rest are cross-checks. "Available" = keyless OR key present in env.

This file holds NO secrets — it reads key presence from config (which reads env).
"""
import config

# role -> ordered list of source specs. Order = precedence (best first).
REGISTRY = {
    "price": [
        {"name": "tiingo",   "tier": 2, "needs_key": True,
         "key": bool(config.TIINGO_API_KEY), "role": "price",
         "note": "maintained API, adjusted closes; recommended primary"},
        {"name": "polygon",  "tier": 2, "needs_key": True,
         "key": bool(getattr(config, "POLYGON_API_KEY", "")), "role": "price",
         "note": "strong market data, free tier (prices only)"},
        {"name": "stooq",    "tier": 2, "needs_key": False, "key": True,
         "role": "price", "note": "keyless light quote; cross-check only"},
        {"name": "yfinance", "tier": 2, "needs_key": False, "key": True,
         "role": "price", "note": "keyless but flaky; last-resort fallback"},
    ],
    "fundamentals": [
        {"name": "edgar_xbrl", "tier": 1, "needs_key": False, "key": True,
         "role": "fundamentals", "note": "SOURCE OF TRUTH for any reported number"},
        {"name": "finnhub",    "tier": 2, "needs_key": True,
         "key": bool(config.FINNHUB_API_KEY), "role": "fundamentals",
         "note": "cross-check / fills estimates where they exist"},
        {"name": "alphavantage", "tier": 2, "needs_key": True,
         "key": bool(config.ALPHAVANTAGE_API_KEY), "role": "fundamentals",
         "note": "cross-check"},
    ],
    "news": [
        {"name": "alphavantage", "tier": 3, "needs_key": True,
         "key": bool(config.ALPHAVANTAGE_API_KEY or config.AV_ALLOW_DEMO),
         "role": "news", "note": "news + per-ticker sentiment; demo key works for some names"},
        {"name": "finnhub",      "tier": 3, "needs_key": True,
         "key": bool(config.FINNHUB_API_KEY), "role": "news",
         "note": "company news feed"},
        {"name": "marketaux",    "tier": 3, "needs_key": True,
         "key": bool(getattr(config, "MARKETAUX_API_KEY", "")), "role": "news",
         "note": "news aggregator with sentiment"},
        {"name": "rss",          "tier": 3, "needs_key": False, "key": True,
         "role": "news", "note": "Reuters/CNBC/MarketWatch/Yahoo free RSS; always available"},
        {"name": "websearch",    "tier": 3, "needs_key": False, "key": True,
         "role": "news", "note": "live synthesizer augments via its own web_search"},
    ],
    "macro": [
        {"name": "fred", "tier": 1, "needs_key": True, "key": bool(config.FRED_API_KEY),
         "role": "macro", "note": "risk-free rate, sentiment indices; falls back to config"},
    ],
}


def available(role):
    """Sources for a role that can actually run now (keyless or key present), in
    precedence order."""
    return [s for s in REGISTRY.get(role, []) if s["key"]]


def primary(role):
    av = available(role)
    return av[0] if av else None


def cross_check_sources(role):
    """Everything after the primary — used to corroborate / flag disagreement."""
    return available(role)[1:]


def registry_report():
    """Human-readable status: what's live, what's dormant (needs a key)."""
    lines = []
    for role, specs in REGISTRY.items():
        lines.append(f"[{role}]")
        for s in specs:
            status = "LIVE" if s["key"] else f"dormant (set {s['name']} key)"
            lines.append(f"  tier{s['tier']} {s['name']:14} {status:28} {s['note']}")
    return "\n".join(lines)
