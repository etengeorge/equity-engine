# AVNT — AVIENT CORP
*Materials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-22 — RICH (conviction: low)

- **Verdict:** rich · price $40.44 · fair value $30.23 · gap -25.2%
- **Growth:** market implies +60.4%, analyst says +7.0% (delta -53.4%)
- **FCFF base overridden** by the analyst to $270.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 8.0% | 9.0% | 10.0% | 11.0% | 12.0% |
|---|---|---|---|---|---|---|
| bear | +2.0% | $34.00 | $26.88 | $21.53 | $17.37 | $14.04 |
| base | +7.0% | $46.02 | $37.00 | $30.23 | $24.97 | $20.76 |
| bull | +11.0% | $57.30 | $46.48 | $38.37 | $32.07 | $27.04 |

At the point WACC of 10.0%: bear -46.8%, base -25.2%, bull -5.1%
Across the whole grid the gap ranges -65.3% to +41.7% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Avient is executing well and the market is paying a normal specialty-formulator multiple for it. Q2 2026 adjusted EPS grew 20% to $0.96, beating the $0.89 guide on better-than-expected organic volume; organic sales grew 4.3%; adjusted EBITDA margin expanded 110bp to a record 18.3%; and management RAISED full-year 2026 adjusted EBITDA guidance to $575-603M and adjusted EPS to $3.10-3.25 (+10-15%). At a $5.17B enterprise value that is 8.8x guided adjusted EBITDA, which is an ordinary price for a specialty polymer formulator compounding EBITDA high single digits with both segments expanding margin. The company is also deleveraging, repaying $50M in Q2 and guiding to $100-150M for the year. Nothing about the price requires a mistake.

**What changed.** Q2 2026 (filed 2026-08-06) raised full-year adjusted EBITDA guidance to $575-603M from an implied lower range and adjusted EPS to $3.10-3.25 from $2.93-3.17. No 8-K under items 1.01, 2.01 or 3.02 in the last two quarters, so enterprise value is not invalidated by a transaction. The share count (91,719,550, dei cover page, 2026-06-30) is current. What actually changed for this model is not news at all: it is an input defect described below.

**Base case.** The engine's FCFF base is wrong by a factor of more than four and the direction is toward false richness. `interest_expense` is recorded as MINUS $115,300,000 against $1,875.8M of debt. Avient presents 'Interest expense, net ( 98.6 ) ( 105.6 ) ( 115.3 )' in parentheses in its 10-K income statement and the extractor kept the sign, so `normalized_fcff` SUBTRACTS $86.5M of after-tax interest instead of adding it: mean(cfo-capex) is $137.4M and the recorded base is $50.9M, which is $86.5M = -$115.3M x 0.75 below it, reproducing the defect to the dollar. The magnitude is also stale (it is the FY2023 figure; FY2025 was $98.6M, and the 10-K states total interest PAID on debt, net of hedging, was $97.6M in 2025). Corrected, the after-tax add-back is +$73.2M. Second defect on the same name: `possible_peak_cycle_base` fires because the newest FCF is 2.4x the oldest, but the series [$82.2M, $134.9M, $195.0M] oldest-to-newest is a monotonic improvement, not a peak - the ITRI error - so the three-year mean UNDERSTATES current generation. FY2025 actual cfo-capex was $195.0M and H1 2026 is tracking flat to prior year ($59.3M CFO less $41.3M capex against $61.7M/$39.5M), on a business whose cash is ~80% H2-weighted. I set the base at $270M (FY2026 CFO of roughly $290-300M less $110-115M of capex, plus $73.2M of after-tax interest paid) and take 7% five-year FCFF growth, below the company's guided adjusted EBITDA trajectory because deleveraging mechanically shrinks the interest add-back that is 27% of this base.

