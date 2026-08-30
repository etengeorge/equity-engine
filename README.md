# Equity Engine

A Russell 2000 screener that looks for large gaps between a defensible intrinsic value and
the market price. It prices all ~1,956 constituents every weekday morning for free, then
spends real analysis on ten names a day.

**It recommends. You decide and you execute.** There is no order-placement path anywhere in
this repository, by design.

## How it works

Every morning a GitHub Action prices the entire index and commits the result. A scheduled
Claude routine then reads that output, researches ten names, argues against its own
conclusions, and writes them into a permanent per-company record. The dashboard rebuilds
and Vercel redeploys on push.

**The model is one two-stage DCF run in both directions.** Backwards, it solves for the
5-year free-cash-flow growth rate that reproduces today's enterprise value — that is what
the market is already assuming. Forwards, it prices an assumption of our own. The
difference between those two numbers is the entire signal.

**Ten names a day, split 6 / 4.** Six by rotation, so the index eventually gets covered
end to end. Four by urgency — a hard price move, a fresh 8-K, a sector-wide selloff, or an
unusually wide gap — so a name that halves while waiting its turn doesn't go unseen.

**It refuses when it should.** Roughly 40% of this universe cannot be honestly valued by a
free cash-flow model: banks and insurers (where debt is raw material, not financing) get a
residual-income model instead, and REITs and cash-burning biotech get no number at all.
Those names are marked, not guessed at.

## Setup

```bash
pip install -r requirements.txt
export SEC_USER_AGENT="equity-engine <your-email>"   # SEC 403s anonymous clients
python run.py screen --limit 40   # a quick slice to check everything works
python run.py pick
python run.py site && open public/index.html
```

For the scheduled version you need three things wired up:

1. **GitHub Action** — set the `SEC_USER_AGENT` repository secret under
   Settings → Secrets and variables → Actions. The workflow runs weekdays at 10:30 UTC and
   fails loudly if the data sources are unreachable.
2. **Vercel** — point a project at this repo's `main` branch. `vercel.json` already sets
   `public/` as the output directory; no build step is needed.
3. **The Claude routine** — schedule an agent against this repo with the contents of
   [`ROUTINE.md`](ROUTINE.md) as its task.

## Layout

| path | what it is |
|---|---|
| `universe.csv` | the frozen index: ticker, sector, and which valuation method applies |
| `edgar.py` | SEC XBRL fundamentals, plus the durable extract in `data/fundamentals.json` |
| `prices.py` | bulk end-of-day prices, returns, liquidity, beta |
| `valuation.py` | the reverse DCF, the forward DCF, and the residual-income model |
| `screen.py` | prices the whole universe — zero LLM tokens |
| `daily.py` | picks today's ten and records why each was picked |
| `brief.py` | writes the self-contained research brief the analyst reads |
| `record.py` | re-prices the analyst's assumption and commits it to memory |
| `research/` | append-only per-company record, organized by sector |
| `dashboard.py` → `public/` | the static site |

## What it can't do

End-of-day prices only. Fundamentals come from annual filings and can be up to a year
stale. Nothing off-balance-sheet, no segment detail, nothing untagged in XBRL. A single
lumpy year still distorts a three-year cash-flow base — briefs flag the dispersion, but
flagging is not fixing. And the absolute size of any gap depends on the equity risk
premium and terminal growth chosen in `config.py`, which is why every gap is also reported
as a percentile against its own sector cohort.

Passing a screen is not an edge. Paper-trade it first.
