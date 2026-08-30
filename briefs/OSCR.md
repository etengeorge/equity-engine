# OSCR — OSCAR HEALTH CLASS A
*Financials · brief generated 2026-08-30 · selected as **opportunistic***

## Why this name is on today's list
- baseline gap -145%
- never researched
- urgency score 1.1

## Market
| | |
|---|---|
| price | $30.47 |
| market cap | $8.0B |
| 5d / 21d / 63d / 252d | -4.9% / -2.4% / +37.1% / +79.0% |
| 60d avg daily $ volume | $176.0M |
| beta (vs IWM) | 0.99 (R²=0.054) |

## What the market's price already assumes
This is a financial. FCFF is meaningless here (debt is raw material, not financing), so the model is justified price/tangible book from sustainable ROTCE.

| | |
|---|---|
| sustainable ROTCE | -25.5% |
| cost of equity | +10.2% |
| justified P/TBV | -3.65 |
| actual P/TBV | 8.18 |
| tangible book / share | $3.73 |
| implied gap | -144.7% |

Cohort: **not ranked** — too few comparable Financials names to define a distribution honestly, so judge the absolute gap with extra caution.
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `speculative_cost_of_debt_but_only_5%_debt_weight`
- `unstable_rotce_-45.3%_to_2.5%`
- `loss_year_in_window`

## Recent filings
- 2026-08-07 **10-Q** — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000069/oscr-20260630.htm
- 2026-08-06 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000066/oscr-20260806.htm
- 2026-06-09 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000059/oscr-20260604.htm
- 2026-06-08 **8-K** — items 7.01 — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000054/oscr-20260608.htm
- 2026-06-02 **8-K** — items 5.02 — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000048/oscr-20260529.htm
- 2026-05-07 **10-Q** — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000040/oscr-20260331.htm
- 2026-05-06 **8-K** — items 2.02,9.01 — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000036/oscr-20260506.htm
- 2026-04-22 **DEF 14A** — https://www.sec.gov/Archives/edgar/data/1568651/000114036126016119/ny20059895x771_def14a.htm
- 2026-04-21 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000028/oscr-20260421.htm
- 2026-03-02 **8-K** — items 7.01 — https://www.sec.gov/Archives/edgar/data/1568651/000156865126000014/oscr-20260302.htm

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
