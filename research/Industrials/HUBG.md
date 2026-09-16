# HUBG — HUB GROUP CLASS A
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-16 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $33.45
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** At $33.45 the market is pricing a logistics company that has told the SEC twice that its own financial statements cannot be relied upon, has not filed a 2025 10-K or either 2026 10-Q, expects a Nasdaq delisting determination, and has pre-announced an operating LOSS for the first half of 2026. The price is not a cash-flow opinion; it is a discount for un-auditable financials plus optionality on the restatement landing without further damage. Intermodal volumes and pricing are actually firming (the company cites tightening market capacity and over-the-road conversion), so the equity is a bet that the accounting problem is contained to purchased-transportation accruals and that the franchise survives the listing process intact.

**What changed.** Everything material postdates the last reliable filing. 2026-02-05: Item 4.02 8-K - Q1/Q2/Q3 2025 financials materially misstated by an understatement of purchased transportation costs and accounts payable, no longer to be relied upon. 2026-05-12: SECOND Item 4.02 extending the review to the 2024 AND 2023 financial statements. 2026-09-14: preliminary H1 2026 revenue $1.70-1.80B with an anticipated OPERATING LOSS before one-time charges; full-year revenue guided $3.6-3.8B; cash ~$132M, debt ~$198M, net debt ~$66M at 2026-06-30, plus a $75M revolver draw in August. Nasdaq exception expired 2026-09-14 and the company expects a Staff Delisting Determination it intends to appeal. Credit agreement amended 2026-09-11 to push the filing deadline to 2026-11-30. David Yeager returned as CEO; Patrick O'Donnell appointed CFO.

**Base case.** No defensible base case exists. The engine's $231.6M FCFF base is the mean of CFO-less-capex for fiscal 2024, 2023 and 2022. The company has formally repudiated 2024 and 2023, and 2022 is the freight-cycle peak (revenue $5.3B against $3.6-3.8B guided for 2026). There is no audited, unrepudiated cash-flow year in the window. Supplying a growth rate here would price a restated set of numbers nobody has seen, including management.

**Devil's advocate.**
- Strongest counter: That 'no_model' is an over-reaction to a bookkeeping error. The misstatement was an understatement of an ACCRUAL - purchased transportation costs and accounts payable - which is a timing and liability-recognition problem, not a cash problem. Cash is cash: the company disclosed $132M of cash and $198M of debt at 2026-06-30, and those figures are not in dispute. On that view the restatement re-cuts the income statement between periods while the cumulative cash flow over 2023-2026 is roughly unchanged, and a $231.6M normalized FCFF base might survive largely intact. The market's -13.9% implied growth would then be a genuine discount worth capturing.
- What would prove it: The restated 10-K, when filed in Q4 2026, showing the cumulative cash-flow effect of the correction and whether restated operating cash flow for 2023-2024 materially differs from what was originally reported.
- Already visible today: Partly, and it cuts AGAINST the counter. Two things are already visible that a pure timing error would not produce. First, the review WIDENED rather than narrowed: the February 4.02 covered three 2025 quarters, and the May 4.02 extended it to two additional full fiscal years, which is the signature of a systemic process failure rather than one misposted accrual. Second, and decisively, the company has pre-announced an OPERATING LOSS for H1 2026 - a period entirely outside the restated years, prepared under current management scrutiny. A business whose current, unrestated half-year is loss-making does not support a $231.6M normalized cash-flow base whatever the restatement concludes. The counter also cannot survive the share-count error below, which is independent of the accounting entirely.
- Left unresolved: The magnitude of the restatement's cash-flow effect, which no public document discloses and which will not exist until the Q4 2026 filings. I record that I could not size it rather than guessing.

**Key risks.** Nasdaq Staff Delisting Determination expected; retention depends on a Hearings Panel appeal and on filing by the amended 2026-11-30 credit-agreement deadline; Restatement has already widened once (three 2025 quarters -> also FY2024 and FY2023); it may widen again; H1 2026 operating loss on higher fuel, rail and drayage costs in ITS and excess Consolidation and Fulfillment capacity in Logistics; Securities litigation and SEC enforcement risk normally follow a two-stage Item 4.02; No audited financial statements for FY2025 exist at all
**Watch for.** Filing of the FY2025 10-K with restated FY2024 and FY2023 - the first point at which any input to this model becomes usable; Nasdaq Hearings Panel decision on the delisting appeal; Whether restated operating cash flow for 2023-2024 differs materially from the originally reported figures the engine is using

**Data quality.** Neither flagged defect was resolved in the engine's favour; both are confirmed and both are fatal. (1) share_count_5809d_stale_market_cap_unreliable is real and is the single largest input error in today's ten. shares_asof is 2026-10-21 in the extract but dated 2010-10-21 - a SIXTEEN-year-old, un-dimensioned fact, exactly the dual-class failure LESSONS.md predicts and names HUBG as the worst case of. The 2025-09-30 10-Q cover page reads 60,578,607 Class A plus 574,903 Class B = 61,153,510 shares. The engine uses 37.3M. Market cap is therefore $2.05B, not $1.25B, and enterprise value $2.23B, not $1.44B - a 55% understatement. Correcting the share count ALONE moves the growth the market implies from -13.9% to -4.1% and collapses the +112.8% gap to roughly nothing, before any accounting question is reached. (2) last_10k_624d_old understates the problem: the issue is not that the 10-K is old but that the company has told the SEC its contents cannot be relied upon. NEW DEFECT CATEGORY: the engine does not read Item 4.02. An Item 4.02 8-K is the loudest data-quality signal EDGAR emits - the filer's own statement that its financial statements are materially misstated - and HUBG filed TWO of them, on 2026-02-05 and 2026-05-12, covering precisely the fiscal years the FCFF base is built from. It still won an opportunistic slot at the 90th percentile of 151 Industrials. Item 4.02 should be a hard gate, not a flag. The multiples table is also unusable: it divides by the same corrupted share count.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/940942/000119312526039396/d77454d8k.htm
- https://www.sec.gov/Archives/edgar/data/940942/000119312526218141/d146211d8k.htm
- https://www.sec.gov/Archives/edgar/data/940942/000119312526391228/d137221dex991.htm
- https://www.sec.gov/Archives/edgar/data/940942/000119312525266623/hubg-20250930.htm
- https://www.globenewswire.com/news-release/2026/09/14/3360965/0/en/hub-group-announces-select-preliminary-first-and-second-quarter-2026-financial-results-and-provides-update-on-restatement-process.html
- https://www.freightwaves.com/news/hub-group-warns-of-nasdaq-delisting-notice-flags-h1-operating-loss

**Ingestion notes.** no usable final_growth
