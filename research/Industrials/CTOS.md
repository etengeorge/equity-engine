# CTOS — CUSTOM TRUCK ONE SOURCE
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-02 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $8.87 · fair value $1.69 · gap -80.9%
- **Growth:** market implies +6.9%, analyst says +5.0% (delta -1.9%)
- **FCFF base overridden** by the analyst to $145.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 8.2% | 9.2% | 10.2% | 11.2% | 12.2% |
|---|---|---|---|---|---|---|
| bear | -2.0% | $1.47 | $0.29 | $-0.60 | $-1.30 | $-1.87 |
| base | +5.0% | $4.61 | $2.95 | $1.69 | $0.71 | $-0.08 |
| bull | +11.0% | $8.00 | $5.81 | $4.16 | $2.87 | $1.84 |

At the point WACC of 10.2%: bear -106.8%, base -80.9%, bull -53.1%
Across the whole grid the gap ranges -121.1% to -9.8% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Custom Truck rents and sells specialty vehicles into transmission and distribution utility markets, and the market is paying about 8x forward Adjusted EBITDA for it. Q2 2026 was a record: revenue $563.4M (+10% y/y), Adjusted EBITDA $116.8M (+25%), rental fleet utilisation 81.6% (up 400bp), total OEC $1.68B, and a return to positive net income of $10.4M from a $28.4M loss. Guidance was raised to $2.1-2.2B revenue and $437.5-455M Adjusted EBITDA. Net leverage fell to 3.85x from 4.31x at year-end. Against that, the price embeds the thing management keeps flagging: this is a capital-devouring business. Fleet investment consumes nearly all the cash the fleet produces, so a 25% EBITDA increase converts into levered free cash flow the company itself guides at only 'in excess of $50 million'. At 3.85x leverage, the equity is a residual on a $1.66B debt stack, and the -16.6% 21-day move is the market marking that residual down as rates back up.

**What changed.** Q2 2026 results and raised guidance (2026-08-03). 2026 net rental fleet investment guidance was raised to $170-200M from a lower prior range, on mid-single-digit net OEC growth — down from over $250M in 2025 but still the dominant use of cash. Levered free cash flow guided to exceed $50M; the longer-term target is net leverage below 3x in 2027.

**Base case.** T&D, grid upgrade, electrification and data-centre demand are real and durable, and CTOS is well placed in them — I do not dispute the operating story. But the FCFF this model discounts has to be the cash left after the fleet is maintained and grown, and on the company's own numbers that is roughly $50M levered, or on the order of $145M unlevered once after-tax interest is added back. Growing that at high-single digits requires either fleet growth (which consumes the cash) or margin expansion on a fixed fleet. Mid-single-digit growth in genuinely free cash flow is the honest central case, and it is far below the +25% clamped revenue baseline the screen applied.

**Devil's advocate.**
- Strongest counter: The counter is that I have replaced the model's cash-flow base with a much smaller number and thereby argued a cheap name into no_edge, and my substitute could be wrong in the same direction the model's was. Growth capex is discretionary: the $170-200M of net fleet investment includes fleet EXPANSION, and a company that chose to stop growing its fleet would convert most of that back into free cash. Maintenance capex on a $1.68B OEC fleet is materially less than $200M. If I strip only maintenance, free cash flow is well above $50M and the stock at 8x EBITDA with 25% EBITDA growth and a falling leverage ratio is genuinely inexpensive — which is roughly what the sell side thinks, with a mean target ~25% above the price.
- What would prove it: The split between maintenance and growth fleet investment, and what happens to free cash flow in a year when OEC is held flat. Management's sub-3x leverage target for 2027 is the testable claim: hitting it requires roughly $300M of debt reduction, which cannot happen on $50M of levered free cash flow unless fleet spending drops a long way.
- Already visible today: Partly, and it cuts both ways. Net leverage genuinely fell from 4.31x to 3.85x in six months, so real deleveraging is happening — that supports the bull. But it happened while net fleet investment was cut from over $250M to $170-200M, which is the point: the deleveraging is funded by spending less on the fleet, not by the fleet generating more. I could not find a maintenance-versus-growth capex split in the release or the 10-Q.
- Left unresolved: The maintenance capex number, which decides whether $50M or $200M is the right free-cash-flow base — a three-to-four-fold range that spans cheap to expensive. That is too wide to call, and it is the reason this is no_edge rather than a verdict in either direction.

**Key risks.** 3.85x net leverage on $1.67B of debt makes the equity a thin residual on a cyclical fleet; Rental fleet residual values fall if used equipment prices normalise, hitting both earnings and the borrowing base; T&D and data-centre demand is the whole thesis on both sides; a pause in utility capex hits utilisation and leverage together
**Watch for.** Q3 2026 utilisation and OEC: utilisation below 78% would mean the fleet is outrunning demand; Actual levered free cash flow against the '>$50M' guide, and whether net leverage keeps falling; Any disclosure separating maintenance from growth fleet investment

**Data quality.** The brief raised no flags, and it should have raised a serious one. The extracted capex_series for CTOS is [$0.87M, $3.07M] — under $4M of capital spending in two years for a company that bought $191.6M of rental equipment in the six months to 2026-06-30 alone and guides $170-200M of NET fleet investment for 2026. The extractor is picking up only non-rental property capex; every dollar of rental fleet purchasing is missing. That is why the model reports a $241.5M normalised FCFF base while the company guides levered free cash flow just over $50M. The entire +184% gap and the 95th-percentile cohort rank are produced by that omission, compounded by a naive baseline built on a +65.9% revenue CAGR (clamped to +25%) that is an artefact of the 2021 Nesco/Custom Truck combination, not organic growth. Enterprise value and share count are CORRECT and I verified them: total debt $1,673.2M less cash $10.3M gives net debt $1,662.9M, matching the model's $3.7B EV. I have set fcff_base_override to a rough unlevered estimate ($50M guided levered FCF plus after-tax interest) so the recorded valuation is at least built on cash the company says it will actually generate; treat that override as an estimate, not a filing figure. This error class is not specific to CTOS — it will affect every rental and leasing company in the universe.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1709682/000170968226000039/ex991q22026pressrelease.htm
- https://www.sec.gov/Archives/edgar/data/1709682/000170968226000040/ctos-20260630.htm
- https://www.fool.com/earnings/call-transcripts/2026/08/10/custom-truck-one-source-ctos-q2-2026-earnings-call-transcript/
- https://finance.yahoo.com/markets/stocks/articles/custom-truck-one-source-ctos-131055188.html
