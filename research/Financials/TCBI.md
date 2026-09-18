# TCBI — TEXAS CAPITAL BANCSHARES
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-18 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $94.48 · fair value $73.82 · gap -21.9%
- **Sustainable ROTCE:** screen said +5.8%, analyst says +10.0%
- **P/TBV:** justified 0.96 vs actual 1.23 on tangible book of $76.59/share

**The case for the price.** Texas Capital is most of the way through a multi-year rebuild from a balance-sheet lender into a full-service Texas financial firm — investment banking, trading, private wealth and a treasury platform bolted onto a commercial bank. The market is paying 1.23x tangible book for the output of that rebuild plus the option on Texas itself: on 2026-09-14 the company announced it will move its corporate listing from Nasdaq to the Texas Stock Exchange, becoming TXSE's first corporate listing, with the ticker changing from TCBI to TXCP on 2026-11-09. Return on average common equity was 9.56% in Q2 2026 (9.80% adjusted) against 9.17% a year earlier, with return on average assets of 1.03% and a CET1 ratio of 12.1%. Tangible book value per share has compounded from $70.14 to $76.98 in four quarters — about 9.8% — while the company bought back stock. Paying a modest premium to book for a franchise whose returns are rising off a repositioning trough is a coherent position.

**What changed.** 8-K 2026-09-14 (items 3.01/7.01/9.01): voluntary delisting from Nasdaq and transfer of the corporate listing to the Texas Stock Exchange, with the ticker becoming TXCP on 2026-11-09. 8-K 2026-09-16 (item 5.02), an officer or director change. Two Texas Capital ETFs (TXS, OILT) became TXSE's first primary listings on 2026-09-16. None of this changes the earning power of the bank; it is a franchise and distribution story. No operational news since the 2026-07-22 Q2 release.

**Base case.** Sustainable ROTCE of 10.0%. Texas Capital carries essentially no goodwill — book value per share of $77.01 against tangible book of $76.98 — so ROTCE and ROE are the same number here, which removes a whole class of error. The last four reported quarters are 12.04%, 11.18%, 8.35% and 9.56%, an average of 10.28%, and the most recent is 9.56% with the trend DOWN over two quarters, not up. I therefore take 10.0% rather than the four-quarter average or the best quarter: this is not the VLY case of a monotonic recovery, so I have no basis for extrapolating the peak.

**Devil's advocate.**
- Strongest counter: The correction cuts both ways and I should not assume the engine is simply wrong. The 2.0% year in `unstable_rotce_2.0%_to_9.4%` was a real year in which real capital was destroyed, and the two most recent quarters — 8.35% then 9.56% — are BELOW the four-quarter average, not above it. A bank earning 10% against a 10.3% cost of equity is earning nothing above its cost of capital and should trade at roughly 1.0x tangible book. It trades at 1.23x. So the corrected answer is still rich, and calling it no_edge is an analyst being polite about a defect he just found.
- What would prove it: Whether the trailing returns are a trough being exited or a peak being left. Four more quarters of ROTCE, or management's own through-cycle target.
- Already visible today: Partly, and it strengthens the counter rather than my base case: the sequence 12.04% -> 11.18% -> 8.35% -> 9.56% is not a recovery, and adjusted returns (9.80%, 8.48%, 10.98%, 12.04%) tell the same story. I accept the counter to the extent that the corrected gap is about -22% at my 10.0%, i.e. still on the rich side, and I have recorded it that way rather than arguing it back to fair.
- Left unresolved: Whether the investment-banking revenue is durable. I could not settle it from the Q2 release and there is no company guidance in anything I could read. That is why conviction is medium rather than high, and why the verdict is no_edge rather than rich: one defensible input choice moves this answer 60 points.

**Key risks.** Return on tangible common equity of roughly 10% against a 10.3% cost of equity — the bank is earning approximately its cost of capital and trades at 1.23x tangible book; Fee income from investment banking and trading is the swing factor and is inherently cyclical; The engine's 5.8% 'sustainable' ROTCE is the ninth instance of the averaged-ROTCE defect; a reader who takes the -63.2% gap at face value is short a bank on an arithmetic error
**Watch for.** The 2026-11-09 ticker change from TCBI to TXCP and the Nasdaq delisting — the price and fundamentals pulls in this engine key off the ticker and will silently fail on this name after that date unless universe.csv is updated; Q3 2026 ROTCE: a third consecutive quarter below 10% would validate the devil's advocate and move this to rich; Any through-cycle ROTCE target from management

**Data quality.** Two flags, and I resolved both against the Q2 2026 earnings release. `unstable_rotce_2.0%_to_9.4%` is the EBC/ASB/AX/NEWT averaged-ROTCE defect again — the engine's 5.8% spans the repositioning years, against a current 9.56% (9.80% adjusted) and a four-quarter average of 10.28%. The gap moves from -63.2% at 5.8% to about -22% at 10.0% and to roughly -2% at the 12.04% peak quarter: a 60-point swing from one input. `last_10k_5193d_old` is the HWC mislabelled-fy_end case, not genuine staleness — the underlying tangible book of $76.59 reconciles to the company's filed $76.98 at 2026-06-30, within 0.5%, so the series are current even though the label is not. Both standing book-method cross-checks pass: no goodwill, and tangible book reconciles. The numerator alone was wrong.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1077428/000107742826000056/a07222026exhibit991.htm
- https://www.sec.gov/Archives/edgar/data/1077428/000107742826000059/tcbi-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1077428/000107742826000061/exhibit991-pressrelease914.htm
- https://www.usatoday.com/story/news/state/texas/2026/09/14/nasdaq-loses-texas-capitol-to-texas-stock-exchange-txse/91757142007/

**Ingestion notes.** no usable final_growth
