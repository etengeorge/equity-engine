# ONB — OLD NATIONAL BANCORP
*Financials · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 8/1956

## Market
| | |
|---|---|
| price | $25.85 |
| market cap | $10.0B |
| 5d / 21d / 63d / 252d | +0.2% / -2.1% / +8.3% / +15.1% |
| 60d avg daily $ volume | $109.7M |
| beta (vs IWM) | 1.12 (R²=0.57) |

## What the market's price already assumes
This is a financial. FCFF is meaningless here (debt is raw material, not financing), so the model is justified price/tangible book from sustainable ROTCE.

| | |
|---|---|
| sustainable ROTCE | +14.0% |
| cost of equity | +10.9% |
| justified P/TBV | 1.38 |
| actual P/TBV | 1.79 |
| tangible book / share | $14.46 |
| implied gap | -23.0% |

Cohort: **54th percentile** of 338 Financials names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: +3.9%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `last_10k_1703d_old`
- `goodwill_and_intangibles_34%_of_book`

## Recent filings
- 2026-08-12 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/707179/000162828026056279/onb-20260812.htm
- 2026-08-05 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/707179/000162828026053527/onb-20260805.htm
- 2026-07-29 **10-Q** — https://www.sec.gov/Archives/edgar/data/707179/000070717926000046/onb-20260630.htm
- 2026-07-22 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/707179/000162828026049108/onb-20260722.htm
- 2026-05-18 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/707179/000162828026035975/onb-20260513.htm
- 2026-05-13 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/707179/000162828026034664/onb-20260513.htm
- 2026-05-06 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/707179/000162828026031184/onb-20260506.htm
- 2026-04-29 **10-Q** — https://www.sec.gov/Archives/edgar/data/707179/000070717926000038/onb-20260331.htm
- 2026-04-22 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/707179/000162828026026389/onb-20260422.htm
- 2026-04-02 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/707179/000110465926039075/onb-20260513xdef14a.htm

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
