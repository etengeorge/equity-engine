# HRI — HERC HOLDINGS
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $140.96 · fair value $114.72 · gap -18.6%
- **Growth:** market implies -0.0%, analyst says +6.0% (delta +6.0%)
- **FCFF base overridden** by the analyst to $576.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 6.0% | 7.0% | 8.0% | 9.0% | 10.0% |
|---|---|---|---|---|---|---|
| bear | -4.0% | $99.32 | $33.60 | $-10.17 | $-41.43 | $-64.88 |
| base | +6.0% | $293.71 | $186.21 | $114.72 | $63.76 | $25.60 |
| bull | +12.0% | $449.71 | $308.36 | $214.42 | $147.51 | $97.46 |

At the point WACC of 8.0%: bear -107.2%, base -18.6%, bull +52.1%
Across the whole grid the gap ranges -146.0% to +219.0% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $140.96 the market is paying ~$12.6B EV for the second-largest North American equipment rental fleet after the H&E Equipment acquisition, with H1 2026 revenue +26% to $2,343M on a 28% increase in equipment rental revenue, mega-project volume and revenue synergies. Rental is a scale business: a larger fleet buys route density, national-account share (49% of equipment rental revenue) and better fleet utilisation, and Herc is mid-integration with synergies still to land. On the engine's reported cash-flow base the price requires roughly zero five-year FCFF growth, which for a levered cyclical at the top of a construction cycle is a defensible thing to underwrite.

**What changed.** H&E Equipment Services acquisition closed 2025 and dominates every year-over-year comparison: H1 2026 revenue $2,343M vs $1,863M (+26%), Q2 $1,204M vs $1,002M (+20%). H1 2026 net cash from operating activities $591M vs $412M. Herc reported a net LOSS in H1 2026 on integration and financing costs. 8-K 2026-09-03 (items 1.01, 9.01) and 2026-08-19 (item 5.02, officer change) filed after the last 10-Q; I did not obtain the 9/3 agreement's terms.

**Base case.** Herc's owner earnings are not the engine's $806M. The 2026-06-30 10-Q investing section carries 'Rental equipment expenditures (557)' for the six months, against 'Purchases of property and equipment' of roughly $80M — and the extract's capex_series is [$157M, $161M, $156M] for the YEAR, i.e. it reads only the non-rental property line and treats every machine Herc buys as free. Rebuilding from the H1 actuals annualised: CFO ~$1,182M less gross rental capex ~$1,114M plus disposal proceeds ~$460M less property capex ~$160M plus P&E disposals ~$40M = ~$408M of owner earnings, or ~$576M after the FCFF convention's after-tax interest add-back. I set the base there. Growth of +6% is organic rental demand plus residual H&E synergies and mega-project volume, below the 2026 acquisition-inflated rate because a roll-up cannot compound 26% without buying it, and Herc is already carrying $7.9B of debt at 63% of capital.

**Devil's advocate.**
- Strongest counter: That my base-case correction double-counts. Gross rental capex includes replacement of fleet sold at a gain ($53M gain on sale of rental equipment in H1), and the $230M of disposal proceeds I add back are the recovery. If Herc's steady-state fleet is not growing, sustaining capex is much closer to depreciation of rental equipment ($484M H1, ~$970M/yr) net of disposals, which is roughly what I used — but if I have understated the after-tax interest add-back (the extract's $224M looks low against $7.9B of debt), the base rises toward $753M and the market's requirement falls back to +1.6%, i.e. no correction at all.
- What would prove it: Herc's own definition of free cash flow in the Q2 deck (EX-99.2) and its full-year net fleet capital expenditure guidance, plus the actual FY2026 interest expense run rate.
- Already visible today: Partly. The H1 10-Q gives CFO, gross rental capex and disposals, which is enough to establish that the engine's $157M capex is wrong by roughly an order of magnitude. It is NOT enough to pin the after-tax interest add-back, and that single input moves the implied requirement from +1.6% to +16.3%.
- Left unresolved: The precise FCFF base. My range of $408M-$753M spans implied growth of +16.3% to +1.6% — the whole answer. I could not narrow it from the documents I read.

**Key risks.** Non-residential construction cycle turning with $7.9B of debt at 63% of capital; H&E integration costs and synergy shortfall; Herc ran a net loss in H1 2026; Fleet capex is non-discretionary — holding share requires spending through a downturn
**Watch for.** Full-year net fleet capital expenditure guidance against operating cash flow; Fleet utilisation and rental rate disclosures in Q3; Terms of the 2026-09-03 item 1.01 agreement

**Data quality.** THREE defects, none flagged by the engine. (1) RENTAL-CAPEX BUG, fourth recorded instance after CTOS, ALTG and WLFC: capex_series [$157M, $161M, $156M] against 'Rental equipment expenditures (557)' for H1 2026 alone. (2) REVENUE SERIES CONTAMINATED BY THE PRE-SPIN PREDECESSOR: revenue_series reads [$4,376M, $3,568M, $3,282M, $10,535M, $11,046M, $10,772M]. Herc's revenue has never been $11B; CIK 1364479 was Hertz Global Holdings' CIK before the 2016 spin-off and Herc retained it, so the XBRL history carries pre-spin Hertz consolidated revenue. That is what produces the '5y revenue CAGR -16.5% (clamped to -10.0%)' baseline and therefore the entire -98.0% gap and 7th-percentile cohort rank. The company is growing 26%, not shrinking 16%. (3) dep_amort_series is EMPTY for a company that depreciated $484M of rental equipment in six months, so no EBITDA can be built. I corrected the base; I could not correct the interest add-back.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1364479/000136447926000109/hri-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1364479/000136447926000108/herc2026q2-pressrelease.htm
- https://www.sec.gov/Archives/edgar/data/1364479/000136447926000050/hri-20251231.htm
