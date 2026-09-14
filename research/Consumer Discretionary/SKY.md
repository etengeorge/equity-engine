# SKY — CHAMPION HOMES INC
*Consumer Discretionary · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $83.16 · fair value $64.50 · gap -22.4%
- **Growth:** market implies +15.0%, analyst says +7.0% (delta -8.0%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 9.8% | 10.8% | 11.8% | 12.8% | 13.8% |
|---|---|---|---|---|---|---|
| bear | +0.0% | $61.52 | $56.20 | $51.96 | $48.51 | $45.63 |
| base | +7.0% | $77.81 | $70.40 | $64.50 | $59.70 | $55.71 |
| bull | +13.0% | $95.32 | $85.63 | $77.93 | $71.66 | $66.47 |

At the point WACC of 11.8%: bear -37.5%, base -22.4%, bull -6.3%
Across the whole grid the gap ranges -45.1% to +14.6% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $83.16 the market is paying ~$3.8B of enterprise value (market cap $4.5B less $785M of net cash) for the largest builder of factory-built housing in North America, at roughly 13x a ~$294M adjusted EBITDA run rate. The case is structural: with mortgage rates at 7% and site-built affordability deteriorating, manufactured housing is the product that still clears at an average selling price of $95,600, and Champion says it 'continued to outperform the broader industry in a challenging environment'. It is also consolidating distribution — Iseman Homes and now Homes Direct — which converts a wholesale margin into a retail one and should raise through-cycle returns on the same factory base.

**What changed.** Q1 FY2027 (quarter ended 2026-06-27, reported 2026-08-04): net sales +1.3% to $710.2M, US homes sold +1.8% to 7,089, ASP +0.6% to $95,600, backlog $421.8M, gross margin 25.2%, adjusted EBITDA $73.6M at a 10.4% margin, adjusted EPS $0.88. Management cites 'higher material costs partially offset by modest sales growth'. The Homes Direct acquisition closed recently; SG&A rose to $119.0M from $111.3M on the inclusion of Iseman Homes and the expanded retail footprint. 8-K 2026-08-26 carried items 5.02/8.01 (officer change).

**Base case.** Champion is growing revenue 1.3% and units 1.8% with gross margin under pressure from material costs, while acquiring retail distribution. The +13.4% naive baseline is a backward-looking revenue CAGR that captures the 2021-23 manufactured-housing boom and says nothing about a company now growing at one percent. My +7% is unit growth in the low-to-mid single digits as affordability keeps pushing buyers toward factory-built product, plus margin recovery as material costs normalise, plus the retail roll-up converting wholesale margin to retail — deliberately above the current 1.3% run rate because the acquisitions are real and the affordability tailwind is real, and deliberately well below the +15.0% the price requires.

**Devil's advocate.**
- Strongest counter: That I am too negative on one soft quarter. Champion has $784.7M of net cash, essentially no debt, a 10.4% adjusted EBITDA margin in what management calls a challenging environment, and a backlog of $421.8M. At ~13x EV/EBITDA it is cheaper than Cavco, and the industry is early in a multi-year recovery from a depressed shipment base, not late in a cycle. On that reading +15% FCFF growth is achievable and the price is fine.
- What would prove it: Unit growth re-accelerating above mid-single digits with gross margin stable or rising, i.e. volume recovery that is not bought with acquisitions.
- Already visible today: Partially, and it is genuinely ambiguous — which is what decides the verdict. Units +1.8% and ASP +0.6% is not recovery, but it is not decline either, and the backlog is respectable. The honest reading is that this quarter does not discriminate between my +7% and the market's +15%.
- Left unresolved: Whether the retail acquisitions are accretive to returns or just to revenue. SG&A rose 7% on the Iseman inclusion while sales rose 1.3%, which is the EVI/EFOR shape — revenue bought rather than earned — but one quarter with two small acquisitions is not enough evidence to call it, and Champion does not disclose organic revenue separately. I could not resolve it.

**Key risks.** Chattel financing rates track the same curve as mortgages — the affordability advantage is relative, not absolute; Material cost inflation compressing a 25.2% gross margin while revenue grows 1.3%; Retail roll-up (Iseman, Homes Direct) may be buying revenue rather than earning it; no organic disclosure
**Watch for.** Organic revenue growth disclosed separately from the Iseman and Homes Direct contributions; Backlog trend from $421.8M; US industry shipment data and gross margin direction in Q2 FY2027

**Data quality.** The recorded gap of -5.1% is inside the +/-15% FCFF band that LESSONS.md calls noise, and that is the main reason this is no_edge rather than rich. `interest_expense_implies_32%_on_reported_debt_debt_likely_understated` — checked and immaterial: interest expense of $7.5M on reported debt of $23.8M does produce an impossible rate, but Champion holds $784.7M of cash against that debt and the debt weight in the WACC is 1%, so no plausible correction to the debt figure moves the valuation. Separately I found an unflagged defect that does NOT affect this valuation but should be recorded: net_income_common_series reads [$146.7M, $401.8M, $248.0M] while net_income_series reads [$206.9M, $198.4M, $146.7M] — the newest value of the common series equals the OLDEST value of the net income series, i.e. the two are offset. That is the AX `_annual` duration bug appearing on a Consumer Discretionary name. It is harmless here because SKY is priced by the fcff method and never touches the common series, but it would be decisive on any book-method name.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/90896/000119312526335147/sky-20260627.htm
- https://www.sec.gov/Archives/edgar/data/90896/000119312526332837/sky-20260804.htm
