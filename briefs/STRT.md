# STRT — STRATTEC SECURITY CORP
*Consumer Discretionary · brief generated 2026-08-31 · selected as **opportunistic***

## Why this name is on today's list
- cheapest 8% of 130 Consumer Discretionary peers (92th pct)
- baseline gap +182%
- 5d move -8%
- 21d move -15%
- filed an 8-K in the last few sessions
- never researched
- urgency score 7.08

## Market
| | |
|---|---|
| price | $75.04 |
| market cap | $299.0M |
| 5d / 21d / 63d / 252d | -8.3% / -15.1% / -6.2% / +12.3% |
| 60d avg daily $ volume | $7.4M |
| beta (vs IWM) | 0.93 (R²=0.125) |

## What the market's price already assumes
Normalized FCFF base **$52.0M** (mean of CFO−capex over 2y, plus after-tax interest)
  annual FCF, newest first: ['$39.0M', '$64.5M']
Enterprise value **$217.6M** · FCFF yield **+23.9%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 9.9% − 1pt | -25.9% |
| **9.9% (point)** | **-23.6%** |
| 9.9% + 1pt | -21.5% |


Naive baseline for comparison: **+3.6%** (5y revenue CAGR +3.6%).
Gap under that baseline: **+181.5%** (fair value $211.25 vs price $75.04).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **92th percentile** of 130 Consumer Discretionary names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: +175.3%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
- none raised

## Recent filings
- 2026-08-28 **10-K** — https://www.sec.gov/Archives/edgar/data/933034/000119312526374333/strt-20260628.htm
- 2026-08-25 **8-K** — items 2.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/933034/000093303426000003/strt-20260825.htm
- 2026-05-28 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/933034/000119312526245261/strt-20260528.htm
- 2026-05-08 **10-Q** — https://www.sec.gov/Archives/edgar/data/933034/000119312526214153/strt-20260329.htm
- 2026-05-07 **8-K** — items 2.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/933034/000119312526212420/strt-20260507.htm
- 2026-04-30 **8-K** — items 1.02 — https://www.sec.gov/Archives/edgar/data/933034/000119312526197481/strt-20260430.htm
- 2026-02-06 **10-Q** — https://www.sec.gov/Archives/edgar/data/933034/000119312526040760/strt-20251228.htm
- 2026-02-05 **8-K** — items 2.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/933034/000119312526039481/strt-20260205.htm
- 2025-10-31 **10-Q** — https://www.sec.gov/Archives/edgar/data/933034/000119312525260138/strt-20250928.htm
- 2025-10-30 **8-K** — items 1.01,2.02,2.03,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/933034/000119312525258802/strt-20251027.htm

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
