# CVLT — COMMVAULT SYSTEMS
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-07 — RICH (conviction: medium)

- **Verdict:** rich · price $136.41 · fair value $87.52 · gap -35.8%
- **Growth:** market implies +21.6%, analyst says +10.0% (delta -11.6%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 8.5% | 9.5% | 10.5% | 11.5% | 12.5% |
|---|---|---|---|---|---|---|
| bear | +4.0% | $89.94 | $77.93 | $68.76 | $61.54 | $55.69 |
| base | +10.0% | $115.44 | $99.60 | $87.52 | $78.01 | $70.33 |
| bull | +16.0% | $146.79 | $126.20 | $110.51 | $98.17 | $88.21 |

At the point WACC of 10.5%: bear -49.6%, base -35.8%, bull -19.0%
Across the whole grid the gap ranges -59.2% to +7.6% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Commvault is no longer the legacy backup vendor its five-year revenue history describes. Subscription annualized recurring revenue reached $1,054M in the quarter ended 2026-06-30, up 22%, with SaaS ARR up 38% and SaaS revenue clearing $100M in a quarter for the first time; total revenue rose 11% to $314.1M and non-GAAP EPS of $1.42 beat by 35%. The market is paying about 5.3x forward ARR for a company that has successfully repositioned from backup to cyber resilience — the one budget line that has not been cut — with a raised full-year EBIT margin outlook and free cash flow up 71% year over year in the quarter. At a 50th-percentile cohort rank, nobody is claiming this is a bargain; the price is a bet that 20%-plus ARR compounding continues long enough for the margin to catch up.

**What changed.** Q1 fiscal 2027 (2026-07-28) raised the full-year EBIT margin guide on 22% ARR growth. But the number that decides this name is the free cash flow guide, and it is the one the market is not paying for: management guides fiscal 2027 free cash flow of $250-260M against $237.2M in fiscal 2026 — growth of 5.4% to 9.6%. Subscription revenue is guided to $1,119-1,129M and subscription ARR to $1,200-1,210M. So ARR compounds at 22% while free cash flow compounds at single digits, which is the arithmetic of a SaaS transition: revenue recognised ratably against costs paid up front.

**Base case.** The model discounts reported free cash flow, and reported free cash flow at Commvault has grown $199.7M to $203.6M to $237.2M over three years — a 9% CAGR — with management guiding 5-10% for the current year. I assume that improves rather than persists: as the SaaS mix matures the cash drag from up-front costs unwinds, and a business at $1.2B of ARR with a mid-70s gross margin should convert better than it does today. So I model roughly 10% five-year FCFF growth: mid-teens revenue growth decelerating from today's 22% ARR pace, partially offset by cash margin expansion, and reduced by the fact that a meaningful part of the reported cash flow is funded by share issuance that the company then buys back. I differ from the naive +10.3% baseline only by coincidence — that baseline is a backward-looking revenue CAGR spanning the pre-SaaS years, and it happens to land near my number for entirely different reasons.

**Devil's advocate.**
- Strongest counter: The strongest case for the price is that reported free cash flow is the wrong meter during a subscription transition, and I am making the classic mistake of valuing the accounting rather than the business. ARR is the forward revenue base; at $1.2B growing 22%, with SaaS at 38%, the cash flow arrives later but arrives with better retention and better margins than the perpetual licence it replaced. Q1 free cash flow was up 71% year over year, which is the first evidence of exactly that inflection, and management guiding $250-260M for a year that includes the heaviest SaaS-cohort investment may well prove conservative. On that reading, +21.6% is not a stretch, it is what a company converting 22% ARR growth into cash at a maturing margin actually delivers.
- What would prove it: Free cash flow as a percentage of subscription revenue, quarter by quarter, over the next four to six quarters. If it climbs while ARR growth stays above 20%, the bulls are right and the required growth is achievable. If ARR decelerates below 18% before the cash margin moves, it is not.
- Already visible today: Genuinely mixed, and this is where the counter-case has its best evidence. Q1 free cash flow rose 71% to $51M and the EBIT margin guide was raised — real signs of the inflection. But management, with that quarter in hand, still guided the full year to $250-260M, which is 5-10% growth. When a company beats by 35% on EPS and does not raise the cash guide, the beat is not converting.
- Left unresolved: I could not separate how much of the fiscal 2027 free cash flow guide is genuine conservatism from how much is the real cash cost of the SaaS cohort. That distinction is the whole argument and management's guidance is the only evidence either way.

**Key risks.** Stock compensation is 52% of the FCFF base; expensed, free cash flow is $103.4M and the price requires +42.3% growth rather than +21.6%; Management's own fiscal 2027 free cash flow guide implies 5-10% growth against a price that requires 21.6% for five years; Competitive intensity in cyber resilience from Rubrik, Cohesity and Veeam; No company-specific news was in the store for the last 90 days, so my read on the competitive position rests on the company's own disclosure
**Watch for.** Free cash flow as a percentage of subscription revenue, quarter by quarter; Any raise to the $250-260M fiscal 2027 free cash flow guide; Subscription ARR growth falling below 18%

**Data quality.** The single flag — `stock_comp_is_52%_of_fcff_reported_cash_flow_treats_it_as_free` — is real and I am underwriting it explicitly. The headline reverse DCF of +21.6% treats stock compensation as free; expensing it gives an FCFF base of $103.4M and requires +42.3% growth for five years. I set final_growth against the REPORTED base the model discounts, so my +10% is comparable with the +21.6%, not with the +42.3%; on the stock-comp-expensed basis the required growth is roughly double mine and the name is correspondingly more expensive, so my verdict is if anything conservative. The enterprise value of $5.6B against a $5.7B market cap is consistent with Commvault's small net cash position and I found nothing to dispute in it. There was no company news in the store for the 90-day window, so everything here comes from the company's own release and guidance rather than from independent reporting — that is the main limit on this note.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1169561/000116956126000024/cvlt-20260630.htm
- https://ir.commvault.com/news-releases/news-release-details/commvault-announces-first-quarter-fiscal-2027-financial-results
- https://www.prnewswire.com/news-releases/commvault-announces-first-quarter-fiscal-2027-financial-results-302835588.html
