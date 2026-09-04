# GATX — GATX
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-04 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $177.31
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** GATX is a railcar lessor, and a lessor's economics are the opposite of the free-cash-flow signature this model looks for: it deliberately spends more on railcars than it collects in lease rentals in any year it is growing the fleet, and the value accrues in the asset base and the lease book rather than in reported free cash flow. On the metrics that do describe it the business is in excellent shape — Q2 2026 EPS of $2.84 against $2.06, full-year 2026 guidance RAISED to $9.90-10.30, Rail North America segment profit of $118.5M versus $96.6M, 98% fleet utilisation, a lease price index up 16.8% and renewal success of 82.6%. At $177.31 the market is paying roughly 17.5x guided earnings for a hard-asset lessor at the strong point of a lease-rate cycle, with the Wells Fargo Rail portfolio acquired alongside Brookfield now expected to deliver at least double the original $0.20-0.30 per share contribution. That is a reasonable price, not an anomaly.

**What changed.** The Wells Fargo Rail asset acquisition with Brookfield Infrastructure completed in January 2026, which is inside the model's window and is exactly the kind of transaction that makes a historical cash-flow series incomparable. Q2 2026 (reported 2026-07-30, 8-K items 2.02/7.01/9.01): EPS $2.84 versus $2.06; full-year 2026 guidance raised to $9.90-10.30 per diluted share; Rail North America segment profit $118.5M versus $96.6M; fleet utilisation 98%; lease price index +16.8%; renewal success 82.6%. Gains on asset dispositions of $67.7M in the quarter and $117.5M year to date, ahead of expectations — the legacy portfolio is running well ahead of its $130M full-year target at $118M year to date, and the joint venture generated about a third of its $70M target in Q2. Management now expects the Wells Fargo joint venture to contribute at least twice its original 2026 estimate. No company-specific news in the engine's store for 90 days, so none of the above reached the brief.

**Base case.** No base case. The engine's normalised FCFF is non-positive and there is no honest way to make it positive, because CFO less capex is structurally negative for a growing lessor — railcar purchases are the business, not a discretionary investment. A five-year FCFF growth rate applied to a negative base is meaningless. The correct instruments for this company are earnings and book value against the lease book, and neither of the engine's two routes offers them.

**Devil's advocate.**
- Strongest counter: The case against refusing is that GATX is not genuinely unmodellable, only unmodellable BY THIS ENGINE. A lessor is straightforwardly valued on earnings power against its lease book and on the market value of its fleet versus its carrying value, and on those measures I could form a view: 17.5x guided earnings, a lease price index still rising 16.8%, and disposition gains running ahead of plan. Declining to value it means the rotation slot produced nothing.
- What would prove it: It is not a question of proof but of instrument. What would change the verdict is an engine that prices lessors on book and earnings rather than on CFO less capex — the same gap that produced no_model on WLFC.
- Already visible today: The relevant facts are all visible and I have recorded them; what is absent is a defensible model to put them through.
- Left unresolved: I have not formed an independent view on where the railcar lease-rate cycle sits, and without that a 17.5x multiple on peak-cycle earnings could be cheap or expensive. Disposition gains at $117.5M year to date against a $130M full-year target, and a lease price index up 16.8%, both suggest late rather than early cycle, but I have not verified that against fleet supply data and I will not assert it.

**Key risks.** Railcar lease rates are cyclical; a 16.8% lease price index and record disposition gains are late-cycle indicators; Highly leveraged balance sheet by design (66% debt weight in the model's own capital structure) — refinancing risk if credit spreads widen; Wells Fargo Rail portfolio integration and the Brookfield joint-venture structure; Freight volumes are levered to industrial production, which the sector feed shows slowing in August
**Watch for.** The lease price index turning negative — the single cleanest indicator of cycle inflection for this business; Fleet utilisation falling below the mid-90s from 98%; Disposition gains normalising, which would remove a large discretionary contributor to reported earnings; Whether full-year EPS lands inside the raised $9.90-10.30 range

**Data quality.** Both flags — `negative_fcf_year_in_window` and `nonpositive_normalized_fcff` — are correct and are a structural property of a leasing business rather than a defect. The important instruction here is that the MULTIPLES BLEND MUST BE DISREGARDED, not weighted: it prints -$46.15 against a $177.31 price, a -126% gap, which is not a valuation of anything. Two of its three rows are negative across every percentile — EV/EBITDA gives -$139.12 / -$55.63 / +$66.45 and EV/sales gives -$306.49 / -$269.03 / -$191.56 — because GATX's enterprise value is dominated by roughly $9B of lease-funding debt that the cohort's asset-light industrial comparables do not carry, so subtracting net debt from a cohort-implied EV drives equity value below zero. The third row, price to tangible book at $186.21, sits 5% ABOVE the price. Rows that straddle the price in opposite directions, negative values, and a cohort the brief itself marks 'not ranked' are precisely the three conditions research/LESSONS.md sets for discarding a multiples number outright. Separately: the Wells Fargo Rail acquisition completed in January 2026 sits inside the cash-flow window and makes the historical series non-comparable in any case. The extract is otherwise sound — balance sheet 2026-06-30, share count 2026-06-30, beta 0.75 on an R-squared of 0.33.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.businesswire.com/news/home/20260105254734/en/GATX-Corporation-and-Brookfield-Infrastructure-Complete-Acquisition-of-Wells-Fargos-Rail-Assets
- https://finance.yahoo.com/markets/stocks/articles/gatx-corp-gatx-q2-2026-230211217.html
- https://finance.yahoo.com/markets/stocks/articles/why-gatx-strengthening-rail-leasing-195721200.html
- https://www.sec.gov/Archives/edgar/data/40211/000004021126000073/gatx-20260730.htm
- https://www.sec.gov/Archives/edgar/data/40211/000004021126000079/gmt-20260630.htm
- data/screen.json (multiple_valuation block for GATX)

**Ingestion notes.** no usable final_growth
