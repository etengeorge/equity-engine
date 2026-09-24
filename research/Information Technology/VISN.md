# VISN — VISTANCE NETWORKS INC
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-24 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $6.45
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Vistance Networks (formerly CommScope) is a post-liquidation stub. At $6.45 the market pays ~$1.48bn for 230.0M shares of a company that has sold its Connectivity and Cable Solutions segment to Amphenol (closed 2026-01-09, $10,541.7M of net divestiture proceeds), repaid all $7,370.8M of third-party debt at that closing, redeemed $1,278.7M of Series A convertible preferred, and sold the RUCKUS segment to Belden for $1.846bn cash on 2026-07-01. It then returned the money: a $2,316.3M special distribution in H1 and a second $5.00/share special distribution declared 2026-08-06, paid 2026-08-27 (ex 08-28), ~$1.15bn. What remains is the Aurora Networks access-network business: Q2 net sales $319.6M (-1.4% y/y), gross margin 35.3% against 45.7%, and an operating LOSS of ~$8.9M after $122.3M of operating expenses. 59% of net sales go to Comcast and 12% to Charter. The price is a residual-cash-plus-a-breakeven-business number, and the market is not obviously wrong about it.

**What changed.** Everything, three times over. (i) CCS sold to Amphenol 2026-01-09; all third-party debt repaid in full at closing ($7,260.2M of long-term debt at 2025-12-31 is $0 at 2026-06-30, confirmed in the debt note: 'Total long-term debt $ -'). (ii) RUCKUS sold to Belden 2026-07-01 for $1.846bn cash, cash-free/debt-free (8-K item 2.01; pro forma 8-K/A filed 2026-07-08). (iii) Two special distributions: $2,316.3M paid in H1 2026 and $5.00/share declared 2026-08-06 and paid 2026-08-27 out of the Belden proceeds. Also: $300M ABL entered 2026-04-07, reduced to $246.9M on the RUCKUS close, undrawn at 2026-06-30 apart from $39.9M of letters of credit; and an additional $150M of buyback authorisation announced 2026-08-26.

**Base case.** No growth rate can be applied, because there is no base to apply it to. The engine's FCFF base of $760.8M is built from a cfo-capex series of [$252.6M, $247.8M, $236.6M] (mean $245.7M) PLUS roughly $515M of after-tax interest add-back - about 68% of the base - on the $7.26bn of debt that was repaid in full on 2026-01-09 and no longer exists. That alone is the SABR condition (add-back over 60% of base) on debt that is not merely unserviceable but extinguished. On top of it, the cfo-capex series belongs to a company that still owned CCS and RUCKUS; the business that remains generated an operating LOSS in Q2 2026 and burned cash at the consolidated level (H1 net cash used in operating activities $299.4M). A DCF on this name is not a valuation, it is an arithmetic accident.

**Devil's advocate.**
- Strongest counter: That this is cheap on net cash. I argued it myself: with $113.6M of balance-sheet cash at 2026-06-30, zero debt and $1.846bn of Belden proceeds landing the next day, enterprise value looks NEGATIVE by roughly $0.46bn against a $1.48bn market cap - i.e. the market pays less than nothing for a $1.24bn-revenue business.
- What would prove it: Whether the RUCKUS proceeds were still inside the company on the pricing date of 2026-09-23.
- Already visible today: Yes, and it defeats the counter. The 2026-08-06 EX-99.1 declares a $5.00 per share special cash distribution, record 2026-08-17, PAID 2026-08-27, ex-dividend 2026-08-28, funded explicitly 'with cash proceeds received in connection with the sale of its Ruckus Networks business to Belden Inc. on July 1, 2026'. That is roughly $1.15bn of the $1.846bn already out the door before the screen priced the stock. Residual net cash is nearer $0.8bn than $1.9bn, so enterprise value is positive (~$0.7bn) and the negative-EV argument is wrong. My own bull case lost to a press release.
- Left unresolved: I did not obtain a post-distribution balance sheet - the next 10-Q is not due until early November - so the ~$0.8bn residual net cash is my arithmetic (June cash $113.6M + ~$1,830M pro forma adjustment - ~$1,150M distribution), not a reported figure. Nor do I know the tax leakage on the RUCKUS gain beyond the $73.8M of accrued liabilities in the pro forma. Whether the remaining business is worth the ~$0.7bn of implied enterprise value is a genuine question I am not answering.

**Key risks.** Customer concentration: Comcast 59% and Charter 12% of net sales in Q2 2026, and 48%/15% of accounts receivable; Gross margin fell from 45.7% to 35.3% year over year on roughly flat revenue; continuing operations posted an operating loss in Q2; Cash is being distributed rather than reinvested, so the equity is converging on a small, concentrated, low-margin access-network business; No post-distribution balance sheet exists yet; the residual cash figure is derived, not reported
**Watch for.** The Q3 10-Q (early November) - the first balance sheet showing actual cash after the $5.00 distribution, and the first full quarter of continuing operations alone; Any further special distribution or acceleration of the $150M incremental buyback authorisation; Comcast or Charter capital-spending guidance, which is now effectively this company's revenue guidance

**Data quality.** RESOLVED and the name is unmodellable. The single flag raised - interest_expense_implies_no_debt_found_on_reported_debt_debt_likely_understated - points at the WRONG NUMBER. Debt is not understated: the 2026-06-30 10-Q debt note reads 'Total long-term debt $ -' against $7,260.2M at 2025-12-31, because the Amphenol purchase agreement required CCS to be delivered debt-free and the company 'repaid in full all of the then-outstanding indebtedness' on 2026-01-09. total_debt = 0 is CORRECT. What is broken is interest_expense, which is stale at roughly $687M/yr and drives a ~$515M after-tax add-back - 68% of the $760.8M FCFF base - on debt that was extinguished. So the flag leads an analyst to ADD debt to enterprise value when the correct inference is to REMOVE two thirds of the cash-flow base. Second unflagged defect: the cfo/capex series describes a company that owned CCS and RUCKUS; both are sold. Third: enterprise value of $1.4B is arithmetically right at the 2026-06-30 balance sheet and economically stale by $1.846bn of proceeds received the next day and ~$1.15bn distributed seven weeks later. revenue_ltm of $1,931.6M also overstates continuing operations (~$1.24bn annualised). The +189.6% gap and the 98th percentile of 122 Information Technology names are 100% artifact.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1517228/000119312526336708/visn-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1517228/000119312526291679/visn-20260701.htm
- https://www.sec.gov/Archives/edgar/data/1517228/000119312526298682/visn-20260701.htm
- https://www.sec.gov/Archives/edgar/data/1517228/000119312526336705/visn-ex99_1.htm
- https://www.sec.gov/Archives/edgar/data/1517228/000119312526368664/visn-ex99_1.htm

**Ingestion notes.** no usable final_growth
