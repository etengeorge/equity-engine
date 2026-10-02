# CARS — CARS.COM INC
*Communication · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-10-02 — CHEAP (conviction: medium)

- **Verdict:** cheap · price $10.00 · fair value $23.92 · gap +139.2%
- **Growth:** market implies -11.6%, analyst says -3.0% (delta +8.6%)
- **FCFF base overridden** by the analyst to $146.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 7.1% | 8.1% | 9.1% | 10.1% | 11.1% |
|---|---|---|---|---|---|---|
| bear | -12.0% | $20.75 | $16.38 | $13.24 | $10.87 | $9.01 |
| base | -3.0% | $36.06 | $28.99 | $23.92 | $20.10 | $17.12 |
| bull | +2.0% | $47.22 | $38.16 | $31.66 | $26.78 | $22.97 |

At the point WACC of 9.1%: bear +32.4%, base +139.2%, bull +216.6%
Across the whole grid the gap ranges -9.9% to +372.2% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $10.00 against a corrected FCFF base of $146.0M the market requires -15.5% five-year FCFF growth, i.e. that Cars.com loses more than half its free cash flow by 2031. The coherent version of that case is AI-mediated search disintermediating the automotive marketplace: Cars.com's dealer subscriptions are priced off the traffic and leads it delivers, that traffic is substantially organic search, and generative answers remove the click. Evidence the market can point to today: Dealer Customers fell to 19,343 from 19,412 a year ago, OEM and National revenue is -18% y/y, management's own release attributes the dealer decline to 'lower Solutions adoption', and FY2026 revenue guidance is 0-2% - i.e. below inflation. Marketplace growth of 7% is being bought with 'value-based pricing' (price per dealer) rather than units, which is the last lever before churn accelerates. Layer on 2.1x leverage ($447M debt vs $535M market cap) and a CFO who departs on 2026-11-06, and a terminal-decline multiple of ~4x levered FCF is internally consistent. The base rate supports them: cheap flat-revenue internet marketplaces (Yelp, TripAdvisor, Ziff Davis) have stayed cheap for a decade.

**What changed.** Q2 2026 (filed 2026-08-06): revenue $179.9M +1%; Dealer subscription revenue $163.3M +3%; Marketplace revenue +7%, the fastest since 2021, with a fourth consecutive quarter of y/y subscriber growth; OEM and National $13.6M -18%; adjusted EBITDA $53M +4% at a 29.4% margin, above the high end of guidance. FY2026 guidance reaffirmed at 0-2% revenue growth and a 29-30% adjusted EBITDA margin. H1 2026 repurchased 6.2M shares for $57.3M at an average $9.23; $116.6M remains of the $250M authorization. On 2026-09-30 the company announced a CFO transition: Trent Ziegler (ex-LendingTree CFO) becomes CFO-Designate 2026-10-19 and CFO 2026-11-06, succeeding Sonia Jain. I could NOT find a specific catalyst for the -14% 21-day move; the only filing in the window is the CFO release, which postdates most of the decline.

**Base case.** Two engine defects cancel in opposite directions and must be fixed together. (1) interest_expense is recorded as -$30,382,000: the 10-K presents 'Interest expense, net ( 30,382 ) ( 32,197 ) ( 32,425 )' in parentheses and the extractor kept the sign, so normalized_fcff SUBTRACTS $22.8M instead of adding it. (2) capex_series [4.286, 3.000, 1.280] is the 'Purchase of property and equipment' line only; the same cash flow statement carries 'Capitalization of internally developed technology ( 21,619 ) ( 21,381 ) ( 19,602 )', so true capex is [25.905, 24.381, 20.882] and the extractor captures 12% of it. Corrected: mean(CFO - true capex) = $123.2M plus after-tax interest $22.8M = $146.0M. Underneath, the business is stable, not declining: operating income is $60.25M / $53.50M / $54.12M across FY2025/24/23 - flat to UP - and the apparent 83% earnings collapse from $118.4M to $20.1M is entirely below the operating line, being a $100.3M deferred-tax valuation-allowance release in FY2023 and a $40.6M one-off other-income gain in FY2024, both now lapped. Against flat-to-up operating income, 0-2% guided revenue, a 29-30% margin guide and Marketplace growing 7%, a mid-single-digit decline is already conservative; I take -3% to charge for secular marketplace pressure and for cash taxes rising as the acquired-intangible amortisation shield (intangibles running off, $669M to $585M to $527M) depletes.

