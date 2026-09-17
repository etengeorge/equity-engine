# MRX — MAREX GROUP LTD
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_MODEL (conviction: low)

- **Verdict:** no_model · price $72.38

**The case for the price.** Marex has compounded hard — the stock is up 124.8% over twelve months — and the market is paying 5.7x tangible book for a diversified commodities broker earning above 30% on tangible equity, with clearing, hedging and market-making franchises that scale with volatility and have been winning share. For a capital-light agency broker that return can persist, and 5.7x book is what that looks like.

**What changed.** NOTHING COULD BE ESTABLISHED, AND THAT IS THE FINDING. Marex Group is a foreign private issuer: its last annual report is a 20-F for the year ended 2025-12-31 and its interim reporting comes on Form 6-K, which this engine does not index. The brief's 'Recent filings' section is consequently empty, and an adhoc-fetch dispatch for this ticker returned an index with ZERO documents. I therefore have no 2026 interim balance sheet, no first-half results and no current share count, and I did not substitute a guess for them.

**Base case.** No ROTCE is supplied because every input to the justified multiple fails a standing check at once. The 'sustainable ROTCE' of 33.1% is not an average of a series: equity_series contains exactly ONE observation ($1,166.2M), net_income_series contains two ($307.7M, $218.0M), and net_income_common_series is EMPTY — so the AII n=1 rule applies in its strongest form, and unstable_rotce cannot fire because a one-observation return has no range. The balance sheet is 260 days old and is the 20-F year-end, so it predates two quarters of a business whose balance sheet turns over continuously. Actual P/TBV of 5.68x is above the ~4x PIPR threshold at which price-to-tangible-book stops describing the business, and for a broker-dealer that is genuinely arguable in both directions — regulatory capital IS a real constraint on a clearing broker, unlike an advisory firm — but I cannot resolve it without the interims. Finally, intangibles are recorded as zero and intangibles_series is empty for a company whose goodwill grew from $176.5M to $237.4M through acquisitions, which overstates tangible book and understates actual P/TBV. The recorded gap of -9.7% is small enough that any one of these defects swamps it.

**Devil's advocate.**
- Strongest counter: That a 33% return on tangible equity and only a -9.7% gap means the model is roughly right and I am refusing a name that is simply fairly priced — a refusal that costs nothing and teaches nothing.
- What would prove it: The 2026 half-year results on Form 6-K: current tangible equity, the return actually earned in the first half, and the share count.
- Already visible today: No. That is the point. The engine cannot index 6-K filings and the adhoc-fetch path returned nothing for this ticker, so there is no free route from this runtime to a Marex interim. This is a fact about my confidence and I am recording it rather than filling the gap.
- Left unresolved: Whether a 33% return earned on a single observed year is a franchise return or a volatility-cycle return, and what the current tangible book is. Both are unanswerable from what I could reach.

**Key risks.** a 124.8% twelve-month move means a great deal of good news is already in the price; broker earnings scale with commodity volatility, which is itself cyclical; no interim financial information is reachable by this engine at all; tangible book is overstated by intangibles recorded as zero against an acquisitive history
**Watch for.** a 2026 interim on Form 6-K, and whether the engine's extractor is ever taught to read 6-K and 40-F filings; the first year in which equity_series carries more than one observation

**Data quality.** RESOLVED: balance_sheet_260d_old is real and compounded by the filer type — Marex is a 20-F filer whose interims come on 6-K, which the engine does not index, so the 'Recent filings' section is empty and an adhoc-fetch returned zero documents. This is the BIPC pattern: no filing route exists to check this name by hand. rotce_33%_suggests_asset_light is also real: actual P/TBV of 5.68x is above the PIPR ~4x threshold. NEW AND UNFLAGGED: equity_series has length ONE and net_income_common_series is EMPTY, so the 33.1% 'sustainable' return is a single observation — the AII rule — and no flag can fire on it. intangibles is recorded as 0.0 with an empty series despite goodwill growing $176.5M to $237.4M, which overstates tangible book. No number is supplied.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- data/adhoc/MRX/index.json — dispatched 2026-09-17, returned zero documents (20-F/6-K filer, not indexed)
- data/fundamentals.json and data/screen.json (engine inputs as recorded: equity_series length 1, empty net_income_common_series and intangibles_series)
- briefs/MRX.md (empty Recent filings section)

**Ingestion notes.** no usable final_growth
