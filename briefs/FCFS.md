# FCFS — FIRSTCASH HOLDINGS INC
*Financials · brief generated 2026-08-30 · selected as **rotation***

## Why this name is on today's list
- rotation position 10/40

## Market
| | |
|---|---|
| price | $219.21 |
| market cap | $9.5B |
| 5d / 21d / 63d / 252d | -2.7% / +8.8% / -0.1% / +48.8% |
| 60d avg daily $ volume | $102.7M |
| beta (vs IWM) | None (R²=0.029) |

## What the market's price already assumes
This is a financial. FCFF is meaningless here (debt is raw material, not financing), so the model is justified price/tangible book from sustainable ROTCE.

| | |
|---|---|
| sustainable ROTCE | +1083.6% |
| cost of equity | +10.2% |
| justified P/TBV | 140.04 |
| actual P/TBV | 428.34 |
| tangible book / share | $0.51 |
| implied gap | -67.3% |

Cohort: **not ranked** — too few comparable Financials names to define a distribution honestly, so judge the absolute gap with extra caution.
Cohort rank is the honest comparator — absolute gaps shift with the ERP (5.5%) and terminal growth (2.5%) constants, which are choices, not facts.

## Data-quality flags
Attack these before you trust any number above.
- `beta_defaulted_to_1.0(unreliable_r2_0.029_raw_0.20)`
- `goodwill_and_intangibles_99%_of_book`
- `unstable_rotce_678.7%_to_1488.4%`
- `rotce_1084%_suggests_asset_light_financial_p_tbv_may_be_the_wrong_model_here`

## Recent filings
- 2026-08-06 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/840489/000084048926000087/fcfs-20260806.htm
- 2026-07-27 **10-Q** — https://www.sec.gov/Archives/edgar/data/840489/000084048926000085/fcfs-20260630.htm
- 2026-07-23 **8-K** — items 2.02,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/840489/000084048926000082/fcfs-20260723.htm
- 2026-07-22 **8-K** — items 5.02 — https://www.sec.gov/Archives/edgar/data/840489/000084048926000080/fcfs-20260722.htm
- 2026-07-16 **8-K** — items 8.01,9.01 — https://www.sec.gov/Archives/edgar/data/840489/000110465926084072/tm2620535d1_8k.htm
- 2026-06-23 **8-K** — items 7.01,8.01,9.01 — https://www.sec.gov/Archives/edgar/data/840489/000110465926076623/tm2618455d1_8k.htm
- 2026-06-18 **8-K** — items 3.03,5.03,9.01 — https://www.sec.gov/Archives/edgar/data/840489/000110465926075855/tm2618096d1_8k.htm
- 2026-06-09 **8-K** — items 5.07 — https://www.sec.gov/Archives/edgar/data/840489/000084048926000073/fcfs-20260609.htm
- 2026-05-12 **8-K** — items 7.01,9.01 — https://www.sec.gov/Archives/edgar/data/840489/000084048926000061/fcfs-20260511.htm
- 2026-05-01 **8-K** — items 1.01,2.03,9.01 — https://www.sec.gov/Archives/edgar/data/840489/000110465926054143/tm2613265d1_8k.htm

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
