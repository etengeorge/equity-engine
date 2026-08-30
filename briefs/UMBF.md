# UMBF — UMB FINANCIAL
*Financials · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 1/1956

## Market
| | |
|---|---|
| price | $144.59 |
| market cap | $11.0B |
| 5d / 21d / 63d / 252d | -0.4% / -0.6% / +10.5% / +19.2% |
| 60d avg daily $ volume | $91.8M |
| beta (vs IWM) | 1.08 (R²=0.569) |

## What the market's price already assumes
This is a financial. FCFF is meaningless here (debt is raw material, not financing), so the model is justified price/tangible book from sustainable ROTCE.

| | |
|---|---|
| sustainable ROTCE | +13.1% |
| cost of equity | +10.7% |
| justified P/TBV | 1.3 |
| actual P/TBV | 2.05 |
| tangible book / share | $70.66 |
| implied gap | -36.4% |

Cohort: **41th percentile** of 338 Financials names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: -9.6%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `goodwill_and_intangibles_30%_of_book`

## Recent filings
- 2026-07-30 **10-Q** — https://www.sec.gov/Archives/edgar/data/101382/000119312526325054/umbf-20260630.htm
- 2026-07-28 **8-K** — items 2.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/101382/000119312526320980/umbf-20260728.htm
- 2026-04-30 **8-K** — items 5.07,9.01 — https://www.sec.gov/Archives/edgar/data/101382/000119312526197753/umbf-20260428.htm
- 2026-04-30 **10-Q** — https://www.sec.gov/Archives/edgar/data/101382/000119312526194310/umbf-20260331.htm
- 2026-04-28 **8-K** — items 2.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/101382/000119312526186932/umbf-20260428.htm
- 2026-03-12 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/101382/000119312526103203/d82141ddef14a.htm
- 2026-02-26 **10-K** — https://www.sec.gov/Archives/edgar/data/101382/000119312526076496/umbf-20251231.htm
- 2026-02-10 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/101382/000119312526044638/umbf-20260209.htm
- 2026-01-27 **8-K** — items 2.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/101382/000119312526024400/umbf-20260127.htm
- 2025-10-30 **10-Q** — https://www.sec.gov/Archives/edgar/data/101382/000119312525257610/umbf-20250930.htm

## What we concluded before
*No prior research — this is the first pass on this name.*

---

## Your task

Work in this order. Do not skip to the answer.

1. **Steelman the price.** The implied-growth number above is what a large number of
   informed people are collectively willing to pay for. Argue their case first, in
   specifics. If you cannot construct a credible reason for the current price, you have
   not understood the name yet — go back and read.
2. **Research.** Read the recent filings. Search for news since the last 10-K: guidance,
   management change, litigation, regulation, end-market demand, capital allocation.
   Note what you could NOT find; absence of news is information about your confidence,
   not permission to assume nothing happened.
3. **Attack the model's inputs before its conclusion.** Every flag above is a live
   objection. Is the FCFF base a peak or a trough? Is the share count current? Is there
   an acquisition inside the window that makes the history incomparable? Is the growth
   history a real trend or one lumpy year?
4. **Form your own base case.** State a 5-year FCFF growth rate (or, for a financial, a
   sustainable ROTCE) and defend it in one paragraph tied to the business, not to the
   stock. Say explicitly where you differ from the naive baseline and why.
5. **Devil's advocate — a genuinely adversarial pass.** Argue the OPPOSITE of your base
   case as well as you argued the base case. The strongest version, not a strawman: what
   would have to be true for you to be wrong, what evidence would show it, and is any of
   that evidence already visible? Then reconcile: state your final assumption and say
   plainly which of the devil's-advocate points you could not answer.
6. **Size the conclusion honestly.** `no_edge` is the correct and expected answer most of
   the time. A gap that exists only because of a data artifact is not a gap. A gap you
   cannot explain with a mechanism is not a thesis — say so and move on.

Return ONLY a JSON object, no prose around it:

```json
{
  "ticker": "XXXX",
  "consensus_case": "the strongest argument for today's price, in specifics",
  "what_changed": "news/filings since the last 10-K, or 'nothing material found'",
  "base_case_growth": 0.05,
  "base_case_rationale": "one paragraph, tied to the business",
  "fcff_base_override": null,
  "devils_advocate": {
    "strongest_counter": "the best case that the base case is wrong",
    "what_would_prove_it": "the observable that would settle it",
    "already_visible": "any of that evidence present today, or 'none'",
    "unresolved": "what you could not answer"
  },
  "final_growth": 0.04,
  "conviction": "low | medium | high",
  "verdict": "cheap | fair | rich | no_model | no_edge",
  "horizon_months": 24,
  "key_risks": ["...", "..."],
  "watch_for": ["the specific event that would change this view"],
  "data_quality_note": "which flags above you resolved and which remain open",
  "sources": ["urls actually read"]
}
```

Rules that override everything above:
- `final_growth` is the single number that moves the valuation. Everything else is the
  audit trail for why. Set it from your reasoning, not from the gap you want.
- If the devil's advocate wins, say so and set `verdict` accordingly. A red-team pass
  that never changes an answer is theatre.
- Never manufacture a fair value for a `no_model` name.
- An extreme gap is a suspected data error until you have personally verified the inputs.
