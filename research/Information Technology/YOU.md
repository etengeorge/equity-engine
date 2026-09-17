# YOU — CLEAR SECURE CLASS A
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $40.67
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** CLEAR is compounding fast and the market knows it: Q2 revenue +26.6% to $277.8M, Total Bookings +32.8% to $295.9M, FY2026 free cash flow guidance RAISED from at least $465M to at least $480M (+39.9% year over year), a CrowdStrike partnership announced 2026-08-31 extending CLEAR1 into the Falcon platform, and a net-cash balance sheet with no debt. At the true enterprise value the market is asking roughly zero five-year FCFF growth from a business growing bookings ~20%, which is a defensible price rather than an obvious mistake — because the free cash flow is flattered by prepaid annual subscriptions and the growth rate is decelerating.

**What changed.** Q2 2026 (filed 2026-08-05) raised FY26 FCF guidance to at least $480M. The share structure is the thing that matters and it is not news, it is an uncorrected input: CLEAR is an Up-C. At 2026-06-30 there were 101,940,628 Class A, 151,787 Class B, 14,246,787 Class C and 18,380,246 Class D shares; Class C and D each accompany an Alclear LLC Unit exchangeable into Class A/B, so the fully-exchanged economic count is 134,719,448. Also disclosed: a Tax Receivable Agreement liability of $256,695k — a real claim on the enterprise that is neither debt nor shares, the PRM pattern.

**Base case.** No fair value is recorded because the engine's share count is 1,356 days stale and 35% too low, and the schema cannot override it. The arithmetic: the engine holds 87,760,831 shares (the 2022-12-31 Class A count) and computes a $3.57B market cap and a $2.65B enterprise value. On the true fully-exchanged 134,719,448 shares market cap is $5.48B and EV is $4.56B — 72% higher. That alone takes the growth the market implies from -3.7% to +9.2% and would make the name expensive. But a SECOND error runs the other way and is just as large: the FCFF base of $275.4M is the three-year mean of [$343.1M, $283.7M, $199.5M] for a company whose own FY2026 guidance is at least $480M. Correcting BOTH leaves the market implying -4.0% at the engine's 10.3% WACC and +0.3% at a defensible 12%. Per the SM rule, two large errors pointing in opposite directions give no_edge, not the average. My own view is that CLEAR compounds FCFF at roughly +5% over five years off an already-elevated base — bookings growth is decelerating (+32.8% year over year in Q2 but guided to +20.5% in Q3, and sequentially $287.1M -> $291.7M -> $295.9M), the deferred-revenue tailwind that inflates free cash flow fades with it, and the fully-exchanged count still creeps up ~2.3% a year.

**Devil's advocate.**
- Strongest counter: The counter changed my answer twice, in both directions. I first established the stale Up-C share count, which raises EV 72% and turns a +160% gap into a name requiring +9.2% growth — i.e. rich. Arguing the opposite case forced me to ask what else the brief had wrong in MY favour, and the answer was the cash-flow base: the company's own guidance is at least $480M against a $275.4M base, which is a 74% understatement and pushes the required rate back to roughly zero. Neither correction alone is honest.
- What would prove it: Whether Total Bookings keep outrunning revenue. Bookings above revenue means the deferred-revenue float is still building and free cash flow overstates earnings; bookings converging on revenue means the reported FCF is real but stops growing.
- Already visible today: Partly. Q2 bookings of $295.9M against revenue of $277.8M is an $18M quarterly build, and H1 deferred revenue rose $56.8M — roughly 15% of the $374.5M of H1 free cash flow is float rather than earnings. Against that, Q3 bookings guidance of $311-316M is a 5-7% sequential step up, so the plateau I suspected in the trailing series is not yet confirmed.
- Left unresolved: What the right discount rate is. beta is 0.96 with an R-SQUARED OF EXACTLY 0.0, sourced yahoo_rescaled, so the 10.3% WACC is not a measurement at all; the answer moves from -4.0% to +0.3% between 10.3% and 12%, which is most of the question. I also could not settle how much of the 26.6% revenue growth is price rather than members.

**Key risks.** free cash flow is structurally flattered by prepaid annual subscriptions; the float reverses if growth stops; CLEAR+ depends on airport and TSA relationships it does not control; a $256.7M Tax Receivable Agreement liability sits outside enterprise value and outside the share count; the fully-exchanged share count rises ~2.3% a year and buybacks have essentially stopped ($1.2M in H1 against $250.3M of remaining authorisation)
**Watch for.** Total Bookings converging on revenue — the tell that the deferred-revenue tailwind has ended; the 3Q26 cover page, and whether the engine ever picks up Class B/C/D rather than Class A alone

**Data quality.** RESOLVED: share_count_1356d_stale is real and is the larger half of the gap — the engine uses 87,760,831 Class A shares from 2022-12-31 against a true fully-exchanged 134,719,448, understating market cap 35% and enterprise value 42%. The possible_peak_cycle_base flag is BACKWARDS: the base is not a peak, it is 43% BELOW the company's own FY26 guidance. NEW AND UNFLAGGED: a $256,695k Tax Receivable Agreement liability outside EV, and beta with R-squared of exactly 0.0 marked yahoo_rescaled. NO final_growth IS SUPPLIED DELIBERATELY: pricing this name through the schema would multiply a corrected base by a share count that is 35% too low and publish a per-share fair value roughly 1.5x too high. The verdict is the output here, not a number.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1856314/000185631426000042/you-20260630.htm (10-Q, 2026-06-30: four-class share counts, TRA liability, equity-based compensation, no outstanding debt)
- https://www.sec.gov/Archives/edgar/data/1856314/000185631426000039/clearq22026pressreleaseear.htm (Q2 2026 EX-99.1: revenue, Total Bookings series, raised FY26 FCF guidance)
- company news in brief: CrowdStrike/CLEAR1 partnership 2026-08-31

**Ingestion notes.** no usable final_growth