**Devil's advocate.**
- Strongest counter: The counter is that I have corrected one input and then quietly trusted a second one I should not. Fixing the interest sign takes the required growth from +60.4% to +16.7%, but the WACC of 10.01% that produces it rests on a beta of 1.44 measured against IWM with an R-squared of 0.469 - which is a GOOD fit, so that is not the attack. The attack is on the FCFF definition itself: for a company carrying $1.88B of debt and repaying $100-150M a year, adding back after-tax interest and then discounting at a blended WACC assumes a stable capital structure that management has explicitly said it is changing. As leverage falls, the add-back shrinks and so does 'FCFF' as defined, even though equity holders are better off. On that reading my 7% is too low and the real answer is closer to the EBITDA growth rate, which would make the stock roughly fair.
- What would prove it: Whether FY2026 free cash flow before interest actually lands near my $290-300M CFO assumption. The settling observable is the full-year cash flow statement: CFO less capex for fiscal 2026 against the $195.0M of fiscal 2025, and whether the Q4 cash build that makes this business H2-weighted arrives on schedule.
- Already visible today: Partly, and it is neutral rather than supportive. H1 2026 CFO of $59.3M against $61.7M a year earlier is DOWN $2.4M, which the 10-Q attributes to 'higher earnings offset by an investment in working capital and higher restructuring payments'. So the earnings improvement is real but has not yet reached cash, and the whole FY2026 cash case rests on H2. That weakens my base rather than strengthening it, which is why conviction is low.
- Left unresolved: I could not determine how much of the $46.3M of interest INCOME embedded in 'Interest expense, net' is economically recurring - it includes cross-currency swap receipts on net investment hedges. Using gross rather than net interest would raise the add-back and lower the required growth further. I also could not reconcile the FCFF base to guided EBITDA: $589M of adjusted EBITDA less $110M of capex should leave more than $270M after cash taxes, which suggests either the three-year cash history carries non-recurring outflows or adjusted EBITDA is flattering.

**Key risks.** the recorded -123.3% gap and +60.4% implied growth are an interest-expense SIGN ERROR and must not be read as a signal in either direction; the verdict rests on a hand-built FCFF base; at the three-year mean the market requires +18.3% and at the FY2025 run rate +12.1%, so the answer moves 6 points on that choice alone; deleveraging shrinks the after-tax interest add-back, which is 27% of my base, so reported FCFF falls even as the equity improves; revenue_series carries a step ([$3,396.9M, $4,818.8M, $3,242.1M]) spanning the 2022 Distribution divestiture, so the '+0.1% 5y revenue CAGR' baseline is not a growth rate
**Watch for.** FY2026 full-year CFO less capex against fiscal 2025's $195.0M - the single number that settles the base; an engine fix asserting interest_expense >= 0 in normalized_fcff, and taking the most recent year rather than the oldest; adjusted EBITDA margin holding above 18% through a raw-material up-cycle

**Data quality.** One flag raised and BOTH the flag and a larger unflagged defect resolved against the engine. (1) `possible_peak_cycle_base_newest_fcf_2.4x_oldest`: FALSE - [$82.2M, $134.9M, $195.0M] oldest-to-newest is monotonic, which is a recovery, not a peak (the ITRI test), so the flag points the wrong way and the mean understates. (2) UNFLAGGED AND LARGE: interest_expense = -$115,300,000, verified against the 10-Q ('Interest expense, net ( 22.3 ) ( 24.7 ) ( 44.3 ) ( 51.6 )') and the 10-K ('Interest expense, net (98.6) (105.6) (115.3)'). The implied rate on absolute value is 6.15%, squarely inside the normal band, so neither the ALTG >12% detector nor the PATK <2% detector can fire - only a sign test catches this. Corrected, implied growth falls from +60.4% to +16.7% at the engine's own WACC. Share count current (2026-06-30, dei cover page); no item 1.01/2.01/3.02 8-K in two quarters; beta R-squared 0.469 is sound.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1122976/000112297626000126/avnt-20260630.htm (10-Q 2026-06-30: interest expense net $44.3M for six months, H1 CFO $59.3M, capex $41.3M)
- https://www.sec.gov/Archives/edgar/data/1122976/000112297626000039/avnt-20251231.htm (10-K FY2025: interest expense net (98.6)/(105.6)/(115.3); total interest PAID on debt net of hedging $97.6M in 2025)
- https://www.sec.gov/Archives/edgar/data/1122976/000112297626000123/avnt-20260630x8k.htm EX-99.1 (Q2 2026 release: adjusted EBITDA guidance raised to $575-603M, adjusted EPS $3.10-3.25, organic sales +4.3%, record 18.3% margin, FY2025 adjusted EBITDA $544.6M)
