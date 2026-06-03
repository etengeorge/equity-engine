# SOURCES.md — multi-source cross-referencing

You asked for as many tools as possible, cross-referenced, with a precedence
ranking. That's `sources_registry.py` + `news_layer.py`. Here's how it works and
how to light up more sources.

## The model

Every source is declared with a **role**, a **trust tier**, and a **precedence
rank**. For each role the engine fans out across all *available* sources (keyless
or key-present), then cross-references.

| Role | Sources (precedence order) | Tier |
|---|---|---|
| **fundamentals** | EDGAR XBRL → Finnhub → AlphaVantage | 1 → 2 |
| **price** | Tiingo → Polygon → Stooq → yfinance | 2 |
| **news** | AlphaVantage → Finnhub → Marketaux → RSS → web_search | 3 |
| **macro** | FRED (→ config fallback) | 1 |

**Trust tiers (the firewall):**
- **Tier 1** — official structured data you ACT ON (EDGAR, FRED).
- **Tier 2** — market-data vendors, used with cross-check (prices, vendor fundamentals).
- **Tier 3** — news/sentiment: VERIFY, never act on directly.

## How cross-referencing works

**News** (`news_layer.gather_news`): queries every available news source, normalizes
each item, and **clusters stories across sources**. A story carried by ≥2 independent
sources is flagged `corroborated` (higher confidence). When sources disagree on
sentiment, that divergence is flagged as a signal to verify. The synthesis prompt is
told to weight corroborated stories higher and treat single-source items as leads.

**Prices** (`news_layer.price_cross_check`): the primary provider's latest close is
compared against an independent keyless source (Stooq). If they differ by more than
the tolerance (config `PRICE_XCHECK_TOLERANCE`, default 2%), it's flagged rather than
trusted — bad price data is a top source of fake signals.

**Fundamentals:** EDGAR XBRL is always the **source of truth** for any reported
number; vendors are cross-checks and fill estimates where they exist. EDGAR wins on
conflict, always.

## What's live with zero keys

Out of the box (no keys): **EDGAR** (fundamentals + filings), **Stooq** + **yfinance**
(prices), **RSS** + **AlphaVantage demo** (news, limited), **web_search** (the live
synthesizer augments). That's already multi-source. Run `python -c "import
sources_registry as r; print(r.registry_report())"` to see live vs. dormant.

## Lighting up the rest (all free tiers)

Set any of these as environment variables; the registry auto-detects them and adds
the source to the fan-out — no code change:

```bash
export TIINGO_API_KEY=...        # https://www.tiingo.com (free tier + academic) — best price source
export FINNHUB_API_KEY=...       # https://finnhub.io (free tier) — company news + fundamentals
export ALPHAVANTAGE_API_KEY=...  # https://www.alphavantage.co (free) — news + per-ticker sentiment
export MARKETAUX_API_KEY=...     # https://www.marketaux.com (free tier) — news aggregator + sentiment
export POLYGON_API_KEY=...       # https://polygon.io (free tier) — prices
export FRED_API_KEY=...          # https://fred.stlouisfed.org (free) — risk-free rate, sentiment indices
```

**Recommended minimum for the live phase:** Tiingo (sturdy adjusted prices) + Finnhub
+ AlphaVantage (so news actually cross-corroborates across ≥2 vendors) + FRED (real
risk-free rate). That turns the corroboration engine on properly — with only RSS live,
stories rarely cross-confirm.

## Rate limits (respect them at scale)

Free tiers are stingy (AlphaVantage especially — a few calls/min). The engine paces
calls and the news layer sleeps between sources. At the full-universe scale, follow
SCALING.md's priority batching — don't fan out across all sources for 2,000 names every
run. News gathering can be disabled per run with `gather_news=False` (used in tests).
