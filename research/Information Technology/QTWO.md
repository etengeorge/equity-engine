# QTWO — Q2 HOLDINGS INC
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-22 — RICH (conviction: low)

- **Verdict:** rich · price $57.93 · fair value $35.45 · gap -38.8%
- **Growth:** market implies +23.8%, analyst says +15.0% (delta -8.8%)
- **FCFF base overridden** by the analyst to $110.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 9.0% | 10.0% | 11.0% | 12.0% | 13.0% |
|---|---|---|---|---|---|---|
| bear | +8.0% | $34.90 | $30.63 | $27.31 | $24.66 | $22.49 |
| base | +15.0% | $45.79 | $39.96 | $35.45 | $31.84 | $28.90 |
| bull | +22.0% | $59.50 | $51.70 | $45.66 | $40.84 | $36.92 |

At the point WACC of 11.0%: bear -52.9%, base -38.8%, bull -21.2%
Across the whole grid the gap ranges -61.2% to +2.7% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Q2 Holdings has turned into a profitable, debt-free compounder and the market is paying a normal price for it. Revenue grew 14.1% to $794.8M on a trailing basis; GAAP diluted EPS was $0.46 in Q2 against $0.18; operating cash flow reached $201.5M against $135.8M and $70.3M in the two prior years; the company repaid the remaining $304.0M of its 0.75% convertible notes IN CASH at maturity in June 2026 and now carries no debt at all; and on the strength of that balance sheet the board authorised an additional $350M of buybacks on top of the November 2025 $150M, bringing capacity to ~$375M. A digital-banking platform selling to community and regional banks with that revenue growth, zero leverage and $375M of repurchase capacity is not an obvious mispricing at 4.4x trailing revenue.

**What changed.** Q2 2026 (filed 2026-07-29): the $304.0M of 0.75% convertible senior notes due June 2026 were repaid in cash before maturity with no conversions, leaving the company debt-free; $120.1M of shares were repurchased in H1 (0.5M shares at ~$45.67 in Q2 alone); a new $350M repurchase authorisation was announced. Cash and equivalents fell from $369.3M at 2025-12-31 to $102.1M, almost entirely because of the note repayment and the buyback.

**Base case.** The deciding input on this name is the stock-compensation treatment, and the BOX rule settles it decisively AGAINST the company. Stock compensation is $86.9M, 66% of the $131.6M FCFF base, and the brief offers the usual binary: treat it as free and the market implies +23.8%, expense it and +55.0%. Neither is the economics - the right test is the NET weighted-average basic share count. Q2 Holdings' basic weighted-average shares were 62,486 thousand in Q2 2026 against 62,353 thousand in Q2 2025, and 62,412 thousand in H1 2026 against 61,790 thousand in H1 2025: the count ROSE 1.0% year over year DESPITE $120.1M of repurchases in the same six months. The buyback did not even absorb the dilution, so the compensation is a real, unpaid-for economic cost and the honest base sits near the expensed end. Note the trap in the same table: DILUTED shares fell from 69,642 to 65,420 thousand, a 6.1% reduction that looks shareholder-friendly and is nothing of the kind - it is the if-converted shares of the 2026 notes dropping out because the notes were repaid in cash. An analyst reading the diluted line gets the sign of this test exactly backwards. On the newest year's cash generation less stock compensation ($194.7M - $86.9M) plus the small interest add-back, owner earnings are about $110M against a $3.51B enterprise value - a 3.1% yield requiring +28.8% growth. I underwrite 15%: revenue compounds around 14% with some margin leverage, but not double that.

**Devil's advocate.**
- Strongest counter: The best case against me is that I am charging Q2 Holdings the full $86.9M of stock compensation as a permanent cash cost while the company has just acquired the balance sheet to stop it. The 2026 converts consumed $304.0M of cash in the very half I measured; that cash is now permanently freed, and $375M of repurchase authorisation against a $3.6B market capitalisation is enough to retire roughly 10% of the shares. A single half-year in which the count rose 1.0% while the company was simultaneously paying off a convertible is weak evidence of a structural failure to fund the comp. On that reading the right base is nearer the newest-year $197M figure, the requirement falls to +13.2%, and against 14% revenue growth the stock is roughly fair.
- What would prove it: The basic weighted-average share count in Q3 and Q4 2026, now that the notes are repaid and the full $375M authorisation is available. If the basic count turns down year over year while stock compensation stays near $87M, the comp is being paid for and my base is too low by roughly $87M - which is the whole verdict.
- Already visible today: No, and that is the honest answer. The only quarter in which the repayment and the new authorisation coexist is Q3 2026, which has not been reported. What IS visible is that in Q2 2026 - a quarter with $22.9M of repurchases at an average of $45.67, well below today's $57.93 - the basic count still rose. Buying back stock 21% cheaper than today and still not shrinking the count is not an encouraging starting point, but it is one quarter.
- Left unresolved: Whether management intends the $375M to shrink the count or merely to offset dilution; the release does not say. I also could not obtain the full-year 2026 adjusted EBITDA guidance figures - the release states guidance was updated but the numeric table was not in the portion of the exhibit I could read - so I could not test my 15% against the company's own margin trajectory.

**Key risks.** the verdict turns almost entirely on one input - the stock-compensation treatment - and the honest range is +13.2% required (newest year, comp free) to +28.8% (comp expensed); the BOX test rests on a single half-year in which the company was simultaneously retiring $304.0M of convertible notes; a reader using DILUTED shares would see a 6.1% reduction and conclude the opposite of what the basic count says; stock compensation is 10.9% of revenue, which is high even for enterprise software
**Watch for.** basic weighted-average shares in Q3 and Q4 2026 - down year over year overturns this verdict; stock compensation as a percentage of revenue trending below 9%; how much of the $375M authorisation is actually spent in the next two quarters

**Data quality.** Three flags; one is a FALSE ALARM and worth recording as such. `interest_expense_implies_no_debt_found_on_reported_debt_debt_likely_understated` fires because interest expense is $2.815M against total_debt of 0.0 - but the debt really is zero: the 10-Q shows 'Convertible notes, current portion - / 303,368' and 'Payment for maturity of convertible notes (303,995)', and states the 2026 notes 'were settled during the three months ended June 30, 2026 and are no longer outstanding'. The $2.8M is the stub-period interest before repayment. So the enterprise value of $3.506B is CORRECT and this is the opposite of the TENB case - the flag names a defect that is not there, and an analyst applying the TENB lesson mechanically would have added debt that does not exist. `possible_peak_cycle_base_newest_fcf_3.0x_oldest` is the ITRI error again: [$64.6M, $129.1M, $194.7M] oldest-to-newest is monotonic, a ramp not a peak, so the mean understates - which is why I used the newest year. `stock_comp_is_66%_of_fcff` is real and is the whole verdict, resolved above by the share-count test. Note `balance_sheet_form` reads '10-K' with `balance_sheet_asof` 2026-06-30 on a December-year-end filer - a provenance mislabel, the SLG shape, cosmetic here. Share count 62,354,695 at 2026-07-29 is current.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1410384/000141038426000053/qtwo-20260630.htm (10-Q 2026-06-30: basic weighted-average shares 62,486/62,353/62,412/61,790 thousand; diluted 65,420/69,642; convertible notes settled and no longer outstanding; repurchases of common shares $120,081 thousand)
- https://www.sec.gov/Archives/edgar/data/1410384/000141038426000051/a260630q2ex9918k.htm (Q2 2026 EX-99.1: additional $350M repurchase authorisation, debt-free balance sheet, 0.5M shares at ~$45.67 for $22.9M in Q2)
