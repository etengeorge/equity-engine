# AWR — AMERICAN STATES WATER
*Utilities · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-10-09 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $81.83
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** American States Water is a regulated water utility plus a long-dated military-base contracting arm, and the market prices it the way regulated utilities are priced: a multiple of allowed earnings on a growing rate base, plus the value of the ASUS military contracts, with a dividend that has been raised for decades. It is NOT priced on free cash flow, because the business model consumes free cash flow by design — capital is sunk into rate base, the regulator allows a return on it, and the gap is funded with equity and debt. The H1 2026 statements show exactly that: $116.6M of operating cash flow against $97.6M of capital expenditures, $39.5M of dividends paid out of the $19.0M of free cash flow that remains, and $39.9M of new common shares issued to bridge it. A year earlier the same lines produced NEGATIVE free cash flow (CFO $109.6M, capex $118.5M). Paying 2x book for a utility whose rate base compounds is a statement about allowed ROE and rate-case outcomes, and that statement cannot be read off a free-cash-flow yield.

**What changed.** Nothing that changes the refusal. The most recent filings are routine: 10-Q for 2026-06-30 filed 2026-08-05 with the usual item 2.02 earnings 8-K, and earlier 8-Ks in February and March 2026. H1 2026 net income $73.2M against $60.5M a year earlier, so earnings are growing. The 10-Q's own risk language names the live issue plainly — 'our ability to finance significant capital expenditures required by our operations, which are increasing' and 'the impact of inflation, tariffs imposed and supply chain disruptions on our operational costs and costs of capital that may not be recovered in rates'. I found no rate-case decision, acquisition or financing event in the window that would alter an input.

**Base case.** No base case, and no fair value. The engine's own gates are correct here: `nonpositive_normalized_fcff` fired and the model failed. A two-stage FCFF model cannot value a company whose free cash flow is structurally at or below zero because its entire purpose is to convert capital into rate base. The defensible model for AWR is rate base times allowed ROE, or a dividend-discount approach — neither of which this engine runs, and neither of which I can supply through `final_growth`.

**Devil's advocate.**
- Strongest counter: The strongest counter is that refusing here is lazy: a regulated water utility is one of the most forecastable businesses in the index, AWR's H1 earnings grew 21% year over year, and declining to value it means declining to say anything about a name whose cash flows are MORE predictable than the average FCFF name the engine happily prices. The right response to a structurally negative free cash flow is to value the earnings stream, not to shrug.
- What would prove it: A rate-base and allowed-ROE model built from the CPUC decisions, compared against the market's implied allowed ROE — which is a model this engine does not contain.
- Already visible today: The counter is correct about the business and wrong about the engine. I accept that AWR is valuable and forecastable; what I cannot do is express that through the one number this schema moves. Worse, even if the base worked, the discount rate would not: `beta 0.525 at R-squared 0.009, beta_source yahoo_rescaled` produces a 7.63% WACC, which is the standing yahoo_rescaled defect in research/LESSONS.md — an R-squared of 0.009 means the regression explains under 1% of the variance, and there is no R-squared gate on a rescaled Yahoo beta at all.
- Left unresolved: What AWR's defensible allowed-ROE-based value is. I did not build it, and I am recording that as a limit of this engine rather than a conclusion about the company.

**Key risks.** Rate-case risk: tariff and inflation cost increases 'that may not be recovered in rates', per the company's own 10-Q; Financing risk — the dividend exceeds free cash flow and the shortfall is met with equity issuance ($39.9M in H1 2026 alone), so a higher cost of capital dilutes; Interest-rate sensitivity of a bond-proxy equity
**Watch for.** A California general rate case decision setting allowed ROE and capital structure; ASUS military base contract awards or losses; Any quarter in which operating cash flow stops covering capital expenditures for a full year

**Data quality.** Three flags raised and all three are correct descriptions of a regulated utility rather than defects: `negative_fcf_year_in_window`, `lumpy_fcff_spread_2.1x_of_mean`, `nonpositive_normalized_fcff`. I verified the mechanism directly in the 2026-06-30 10-Q cash flow statement — H1 2026 CFO $116,553k less capex $97,561k, against H1 2025 CFO $109,636k less capex $118,481k — so the negative and lumpy free cash flow is the business model, not a tagging error. UNRESOLVED and material if anyone ever repairs the base: the 7.63% WACC rests on a beta of 0.525 at R-squared 0.009 sourced `yahoo_rescaled`, which carries no usable R-squared gate. No fair value is recorded, so no number is contaminated by it.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- data/adhoc/AWR/2026-08-05-10-Q-awr-20260630.htm.txt (cash flow statement, risk factors; fetched via adhoc-fetch)
- data/adhoc/AWR/2026-08-05-EX-99.1.txt (Q2 2026 earnings release)
- data/picks.json row for AWR (screen 2026-10-09, prices as of 2026-10-08)

**Ingestion notes.** no usable final_growth
