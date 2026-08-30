# BTSG — BRIGHTSPRING HEALTH SERVICES INC
*Health Care · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 6/1956

## Market
| | |
|---|---|
| price | $59.13 |
| market cap | $11.7B |
| 5d / 21d / 63d / 252d | +0.4% / -18.9% / -4.1% / +147.1% |
| 60d avg daily $ volume | $253.0M |
| beta (vs IWM) | 1.1 (R²=0.235) |

## What the market's price already assumes
Normalized FCFF base **$289.9M** (mean of CFO−capex over 2y, plus after-tax interest)
  annual FCF, newest first: ['$394.7M', '$-57.1M']
Enterprise value **$14.1B** · FCFF yield **+2.1%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 10.5% − 1pt | +33.5% |
| **10.5% (point)** | **+37.9%** |
| 10.5% + 1pt | +41.9% |


> **Stock compensation is 41% of this FCFF base.** Reported operating cash flow adds it back, so the number above treats it as free. Expensing it gives FCFF of **$220.3M** and an implied growth of **+46.2%** instead of +37.9%. Decide which treatment you are underwriting and say so explicitly.

Naive baseline for comparison: **n/a** (insufficient_revenue_history).
Gap under that baseline: **n/a** (fair value n/a vs price $59.13).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **not ranked** — too few comparable Health Care names to define a distribution honestly, so judge the absolute gap with extra caution.
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `negative_fcf_year_in_window`
- `lumpy_fcff_spread_2.7x_of_mean`
- `stock_comp_is_41%_of_fcff_reported_cash_flow_treats_it_as_free`
- `no_baseline_growth`

## Recent filings
- 2026-07-31 **10-Q** — https://www.sec.gov/Archives/edgar/data/1865782/000119312526327014/btsg-20260630.htm
- 2026-07-31 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1865782/000119312526326654/btsg-20260731.htm
- 2026-06-12 **8-K** — items 5.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1865782/000119312526269360/btsg-20260611.htm
- 2026-06-05 **8-K** — items 1.01,9.01 — https://www.sec.gov/Archives/edgar/data/1865782/000119312526259531/btsg-20260603.htm
- 2026-05-21 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/1865782/000119312526234435/btsg-20260521.htm
- 2026-05-01 **10-Q** — https://www.sec.gov/Archives/edgar/data/1865782/000119312526199339/btsg-20260331.htm
- 2026-05-01 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1865782/000119312526198983/btsg-20260501.htm
- 2026-04-10 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/1865782/000119312526151207/btsg-20260410.htm
- 2026-03-31 **8-K** — items 2.01,5.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1865782/000119312526133307/btsg-20260330.htm
- 2026-03-04 **8-K** — items 1.01,9.01 — https://www.sec.gov/Archives/edgar/data/1865782/000186578226000008/btsg-20260302.htm

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
