# ADPT — ADAPTIVE BIOTECHNOLOGIES
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-24 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $27.89
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** The market is paying $4.5bn for an MRD franchise that is finally compounding and about to be separated from the thing that was diluting it. Q2 2026 revenue was $71.6M with the MRD business - 92% of revenue - growing 33% year over year and clonoSEQ test volume up 43% to 36,111 tests. In June the company priced an upsized $345M zero-coupon convertible note offering, used it to repay the OrbiMed revenue-interest purchase agreement, bought a capped call at a 100% premium and repurchased $25M of stock. And it announced plans to SEPARATE the MRD and Immune Medicine businesses, which is a direct answer to the sum-of-parts argument - MRD alone at a diagnostics multiple on a 33%-growing, 43%-volume-growing base is the whole bull case, and the stock is +61.9% over 63 days and +108.8% over 252 on exactly that.

**What changed.** A great deal, and all of it after the last 10-K. (i) $345M of zero-coupon convertible senior notes priced June 2026 (upsized from $300M), OrbiMed purchase agreement repaid, capped call at 100% premium, $25M buyback. (ii) Announced plans to pursue a separation of the MRD and Immune Medicine businesses. (iii) Q2 2026: revenue $71.6M, MRD +33%, clonoSEQ volumes +43%. (iv) Harlan Robins transitioning from Chief Scientific Officer to a strategic consultant.

**Base case.** There is no base. Adaptive generates negative free cash flow in every year of the window - `nonpositive_normalized_fcff` fires, the FCFF base is n/a over 0 years, and there is no reverse DCF to argue with. That leaves the multiples table, and it fails the standing refusal test in the loudest possible way: the cohort is UNRANKED ('too few comparable Health Care names to define a distribution honestly'), and the rows do not merely disagree, they straddle by a factor of fifty - ev_sales gives $5.60/$9.79/$35.45, ev_gross_profit gives $6.46/$10.99/$27.06, and p_tbv at 290.7x gives $0.20/$0.39/$0.71. Averaging those into a $7.05 blended midpoint and calling it a -74.7% gap is exactly the RIOT/EPRT error. A commercial-stage diagnostics company about to split in two is not valued by a Health Care sector median.

**Devil's advocate.**
- Strongest counter: That refusing is not neutral here and the multiples table's -74.7% is a real warning. Adaptive trades at 14.9x its own EV/sales against a Health Care cohort median of 4.4x, and at $4.5bn of market capitalisation on roughly $286M of annualised revenue for a business that has never generated positive free cash flow. The stock has doubled in a year. That is a lot to pay for a 33% grower that still loses money.
- What would prove it: The separation terms and standalone MRD financials - specifically whether MRD alone is cash-generative and what is left to fund in Immune Medicine.
- Already visible today: Only in fragments. The Q2 release says MRD is growing in 'both profitability and growth' but the separation has been announced, not executed, and no standalone MRD segment cash flow is available. The richness argument is plausible and I am explicitly NOT rejecting it - I am declining to convert it into a fair value from a table whose rows disagree by 50x on an unranked cohort.
- Left unresolved: Whether the name is expensive. I think it probably is, and I could not build a defensible number to say so. Refusing is a statement that no row on this page can be believed, not a statement that the stock is cheap.

**Key risks.** Negative free cash flow in every year of the window with no path to a modellable base until the separation completes; $345M of zero-coupon convertible notes that the debt extractor almost certainly does not see (see data quality), so enterprise value is understated; A pending corporate separation makes every consolidated historical input obsolete; +108.8% over 252 days on a business that does not yet generate cash
**Watch for.** Separation terms, timing and standalone MRD financials; clonoSEQ volume growth and MRD gross margin trajectory in Q3/Q4; Whether MRD reaches cash breakeven before the convertible matures

**Data quality.** `interest_expense_implies_no_debt_found_on_reported_debt_debt_likely_understated` is CORRECT here and is the TDOC convertible bug - the 2026-06-30 10-Q carries 'Convertible senior notes, net' on the balance sheet (Note 8, Convertible Senior Notes and Capped Call Transactions) from the $345M zero-coupon offering completed in June, and the FIELDS alias family for total_debt does not cover ConvertibleNotesPayable/ConvertibleDebt concepts. A ZERO-COUPON convertible is the worst case for the detector, because the interest-expense cross-check that normally catches missing debt has almost nothing to find. Enterprise value is therefore understated. It does not change the verdict, because `nonpositive_normalized_fcff` blocks the DCF anyway. The multiples fallback is disqualified wholesale: the cohort is UNRANKED and the three rows straddle by ~50x (p_tbv 290.7x giving $0.20-$0.71 against ev_sales giving $5.60-$35.45), which is the RIOT/EPRT refusal test at full volume. The blended $7.05 midpoint and the -74.7% gap should be disregarded entirely.

*Horizon: 18 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1478320/000119312526332940/adpt-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1478320/000119312526323753/adpt-ex99_1.htm
- https://www.sec.gov/Archives/edgar/data/1478320/000119312526277516/d28937d8k.htm

**Ingestion notes.** no usable final_growth
