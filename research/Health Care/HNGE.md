# HNGE — HINGE HEALTH CLASS A
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-10-02 — NO_MODEL (conviction: low)

- **Verdict:** no_model · price $97.94
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Hinge Health is a digital musculoskeletal care company that IPO'd in May 2025 and is now priced on growth and gross margin: trailing revenue $587.9M, gross profit $468.2M (79.7% gross margin), and reported operating cash flow of $171.4M against capital expenditure of $0.7M - a genuinely asset-light model that converts revenue to cash. The stock is +99.6% over 252 days. The market is paying for continued enterprise and health-plan adoption of virtual MSK care at a margin structure software investors recognise. None of that can be tested against this brief, because every per-share figure on it is wrong.

**What changed.** Not researched, because no business question survives the data defect. For the record: the Q2 2026 10-Q was filed 2026-08-06 and during H1 2026 all 2,581,837 remaining shares of Series E preferred converted voluntarily into Class A common, leaving no preferred outstanding.

**Base case.** No valuation is possible: the share count is wrong by a factor of 4.9 and every derived figure on the brief inherits it. The extract holds shares = 16,379,906 with shares_asof 2024-12-31 and shares_source 'us-gaap:CommonStockSharesOutstanding (10-Q)' - NOT the dei cover-page fact. That is a PRE-IPO balance-sheet common-stock line from a company that was still private, still had multiple series of redeemable convertible preferred outstanding, and whose preferred only converted to common at and after the May 2025 IPO. The Q2 2026 10-Q cover page reads: 'As of July 29, 2026, the registrant had 62,468,721 shares of Class A common stock ... and 18,225,696 shares of Class B common stock ... outstanding' - 80,694,417 shares. At $97.94 market capitalisation is therefore about $7.90bn, not the $1.60bn in the brief, and enterprise value about $7.51bn, not $1.21bn. Consequences: the multiples table is disqualified wholesale per the WHD rule - its blended $153.11 and '+56.3%' gap are computed on a market cap one fifth of the real one, and the p_tbv row of 5.8x is actually about 28x. The reverse DCF is separately unusable even before the share count: the FCFF base of $170.7M is a SINGLE year with no normalisation, and stock compensation of $643.0M is 377% of it - more than the company's entire revenue - so on an expensed basis free cash flow is MINUS $472.3M and no growth rate exists. GAAP operating income is minus $546.4M and net income minus $528.3M. Refusing here is not a statement that Hinge Health is expensive or cheap; it is a statement that nothing on this page can be believed.

**Devil's advocate.**
- Strongest counter: That the share count is fixable by hand - I have the cover page - so I could reprice and produce a view rather than refuse. Corrected, enterprise value is about $7.51bn against reported operating cash flow of $171.4M, which is roughly 44x, and against expensed-SBC free cash flow of minus $472.3M, which is not a multiple at all.
- What would prove it: A second year of cash flow history, and basic weighted-average share count for FY2026 against FY2025 to run the BOX test on whether $643M of stock compensation is being paid for.
- Already visible today: The one-year window is visible and is itself disqualifying: single_year_base_no_normalization is flagged, and the single year is the IPO year, in which the $643M compensation charge is largely one-off IPO vesting rather than a run rate. There is no way to tell a run rate from an IPO artifact with n=1.
- Left unresolved: Everything. The schema has no share-count override, so even a hand-corrected enterprise value cannot be recorded, and a single year containing an IPO is not a cash-flow history.

**Key risks.** Market capitalisation on the brief is understated 4.9x; every per-share and multiple figure is wrong; Stock compensation of $643.0M exceeds revenue of $587.9M and is 377% of the FCFF base; One year of cash flow history, and that year contains the IPO; GAAP operating loss of $546.4M
**Watch for.** A second full year of cash flow and a basic weighted-average share count comparison, which would make the BOX test runnable; Stock compensation normalising below revenue once IPO vesting laps

**Data quality.** share_count_640d_stale_market_cap_unreliable IS flagged and badly understates the problem, which is not staleness but provenance. shares_source is 'us-gaap:CommonStockSharesOutstanding (10-Q)', not dei:EntityCommonStockSharesOutstanding, and the value taken (16,379,906 at 2024-12-31) is a PRE-IPO balance-sheet common line from a company that then had multiple series of redeemable convertible preferred outstanding and that IPO'd in May 2025. The cover page of the Q2 2026 10-Q reads 62,468,721 Class A plus 18,225,696 Class B = 80,694,417 shares as of 2026-07-29. Market cap is $7.90bn against the brief's $1.60bn; EV $7.51bn against $1.21bn. This is a NEW variant of the share-count family: the SAH entry makes a NULL shares_source a hard gate, and this is the case where shares_source is non-null but is not the dei cover-page fact - on a recent IPO that reliably returns a pre-conversion count, and on a dual-class filer it would miss Class B even if current. Direction: understates market cap and manufactures cheapness. The other two flags (single_year_base_no_normalization, stock_comp 377%) are each independently disqualifying. The multiples table is void per the WHD rule.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1673743/000162828026054327/hnge-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1673743/000162828026052558/hnge-20260729.htm

**Ingestion notes.** no usable final_growth
