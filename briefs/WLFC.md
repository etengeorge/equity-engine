# WLFC — WILLIS LEASE FINANCE
*Industrials · brief generated 2026-08-30 · selected as **opportunistic***

## Why this name is on today's list
- cheapest 7% of 152 Industrials peers (93th pct)
- baseline gap +177%
- 21d move -26%
- filed an 8-K in the last few sessions
- never researched
- urgency score 7.54

## Market
| | |
|---|---|
| price | $53.42 |
| market cap | $1.1B |
| 5d / 21d / 63d / 252d | -1.7% / -26.2% / -69.7% / -64.5% |
| 60d avg daily $ volume | $23.0M |
| beta (vs IWM) | 1.53 (R²=0.185) |

## What the market's price already assumes
Normalized FCFF base **$350.2M** (mean of CFO−capex over 3y, plus after-tax interest)
  annual FCF, newest first: ['$252.2M', '$268.8M', '$224.6M']
Enterprise value **$3.8B** · FCFF yield **+9.1%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 14.6% − 1pt | +6.8% |
| **14.6% (point)** | **+9.1%** |
| 14.6% + 1pt | +11.4% |


> **Stock compensation is 12% of this FCFF base.** Reported operating cash flow adds it back, so the number above treats it as free. Expensing it gives FCFF of **$320.7M** and an implied growth of **+11.5%** instead of +9.1%. Decide which treatment you are underwriting and say so explicitly.

Naive baseline for comparison: **+20.4%** (5y revenue CAGR +20.4%).
Gap under that baseline: **+176.7%** (fair value $147.81 vs price $53.42).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **93th percentile** of 152 Industrials names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: +190.6%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
- none raised

## Recent filings
- 2026-08-25 **8-K** — items 2.01,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1018164/000101816426000072/wlfc-20260824.htm
- 2026-08-06 **8-K** — items 1.01 — https://www.sec.gov/Archives/edgar/data/1018164/000101816426000070/wlfc-20260803.htm
- 2026-08-04 **10-Q** — https://www.sec.gov/Archives/edgar/data/1018164/000101816426000068/wlfc-20260630.htm
- 2026-08-04 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1018164/000101816426000065/wlfc-20260804.htm
- 2026-07-30 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1018164/000101816426000063/wlfc-20260729.htm
- 2026-07-21 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1018164/000101816426000061/wlfc-20260721.htm
- 2026-07-17 **8-K** — items 5.03,9.01 — https://www.sec.gov/Archives/edgar/data/1018164/000119312526307870/d85905d8k.htm
- 2026-07-14 **8-K** — items 1.01,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1018164/000101816426000058/wlfc-20260710.htm
- 2026-07-10 **8-K** — items 8.01 — https://www.sec.gov/Archives/edgar/data/1018164/000119312526300912/d142690d8k.htm
- 2026-06-23 **8-K** — items 5.07,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1018164/000119312526279754/d129925d8k.htm

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
