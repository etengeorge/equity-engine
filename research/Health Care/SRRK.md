# SRRK — SCHOLAR ROCK HOLDING
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-04 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $55.94
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Scholar Rock's $6.8B market capitalisation is a probability-weighted claim on a single regulatory decision that is due within 26 days. Apitegromab is the first and only muscle-targeted therapeutic to have shown a statistically significant and clinically meaningful benefit in a pivotal Phase 3 trial in spinal muscular atrophy (SAPPHIRE), the BLA has been accepted with a PDUFA action date of 2026-09-30, and the company says the review is advancing along two independent fill-finish paths with commercial supply already manufactured and awaiting packaging and labelling. SMA is a chronic, high-value orphan indication where an approved add-on to existing SMN-directed therapy would carry rare-disease pricing across a durable patient base, and the FSHD program received Fast Track and Orphan Drug designation on 2026-09-02, adding a second indication to the same molecule. The market's price is a straightforward expected-value calculation on that: high probability of approval multiplied by a large addressable revenue stream. It is not a claim about cash flows, because there are none.

**What changed.** Q2 2026, reported 2026-08-06: net loss of $109.9M for the quarter (including $19.7M of stock-based compensation), against $110.0M a year earlier. Cash, cash equivalents and marketable securities of $492.1M at 2026-06-30, which INCLUDES $62.8M of net proceeds raised through the at-the-market equity program during the quarter — the company is funding itself by issuing stock into strength. The apitegromab BLA remains on track for a decision by the 2026-09-30 PDUFA date, with the FDA review advancing at both the Catalent Indiana fill-finish facility and a second US facility, described by the company as two independent paths to approval. On 2026-09-02 the FDA granted Fast Track and Orphan Drug designation to apitegromab in facioscapulohumeral muscular dystrophy as dosing began in the Phase 2 FORGE trial. As of today, 2026-09-04, the drug is NOT approved. No company-specific news is in the engine's own store for this name, which understates how much is happening here.

**Base case.** There is no base case to state. Revenue in the engine's extract is zero, LTM EBITDA is -$383.0M, and normalised FCFF is negative. A discounted cash flow requires cash flows and there are none to discount; a growth rate applied to a negative base is not a valuation, it is a sign error. The honest description of this security is a binary claim on an FDA decision with a known date, and neither method in this engine prices that.

**Devil's advocate.**
- Strongest counter: The case for putting a number on this anyway is that the binary is not really 50/50: a positive pivotal Phase 3, an accepted BLA, two qualified fill-finish paths, and commercial supply already manufactured make approval the strong base case, and a disciplined analyst could build a risk-adjusted NPV — peak sales, penetration of the treated SMA population, pricing, probability of approval, discount rate — and compare it to $6.8B. Refusing to do so means having no view on a $6.8B company at the single most decision-relevant moment in its history.
- What would prove it: The FDA decision itself, on or before 2026-09-30. After that, the first two or three quarters of net product revenue against the treated SMA population, which is what converts an approval into a valuation.
- Already visible today: The approval is not visible; it has not happened. Everything else — trial data, BLA acceptance, manufacturing readiness — is visible and is already why the stock is up 62.7% over twelve months and 16.9% in the last 21 days.
- Left unresolved: Whether apitegromab is approved, and at what label. Building a risk-adjusted NPV would require me to assign a probability of approval and a peak-sales estimate, neither of which I can source from free primary documents with any rigour. Publishing a fair value derived from two numbers I invented would be exactly the failure this engine exists to prevent, so I have not.

**Key risks.** Binary FDA decision due by 2026-09-30 — a complete response letter is the dominant single risk; Zero revenue against a $6.8B market capitalisation and a ~$110M quarterly net loss; $492.1M of cash is roughly 4-5 quarters of runway at the current burn, before any commercial launch spend; The company is funding itself through an at-the-market program ($62.8M in Q2 alone) — ongoing dilution; Manufacturing and fill-finish execution is an explicit part of the review, not a formality; Post-approval, reimbursement and penetration in a market where patients are already on SMN-directed therapy
**Watch for.** The FDA action on or before 2026-09-30 — this is the event, and it is inside four weeks; Launch metrics in the first full quarter post-approval: patients started, gross-to-net, and the treated-population penetration curve; Any further ATM issuance, which sizes the real cost of the launch; Phase 2 FORGE readouts in FSHD as a second indication

**Data quality.** The engine's flags are all correct and all point the same way: `nonpositive_normalized_fcff`, `negative_fcf_year_in_window`, `negative_ebitda_valued_on_revenue_or_gross_profit_only`, and `speculative_cost_of_debt_but_only_3%_debt_weight`. Revenue LTM reads zero and EBITDA -$383.0M, both of which I believe are accurate rather than extraction errors — the company is pre-commercial. The multiples fallback should be DISREGARDED entirely, not weighted. It has exactly one row, price to tangible book, showing 26.8x against a Health Care cohort median of 4.5x and producing a blended value of $9.45 against a $55.94 price. Tangible book is a meaningless denominator for a clinical-stage biotech: it is essentially the cash pile, so the ratio says only that the market values the pipeline at roughly 26x the remaining cash, which is a restatement of the question rather than an answer to it. The brief also flags the cohort as unranked. This is the case research/LESSONS.md describes — an unranked cohort and a single row on a non-operating company — and the rule there is to report no_model and say the multiples number should be disregarded, which is what I am doing. One further note: the beta of 0.65 is `yahoo_rescaled` with an R-squared of 0.014, so the 8.47% WACC is not defensible either; it does not matter here because no DCF is being run, but it would matter the moment anyone tried.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- data/adhoc/SRRK/2026-08-06-EX-99.1.txt (Q2 2026 press release, fetched via adhoc-fetch)
- data/adhoc/SRRK/2026-08-06-10-Q-srrk-20260630.htm.txt
- https://www.biospace.com/press-releases/scholar-rock-reports-second-quarter-2026-financial-results-and-recent-business-highlights
- https://investors.scholarrock.com/news-releases/news-release-details/scholar-rock-announces-fda-review-apitegromab-biologics-license
- https://finance.yahoo.com/healthcare/articles/scholar-rock-receives-fda-fast-120000447.html
- data/fundamentals.json CIK 1727196 (stored EDGAR extract, v5)

**Ingestion notes.** no usable final_growth
