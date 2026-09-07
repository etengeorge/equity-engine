# UEC — URANIUM ENERGY
*Energy · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-07 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $11.54
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Nobody buying UEC at $11.54 is buying trailing cash flow — there is none. They are buying licensed capacity in the right jurisdiction at the right moment: roughly 12 million pounds of annual licensed capacity, which is what Jefferies cited when it initiated coverage on 2026-09-03, positioned into a US re-shoring policy push and a reactor build-out narrative. Burke Hollow, the largest US greenfield in-situ recovery project to enter production in more than a decade, has commenced production, and new header houses are producing at Christensen Ranch. The balance sheet supports the wait: $794M of liquid assets including $488M of cash, no debt, and 1,456,000 pounds of physical U3O8 worth $127M at market. The bull case is a real option — capacity plus inventory plus no debt, exercised if the uranium price and the ramp both arrive. The market pays $5.7B for that option.

**What changed.** The ramp is starting and the revenue is not. Trailing twelve-month revenue to 2026-04-30 was $20.2M, down 70% year over year, and the quarter ended 2026-04-30 produced $0.0M of revenue against an $8.6M consensus. The only meaningful sale in the period was 200,000 pounds at $101/lb in fiscal Q2 for $20.2M of revenue and $10.0M of gross profit. Coverage initiations and sector flows have driven the tape (the 21d return is +7.2% while the 63d is -8.8%), not company results.

**Base case.** There is no cash-flow base to grow. The company generated no revenue in its most recent reported quarter and the normalized FCFF is not positive. Stating a five-year FCFF growth rate here would be inventing a fair value for a name the model has correctly refused, which is the one thing the rules forbid outright.

**Devil's advocate.**
- Strongest counter: The strongest case against refusing is that a producer with a ramping asset base is not the same as a pre-revenue biotech, and that a defensible net-asset-value model — pounds of proven resource times a long-run realised price less operating and capital cost — exists and is what every sell-side analyst on the name actually uses. That is true, and it is a real method. It is also not a method this engine has, and it is not one I can execute honestly from the disclosure available to me: it requires per-pound operating cost at each ISR wellfield, capital cost to bring the remaining capacity online, and a long-run contracted price, none of which I have. Building a rough version and calling it a fair value would be manufacturing precision on the most sentiment-driven cohort in the index.
- What would prove it: Realised pounds sold and cash cost per pound over the next three to four quarters as Burke Hollow ramps, and the contract book: how many pounds are committed to utilities, at what price, over what term.
- Already visible today: The tape is telling. The 24/7 Wall St pieces in late August describe nuclear equities moving 5-7% in a day on 'risk appetite' and 'sector positioning rather than new company specific announcements'. Trefis put it precisely: the stock is priced on pounds it has not sold yet, on about $20M of trailing revenue that 'rounds to zero in the billions the company reports'. That is a fair description of what the market cap rests on.
- Left unresolved: The all-in sustaining cost per pound at the ramping wellfields. Without it I cannot say whether 12 million pounds of licensed capacity is worth $5.7B or a fraction of it, and neither can the multiples table.

**Key risks.** $5.7B market cap on $20.2M of trailing revenue and zero revenue in the most recent reported quarter; Execution risk on the ISR ramp at Burke Hollow and Christensen Ranch; Uranium price and contracting terms are the whole valuation and neither is under company control; The name trades on nuclear-sector sentiment: 5-7% single-day moves on positioning rather than news
**Watch for.** Fiscal 2026 annual results (year ended 2026-07-31) — realised pounds, realised price, and cash cost per pound; Any multi-year utility contract disclosure with stated volumes and pricing

**Data quality.** All five flags are correct and collectively they are the answer: `nonpositive_normalized_fcff`, `negative_fcf_year_in_window`, `lumpy_fcff_spread_5.1x_of_mean`, `negative_ebitda_valued_on_revenue_or_gross_profit_only` and `speculative_cost_of_debt_but_only_0%_debt_weight`. The reverse DCF correctly returns n/a. The multiples table must be disregarded, and its own numbers say so: UEC trades at 78.1x EV/sales against a cohort median of 2.4x, and 213.3x EV/gross profit against a median of 8.2x, because the denominator is $20.2M of trailing revenue for a company whose production has not arrived. CLAUDE.md names this case exactly — 'treat a multiples number on a pre-revenue name with suspicion; EV/sales on a company whose revenue has not arrived yet is close to meaningless, and the model will still print it.' The blended midpoint of $2.56 against a price of $11.54 is not a 78% overvaluation finding, it is a division by a number that has no meaning yet, and the cohort is 'not ranked' besides. The only row carrying information is p_tbv at 4.0x, and tangible book for a developer is capitalized mineral property, not earning power. One minor inconsistency I could not resolve: the brief dates the balance sheet 2026-04-30 and labels the source a 10-K, but UEC's fiscal year ends 31 July, so that period is a 10-Q — the form classifier appears to have mislabelled it. It does not change the conclusion.

**Sources.**
- https://www.prnewswire.com/news-releases/uranium-energy-corp-reports-results-for-the-third-quarter-of-fiscal-2026-302794776.html
- https://www.prnewswire.com/news-releases/uranium-energy-corp-reports-results-for-second-quarter-of-fiscal-2026-302708835.html
- https://www.trefis.com/articles/612595/uranium-energy-stock-is-priced-on-pounds-it-has-not-sold-yet/2026-08-24
- https://finance.yahoo.com/markets/stocks/articles/uranium-energy-rose-jefferies-started-121900247.html
- https://stockanalysis.com/stocks/uec/revenue/

**Ingestion notes.** no usable final_growth
