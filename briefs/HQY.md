# HQY — HEALTHEQUITY
*Health Care · brief generated 2026-08-30 · selected as **opportunistic***

## Why this name is on today's list
- baseline gap +26%
- discounted: stock comp is 24% of reported FCFF
- discounted: cash-flow base may be a cycle peak
- 5d move -9%
- filed an 8-K in the last few sessions
- never researched
- urgency score 2.63

## Market
| | |
|---|---|
| price | $96.37 |
| market cap | $8.0B |
| 5d / 21d / 63d / 252d | -8.6% / -4.6% / +9.5% / +9.5% |
| 60d avg daily $ volume | $83.7M |
| beta (vs IWM) | 0.69 (R²=0.158) |

## What the market's price already assumes
Normalized FCFF base **$387.4M** (mean of CFO−capex over 3y, plus after-tax interest)
  annual FCF, newest first: ['$455.1M', '$337.8M', '$241.1M']
Enterprise value **$8.6B** · FCFF yield **+4.5%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 8.1% − 1pt | +2.6% |
| **8.1% (point)** | **+7.1%** |
| 8.1% + 1pt | +11.2% |


> **Stock compensation is 24% of this FCFF base.** Reported operating cash flow adds it back, so the number above treats it as free. Expensing it gives FCFF of **$305.2M** and an implied growth of **+12.8%** instead of +7.1%. Decide which treatment you are underwriting and say so explicitly.

Naive baseline for comparison: **+12.4%** (5y revenue CAGR +12.4%).
Gap under that baseline: **+26.4%** (fair value $121.80 vs price $96.37).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **not ranked** — too few comparable Health Care names to define a distribution honestly, so judge the absolute gap with extra caution.
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `possible_peak_cycle_base_newest_fcf_1.9x_oldest_growth_applied_to_a_peak_overstates_value`
- `stock_comp_is_24%_of_fcff_reported_cash_flow_treats_it_as_free`

## Recent filings
- 2026-08-27 **10-Q** — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000041/hqy-20260731.htm
- 2026-08-27 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000040/hqy-20260827.htm
- 2026-06-26 **8-K** — items 5.07,9.01 — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000034/hqy-20260625.htm
- 2026-05-28 **10-Q** — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000028/hqy-20260430.htm
- 2026-05-28 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000027/hqy-20260528.htm
- 2026-05-13 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000022/hqy-20260513.htm
- 2026-05-08 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000016/hqy-20260505.htm
- 2026-04-06 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000014/hqy-20260406.htm
- 2026-03-30 **8-K** — items 5.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000012/hqy-20260326.htm
- 2026-03-17 **10-K** — https://www.sec.gov/Archives/edgar/data/1428336/000142833626000010/hqy-20260131.htm

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
