# TWST — TWIST BIOSCIENCE
*Health Care · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 11/1956

## Market
| | |
|---|---|
| price | $141.38 |
| market cap | $8.9B |
| 5d / 21d / 63d / 252d | -2.9% / +54.8% / +111.4% / +420.0% |
| 60d avg daily $ volume | $183.0M |
| beta (vs IWM) | 2.01 (R²=0.299) |

## What the market's price already assumes
Normalized FCFF base **n/a** (mean of CFO−capex over 0y, plus after-tax interest)
Enterprise value **n/a** · FCFF yield **n/a**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 15.8% − 1pt | n/a |
| **15.8% (point)** | **n/a** |
| 15.8% + 1pt | n/a |


Naive baseline for comparison: **n/a** (None).
Gap under that baseline: **n/a** (fair value n/a vs price $141.38).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **not ranked** — too few comparable Health Care names to define a distribution honestly, so judge the absolute gap with extra caution.
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `speculative_cost_of_debt_but_only_0%_debt_weight`
- `negative_fcf_year_in_window`
- `nonpositive_normalized_fcff`

## Recent filings
- 2026-08-19 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1581280/000110465926098830/tm2623545d1_8k.htm
- 2026-08-19 **8-K** — items 7.01 — https://www.sec.gov/Archives/edgar/data/1581280/000158128026000050/twist-20260818.htm
- 2026-08-05 **8-K** — items 1.01,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1581280/000110465926091280/tm2622018d2_8k.htm
- 2026-08-03 **10-Q** — https://www.sec.gov/Archives/edgar/data/1581280/000158128026000047/twst-20260630.htm
- 2026-08-03 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1581280/000158128026000044/twist-20260803.htm
- 2026-05-04 **10-Q** — https://www.sec.gov/Archives/edgar/data/1581280/000158128026000040/twst-20260331.htm
- 2026-05-04 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1581280/000158128026000037/twist-20260504.htm
- 2026-02-17 **8-K** — items 3.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1581280/000110465926015730/tm266463d1_8k.htm
- 2026-02-06 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/1581280/000158128026000022/twist-20260205.htm
- 2026-02-02 **10-Q** — https://www.sec.gov/Archives/edgar/data/1581280/000158128026000019/twst-20251231.htm

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
