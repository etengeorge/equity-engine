# FG — F&amp;G ANNUITIES AND LIFE INC
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-04 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $24.87

**The case for the price.** F&G is a fast-growing annuity and life platform (assets approaching $75B, gross sales compounding, an owned distribution and pension-risk-transfer flywheel) that is 85% owned by FNF and trades at roughly 0.54x its own reported ex-AOCI book value of $45.93 per share. The market pays a low multiple because spread-based annuity earnings are levered to credit and alternative-investment returns, because the free float is small and the FNF overhang is permanent, and because Q2 2026 adjusted net earnings of $85M ($0.65/share) missed on weaker alternative-investment returns and a reinsurance transaction. At an 8.0% adjusted ROE excluding AOCI against a ~9.1% cost of equity, a discount to book is the arithmetically correct price, not a mistake.

**What changed.** Q2 2026 (reported 2026-08-05): adjusted net earnings $85M / $0.65 per share, adjusted ROA 68bp, and — decisively for this model — adjusted ROE excluding AOCI of 8.0%. Total F&G equity attributable to common shareholders excluding AOCI was $6.0B, or $45.93 per share at 2026-06-30, up $1.50/share from 2025-12-31. Management attributed the quarter's softness to lower alternative-investment returns and the impact of a reinsurance transaction. Quarterly dividends declared on both the common and the Series A mandatory convertible preferred on 2026-08-06.

**Base case.** I do not produce a base case for this name, because the model the engine applied to it does not describe the company. The justified-P/TBV route prices a sustainable ROTCE against tangible common equity; on F&G both terms are artifacts. See below.

**Devil's advocate.**
- Strongest counter: The strongest case for engaging rather than refusing is that F&G is genuinely cheap on the numbers that DO describe it: 0.54x ex-AOCI book, an 8% adjusted ROE that management guides toward the low double digits as the in-force book seasons and alternative returns normalize, and a stock down 26.5% over twelve months. If sustainable ROE recovers to 11-12% against a ~9.1% cost of equity, book-value-plus is the right price and the stock is materially below it. Refusing to model the name means declining to say that.
- What would prove it: Four to six quarters of adjusted ROE ex-AOCI printing 11%+ with alternative-investment returns at or above their long-run assumption, plus stable ex-AOCI book value per share growth; and an engine-side fix that reads insurer equity ex-AOCI and stops treating FNF purchase-accounting goodwill as a deduction from the earning capital base.
- Already visible today: The opposite is visible: the most recent print is 8.0%, below the ~9.1% cost of equity the engine assigns, and it was reached with the help of a reinsurance transaction. Nothing in the current disclosure supports the 31.7% the screen used.
- Left unresolved: I could not determine what a defensible sustainable ROE for F&G actually is, because that requires a view on alternative-investment returns and FIA spread compression that I have not built. That is precisely why this is no_model rather than a number I am 60% confident in.

**Key risks.** Spread compression on fixed indexed annuities if rates fall faster than crediting rates reset; Alternative-investment returns below plan — already the named cause of the Q2 miss; Credit losses in a $75B portfolio that is not marked through earnings; FNF's ~85% ownership: minority holders do not control capital allocation or a sale; Mandatory convertible preferred dilution
**Watch for.** Adjusted ROE excluding AOCI sustaining above 11% for four consecutive quarters; Ex-AOCI book value per share growth stalling, which would signal the 8% is the ceiling not the floor; Any FNF action on the stake (spin, buy-in, secondary), which would reprice the float discount

**Data quality.** Resolved and fatal. All four engine flags are live and they compound: (1) `unstable_rotce_12.0%_to_51.4%` — I reproduced this from the stored extract. The 31.7% is the mean of exactly TWO observations, 12.0% (2025) and 51.4% (2024). The third year is excluded because tangible common equity computes NEGATIVE in 2023 (equity $3,103M less goodwill $1,749M less intangibles $4,207M = -$2,853M). A denominator that goes negative is not a capital base. (2) The intangibles series runs $4,207M -> $562M -> $551M across three years, a 7.5x collapse that is a concept switch in the extract, not a write-off, and it is what makes the 2024 denominator small enough to print 51.4%. (3) `goodwill_and_intangibles_56%_of_book`: TCE is a residual of large subtractions of FNF purchase-accounting balances, so small changes in the subtrahend swing the ratio violently. (4) The company's own Q2 2026 release reports adjusted ROE excluding AOCI of 8.0% and ex-AOCI common equity of $45.93 per share, against the engine's 31.7% ROTCE and $15.83 tangible book per share. Both engine inputs are wrong, in opposite directions, and the +166% gap is the product of the two errors. This is the JXN pattern in research/LESSONS.md (GAAP net income is not a return for anything whose earnings are a mark) made worse by a tangible-book construction that is meaningless for a life insurer, where AOCI on the bond portfolio is the dominant swing item. Also unresolved: `speculative_cost_of_debt_at_41%_debt_weight_wacc_unreliable`. I did not fetch the 10-Q line by line because the press release already settled the question.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.prnewswire.com/news-releases/fg-annuities--life-reports-second-quarter-2026-results-302843953.html
- https://www.sec.gov/Archives/edgar/data/0001934850/000193485026000081/a2q26fgearningsrelease_f.htm
- https://finance.yahoo.com/markets/stocks/articles/f-g-annuities-life-q2-070408966.html
- https://www.sec.gov/Archives/edgar/data/1934850/000193485026000085/fg-20260630.htm
- data/adhoc/FG/ (2026-08-05 8-K and exhibits, fetched via adhoc-fetch)
- data/fundamentals.json CIK 1934850 (stored EDGAR extract, v5)

**Ingestion notes.** no usable final_growth
