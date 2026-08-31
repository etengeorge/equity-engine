# HUT — HUT CORP
*Information Technology · brief generated 2026-08-31 · selected as **rotation***

## Why this name is on today's list
- rotation position 21/1956

## Market
| | |
|---|---|
| price | $77.00 |
| market cap | $9.5B |
| 5d / 21d / 63d / 252d | -3.2% / -28.5% / -41.8% / +190.5% |
| 60d avg daily $ volume | $460.3M |
| beta (vs IWM) | 2.19 (R²=0.236) |

## What the market's price already assumes
Normalized FCFF base **n/a** (mean of CFO−capex over 0y, plus after-tax interest)
Enterprise value **n/a** · FCFF yield **n/a**

**Reverse DCF — the 5y FCFF growth the current price requires:**

| WACC | implied 5y FCFF growth |
|---|---|
| 16.4% − 1pt | n/a |
| **16.4% (point)** | **n/a** |
| 16.4% + 1pt | n/a |


Naive baseline for comparison: **n/a** (None).
Gap under that baseline: **n/a** (fair value n/a vs price $77.00).

> The baseline is the company's own revenue history mechanically applied to FCFF. It is NOT a thesis and carries no judgment — it exists only to rank candidates. Your job below is to replace it.

Cohort: **not ranked** — too few comparable Information Technology names to define a distribution honestly, so judge the absolute gap with extra caution.
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `negative_fcf_year_in_window`
- `nonpositive_normalized_fcff`

## Recent filings
- 2026-08-04 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926090041/tm2621890d1_8k.htm
- 2026-08-04 **10-Q** — https://www.sec.gov/Archives/edgar/data/1964789/000110465926090025/hut-20260630x10q.htm
- 2026-07-20 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926084862/tm2620835d1_8k.htm
- 2026-06-12 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926073505/tm2617732d1_8k.htm
- 2026-06-10 **8-K** — items 1.01,2.03,9.01 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926071952/tm2617190d1_8k.htm
- 2026-06-05 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926070744/tm2616926d1_8k.htm
- 2026-06-04 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926070393/tm2616869d1_8k.htm
- 2026-05-06 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926055894/hut-20260506x8k.htm
- 2026-05-06 **10-Q** — https://www.sec.gov/Archives/edgar/data/1964789/000110465926055891/hut-20260331x10q.htm
- 2026-05-01 **8-K** — items 1.01,2.03,9.01 — https://www.sec.gov/Archives/edgar/data/1964789/000110465926053247/tm2613163d1_8k.htm

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
