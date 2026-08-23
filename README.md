# Equity Engine

A reverse-DCF research engine for the Russell 2000. It sources ideas, values
companies against the growth the market is actually pricing, tracks your holdings,
and produces a ranked **recommendation** dashboard plus an email brief.

It does **not** trade. It reads, values, ranks, and recommends. You decide and
you place every order. That line is deliberate and it is the most important thing
in this repo — see "Safety model" below.

---

## What it does, in one breath

For each name: pull financials from SEC EDGAR (free), pull adjusted prices, run a
data-validation gate, compute risk stats (beta/vol/ATR/liquidity), build a WACC
(CAPM cost of equity + synthetic-rating cost of debt, with a sensitivity band),
then run a **reverse DCF** that solves for the FCFF growth the market's price
requires. It compares that implied growth to the company's own history (an
objective sourcing signal), and — where you supply a research growth view — prices
your view into a fair value and a gap, then turns gaps + your positions into
BUY / SELL / TRIM / ADD / HOLD / RESEARCH calls.

---

## Safety model (read this)

- **The engine never places trades.** There is no order-placement code path. The
  Robinhood connection is read-only context.
- **Recommendations end on your screen.** The dashboard and email are the output.
  You open Robinhood and execute yourself.
- **PAPER_MODE** (config) drives a banner on every output. Keep it on until the
  system has earned the right to your capital on out-of-sample results.
- **Paper-trade gate.** Before funding: run the pipeline daily, log every
  recommendation with its assumptions and falsification condition, and *do not
  trade*. After a meaningful sample, score the calls on idiosyncratic excess
  (return above a same-sector basket, not just above zero). If there's no edge net
  of sector beta, no plugin will create one. Fund only after it clears.
- Not investment advice. Not a financial advisor. This is methodology.

---

## What runs free vs. what needs a key

| Piece | Source | Cost |
|---|---|---|
| Ticker → CIK, financials (10-K XBRL) | SEC EDGAR CompanyFacts | **free, no key** |
| Risk-free rate (10y UST) | FRED `DGS10` | free key (falls back to config without one) |
| Prices (adjusted OHLCV) | Tiingo (recommended) | free tier / academic |
| Prices (fallback) | yfinance | free, **flaky** — fine for testing, not production |
| Fundamentals cross-check, news triage | Finnhub / Alpha Vantage | free tiers |

Set keys as environment variables (never hard-code):

```bash
export SEC_USER_AGENT="equity-engine yourname you@email.com"   # SEC requires this
export TIINGO_API_KEY="..."        # then: export PRICE_PROVIDER=tiingo
export FRED_API_KEY="..."          # optional; without it Rf uses config fallback
```

---

## Run it

```bash
pip install yfinance        # only if using the fallback price provider

# quick run
python run.py --tickers PLAB,SHOO,UFPT,CALM

# with your holdings (enables SELL/ADD/HOLD on owned names)
python run.py --tickers PLAB,SHOO,UFPT,CALM --positions positions.json

# with research views (enables fair-value gaps -> BUY/SELL)
python run.py --tickers PLAB,SHOO --views views.json
```

`positions.json` → `[{"ticker":"SHOO","shares":50,"avg_cost":40.0}]`
`views.json` → `{"SHOO":0.06}` — the 5y FCFF growth *your research* supports, per name.

Outputs land in `out/`: `dashboard.html` (full ranked view) and
`email_brief.html` (the actionable alerts on names you hold + top buy ideas).

To run the full universe, replace the `--tickers` list with the IWM holdings pull
(`config.IWM_HOLDINGS_URL`) — but respect the priority/cadence design: don't touch
2,000 names every run, refresh news-active names first and rotate the cold tail.

---

## Scheduling it (and wiring in Robinhood + email)

This codebase is the engine. To make it a recurring, hands-off loop:

- **Claude Cowork scheduled task** or **Claude Code routine** runs it daily.
  Inside that scheduled run, the agent can use your connected **Robinhood** tools
  to read current positions and feed them in as `positions`, and your **Gmail**
  connector to send `email_brief.html` to you. That is how the read-only account
  access and the email alert you asked for get wired — at the orchestration layer,
  not inside this Python (which has no credentials of its own).
- The **research views** (the growth numbers that turn implied-growth into a
  fair-value gap) are produced by the synthesis step: the agent reads the 8-Ks,
  earnings calls, and sector signals, forms a differentiated view, and passes the
  adjusted growth per name into the engine. The implied growth is objective; the
  view is where judgment enters.