**Devil's advocate.**
- Strongest counter: The AI-disintermediation case is real, is not priced into my -3%, and would validate the market's -15.5% if it arrives. Cars.com is the #3 marketplace behind Autotrader and CarGurus; a traffic-dependent intermediary with no supply-side lock-in is exactly what generative search removes. Secondly, the base rate for 'cheap internet marketplace on flat revenue' is poor - these names stay cheap for years while FCF erodes. Thirdly, my corrected base relies on treating $31.3M of stock compensation as free, and on CFO that is flattered by a depleting deferred-tax asset, so steady-state FCF is nearer $110M than $128M.
- What would prove it: Dealer Customers declining more than ~2% y/y for two consecutive quarters; Marketplace revenue growth decelerating below ~3%; average revenue per dealer falling; or management withdrawing the 29-30% margin guide. On the tax point, a rising cash tax rate in the FY2026 10-K cash flow statement.
- Already visible today: Partly. Dealer Customers are already down y/y (19,343 vs 19,412), OEM/National is -18%, and 'lower Solutions adoption' is management's own language. But these are offset by the fastest Marketplace growth since 2021 and four consecutive quarters of subscriber growth - the opposite of accelerating churn - so what is visible is a mix shift, not yet an erosion.
- Left unresolved: I cannot observe Cars.com's traffic or lead volume from free sources, and the company does not disclose them. That is the single input that decides between my -3% and the market's -15.5%, and I could not get it. I also could not explain the -14% 21-day move: no filing in the window accounts for it.

**Key risks.** AI-mediated search erodes organic traffic, the mechanism that would justify the market's -15.5% and which I cannot observe; 2.1x leverage against a $535M market cap: a 20% FCF decline is roughly a 40% equity decline; Cash taxes rise as the acquired-intangible amortisation shield runs off (intangibles $669M -> $585M -> $527M), worth perhaps $15M a year of FCF; New CFO effective 2026-11-06 may reset guidance or take an impairment; goodwill $166M plus intangibles $505M exceed the $535M market cap; Buybacks are retiring 10-11% of the count a year and are the main per-share driver; if FCF falls the buyback stops and the per-share math inverts
**Watch for.** Dealer Customer count in the Q3 2026 release - two consecutive quarters below -2% y/y would move me to no_edge; Marketplace revenue growth decelerating below 3%, or average revenue per dealer declining; FY2027 guidance from the incoming CFO: anything below flat revenue breaks the base case; Cash taxes paid in the FY2026 10-K cash flow statement against the $14M book tax expense

**Data quality.** RESOLVED, both from the primary filings. (1) The flagged stock_comp_is_21%_of_fcff is settled in favour of treating it as free: BASIC weighted-average shares are 55,871k in Q2 2026 against 63,163k in Q2 2025 (-11.5%) and 57,453k against 63,859k for H1 (-10.0%), so the $31.3M of compensation is more than paid for out of cash, per the BOX rule run on basic rather than diluted. (2) UNFLAGGED and corrected: interest_expense = -$30,382,000 is a sign error from the parenthesised income-statement presentation, the fourth instance of the AVNT/BDC/SLG defect and the first in Communication. (3) UNFLAGGED and corrected: capex_series omits 'Capitalization of internally developed technology' ($21.6M/$21.4M/$19.6M), a new tag family for the CTOS/WLFC missing-capex bug. The two corrections run in opposite directions and I applied both; fcff_base_override is set to the corrected $146.0M. OPEN: the FCFF window is FY2023-25 and the amortisation-driven deferred tax benefit inside CFO is not separable from free sources, so my base may be ~$15M generous.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1683606/000119312526337949/cars-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1683606/000119312526336773/cars-20260806.htm
- https://www.sec.gov/Archives/edgar/data/1683606/000119312526409040/cars-20260924.htm
- https://www.sec.gov/Archives/edgar/data/1683606/000095017026000000/cars-20251231.htm
- https://investor.cars.com/2026-08-06-Cars-com-Reports-Second-Quarter-2026-Results
- https://www.fool.com/earnings/call-transcripts/2026/08/13/carscom-cars-q2-2026-earnings-call-transcript/
