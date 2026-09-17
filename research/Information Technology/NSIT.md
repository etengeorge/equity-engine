# NSIT — INSIGHT ENTERPRISES INC
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $165.19 · fair value $186.86 · gap +13.1%
- **Growth:** market implies -3.1%, analyst says +5.0% (delta +8.1%)
- **FCFF base overridden** by the analyst to $400.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 7.0% | 8.0% | 9.0% | 10.0% | 11.0% |
|---|---|---|---|---|---|---|
| bear | +0.0% | $214.70 | $173.16 | $143.42 | $121.08 | $103.68 |
| base | +5.0% | $277.58 | $224.68 | $186.86 | $158.46 | $136.37 |
| bull | +10.0% | $353.00 | $286.39 | $238.78 | $203.08 | $175.32 |

At the point WACC of 9.0%: bear -13.2%, base +13.1%, bull +44.5%
Across the whole grid the gap ranges -37.2% to +113.7% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Insight is being re-rated as an AI-infrastructure and services beneficiary rather than a hardware reseller, and the numbers support it: Q2 net sales +15%, gross profit +18%, gross margin +60bp to 21.7%, adjusted earnings from operations +31%, adjusted diluted EPS +44%, and FY2026 guidance RAISED to $12.20-12.70 of adjusted EPS (+16% at the midpoint) with gross profit growth of 8-10%. At $165.19 that is roughly 13x adjusted earnings for a business whose gross profit is compounding, which is why the market implies slightly negative FCFF growth rather than a premium.

**What changed.** Q2 2026 (filed 2026-08-06) raised full-year guidance on both gross profit growth and adjusted EPS. A three-year 'One Insight' plan was introduced targeting AI infrastructure and services with improved operating efficiency. The prior convertible notes were repaid ($333.1M of principal in the comparable prior-year period), leaving the ABL revolver and inventory financing as the debt.

**Base case.** The +16.4% gap is small and the base behind it is not trustworthy, so this is not a thesis either way. The $512.7M FCFF base is the mean of cfo-less-capex of [$279.3M, $586.1M, $580.3M] — and the two large years are working-capital releases, not earnings: Insight's net sales fell from $10,431M to $8,247M across the window and a declining reseller liquidates receivables and inventory into cash. Building owner earnings from the income statement instead — EBIT of $334.9M taxed at 27%, plus $106.3M of depreciation and amortisation, less $24.5M of capex — gives roughly $330M, and the company's own guided adjusted net earnings are about $365M on ~29.3M diluted shares. Across that range the market implies +1.5% to +8.5% five-year FCFF growth rather than the -3.1% the brief reports. Against guided gross profit growth of 8-10% and adjusted EPS growth of 16%, a requirement of roughly +5% is close to fair. Note also that the 'possible_trough_cycle_base' flag is misleading in the usual way: the newest year is the LOWEST cash-flow year precisely because the business stopped shrinking, so the flag reads a working-capital normalisation as a cyclical trough.

**Devil's advocate.**
- Strongest counter: That I have the cash-flow direction exactly backwards. If Insight is now GROWING again — net sales +15% in Q2 — then working capital swings from a source of cash to a use of it, and free cash flow could run well BELOW my $400M normalisation for several years even as earnings rise. On that reading the required growth is nearer +8.5% against a company whose gross profit is guided to grow 8-10%, which is fair at best and leaves nothing for the equity.
- What would prove it: Operating cash flow in the FY2026 10-K against the $303.8M of the prior year, with the receivables and inventory lines broken out.
- Already visible today: Partly. The newest year in the series is already the weakest at $303.8M against $632.8M and $619.5M, which is consistent with the release having ended. The company also states it intends to use cash generated in excess of working capital needs to pay down the ABL facility and repurchase shares, which implies management expects working capital to absorb cash as growth resumes.
- Left unresolved: Whether gross margin expansion is mix or pricing. Management says it expects margins to improve as services and solutions grow, but a reseller's gross margin also rises mechanically when cloud is booked net rather than gross, and that is an accounting presentation rather than economics.

**Key risks.** net sales have fallen from $10.4B to $8.2B across the cash-flow window; gross profit growth is doing all the work; free cash flow has been flattered by working-capital release and reverses as the business grows; partner incentive programmes are a disclosed swing factor on gross margin; a disclosed global memory chip shortage affects supply and pricing
**Watch for.** FY2026 operating cash flow against the $303.8M prior year — the working-capital reversal test; whether gross margin holds above 21.5% once the AI hardware cycle normalises

**Data quality.** RESOLVED: possible_trough_cycle_base is the AMR pattern — the flag advises that a trough understates value, when in fact the three-year mean is INFLATED by two working-capital-release years on a shrinking revenue base; the newest year is the cleanest. Implied interest rate of 2.79% on $1,475M of debt is above the PATK alarm threshold and is consistent with the ABL plus inventory financing structure disclosed in the 10-Q; the convertible notes that would have been the TDOC risk were repaid. Share count is current (2026-07-31). No unresolved data defects; the uncertainty here is about the right cash-flow base, not about a broken input.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/932696/000093269626000062/nsit-20260630.htm (10-Q, 2026-06-30: ABL borrowings and repayments, convertible note repayment, liquidity discussion)
- Q2 2026 EX-99.1 filed 2026-08-06 (results and raised FY2026 guidance: adjusted diluted EPS $12.20-12.70, gross profit growth 8-10%)
- Q2 2026 EX-99.2 filed 2026-08-06
