# EAT — BRINKER INTERNATIONAL INC
*Consumer Discretionary · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 5/1956

## Market
| | |
|---|---|
| price | $230.19 |
| market cap | $9.6B |
| 5d / 21d / 63d / 252d | -6.4% / +9.7% / +61.7% / +47.4% |
| 60d avg daily $ volume | $201.2M |
| beta (vs IWM) | 0.73 (R²=0.081) |

## What the market's price already assumes
Normalized FCFF base **$429.3M** (mean of CFO−capex over 3y, plus after-tax interest)
  annual FCF, newest first: ['$557.5M', '$413.7M', '$223.0M']
Enterprise value **$9.9B** · FCFF yield **+4.3%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 8.5% − 1pt | +5.3% |
| **8.5% (point)** | **+9.7%** |
| 8.5% + 1pt | +13.6% |


Naive baseline for comparison: **+11.7%** (5y revenue CAGR +11.7%).
Gap under that baseline: **+8.9%** (fair value $250.75 vs price $230.19).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **52th percentile** of 130 Consumer Discretionary names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: +2.7%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `possible_peak_cycle_base_newest_fcf_2.5x_oldest_growth_applied_to_a_peak_overstates_value`

## Recent filings
- 2026-08-19 **10-K** — https://www.sec.gov/Archives/edgar/data/703351/000070335126000029/eat-20260624.htm
- 2026-08-12 **8-K** — items 2.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/703351/000070335126000026/eat-20260810.htm
- 2026-06-17 **8-K** — items 8.01 — https://www.sec.gov/Archives/edgar/data/703351/000070335126000022/eat-20260616.htm
- 2026-04-29 **10-Q** — https://www.sec.gov/Archives/edgar/data/703351/000070335126000015/eat-20260325.htm
- 2026-04-29 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/703351/000070335126000013/eat-20260429.htm
- 2026-03-02 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/703351/000070335126000008/eat-20260226.htm
- 2026-01-28 **10-Q** — https://www.sec.gov/Archives/edgar/data/703351/000070335126000006/eat-20251224.htm
- 2026-01-28 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/703351/000070335126000004/eat-20260128.htm
- 2025-11-24 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/703351/000070335125000051/eat-20251120.htm
- 2025-10-29 **10-Q** — https://www.sec.gov/Archives/edgar/data/703351/000070335125000046/eat-20250924.htm

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
