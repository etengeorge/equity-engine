# KRYS — KRYSTAL BIOTECH
*Health Care · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 9/40

## Market
| | |
|---|---|
| price | $351.46 |
| market cap | $10.4B |
| 5d / 21d / 63d / 252d | +1.4% / -4.2% / +13.7% / +138.1% |
| 60d avg daily $ volume | $142.7M |
| beta (vs IWM) | 0.73 (R²=0.11) |

## What the market's price already assumes
Normalized FCFF base **$69.2M** (mean of CFO−capex over 3y, plus after-tax interest)
  annual FCF, newest first: ['$188.9M', '$119.2M', '$-100.6M']
Enterprise value **$9.6B** · FCFF yield **+0.7%**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 8.7% − 1pt | +55.2% |
| **8.7% (point)** | **+61.7%** |
| 8.7% + 1pt | +67.5% |


> **Stock compensation is 69% of this FCFF base.** Reported operating cash flow adds it back, so the number above treats it as free. Expensing it gives FCFF of **$21.3M** and an implied growth of **+100.0%** instead of +61.7%. Decide which treatment you are underwriting and say so explicitly.

Naive baseline for comparison: **+25.0%** (2y revenue CAGR +177.0% (clamped to +25.0%)).
Gap under that baseline: **-65.0%** (fair value $123.02 vs price $351.46).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **not ranked** — too few comparable Health Care names to define a distribution honestly, so judge the absolute gap with extra caution.
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `negative_fcf_year_in_window`
- `lumpy_fcff_spread_4.2x_of_mean`
- `stock_comp_is_69%_of_fcff_reported_cash_flow_treats_it_as_free`

## Recent filings
- 2026-08-03 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000058/krys-20260803.htm
- 2026-08-03 **10-Q** — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000057/krys-20260630.htm
- 2026-07-21 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000050/krys-20260721.htm
- 2026-05-20 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000047/krys-20260515.htm
- 2026-05-04 **8-K** — items 9.01 — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000044/krys-20260504.htm
- 2026-05-04 **10-Q** — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000043/krys-20260331.htm
- 2026-04-03 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000036/krys-20260403.htm
- 2026-02-17 **8-K** — items 2.02 — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000018/krys-20260217.htm
- 2026-02-17 **10-K** — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000016/krys-20251231.htm
- 2026-01-12 **8-K** — items 2.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1711279/000171127926000008/krys-20260111.htm

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
