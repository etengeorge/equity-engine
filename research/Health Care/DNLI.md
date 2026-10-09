# DNLI — DENALI THERAPEUTICS
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-10-09 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $18.67
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Denali is eight months into its first commercial launch and the market is pricing execution, not cash flow. AVLAYAH (tividenofusp alfa) received accelerated FDA approval in March 2026 for Hunter syndrome (MPS II), commercial distribution began in April 2026, and Q2 2026 net product revenue was $3.6 million against a guided $10-12 million for Q3. At $18.67 the stock is roughly 29% below its 52-week high of $27.30 and has fallen 27.3% over 63 days while remaining +25.3% over 252 days. The bear case the market is expressing is specific and reasonable: an ultra-rare enzyme-replacement launch is a slow, patient-identification-limited ramp; the Q2 loss of $0.68 per share was worse than the roughly $0.51 expected even as revenue beat a $2.15 million consensus; and the company still funds a broad neurodegeneration pipeline whose value is entirely in the terminal. A company with $14 million of annualised product revenue, a widening loss and a multi-year path to profitability is priced on probability-weighted pipeline value, which is not something a free-cash-flow model computes.

**What changed.** Two material items the engine knows nothing about, both after the 2026-06-30 balance sheet it priced. (1) Denali sold its Rare Pediatric Disease Priority Review Voucher — awarded on AVLAYAH's March 2026 approval — for GROSS PROCEEDS OF $195.0 MILLION IN CASH, under an asset purchase agreement dated 2026-06-12 (8-K item 1.01, filed 2026-06-18) that CLOSED on 2026-07-27 (8-K item 2.01, filed 2026-07-28). That $195M landed in Q3, one month after the balance sheet date the engine uses, so the enterprise value in this brief is overstated by roughly that amount. (2) The launch itself: Q2 net product revenue $3.6M, Q3 guided $10-12M. I could NOT find a single dated catalyst for the -27.3% 63-day move; the coverage I read attributes it to launch-metric derating and to profit-taking after a July run, and several of those sources are low-quality aggregators whose dates do not reconcile. I am recording that the move is unexplained rather than inventing a cause.

**Base case.** No base case and no fair value. The engine's gates are right: `negative_fcf_year_in_window`, `nonpositive_normalized_fcff` and `negative_ebitda_valued_on_revenue_or_gross_profit_only` all fired and the model failed. A company burning cash in every year of the window has no FCFF to grow.

**Devil's advocate.**
- Strongest counter: The strongest counter to refusing is that the multiples path is not empty here — the engine computed a revenue-and-gross-profit valuation — and that a $195M cash receipt the model cannot see is exactly the kind of correction an analyst is for: adjust the enterprise value down by $195M, apply the cohort's EV/sales, and you have a number. If the correction makes the name cheap, saying 'no_model' hides a real finding.
- What would prove it: Whether the EV/sales row is meaningful on this denominator. It is not, and that is checkable rather than arguable.
- Already visible today: Yes, and it defeats the counter. The multiples denominator is trailing revenue that PREDATES the launch almost entirely — $3.6M in the first full commercial quarter against a product that was approved in March 2026 — so EV/sales on this company is the documented AXTI/MXL condition in research/LESSONS.md: a multiple whose denominator describes a company that no longer exists. Gross profit is barely positive and EBITDA is negative, so two of the rows are unusable by construction. Correcting the enterprise value by $195M would make a meaningless ratio 7% less wrong, not meaningful. I therefore accept the counter's factual point — the EV IS overstated by roughly $195M — and still refuse the valuation.
- Left unresolved: The cause of the -27.3% 63-day move. I searched and found only derating commentary, no dated event, and I did not find an 8-K after 2026-08-06. An unexplained 27% decline on a name I am refusing to value is a gap in my confidence, not in the verdict.

**Key risks.** Accelerated approval carries a confirmatory-trial obligation; failure would withdraw AVLAYAH; Launch ramp below guidance in an ultra-rare indication where patient identification, not demand, is the constraint; Continued cash burn against a broad neurodegeneration pipeline; the $195M PRV sale funds it but does not change the burn; An unexplained 27% three-month decline that I could not attribute to any disclosed event
**Watch for.** Q3 2026 net product revenue against the $10-12M guide — the single number that settles the launch debate; Confirmatory trial enrolment and data for AVLAYAH's full approval; Any 8-K between 2026-08-06 and today that would explain the 63-day decline

**Data quality.** All three engine flags are correct and none is a defect. RESOLVED by filing: the enterprise value is overstated by roughly $195M because the PRV sale closed 2026-07-27, one month after the 2026-06-30 balance sheet the extract uses — and no flag fires for a receipt that lands after the balance sheet date. The multiples table is disqualified on its denominator rather than its arithmetic: trailing revenue predates a March 2026 approval. UNRESOLVED: the 63-day price move has no cause I could find in a filing or a credible source, and the secondary sources I did read were aggregator-quality with inconsistent dates, so the launch figures above ($3.6M Q2, $10-12M Q3 guide, $0.68 Q2 loss) are corroborated secondary reporting rather than figures I read off the 10-Q line by line.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- data/adhoc/DNLI/2026-07-28-8-K-dnli-20260727.htm.txt (item 2.01, PRV sale completed, $195.0M gross proceeds; fetched via adhoc-fetch)
- data/adhoc/DNLI/2026-06-18-8-K-dnli-20260612.htm.txt (item 1.01, PRV Transfer Agreement)
- data/adhoc/DNLI/2026-08-06-EX-99.1.txt (Q2 2026 results release)
- https://www.stocktitan.net/news/DNLI/denali-therapeutics-reports-first-quarter-2026-financial-results-and-y2zga4tq6yew.html
- https://finance.yahoo.com/healthcare/articles/recent-setbacks-impact-growth-prospects-170200645.html
- data/picks.json row for DNLI (screen 2026-10-09, prices as of 2026-10-08)

**Ingestion notes.** no usable final_growth