- **Store as git:** `git init` the `store/` directory. Each run commits, so commit
  history becomes the point-in-time audit trail the retrospective scores against.

---

## Architecture

```
config.py         all assumptions & thresholds (ERP, tax, bands, buy/sell gates)
data_sources.py   EDGAR (CIK map, CompanyFacts, SIC->sector, 8-K/10-K text), FRED, prices
analytics.py      validate() · risk_stats() (gap-aware beta) · compute_wacc() · reverse_dcf()
synthesis.py      research brain: filings+history+all-verticals -> variant growth + rationale
                  (free: live reasoning runs through Claude at the orchestration layer;
                   deterministic stub makes the whole chain testable now)
thesis.py         structured rationale: deviation, evidence w/ receipts, catalyst,
                  falsification, conviction, horizon, pinned evaluation window
engine.py         orchestration: synthesis -> thesis -> valuation -> recommendation -> journal
journal.py        Drive-mirrored folder tree; ALL vertical notes read together,
                  company docs read one-at-a-time; git-tracked audit trail
outputs.py        dashboard + email, each surfacing the FULL reasoning chain
store.py          per-company JSON snapshots, append-only
qa_harness.py     adversarial QA pass (edge cases + live integration); run before trusting output
run.py            CLI

CONNECTING.md     wire live Claude synthesis + Google Drive + Gmail + Robinhood (all free)
SCALING.md        flip from a watchlist to the full 2,000-name IWM universe safely
```

## QA

`python qa_harness.py` runs the adversarial pass: WACC edge cases (no-debt,
negative-EBIT, missing shares/beta), reverse-DCF monotonicity and divide-by-zero
guards, thesis/evaluation-window integrity, recommendation and ranking logic, a
**beta date-alignment regression test**, and live integration on real tickers.

> The QA pass already caught one real, valuation-corrupting bug: beta was being
> computed by aligning stock and market returns by tail length, so any name with a
> trading gap or short history produced a garbage beta (→ garbage WACC → garbage
> valuation). It's fixed (gap-aware, date-keyed pairing) and locked with a
> regression test. This is exactly what the QA member is for; keep running it after
> any change.

**What QA verifies:** logic, math, wiring, graceful degradation. **What it cannot
verify:** whether the synthesis produces *good investment judgment* — that's the
paper-trade gate's job over time. "Passed QA" ≠ "has edge."

---

## Honest limitations (the parts to distrust)

- **FCFF normalization is the accuracy ceiling, not the WACC.** The reverse DCF is
  most sensitive to normalized starting FCFF. We average CFO−capex over a few years
  and add back after-tax interest; SBC stays inside reported CFO. Cyclical peaks
  (see CALM, whose egg-price boom inflates FCFF) will mislead — the FCFF sensitivity
  band flags when a conclusion doesn't survive re-normalization. Treat names where
  the band flips the sign as no-signal.
- **Small-cap betas are noisy.** Thin/non-synchronous trading biases beta; we apply
  a Blume shrink and flag low-R² names (`beta_low_r2`) as low-reliability. A proper
  bottom-up peer beta (unlever sector peers, relever at target) is the upgrade once
  the full universe is loaded.
- **Synthetic rating uses reported interest expense**, which is lumpy for small-caps
  (a name can show a near-infinite coverage ratio off a tiny tagged interest figure).
  It barely moves WACC when debt is small, but don't read the implied rating as gospel.
- **Point-in-time integrity is forward-only.** XBRL shows current/restated numbers.
  Integrity accrues from the day you start committing the store; backfilled history
  is not a clean validation set.
- **Screening 2,000 names guarantees false positives.** The most extreme gaps are
  disproportionately data errors or model breakdowns. Ranking is reliability-weighted
  and extreme gaps should be treated as suspicious first, researched second.
- **yfinance breaks.** Use Tiingo for anything you rely on.
```

## v2 (August 2026)

An audit of the scheduled routine found 27 "successful" cloud runs that persisted nothing (silent
push failure in a fresh clone), a 10k-name universe instead of the Russell 2000, and a research
prompt truncated before the memory layer. v2 fixes each and adds a binding devil's-advocate pass,
a street-consensus seam, a run manifest, and a short side. Start with `CLAUDE.md` ("v2 changes")
and `ROUTINE_PROMPT.md`. Tests: `_v2_cases.py`, `_extreme_cases.py`, `qa_harness.py`.
