# BBW — BUILD A BEAR WORKSHOP
*Consumer Discretionary · brief generated 2026-08-30 · selected as **opportunistic***

## Why this name is on today's list
- cheapest 4% of 130 Consumer Discretionary peers (96th pct)
- baseline gap +216%
- 5d move -23%
- 21d move -15%
- filed an 8-K in the last few sessions
- never researched
- urgency score 9.1

## Market
| | |
|---|---|
| price | $29.85 |
| market cap | $374.2M |
| 5d / 21d / 63d / 252d | -23.2% / -15.4% / -19.2% / -48.0% |
| 60d avg daily $ volume | $16.2M |
| beta (vs IWM) | 0.66 (R²=0.065) |

## What the market's price already assumes
Normalized FCFF base **$37.8M** (mean of CFO−capex over 3y, plus after-tax interest)
  annual FCF, newest first: ['$39.5M', '$27.8M', '$46.0M']
Enterprise value **$346.0M** · FCFF yield **+10.9%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 8.3% − 1pt | -15.2% |
| **8.3% (point)** | **-11.7%** |
| 8.3% + 1pt | -8.6% |


Naive baseline for comparison: **+15.7%** (5y revenue CAGR +15.7%).
Gap under that baseline: **+216.1%** (fair value $94.37 vs price $29.85).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **96th percentile** of 130 Consumer Discretionary names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: +210.0%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `operating_leases_29%_of_EV_kept_as_opex_not_debt_capitalizing_them_would_materially_change_this`

## Recent filings
- 2026-08-27 **8-K** — items 2.02,5.02,9.01 — https://www.sec.gov/Archives/edgar/data/1113809/000143774926029054/bbw20260826_8k.htm
- 2026-06-12 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/1113809/000143774926020380/bbw20260610c_8k.htm
- 2026-06-12 **8-K** — items 5.07,9.01 — https://www.sec.gov/Archives/edgar/data/1113809/000143774926020370/bbw20260610_8k.htm
- 2026-06-11 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1113809/000143774926020299/bbw20260605_8k.htm
- 2026-06-11 **10-Q** — https://www.sec.gov/Archives/edgar/data/1113809/000143774926020239/bbw20260417_10q.htm
- 2026-05-28 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1113809/000143774926018669/bbw20260527_8k.htm
- 2026-04-30 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/1113809/000143774926013976/bbw20260427_def14a.htm
- 2026-04-16 **10-K** — https://www.sec.gov/Archives/edgar/data/1113809/000143774926012501/bbw20251218c_10k.htm
- 2026-03-12 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/1113809/000143774926007825/bbw20260311c_8k.htm
- 2026-03-12 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1113809/000143774926007824/bbw20260312_8k.htm

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
