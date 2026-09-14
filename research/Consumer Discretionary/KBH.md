# KBH — KB HOME
*Consumer Discretionary · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $49.16 · fair value $59.38 · gap +20.8%
- **Growth:** market implies -18.0%, analyst says +0.0% (delta +18.0%)
- **FCFF base overridden** by the analyst to $300.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 8.2% | 9.2% | 10.2% | 11.2% | 12.2% |
|---|---|---|---|---|---|---|
| bear | -12.0% | $45.84 | $40.38 | $36.25 | $33.00 | $30.38 |
| base | +0.0% | $77.35 | $67.12 | $59.38 | $53.34 | $48.48 |
| bull | +10.0% | $116.98 | $100.60 | $88.25 | $78.60 | $70.87 |

At the point WACC of 10.2%: bear -26.3%, base +20.8%, bull +79.5%
Across the whole grid the gap ranges -38.2% to +138.0% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $49.16 KB Home trades at about 0.79x its own book value of roughly $61.94 a share, having fallen 23.7% over twelve months. The market's case is dated and mechanical rather than sentimental: the 30-year mortgage rate has reached 7%, RBC and others are describing renewed affordability headwinds, and the market is now weighing the prospect of Fed HIKES rather than cuts. A homebuilder's earnings are a spread between land basis and selling price, and in a 7% rate environment that spread is closed by incentives — mortgage rate buydowns paid out of gross margin. Buying homebuilders below book has historically worked, but the market is not mispricing the rate; it is pricing it.

**What changed.** Nothing at the company since the 2026-06-23 second-quarter release; the third-quarter report for the period ended 2026-08-31 is due 2026-09-22, eight days from now, and that is the next real information. What changed is the rate environment: the 10-year Treasury surged in late August (KBH, Meritage and LGI all fell together on 2026-08-20), mortgage rates hit 7% by 2026-09-11, and the 21-day move of -11.9% is that, not a company event.

**Base case.** I will not put much weight on a growth rate here because the reverse DCF on this name is built on two broken inputs, but the number has to be defensible: zero. For a homebuilder, operating cash flow is dominated by investment in land and inventory, so it is large and positive when the builder is shrinking and negative when it is growing — the $1.08B in the oldest year of the series is the 2023 inventory-liquidation year, not earnings power. The recent two-year run rate of ~$300M is a better description of a company in a normal land-spend posture. At 7% mortgage rates with incentives running, flat is the honest base case: volumes fall, average selling price holds, and margin absorbs the buydown.

**Devil's advocate.**
- Strongest counter: That a +204.1% gap at the 95th percentile of 129 Consumer Discretionary peers, on a name trading at 0.79x tangible book with no goodwill, is exactly the kind of signal this screen exists to find, and I am explaining it away with a data objection.
- What would prove it: Whether the enterprise value the gap is computed from is the company's actual enterprise value.
- Already visible today: It is not, and this settles it. The extract records total_debt of ZERO and interest_expense of ZERO. Note 14 of the 2026-05-31 10-Q reads: unsecured revolving credit facility $275,000; senior unsecured term loan due 2029 $358,532; 6.875% senior notes due 2027 $299,379; 4.80% senior notes due 2029 $298,505; 7.25% senior notes due 2030 $347,354; 4.00% senior notes due 2031 $387,330; mortgages and land contracts $2,614 — TOTAL $1,968,714 thousand. The engine's $2.8B enterprise value is market capitalisation less cash and nothing else; the true figure is about $4.77B. Homebuilders capitalise interest into inventory, which is why the interest-expense detector reads zero and cannot flag this. Correcting BOTH defects — enterprise value up by $1.969B and the cash-flow base down to the $300M run rate — moves the growth the market implies from -18.1% to PLUS 7.9%. The gap does not shrink, it inverts: the market is requiring positive compounding from a builder facing 7% mortgage rates, not pricing in a collapse. This is the ALTG/HOG missing-debt bug in a new tag family, and like every instance of it the error manufactures cheapness.
- Left unresolved: Whether the $2.0B should be netted against KBHS warehouse borrowings and mortgage loans held for sale, which are a financial-services funding line rather than corporate leverage. That would reduce but not remove the correction. I also could not test Q3, which lands 2026-09-22.

**Key risks.** 7% mortgage rates with the market now pricing Fed hikes rather than cuts; Land optioned at 2024-25 prices is an impairment risk if incentives keep widening; Recorded fair value is computed on an enterprise value missing $1.969B of debt and must not be read as a signal
**Watch for.** Q3 results on 2026-09-22: net orders, cancellation rate and gross margin ex-land-sale; Incentive load as a percentage of average selling price; Whether the 30-year mortgage rate breaks back below 6.5%

**Data quality.** THE HEADLINE NUMBER ON THIS BRIEF IS WRONG AND IT IS WRONG IN THE CHEAP DIRECTION. total_debt reads 0.0 and interest_expense reads 0 against $1,968,714 thousand of notes payable disclosed in Note 14 of the 2026-05-31 10-Q (revolver $275.0M, term loan $358.5M, four series of senior notes $1,332.6M, mortgages and land contracts $2.6M). Enterprise value is therefore understated by roughly 70%, $2.8B against ~$4.77B. This is the ALTG revolver bug in a new tag family: homebuilders capitalise interest into inventory, so the `interest_expense / total_debt` detector that caught ALTG and HOG reads 0/0 here and cannot fire — no flag was raised. Second defect: `possible_trough_cycle_base_newest_fcf_0.27x_oldest` fires on a cfo_series of [$335.7M, $362.7M, $1,082.7M] and advises that value is understated, but for a homebuilder operating cash flow is inversely related to land investment, so the $1.08B year is the inventory-liquidation year and the flag is pointing backwards — the AMR/LPG lesson again. I corrected the base; I could NOT correct the enterprise value, because the analyst schema has no field for it, so the fair value this verdict produces remains built on a $2.8B enterprise value and should be disregarded entirely. On corrected inputs the implied growth is +7.9%, not -18.1%.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/795266/000079526626000063/kbh-20260531.htm
- https://www.sec.gov/Archives/edgar/data/795266/000079526626000060/kbh-20260623.htm
