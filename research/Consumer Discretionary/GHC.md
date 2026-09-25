# GHC — GRAHAM HOLDINGS COMPANY CLASS B
*Consumer Discretionary · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-25 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $1.1K · fair value $1.0K · gap -10.2%
- **Growth:** market implies +5.3%, analyst says +3.0% (delta -2.3%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 6.6% | 7.6% | 8.6% | 9.6% | 10.6% |
|---|---|---|---|---|---|---|
| bear | -1.0% | $1.3K | $1.0K | $848.42 | $725.74 | $631.65 |
| base | +3.0% | $1.5K | $1.2K | $1.0K | $879.51 | $765.25 |
| bull | +7.0% | $1.8K | $1.5K | $1.2K | $1.1K | $919.41 |

At the point WACC of 8.6%: bear -25.9%, base -10.2%, bull +8.0%
Across the whole grid the gap ranges -44.8% to +60.2% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $1,145 the market requires about +5.3% five-year FCFF growth from Graham Holdings, and that is close to what a diversified holding company of this shape should be expected to deliver. GHC is Kaplan education, seven television stations, a set of healthcare businesses, manufacturing, restaurants and automotive dealerships, assembled and reassembled by continuous small acquisitions. Its revenue has compounded 11.2% over five years, but that growth is bought: the company acquired five businesses in the comparative period alone and more in 2026, and cash paid for acquisitions never appears in the CFO-minus-capex free cash flow the model grows. Strip the purchases and the organic engine is low-single-digit, with broadcast structurally declining and Kaplan's international business the swing factor. A ~5% requirement against a ~3% organic reality is a market that is, if anything, mildly optimistic.

**What changed.** Nothing material found, and that absence is itself a limitation I am recording. There was NO company-specific news in the store for the trailing 90 days - GHC did not move, did not trade abnormal volume and filed only routine reports, so the news layer contributes nothing here and I am relying entirely on the Q2 10-Q and the two 8-Ks. From the filings: the Q2 2026 10-Q (2026-07-30) confirms continued bolt-on acquisition activity - one small business acquired in the current period, five in the comparative period (one education, two other healthcare, one manufacturing, one automotive) - and the cover page shows Class A 964,001 and Class B 3,270,927 shares. There is remaining authorisation to repurchase 352,011 Class B shares. An 8-K on 2026-08-05 under item 8.01.

**Base case.** I underwrite +3% five-year FCFF growth. The engine's $302.7M base is sound - the free cash flow series [$275.3M, $324.1M, $166.4M] averages $255.3M and the after-tax interest add-back of $47.5M on $900.4M of debt at a plausible 7.0% implied rate is correct - so this is a growth-rate question rather than a data question. I differ from the naive +11.2% baseline by eight points for one reason: that CAGR is acquired revenue. A serial acquirer's reported growth is paid for in cash that CFO-minus-capex never charges, so applying it to free cash flow double-counts the purchases. Organically, education is low-single-digit, broadcast television is structurally declining with political-advertising cyclicality on top, and the healthcare and manufacturing units are steady but small. Low-single-digit organic FCFF growth, supplemented by capital allocation that has been genuinely good but is a return ON reinvestment rather than free growth, is +3%.

**Devil's advocate.**
- Strongest counter: Dismissing the +11.2% revenue CAGR as 'bought' may understate a real skill. Graham Holdings has compounded book and free cash flow for years precisely BY acquiring private businesses below public multiples, and free cash flow of [$275.3M, $324.1M, $166.4M] is not the profile of a company destroying capital - the two most recent years average $300M against a $5.0B market cap, a 6% yield, with the oldest year the outlier. If the acquisition engine keeps working, +5.3% is easily cleared and the +30.1% headline gap is directionally right rather than an artifact.
- What would prove it: Cash paid for acquisitions against the incremental revenue and operating income it bought, over a full cycle - the EVI/EFOR test. If each dollar of acquisition spend has bought durable operating income at a good return, the growth is real even though the free cash flow measure never charged for it; if revenue rises while consolidated operating margin falls, it is revenue purchased at a bad price.
- Already visible today: Partially, and I could not complete the test. The 10-Q discloses the acquisitions and gives a purchase price for the comparative-period group, but I did not reconstruct cash paid for acquisitions against incremental segment operating income across a full cycle, which is what would settle it. What IS visible and supports the counter is that free cash flow in the two most recent years ($275.3M and $324.1M) is well above the oldest ($166.4M), so the trend is up, not down - the possible_peak_cycle_base flag reads on that basis rather than on a cycle.
- Left unresolved: The acquisition-return test above, which is the crux. Also unresolved: with no company news in the store for 90 days I have no visibility on current trading at Kaplan or in broadcast beyond the 10-Q, and the gap between my +3% and the required +5.3% is only about -10% on fair value - comfortably inside the range that a single better or worse year of the acquisition engine would move. That is why this is no_edge rather than rich.

**Key risks.** The reported 11.2% revenue CAGR is substantially acquired; free cash flow never charges for the purchase price; Broadcast television is in structural decline with political-advertising cyclicality layered on top; Kaplan international enrolment is exposed to UK and Australian student-visa policy; Operating lease liabilities of $376.9M are 7% of enterprise value and are deliberately excluded from debt; A conglomerate of six unrelated segments resists any single valuation frame
**Watch for.** Cash paid for acquisitions against incremental segment operating income - the test of whether bought growth is good growth; Kaplan international enrolment trends and any visa-policy change in the UK or Australia; Broadcast retransmission revenue and the 2026 political advertising cycle; Use of the remaining 352,011 share repurchase authorisation against only 4.23M shares outstanding

**Data quality.** One real defect and it is the SAH signature. shares_source and shares_asof are BOTH NULL, and the count used is 4,373,000 - which is NOT the cover-page figure. The Q2 10-Q cover reads Class A 964,001 and Class B 3,270,927, total 4,234,928, so the engine's count is 3.3% too high, overstating market capitalisation by about $158M and enterprise value with it. That inflates the growth the market appears to require, from a corrected +4.6% to the reported +5.3%, so the error runs in the EXPENSIVE direction here and my correction makes the name slightly cheaper, not dearer. This is the second confirmed instance of a NULL shares_source producing a number that is not a cover-page count, and it supports treating a NULL shares_source as a hard gate. The flag possible_peak_cycle_base_newest_fcf_1.7x_oldest is the ITRI pattern once more: the series is [$275.3M, $324.1M, $166.4M] newest first, so the 1.7x is measured against an OLDEST year that was the low, and the flag invites the analyst to discount a base that is not a peak - the middle year is the high, and the newest sits between. Everything else checks out: interest_expense of $63,301k over total_debt of $900,373k is 7.03%, plausible and inside the band; capex is positive and steady; minority interest of $34.5M is correctly added to enterprise value; equity_concept is not needed for an fcff name. dep_amort_series is EMPTY, which does not affect the FCFF calculation but disqualifies any EBITDA cross-check. The +30.1% headline gap is an artifact of the serial-acquirer baseline, not a mispricing. No company-specific news in the store for 90 days, so this verdict rests on filings alone.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/104889/000162828026050826/ghc-20260630.htm
- https://www.sec.gov/Archives/edgar/data/104889/000162828026050829/ghc-20260730.htm
- https://www.sec.gov/Archives/edgar/data/104889/000162828026053479/ghc-20260805.htm
