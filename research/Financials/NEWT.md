# NEWT — NEWTEKONE
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $11.89 · fair value $15.57 · gap +30.9%
- **Sustainable ROTCE:** screen said +19.3%, analyst says +15.0%
- **P/TBV:** justified 1.24 vs actual 0.95 on tangible book of $12.58/share

**The case for the price.** NewtekOne is a genuinely differentiated branchless bank for independent business owners: assets up almost 50% year over year, operating expenses up 3.6%, the efficiency ratio improving to 58.4%, deposits nearly doubling, and ROTCE still 15.7%. At roughly 1.0x tangible common book for a bank earning mid-teens returns, the market is pricing the deliberate transition away from gain-on-sale income — near-term EPS falls even though the franchise is getting better — rather than mispricing the franchise.

**What changed.** THE BUSINESS MODEL IS BEING CHANGED ON PURPOSE AND MANAGEMENT SAID SO. In the Q2 2026 release (2026-08-06) the CEO states the mix 'will involve more net interest income by holding more loans on balance sheet and less revenue from gain on sale of loans, and, as a result, our current guidance going forward is being re-evaluated.' On 2026-08-28 the company re-guided: 2026 EPS of $1.70-$1.80. Q2 EPS was $0.48 basic against $0.53 a year earlier, and ROTCE fell from 19.6% to 15.7%. Loans held on the Bank's balance sheet are now 86% of total loans, up from 68% a year ago.

**Base case.** The +74% gap is roughly two-thirds defect. The engine's 19.3% 'sustainable ROTCE' is a three-year average of [16.0%, 18.8%, 23.0%] that spans NewtekOne's conversion from a BDC to a bank holding company in early 2023 and the gain-on-sale era that is now being deliberately wound down; the company's own current ROTCE is 15.7% for Q2 2026, 14.8% for Q1 2026 and 19.6% for Q2 2025 — a clear downtrend, and the VLY rule cuts the other way here: a monotonic trend means the average describes a company that no longer exists. The re-guided 2026 EPS of $1.70-1.80 on ~28.9M shares implies about $49-52M to common against roughly $346M of average tangible common equity, i.e. ROTCE of 14-15%, so I use 15%. There is also a straightforward input error: the engine carries preferred of $19,738k, which is the prior-year figure, against the $48,181k the company reports at 2026-06-30, so tangible book per common share reads $12.575 against the company's own $12.13 and actual P/TBV reads 0.946 against a true 0.980. At a 15% ROTCE and the engine's 12.5% cost of equity the justified multiple is 1.24 against an actual 0.98 — a gap of about +26%, not +74%.

**Devil's advocate.**
- Strongest counter: That the return is not a return at all. Of $75.1M of total income in Q2 2026, $60.1M is NON-interest income and only $15.0M is net interest income — so roughly 80% of NewtekOne's reported earnings come from gain-on-sale and fair-value marks on SBA loans it originates and revalues itself. Per the JXN rule, GAAP net income is not a return for anything whose earnings are a mark, and a 15.7% ROTCE built mostly on self-marked loan valuations does not deserve to be capitalised at a 12.5% cost of equity.
- What would prove it: The credit performance of the SBA 7(a) book now being retained rather than sold — charge-offs and non-accruals on the guaranteed and unguaranteed portions — and whether the fair-value marks have historically been realised on sale.
- Already visible today: Partly, and it is why I did not call this cheap. The company is retaining more of what it used to sell, which removes the market test that validated the marks; the legacy non-bank 7(a) portfolio at NSBF has fallen below 10% of loans from 19%; and management itself withdrew guidance mid-quarter and then re-guided EPS DOWN. I did not obtain the non-accrual and charge-off series, so the credit question is open.
- Left unresolved: Whether a mid-teens ROTCE survives the transition. Management's own 2027 guidance would settle much of it and I did not retrieve the figure — the 2026-08-28 release was in the news store as a headline only, and I read the Q2 release rather than the re-guidance release itself.

**Key risks.** roughly 80% of total income is non-interest income including self-determined fair-value marks on SBA loans; retaining loans rather than selling them moves small-business credit risk onto the balance sheet; ROTCE has fallen from 19.6% to 15.7% year over year and management re-guided EPS down mid-year; assets up ~50% year over year is fast growth for a bank of this size, funded by consumer deposits that more than doubled
**Watch for.** the 2027 EPS guidance from the 2026-08-28 re-guidance and whether it implies ROTCE below 14%; non-accruals and net charge-offs on the retained SBA 7(a) portfolio

**Data quality.** RESOLVED: ebit_derived_from_pretax_plus_interest is immaterial for a book-method name. NEW AND UNFLAGGED: preferred is recorded as $19,738k — the prior-year figure — against $48,181k reported at 2026-06-30, so tangible book per common share is overstated at $12.575 against the company's own $12.13 and the name reads cheaper than it is. The stale-book bug is also present (equity_now $413.4M vs equity_series[0] $397.6M, +4.0%). The sustainable ROTCE of 19.3% averages across the 2023 BDC-to-bank conversion and the gain-on-sale era that management is deliberately ending; unstable_rotce cannot fire because the series is smoothly declining, which is the ENVA blind spot in reverse. OPEN: the 2027 guidance figure and the retained-portfolio credit series.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1587987/000162828026054302/finalpr_earningsreleaseq.htm (Q2 2026 EX-99.1: ROTCE reconciliation, tangible book value per common share $12.13, preferred $48,181k, income mix, CEO statement on the revenue-mix shift)
- https://www.sec.gov/Archives/edgar/data/1587987/000162828026055245/newt-20260630.htm (10-Q, 2026-06-30)
- company news in brief: 2026-08-28 re-guidance to 2026 EPS $1.70-1.80 (headline and summary only)

**Ingestion notes.** no usable final_growth
