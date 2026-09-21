# SLG — SL GREEN REALTY REIT CORP
*Real Estate · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-21 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $52.08

**The case for the price.** SL Green is Manhattan's largest office landlord and the price is a leveraged bet on New York office rents and cap rates. At $52.08 the market pays $3.7B of equity on top of $3.2B of recorded debt for a portfolio whose reported operating cash flow ran [$229.5M, $129.6M, $82.9M] oldest to newest — declining — while the company funds redevelopment and debt-investment activity. The buyer's case is that Manhattan office has bottomed, that SLG's Park Avenue concentration is the first to re-let, and that a 1.2x price-to-tangible-book on depreciated historical cost understates replacement value. That is a real-estate judgment about one submarket, not a free-cash-flow claim.

**What changed.** Nothing found. No company-specific news in the store for the last 90 days, which for a $3.7B REIT with $51.8M of average daily volume means the name did not move enough, trade abnormal volume or file an 8-K to earn a per-company pull. That is a fact about coverage and it lowers my confidence in 'nothing happened' rather than confirming it. The shares are -9.7% over 21 days and -11.8% over 252 days, which is a drift rather than an event.

**Base case.** No fair value, and this is the correct and expected answer rather than a failure. SLG is assigned `method: none` in universe.csv because the FCFF identity is meaningless for a REIT: depreciation is the largest non-cash item, properties are carried at depreciated historical cost, and negative free cash flow is the NORMAL state of a landlord funding redevelopment — the BKH utility case applied to real estate. CLAUDE.md is explicit that roughly 40% of this universe cannot be honestly valued by a free FCFF model and that the engine should say so rather than guess. The multiples fallback does not rescue it either, and fails the RIOT/EPRT refusal test on two counts at once. First, a row is NEGATIVE: ev_sales at the cohort 25th percentile returns MINUS $0.60 per share. Second, the rows disagree by a factor of nearly three at their own medians — ev_ebitda $157.72, p_tbv $67.66, ev_sales $58.31 — against a $52.08 price, so the blended $94.56 and its +81.6% gap are an average of inputs that do not agree on what the company is. The ev_sales row is the EPRT error verbatim: a REIT's rental revenue priced against a cohort median drawn from operating companies sharing the Real Estate GICS bucket. I record no fair value and state plainly that the +81.6% blended gap should be disregarded.

**Devil's advocate.**
- Strongest counter: That +81.6% on the multiples blend and 1.2x tangible book is a lot of apparent value to walk away from, and 'REITs are hard' is not an argument. Two of the three rows (ev_ebitda $157.72, p_tbv $67.66) sit well above the $52.08 price, and the p_tbv row is the one most appropriate to a property company.
- What would prove it: Net operating income by submarket and the implied cap rate against recent Manhattan office transaction comps — which is what actually values this, and which is not derivable from anything on this page or in any free XBRL extract.
- Already visible today: No. The one row the counter leans on hardest, p_tbv at 1.2x, is the least informative for a REIT that has held Manhattan assets for decades: accumulated depreciation drives tangible book below economic value almost mechanically, so 1.2x does not mean what 1.2x means for a bank. The negative ev_sales row is the tell that the cohort is not a cohort.
- Left unresolved: Everything that would decide the name. I have no occupancy, no leasing spreads, no NOI, no cap rate and no recent transaction comps, and no free source in this runtime provides them. That is a statement about my confidence, not a licence to fill the gap.

**Key risks.** refusal is not a judgment that SLG is cheap; the +81.6% multiples blend contains a negative row and should be disregarded entirely; the ev_sales row prices REIT rental revenue against operating companies in the same GICS bucket (the EPRT error); `interest_expense` is recorded as NEGATIVE $187.7M against $3,227.6M of debt — an implied minus 5.8% — the BDC sign-inversion defect, second instance in five sessions; `capex_series` holds a single observation ($253.0M) and `balance_sheet_form` reads 10-K with a 2026-03-31 date on a December-year-end filer, so the provenance of the balance sheet is unclear
**Watch for.** Manhattan office leasing volumes and SLG's own occupancy and mark-to-market leasing spreads; debt maturities and refinancing spreads across the $3.2B recorded balance; a negative interest_expense on any other name — the BDC defect now has two instances and deserves a gate

**Data quality.** One flag raised, `sector_has_no_defensible_free_model`, and it is correct — this is a by-design refusal, not a failure. Three unflagged defects found and recorded for the engine rather than for the verdict: (1) `interest_expense` of MINUS $187,700,000 against `total_debt` of $3,227.6M, an implied rate of -5.8%, which is the BDC sign-inversion pattern (2026-09-17) recurring — it does not affect a `method: none` name but would corrupt any fcff name carrying it; (2) `capex_series` has length 1 against a `cfo_series` of length 3, so cfo-capex could only be computed for one year; (3) `balance_sheet_form` is recorded as 10-K with `balance_sheet_asof` 2026-03-31 for a December-year-end filer. The multiples table fails the standing refusal test on a negative row and on rows disagreeing by ~3x.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- brief for SLG dated 2026-09-21 (multiples table: ev_ebitda n=77 7.7x own vs 10.7/15.9/21.9 cohort; ev_sales n=91 7.0x own, p25 value MINUS $0.60; p_tbv n=83 1.2x own; blended midpoint $94.56 vs $52.08)
- data/fundamentals.json extract for CIK 1040971 (interest_expense -187,700,000; total_debt 3,227.6M; cfo_series [82.9M, 129.6M, 229.5M]; capex_series [253.0M]; balance_sheet_asof 2026-03-31 form 10-K)
- No company-specific news in the store for the last 90 days; no filings fetched for this name, because no document could change a by-design refusal.

**Ingestion notes.** no usable final_growth
