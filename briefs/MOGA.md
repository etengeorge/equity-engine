# MOGA — MOOG INC CLASS A
*Industrials · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 3/1956

## Market
| | |
|---|---|
| price | $374.66 |
| market cap | $12.0B |
| 5d / 21d / 63d / 252d | -3.7% / -10.6% / +4.2% / +89.8% |
| 60d avg daily $ volume | $121.1M |
| beta (vs IWM) | 1.08 (R²=0.411) |

## What the market's price already assumes
Normalized FCFF base **$101.3M** (mean of CFO−capex over 3y, plus after-tax interest)
  annual FCF, newest first: ['$128.4M', '$46.3M', '$-37.4M']
Enterprise value **$12.9B** · FCFF yield **+0.8%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 10.2% − 1pt | +61.7% |
| **10.2% (point)** | **+67.2%** |
| 10.2% + 1pt | +72.3% |


> **Stock compensation is 31% of this FCFF base.** Reported operating cash flow adds it back, so the number above treats it as free. Expensing it gives FCFF of **$87.2M** and an implied growth of **+72.5%** instead of +67.2%. Decide which treatment you are underwriting and say so explicitly.

Naive baseline for comparison: **+6.0%** (5y revenue CAGR +6.0%).
Gap under that baseline: **-94.4%** (fair value $21.06 vs price $374.66).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **5th percentile** of 152 Industrials names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: -80.5%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `negative_fcf_year_in_window`
- `lumpy_fcff_spread_3.6x_of_mean`
- `stock_comp_is_31%_of_fcff_reported_cash_flow_treats_it_as_free`

## Recent filings
- 2026-07-31 **10-Q** — https://www.sec.gov/Archives/edgar/data/67887/000162828026051294/mog-20260627.htm
- 2026-07-31 **8-K** — items 2.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/67887/000162828026051250/mog-20260731.htm
- 2026-07-06 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/67887/000162828026047105/mog-20260701.htm
- 2026-04-24 **10-Q** — https://www.sec.gov/Archives/edgar/data/67887/000162828026027064/mog-20260328.htm
- 2026-04-24 **8-K** — items 2.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/67887/000162828026027030/mog-20260424.htm
- 2026-04-03 **8-K** — items 1.02 — https://www.sec.gov/Archives/edgar/data/67887/000162828026023542/mog-20260403.htm
- 2026-03-24 **8-K** — items 1.01,2.03,2.04 — https://www.sec.gov/Archives/edgar/data/67887/000162828026020809/mog-20260324.htm
- 2026-03-10 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/67887/000162828026016411/mog-20260310.htm
- 2026-03-10 **8-K** — items 7.01,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/67887/000162828026016242/mog-20260310.htm
- 2026-03-03 **8-K** — items 1.01,2.03,9.01 — https://www.sec.gov/Archives/edgar/data/67887/000162828026013594/mog-20260226.htm

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
