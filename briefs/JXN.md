# JXN — JACKSON FINANCIAL CLASS A
*Financials · brief generated 2026-08-31 · selected as **rotation***

## Why this name is on today's list
- rotation position 23/1956

## Market
| | |
|---|---|
| price | $133.65 |
| market cap | $9.1B |
| 5d / 21d / 63d / 252d | +1.0% / +9.3% / +28.9% / +40.7% |
| 60d avg daily $ volume | $73.1M |
| beta (vs IWM) | 1.08 (R²=0.365) |

## What the market's price already assumes
This is a financial. FCFF is meaningless here (debt is raw material, not financing), so the model is justified price/tangible book from sustainable ROTCE.

| | |
|---|---|
| sustainable ROTCE | +6.4% |
| cost of equity | +10.7% |
| justified P/TBV | 0.47 |
| actual P/TBV | 0.91 |
| tangible book / share | $146.95 |
| implied gap | -47.9% |

Cohort: **32th percentile** of 338 Financials names priced the same way — a HIGH percentile means cheap relative to peers (gap vs cohort median: -21.0%).
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `speculative_cost_of_debt_but_only_18%_debt_weight`
- `unstable_rotce_0.3%_to_9.7%`

## Recent filings
- 2026-08-03 **10-Q** — https://www.sec.gov/Archives/edgar/data/1822993/000182299326000124/jxn-20260630.htm
- 2026-08-03 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1822993/000110465926089809/tm2621730d1_8k.htm
- 2026-08-03 **8-K** — items 2.02 — https://www.sec.gov/Archives/edgar/data/1822993/000182299326000123/jxn-20260803.htm
- 2026-07-22 **8-K** — items 5.02,7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1822993/000110465926085839/tm2621047d1_8k.htm
- 2026-07-01 **8-K** — items 1.01,2.03,9.01 — https://www.sec.gov/Archives/edgar/data/1822993/000110465926079925/tm2618572d2_8k.htm
- 2026-06-25 **8-K** — items 5.02,9.01 — https://www.sec.gov/Archives/edgar/data/1822993/000110465926077762/tm2618572d1_8k.htm
- 2026-06-15 **8-K** — items 2.03,9.01 — https://www.sec.gov/Archives/edgar/data/1822993/000110465926074038/tm2616971d4_8k.htm
- 2026-05-26 **8-K** — items 5.07,9.01 — https://www.sec.gov/Archives/edgar/data/1822993/000110465926066299/tm2615669d1_8k.htm
- 2026-05-05 **10-Q** — https://www.sec.gov/Archives/edgar/data/1822993/000182299326000072/jxn-20260331.htm
- 2026-05-05 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1822993/000110465926055652/tm2613079d1_8k.htm

## What we concluded before
*No prior research — this is the first pass on this name.*

## Prior verdicts elsewhere in Financials
- VEL: no_edge · price $18.01

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
