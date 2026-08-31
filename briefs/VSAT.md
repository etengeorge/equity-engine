# VSAT — VIASAT INC
*Information Technology · brief generated 2026-08-31 · selected as **rotation***

## Why this name is on today's list
- rotation position 19/1956

## Market
| | |
|---|---|
| price | $66.93 |
| market cap | $9.2B |
| 5d / 21d / 63d / 252d | -7.4% / -13.0% / -8.1% / +105.7% |
| 60d avg daily $ volume | $182.8M |
| beta (vs IWM) | 1.28 (R²=0.085) |

## What the market's price already assumes
Normalized FCFF base **$392.0M** (mean of CFO−capex over 3y, plus after-tax interest)
  annual FCF, newest first: ['$512.9M', '$-30.1M', '$-139.0M']
Enterprise value **$14.0B** · FCFF yield **+2.8%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 14.2% − 1pt | +38.3% |
| **14.2% (point)** | **+41.5%** |
| 14.2% + 1pt | +44.6% |


> **Stock compensation is 71% of this FCFF base.** Reported operating cash flow adds it back, so the number above treats it as free. Expensing it gives FCFF of **$310.3M** and an implied growth of **+48.9%** instead of +41.5%. Decide which treatment you are underwriting and say so explicitly.

Naive baseline for comparison: **+15.5%** (5y revenue CAGR +15.5%).
Gap under that baseline: **-90.1%** (fair value $6.63 vs price $66.93).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **6th percentile** of 122 Information Technology names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: -58.4%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `negative_fcf_year_in_window`
- `lumpy_fcff_spread_5.7x_of_mean`
- `stock_comp_is_71%_of_fcff_reported_cash_flow_treats_it_as_free`

## Recent filings
- 2026-08-06 **10-Q** — https://www.sec.gov/Archives/edgar/data/797721/000119312526337903/vsat-20260630.htm
- 2026-08-04 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/797721/000119312526332896/d131434d8k.htm
- 2026-07-27 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/797721/000119312526318060/d136591ddef14a.htm
- 2026-05-29 **10-K** — https://www.sec.gov/Archives/edgar/data/797721/000119312526248290/vsat-20260331.htm
- 2026-05-28 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/797721/000119312526245304/d133220d8k.htm
- 2026-05-07 **8-K** — items 1.01,5.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/797721/000119312526210427/d108013d8k.htm
- 2026-02-06 **10-Q** — https://www.sec.gov/Archives/edgar/data/797721/000119312526041421/vsat-20251231.htm
- 2026-02-05 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/797721/000119312526039528/d39970d8k.htm
- 2026-01-26 **8-K** — items 1.01,2.03,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/797721/000119312526022564/d232462d8k.htm
- 2025-12-11 **8-K** — items 5.02 — https://www.sec.gov/Archives/edgar/data/797721/000119312525316132/d73015d8k.htm

## What we concluded before
*No prior research — this is the first pass on this name.*

## Prior verdicts elsewhere in Information Technology
- IDCC: fair · price $335.15 · fair value $296.08 · gap -11.7%

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
