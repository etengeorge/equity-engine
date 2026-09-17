# SFBS — SERVISFIRST BANCSHARES INC
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $41.28

**The case for the price.** ServisFirst is an exceptional operator — 1.90% ROAA, a 29.7% efficiency ratio, 23% organic asset CAGR since 2005, tangible book per share up at least 10% every year since founding. At an honest 2.30x tangible book the market is paying a deserved premium for a branchless commercial bank compounding book value in the mid-teens. The market is NOT pricing this at 1.23x; that figure is an artifact (below).

**What changed.** THE DECISIVE FACT IS A STOCK SPLIT THE ENGINE CANNOT SEE. On 2026-07-20 the Board declared a TWO-FOR-ONE split effected as a 100% stock dividend, record date 2026-08-05, distributed ~2026-08-20, trading post-split from ~2026-08-21 (10-Q Note, 'Stock Split'). Shares go from ~54.7M to ~109.3M. The 10-Q states plainly that all share and per-share amounts in it 'are presented on a pre-split basis'. The engine's shares_asof is 2026-08-04 — ONE DAY BEFORE the record date — so it holds the PRE-split 54,672,510, while the yfinance price series IS split-adjusted at $41.28. Market cap is therefore $2.26B against a true $4.51B, and tangible book per share reads $33.59 (pre-split, and also the stale FY2025 figure) against a true post-split $17.97. Separately, asset quality has deteriorated sharply: NPAs/assets went 0.14% (2023) -> 0.26% (2024) -> 0.97% (2025) -> 0.96% (6/30/26), a sevenfold rise, with the credit loss reserve flat at ~1.26% of gross loans.

**Base case.** No fair value is supplied because the model's market capitalisation is wrong by exactly the split factor and the schema has no field to override a share count. On corrected inputs: tangible common equity $1,964,803k over 109,342,046 post-split shares is $17.97 per share, so actual P/TBV is 41.28/17.97 = 2.30x, not 1.23x. Against a justified multiple of 1.42 at the engine's 14.58% ROTCE — or 1.58 to 1.79 at the company's own current return on average common equity of 16.0% (FY2025) to 17.81% (1H26) — the gap runs MINUS 22% to MINUS 38%. The +15.8% gap and the 88.5th percentile rank of 339 Financials do not shrink, they invert. Supplying a ROTCE would launder a 2x share-count error into a published fair value, which is precisely what the PIPR/WLTH rule forbids.

**Devil's advocate.**
- Strongest counter: The counter here WON and reversed the screen's conclusion, so the roles are inverted: the bull case was the engine's own +15.8% gap at the 88th percentile, i.e. a high-performing bank at 1.23x tangible book. Running the standing AII/BUR check — reconcile tangible_book_per_share to the company's own disclosure — killed it. ServisFirst reports $35.94 of tangible book per share at 6/30/2026 on a PRE-split basis against an engine price that is POST-split. One of the two numbers had to be converted and neither was.
- What would prove it: The 10-Q subsequent-events note, and whether shares_asof precedes the split record date.
- Already visible today: Yes, and twice over. The company's own investor deck states the 6/30/2026 closing price was $86.75 while the engine carries $41.28 with a 63-day return of +1.5% — a factor of ~2.1 that no price move explains. And the 10-Q says the split in terms: 'the number of shares of common stock issued and outstanding will increase from approximately 54.7 million to approximately 109.3 million.'
- Left unresolved: How many other book-method names in this screen carry the same defect. A forward split always understates market cap and manufactures cheapness, and the analyst runtime cannot reach a split calendar to scan for it.

**Key risks.** NPAs/assets rose sevenfold in two years to 0.96% with no matching reserve build; NIM expansion to 3.58% is rate-cycle dependent and reverses as rates fall; loans/deposits at 98% versus 87% in 2023 — the balance sheet is fully lent; concentrated Alabama/Southeast commercial and CRE exposure run with almost no branch infrastructure
**Watch for.** the 3Q26 10-Q cover page, which will carry the post-split ~109.3M count and silently repair the engine's market cap; whether the credit loss reserve is built toward the 0.96% NPA level, which would cut the ROTCE that the whole valuation rests on

**Data quality.** RESOLVED: 'none raised' was wrong — there are two defects and no flag fired for either. (1) A 2-for-1 stock split effective ~2026-08-21 against a shares_asof of 2026-08-04, so a split-adjusted price is divided by an unsplit share count; market cap $2.26B vs a true $4.51B and P/TBV 1.23 vs a true 2.30. No staleness test can catch this — the share date is six weeks old and looks fine; the test is shares_asof against the split RECORD date, the same shape as the MCFT item-2.01 rule. (2) The stale-tangible-book bug is also present: justified_pb prices against equity_series[0] of $1,849,847k (FY2025) while equity_now is $1,977,918k, a 6.9% divergence. OPEN: no universe-wide scan for other split-affected names was possible from this runtime. The AX numerator check PASSES (net_income_common_series matches net_income_series to within $62k of preferred).

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1430723/ (10-Q for the quarter ended 2026-06-30, filed 2026-08-07 — Stock Split note and balance sheet)
- 8-K EX-99.1/EX-99.2 filed 2026-07-20 (investor presentation: key operating metrics, GAAP reconciliation, asset quality history, 6/30/2026 closing price $86.75)
- data/screen.json and data/fundamentals.json (engine inputs as recorded)

**Ingestion notes.** no usable final_growth
