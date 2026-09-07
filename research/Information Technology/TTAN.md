# TTAN — SERVICETITAN CLASS A
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-07 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $87.92
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** ServiceTitan at $87.92 on 95.4M shares is an $8.4B business doing ~$1.13-1.14B of fiscal 2027 revenue, growing 25% (Q1 FY27 revenue $268.8M, gross transaction volume $21.7B up 23%), with guided non-GAAP operating income of $142-147M. The market pays roughly 7x forward revenue for the category-defining vertical software platform for the residential and commercial trades, with a durable land-and-expand motion, payments attach on a growing GTV base, and a founder-controlled board with 61% of voting power. That is a full but not extraordinary multiple for 25% growth with a positive non-GAAP operating margin — the bull case is that GTV, not revenue, is the real TAM meter, and payments monetization on $21.7B of volume is barely started.

**What changed.** Nothing that changes the business: Q1 FY27 (quarter ended 2026-04-30) beat and the full-year guide was raised. What changed for the model is that I established the share count. The 10-Q filed 2026-06-05 states 82,746,425 Class A and 12,651,154 Class B shares outstanding as of 2026-05-31 — 95,397,579 in total. Q2 FY27 results are due 2026-09-08, one day after this brief.

**Base case.** No growth rate can be stated against this model because the denominator is wrong. Every valuation figure on the brief is built on a share count that is 676 days stale.

**Devil's advocate.**
- Strongest counter: The strongest case against refusing is that I have enough to form a view anyway: at a corrected ~7x forward revenue against a cohort median of 2.9x, ServiceTitan is expensive, and I could record 'rich' on the multiple alone. I decline for two reasons. First, a 25%-growing vertical SaaS leader trading at 7x forward revenue is squarely inside the normal band for that profile, so the multiple by itself does not settle anything. Second, the stock-comp problem is unresolved in a way that matters more than the multiple: SBC is 260% of the reported FCFF base, and expensing it turns FCFF from +$69.3M to -$111.1M. A company whose free cash flow exists only because share issuance is treated as free is one where the correct share count is not a rounding detail, it is the whole question — and the engine has the wrong one.
- What would prove it: The FY27 Q2 print on 2026-09-08: net revenue retention, the GTV growth rate, and — decisively — diluted share count and SBC as a percentage of revenue.
- Already visible today: Partly. The CFO has sold under a 10b5-1 plan twice in six weeks (2,276 shares in July, 9,000 in August), which is routine and tells me nothing. What is visible and does matter is that dilution is the funding mechanism: 24.0M shares are reserved under the 2024 Incentive Award Plan and 12.8M under the 2015 plan, against 95.4M outstanding.
- Left unresolved: Whether ServiceTitan's non-GAAP operating income becomes GAAP cash generation on a per-share basis, or whether the share count grows fast enough to absorb it. I cannot answer that until the model prices the right number of shares.

**Key risks.** Stock compensation is 260% of the reported FCFF base; expensed, free cash flow is negative $111.1M; Dual-class structure with 61% of voting power held by the co-founders, rising to ~73% fully vested; The engine's own multiples table reports ServiceTitan at 2.8x EV/sales against a cohort median of 2.9x — i.e. 'in line' — when the true figure is ~7x
**Watch for.** Q2 FY27 results on 2026-09-08; An engine fix that reads the cover-page share count per class for dual-class filers

**Data quality.** RESOLVED AND FATAL, and it generalises. The brief's `share_count_676d_stale_market_cap_unreliable` is right and understates the damage. The 10-Q filed 2026-06-05 shows 82,746,425 Class A plus 12,651,154 Class B = 95,397,579 shares at 2026-05-31. At $87.92 that is a market cap of $8.39B; the brief says $3.11B, an understatement of 2.7x. Consequences: enterprise value, FCFF yield and implied growth are all wrong, and so is every row of the multiples table — 'its own' ev_sales reads 2.8x when the true figure against the $1.135B FY27 revenue guide is ~7.0x, so ServiceTitan sits in the top quartile of its cohort rather than at the median, and the '+11.6% blended gap' inverts. 676 days before today is 2024-10-31, i.e. the pre-IPO S-1 period, and the mechanism is that a dual-class filer tags dei:EntityCommonStockSharesOutstanding per class on a member axis, so an un-dimensioned read falls back to a stale fact. I scanned the full screen: 104 of 1,956 names carry this flag, median staleness 1,769 days and maximum 5,800 (HUBG); 22 have a positive gap, 19 of those above +50%, and 15 sit in the 90th-plus percentile of their sector cohort — i.e. they are being ranked among the cheapest names in the index on a market cap that does not exist. The list is dominated by dual- and multi-class filers: CENT/CENTA, BELFA/BELFB, HVT, GTN, HUBG, VLGEA, JBSS, MBUU, FNKO, TBLA, ZGN. Two are catastrophic: MBUU's market cap computes to $334.56 and FNKO's to $568.00 — dollars, not millions — producing gaps of +160,066,846% and +140,231,237% and cohort percentiles of exactly 100.0. Both sit at the top of the Consumer Discretionary cheapness ranking that this same brief cites for HOG and WEN. Like the convertible, ABL, rental-capex and low-R2 beta bugs, an understated share count understates market cap, understates EV, lowers implied growth and manufactures a positive gap — it produces false buys, never false sells.

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1638826/000163882626000047/ttan-20260430.htm
- https://www.stocktitan.net/news/TTAN/service-titan-announces-fiscal-first-quarter-financial-n0lurtlrhm9y.html
- https://finance.yahoo.com/markets/stocks/articles/servicetitan-announce-fiscal-second-quarter-130000094.html

**Ingestion notes.** no usable final_growth
