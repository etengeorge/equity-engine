# ENVA — ENOVA INTERNATIONAL
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $225.79 · fair value $158.24 · gap -29.9%
- **Sustainable ROTCE:** screen said +23.7%, analyst says +40.0%
- **P/TBV:** justified 3.74 vs actual 5.33 on tangible book of $42.32/share

**The case for the price.** Enova is compounding at a rate the model's terminal assumption cannot represent. Q2 2026: diluted EPS $4.00 up 40%, adjusted EPS $4.31 up 33% - the eighth consecutive quarter of 30%+ adjusted EPS growth - originations up 27% to $2.3 billion in the quarter, combined loans and finance receivables up 28% year over year to a record $5.5 billion, net revenue margin improving to 61% from 58%, and the consolidated net charge-off ratio FALLING to 7.3%. Credit is getting better while the book grows nearly 30%. On top of that the company has a pending acquisition of Grasshopper Bank, in constructive dialogue with regulators and expected to close later this year, which would replace warehouse funding with deposits. At $225.79 and roughly $17-18 of annualised adjusted EPS that is about 13x earnings. The market is paying 5.3x tangible book because the company is earning something close to 40% on it.

**What changed.** Q2 2026 (2026-07-23): adjusted EPS $4.31 (+33%), originations +27%, receivables +28% to $5.5B, net revenue margin 61%, net charge-off ratio 7.3% (improving). Grasshopper Bank acquisition pending regulatory approval, targeted to close later this year. Three financing 8-Ks since (2026-06-25, 2026-08-14, 2026-08-21, all items 1.01/2.03) plus an officer change on 2026-07-10. No company-specific news in the store for the last 90 days, which lowers my confidence that nothing else happened, though the filings are complete.

**Base case.** See rotce_override. I use 40%, derived rather than assumed: Q2 2026 adjusted EPS of $4.31 annualises to roughly $17.2 against tangible book value per share of $42.32, which is 40.7%. The engine's 23.7% is a three-year GAAP average and is describing a materially smaller, less profitable Enova - eight consecutive quarters of 30%+ adjusted EPS growth means a trailing three-year average is arithmetically guaranteed to understate the current return. This is the VLY lesson running in the growth direction rather than the recovery direction.

**Devil's advocate.**
- Strongest counter: That 5.3x tangible book on a subprime consumer lender is where these names always look best and always end worst. Improving charge-offs and accelerating originations at the same time is the classic late-cycle signature: you grow into a benign loss environment, the vintages season, and the losses show up eighteen months later against a book that has doubled. The engine's -60.1% gap may be reached by the wrong route - a stale average ROTCE - but arrive at the right conclusion. And note that unlike most names in this engine the defect here does not manufacture a false BUY; correcting it makes an already-expensive-looking stock look less expensive, which is the direction that should make me most suspicious of my own correction.
- What would prove it: Net charge-offs rising while origination growth stays high, or a widening gap between GAAP and adjusted earnings, or fair-value marks on the loan book moving adversely.
- Already visible today: No - and I looked for it. The charge-off ratio is falling, not rising (7.3% versus a higher prior-year figure), and net revenue margin is expanding to 61% from 58%, which is the opposite of what a deteriorating book produces. So the bear case is a cycle argument without current evidence, which by the standing lesson on expectations/sentiment theses is not yet a thesis. It is, however, enough to stop me calling this cheap on a corrected ROTCE.
- Left unresolved: The terminal growth constant defeats the model here and I want to say so plainly. At the engine's 2% terminal growth and my 40.7% ROTCE the justified multiple is 3.79 against an actual 5.33 (-29%); at 5% terminal growth it is 4.96 (-7%); at 8% it exceeds the price. A lender growing receivables 28% is not a 2%-terminal-growth business, and the Gordon form becomes arbitrarily sensitive as growth approaches the cost of equity. I cannot pin the answer inside a range that spans the verdict.

**Key risks.** Subprime consumer and SMB credit at 5.3x tangible book - no cushion if loss rates normalise; Regulatory risk to high-APR consumer lending, and to the pending bank charter acquisition; Funding: 47% debt weight with warehouse and securitisation facilities being refinanced repeatedly (three financing 8-Ks since June)
**Watch for.** Grasshopper Bank approval and close - the single largest change to the funding model; The first quarter in which the net charge-off ratio rises while originations are still growing; Any divergence between GAAP and adjusted earnings beyond amortisation

**Data quality.** No flags were raised, and two separate problems sit underneath that silence. (1) The 'sustainable' ROTCE of 23.7% is a three-year GAAP average on a company that has grown adjusted EPS more than 30% for eight consecutive quarters; the current return computes to roughly 40.7% ($4.31 quarterly adjusted EPS annualised against $42.32 of tangible book per share). Correcting it moves the justified P/TBV from 2.13 to 3.79 and the gap from -60.1% to about -29%. Nothing flags a stale average on a fast-growing financial - the `unstable_rotce` flag only fires on a RANGE, and a smoothly compounding series is stable by construction. (2) A STRUCTURAL POINT ABOUT THE MODEL, not this company: the justified P/TBV form is (ROTCE - g)/(CoE - g) with g fixed at 2.0%, and its sensitivity to g explodes as g approaches the cost of equity. On ENVA the same 40.7% ROTCE gives -29% at g=2%, -7% at g=5%, and a positive gap above g=8%. The constant therefore imposes a systematic bias across all 339 book-method Financials - it marks high-growth lenders expensive and slow or shrinking ones fair, independent of anything about the businesses. That is the mirror image of the low-R-squared beta bias already in LESSONS.md and it deserves the same treatment. I could not cross-check tangible book per share against a multiples table (book-method names do not carry one), so the AII stale-book check is OPEN on this name; if $42.32 is the 2025-12-31 figure on a book compounding ~20%, the actual P/TBV is nearer 4.7 and the gap narrows further, which strengthens rather than weakens the no_edge call.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1529864/000119312526314134/enva-ex99_1.htm
- https://www.sec.gov/Archives/edgar/data/1529864/000119312526314590/enva-20260630.htm

**Ingestion notes.** no usable final_growth
