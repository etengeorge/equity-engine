# ITRI — ITRON
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-18 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $91.38 · fair value $100.83 · gap +10.3%
- **Growth:** market implies +8.8%, analyst says +5.0% (delta -3.8%)
- **FCFF base overridden** by the analyst to $300.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 6.6% | 7.6% | 8.6% | 9.6% | 10.6% |
|---|---|---|---|---|---|---|
| bear | +0.0% | $119.03 | $94.53 | $77.43 | $64.83 | $55.15 |
| base | +5.0% | $153.80 | $122.59 | $100.83 | $84.80 | $72.50 |
| bull | +10.0% | $195.53 | $156.21 | $128.82 | $108.66 | $93.20 |

At the point WACC of 8.6%: bear -15.3%, base +10.3%, bull +41.0%
Across the whole grid the gap ranges -39.7% to +114.0% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Itron sells the metering, networking and grid-edge software that utilities are obliged to deploy, and it is converting a hardware franchise into a higher-margin outcomes business. Second-quarter 2026 brought record gross margins, and management raised non-GAAP diluted EPS guidance to $6.30-6.50 from the $5.75-6.25 set in February while narrowing revenue to $2.37-2.41 billion. Backlog stands at $4.4 billion, roughly 1.8x annual revenue, which is unusual visibility for an industrial. At $91.38 the shares trade on about 14x the midpoint of that EPS guide after falling 22% over the last year, so the market is not paying for the grid-investment narrative — it is paying about a market multiple for a company whose revenue grows 1% and whose earnings grow because margins do.

**What changed.** Nothing in the news store — no company-specific items in 90 days, which lowers my confidence that nothing happened rather than confirming it. From the filings: total debt rose to $1,610,000 thousand at 2026-06-30 from $1,265,000 thousand at 2025-12-31, the February 2026 convertible notes issue (8-K 2026-02-26, items 1.01/2.03/3.02), and cash fell to $745.2 million from $1,020.4 million. First-half cash from operations was $173,592 thousand against $168,802 thousand a year earlier, essentially flat; second-quarter free cash flow was $81 million against $91 million, the decline attributed to higher tax payments and lower interest income. I could NOT establish why the stock is down 22% over twelve months or why it fell about 7% on a quarter that raised EPS guidance, and that gap is the main reason conviction is capped.

**Base case.** Mid-single-digit FCFF growth. Revenue grows about 1% and will not do much better: Device Solutions is flat to declining and the growth is in Networked Solutions and Outcomes. What compounds is margin and mix, and Itron has proved it can do that — the EPS guide was raised 8% on a reaffirmed revenue guide. But gross margins are described by the company as records, so the runway for further expansion is finite, and I will not extrapolate a second doubling. 1% of volume plus continued but decelerating mix gain, less the stock compensation the reported figure treats as free, nets to about 5%.

**Devil's advocate.**
- Strongest counter: I have marked the cash-flow base UP by 27% from the engine's $235.8 million and then called the result cheap-to-fair, which is the exact move the standing lessons warn against. Revenue grows 1%. Gross margins are at records by the company's own description. A base built on the current run rate assumes those records hold for five years, and the stock is down 22% because the market does not believe they will. On the engine's own base the market asks +8.8% from a 1%-growth company, and that is demanding — the honest verdict is rich.
- What would prove it: Whether the newest year in the window is a peak to be discounted or a normal level to be kept — i.e. whether $383.1 million of free cash flow in the most recent year is the anomaly or $98.1 million in the oldest one is.
- Already visible today: Yes, and it decides the question against the flag. The series is [$98.1M, $207.6M, $383.1M] oldest to newest — a monotonic RECOVERY out of the 2023 supply-chain trough, not a cycle peak, and the `possible_peak_cycle_base` flag reads it backwards for the same reason the trough flag has been wrong before. First-half 2026 cash from operations of $173.6 million is flat against the prior year, so the newest level is holding rather than rolling over. The mean of the three is dragged down by one abnormal year, so the engine's base UNDERSTATES current generation. The counter is right that I should not use the full run rate, and I have not: $300 million is the FY2026 pace less a stock-compensation charge, not the roughly $370 million the first half implies.
- Left unresolved: Why the stock fell 22% in a year and about 7% on a guidance raise. There is no company news in the store and I found no explanation. Something is being priced that I cannot see, and that is an argument for humility, not for either verdict.

**Key risks.** Revenue growth of 1% — everything depends on margin, and margin is at record levels by the company's own description; The `possible_peak_cycle_base` flag is pointed the wrong way, which means a reader who acts on it will underestimate the base rather than overestimate it; A 22% twelve-month decline and a ~7% fall on a raised EPS guide that I could not explain; Convertible notes issued February 2026 lifted debt to $1.61bn; these are captured in enterprise value, but the conversion dilution is not in the share count
**Watch for.** Full-year 2026 free cash flow against the roughly $370 million the first half implies — the number that settles the base; Gross margin sequentially: the first quarter of compression turns this rich; Backlog conversion and bookings, the read on whether $4.4 billion is a durable pipeline or a pull-forward

**Data quality.** One flag, and it is inverted. `possible_peak_cycle_base_newest_fcf_3.9x_oldest` is technically true and analytically backwards: [$98.1M, $207.6M, $383.1M] is a supply-chain recovery ramp, so the correct reading is that the OLDEST year is the anomaly and the three-year mean understates. I verified enterprise value independently — $4.0bn of market capitalisation plus $1,610,000 thousand of total debt less $745.2 million of cash is $4.87bn, matching the engine's $4.9bn — so unlike TENB and MGY the February convertible IS captured and there is no missing-debt bug. My base override of $300 million is the FY2026 run rate less roughly $65 million a year of stock compensation; at that base the market requires about +4% rather than +8.8%, against my +5%, which is inside the noise band. The -31.4% 'rich' gap on the brief is the +1.7% naive revenue baseline and carries no judgment.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/780571/000078057126000178/itri-20260630.htm
- https://www.sec.gov/Archives/edgar/data/780571/000117184326004912/exh_991.htm
- https://na.itron.com/w/itron-announces-second-quarter-2026-financial-results
- https://www.investing.com/news/company-news/itron-q2-2026-slides-record-margins-offset-revenue-decline-93CH-4817480
