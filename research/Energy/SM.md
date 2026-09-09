# SM — SM ENERGY
*Energy · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $37.76 · fair value $51.19 · gap +35.6%
- **Growth:** market implies -0.5%, analyst says +0.0% (delta +0.5%)
- **FCFF base overridden** by the analyst to $870.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 6.2% | 7.2% | 8.2% | 9.2% | 10.2% |
|---|---|---|---|---|---|---|
| bear | -10.0% | $46.38 | $37.16 | $30.90 | $26.37 | $22.94 |
| base | +0.0% | $77.27 | $61.72 | $51.19 | $43.59 | $37.84 |
| bull | +6.0% | $102.43 | $81.67 | $67.62 | $57.49 | $49.83 |

At the point WACC of 8.2%: bear -18.2%, base +35.6%, bull +79.1%
Across the whole grid the gap ranges -39.3% to +171.3% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** SM Energy is a different company from the one this model prices. The Civitas Resources merger closed 2026-01-30 and Q2 2026 was the first full quarter of the combined business: operating cash flow of $1.1 billion in the quarter, capital expenditures of $754M, adjusted free cash flow of $467M, second-half production guidance raised to 435-440 MBoe/d including ~238 MBbl/d of oil, and 95% of targeted run-rate synergies actioned. The balance sheet has been dismantled deliberately - a $950M South Texas divestiture closed 2026-04-30, $819M of 2026 notes redeemed with the proceeds, net debt down $1.1 billion sequentially, and on 2026-09-04 the remaining $417M of 6.625% 2027 notes redeemed at par with cash on hand, retiring every senior note due through mid-2028. At $37.76 the market is paying roughly ten times annualised free cash flow for a depleting asset base and asking for approximately flat FCFF in perpetuity. For a shale producer whose growth requires drilling to stand still, flat is not a pessimistic assumption - it is close to the right one.

**What changed.** Everything that matters. Civitas merger closed 2026-01-30 (11 months of contribution in FY26 guidance). South Texas divestiture of $950M closed 2026-04-30. Q2 2026 (2026-08-05): OCF $1,103M, capex $754M, adjusted FCF $467M, $137M returned to shareholders via $84M of buybacks and a $0.22 dividend. Second-half production guidance raised from 430 to 435-440 MBoe/d, full-year narrowed to 418-423 MBoe/d, full-year capital reaffirmed, G&A guidance reduced. 8-K 2026-09-04 (item 1.02): $416,791,000 paid to redeem the 2027 Senior Notes. Also terminated the Erie, Colorado mineral rights agreement after resident opposition (August).

**Base case.** I take flat FCFF. The combined company is generating roughly $870M of GAAP free cash flow annualised (H1 2026 CFO $1,743M less capex $1,309M = $434M for the half) and more on the company's adjusted definition, against a base the engine set at $673M from standalone pre-merger years. But an E&P is a depleting asset: production growth beyond the current 435-440 MBoe/d requires either more capital or acquisitions, and the recent history here is asset SALES, not purchases. Synergy capture is nearly complete, so the easy cost tailwind is behind. Against that, the Uinta and DJ inventory acquired with Civitas and XCL is real and the capital programme is disciplined. Flat real FCFF, i.e. reinvesting enough to hold volumes while returning the rest, is what this asset base does. The recorded fair value should NOT be read as a buy signal - see the data-quality note.

**Devil's advocate.**
- Strongest counter: The strongest bear case is that I am buying a commodity spike and calling it a valuation. This name won its opportunistic slot on a +31.5% twenty-one-day move, and the company news in the brief says exactly why: 'crude oil prices climbed sharply following strikes on Saudi Arabian energy facilities' (2026-09-09) and an earlier jump when 'Iran ruled out extending a 60-day memorandum of understanding with the United States' (2026-08-18). None of that is SM Energy. A geopolitical risk premium is the least durable input in any energy thesis, and the reverse DCF is being run against an enterprise value that has just been inflated by it. The mirror-image counter is also live: the strongest BULL case is that at a corrected post-merger base the market is asking for negative growth from a company with a fresh, larger, lower-cost asset base and no notes due until mid-2028.
- What would prove it: Two or three quarters of realised free cash flow at a normalised strip, and the first full-year post-merger capital programme showing what maintenance capital actually is for a 435 MBoe/d combined entity.
- Already visible today: Yes, and it is why my answer landed on flat rather than positive. The 21-day move is demonstrably a macro move - two separate Middle East headlines in the news store, and the same StockStory piece names Centrus, BKV, Select Water and ProFrac moving with it. Whatever SM is worth, it is not worth more today than three weeks ago because of anything SM did.
- Left unresolved: I could not separate maintenance capital from growth capital in the combined programme, so I could not test whether $870M of free cash flow is sustaining or partly harvesting. I also cannot correct the cost of equity - see below.

**Key risks.** The entire recent price move is a Middle East supply premium that can unwind in a week; Integration of Civitas is only two quarters old and the synergy number is management's; Depleting asset base: flat FCFF already requires continuous reinvestment, and inventory depth is the unverifiable input
**Watch for.** Q3 2026 results - the first full quarter with the combined asset base and no one-time integration costs; The 2027 capital budget, which will reveal maintenance capital for the combined entity; Any resolution or escalation of the Saudi/Iran situation, which is currently setting the price

**Data quality.** Three separate defects, and I am flagging one of them loudly because it means the RECORDED FAIR VALUE ON THIS NAME SHOULD NOT BE READ AS A SIGNAL. (1) The FCFF base of $673.0M is the mean of standalone pre-merger years [$573.0M, $471.9M, $585.0M]; the Civitas merger closed 2026-01-30 and H1 2026 free cash flow alone was $434M. I have overridden the base to $870M, which is the H1 GAAP run rate annualised. (2) The naive +22.9% five-year revenue CAGR that produced the +178.4% gap and the 87th-percentile rank is an acquisition artifact - Civitas 2026, XCL Uinta 2024, and the 2021-22 price spike - exactly the RES/PTEN pattern in LESSONS.md. It carries no information. (3) THE COST OF CAPITAL IS BROKEN AND I CANNOT FIX IT. Beta is 0.71 with an R-squared of 0.014, marked `yahoo_rescaled`, giving an 8.19% WACC for a levered shale producer - the failed-beta bias at close to its most extreme reading, and worse than a bad regression because a rescaled Yahoo figure is not our regression at all, so the R-squared gates nothing. At a defensible E&P beta of ~1.3 the WACC is roughly 11.1%, and at that discount rate my own $870M base and flat growth reproduce the market price almost exactly (implied growth +2.4%). At the engine's 8.19% the same inputs print an enterprise value of $13.1B against a market $9.9B, i.e. a spurious +32% 'cheap'. The analyst JSON has no field to override cost of equity, so the verdict is the output here and the fair value is not. One FALSE ALARM cleared: the 2026-09-04 item 1.02 8-K redeemed $416.8M of notes with cash on hand, which reduces debt and cash equally and leaves enterprise value unchanged - it does not invalidate the EV.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/893538/000089353826000128/sm-20260904.htm
- https://www.sec.gov/Archives/edgar/data/893538/000089353826000119/sm-20260805.htm
- https://www.sec.gov/Archives/edgar/data/893538/000089353826000121/sm-20260630.htm
- https://finance.yahoo.com/energy/articles/centrus-energy-sm-energy-bkv-011118972.html
- https://finance.yahoo.com/energy/articles/solaris-energy-infrastructure-sm-energy-020620676.html
