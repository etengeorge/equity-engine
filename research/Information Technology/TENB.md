# TENB — TENABLE HOLDINGS
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-18 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $36.06 · fair value $38.08 · gap +5.6%
- **Growth:** market implies +6.6%, analyst says +8.0% (delta +1.4%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 7.7% | 8.7% | 9.7% | 10.7% | 11.7% |
|---|---|---|---|---|---|---|
| bear | +2.0% | $39.88 | $34.34 | $30.23 | $27.07 | $24.55 |
| base | +8.0% | $50.88 | $43.52 | $38.08 | $33.89 | $30.57 |
| bull | +14.0% | $64.46 | $54.85 | $47.74 | $42.27 | $37.95 |

At the point WACC of 9.7%: bear -16.2%, base +5.6%, bull +32.4%
Across the whole grid the gap ranges -31.9% to +78.8% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Tenable is the share leader in device vulnerability and exposure management for the eighth consecutive year, growing revenue 8.6% to $268.5 million in Q2 2026 with unlevered free cash flow guided to $289-295 million for the year, 27.1% of revenue at the midpoint. It is converting that cash into share count: 11.4 million shares for about $230 million in the first half, a further ~5.3 million for $170.5 million alongside the September convertible, and a weighted-average diluted count at its lowest since Q4 2020. On 2026-09-15 it issued $800 million of 0.25% convertible notes due 2031 at a $44.84 conversion price with a capped call to $64.06, repaid its term loans in full and terminated the credit agreement. The market is paying roughly 3.9x revenue for an 8%-growing security platform with a 27% cash margin that is shrinking its share count 8% a year. The stock rose 16.5% on 2026-09-15 in a broad software rally.

**What changed.** The capital structure, entirely after the 2026-06-30 balance sheet. 8-K 2026-09-15 (items 1.01/1.02/2.03/3.02/8.01/9.01): $800.0 million of 0.25% convertible senior notes due 2031, upsized twice from the $650 million first announced, including the initial purchasers' $75 million option exercised in full. Net proceeds $778.8 million, applied to $64.1 million of capped call cost, $170.5 million of stock repurchased at the $32.03 pricing-date price, and full repayment of the term loans under the July 2021 credit agreement, which was terminated effective 2026-09-15. Notes convert into 17,840,400 shares, 24,976,560 at the maximum. Also announced: Claude Mythos 5 embedded into Tenable One Adversary View (2026-09-08) and OpenAI GPT cyber models in CyberAgents Exchange (2026-09-03).

**Base case.** Revenue is guided to $1.075-1.081 billion, up 7.9% at the midpoint, and unlevered free cash flow to $289-295 million, up from $254.6 million, $213.2 million and $148.2 million in the three years of the model's window. That ramp is a margin story — the cash margin has roughly doubled to 27% — and margin expansion of that size does not repeat from here. So FCFF growth should converge on revenue growth, and 8% is where I put it: the platform consolidation thesis (Tenable One, exposure management, the AI-security attach) is real enough to hold mid-to-high-single-digit growth, and not strong enough to reaccelerate it.

**Devil's advocate.**
- Strongest counter: The bear case on the flag is the obvious one and it is very strong: stock compensation is 81% of the FCFF base. It ran $46,349 thousand in Q2 and $90,203 thousand in the first half — about $180 million a year, 17% of revenue. Charge it and owner earnings are roughly $292 million of guided unlevered free cash flow less $180 million, or about $112 million, against a corrected enterprise value near $4.2 billion: a 2.7% yield on a business growing 8%. On that treatment the market is asking for something like +30% compounding and the name is not 86th-percentile cheap, it is expensive.
- What would prove it: The NET share count — whether buybacks are genuinely absorbing the dilution or merely offsetting part of it. This is the BOX test from 2026-09-15.
- Already visible today: Yes, and it cuts BOTH ways, which is why this ends where it does. In Tenable's favour: weighted-average basic shares fell from 120,979 thousand in Q2 2025 to 110,742 thousand in Q2 2026, a NET reduction of 8.5% after absorbing every dollar of stock compensation, with treasury stock rising from 10,596 to 21,914 thousand shares. That is a larger net shrink than BOX's 5.2% and it says shareholders are capturing the cash. Against Tenable: the buybacks were not funded from operations. About $402 million has been spent in nine months against $292 million of annual unlevered free cash flow, and the September tranche came out of an $800 million convertible. A share count shrinking on borrowed money is not the same claim as a share count shrinking on earnings.
- Left unresolved: Which treatment of stock compensation is right. I could not resolve it, and the two are not close: the required growth is about +4% if stock compensation is free and about +30% if it is charged in full. That spread is far outside the +/-15% FCFF band, so by the standing rule this is no_edge and I record the range rather than a false midpoint. I have left the engine's $228.8 million base in place precisely because it sits between the two treatments — it is close to charging half the stock compensation against the current run rate.

**Key risks.** Stock compensation of about $180 million a year, 17% of revenue; charging it takes owner earnings to roughly $112 million and the required growth to about +30%; Enterprise value is understated: the engine's $3.7bn carries a ZERO debt weight and omits the $352,983 thousand of term debt on the 2026-06-30 balance sheet, and now the $800 million convertible — the flag `interest_expense_implies_no_debt_found` names the bug and the model used the broken number anyway; The $800m convertible adds 17,840,400 shares of potential dilution above $44.84, capped-called to $64.06; Beta 0.86 with R-squared 0.111 is in the band where the low-fit beta bias manufactures apparent cheapness
**Watch for.** Q3 2026 unlevered free cash flow against the $289-295 million guide, and whether the buyback pace moderates once the convertible proceeds are spent; Stock compensation as a percentage of revenue — a fall below 15% would settle the argument in Tenable's favour; Net retention rate disclosure, the cleanest read on whether exposure management is consolidating or commoditising

**Data quality.** Three flags, all live. `interest_expense_implies_no_debt_found_on_reported_debt_debt_likely_understated` is correct and material: the engine's enterprise value of $3.7bn is market capitalisation less $298.3 million of cash and short-term investments with NO debt deducted, while the 10-Q reports $352,983 thousand of term debt — enterprise value understated by roughly 10% before the convertible, which is the TDOC missing-debt shape running toward false cheapness. `possible_peak_cycle_base` is backwards: the newest year is the lowest of the three only in the sense that the series is RISING, and the company's own guide of $289-295 million is above every year in the window, so the base understates rather than overstates. `stock_comp_is_81%_of_fcff` is the flag that decides the name and I could not resolve it in either direction — see the devil's advocate. Post-transaction enterprise value is roughly $4.2bn: $800m of converts, term loan repaid, about $191m of net new cash, 5.3m fewer shares.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1660280/000166028026000039/tenb-20260910.htm
- https://www.sec.gov/Archives/edgar/data/1660280/000166028026000039/exhibit991.htm
- https://www.sec.gov/Archives/edgar/data/1660280/000166028026000035/tenb-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1660280/000166028026000032/q22026financialresults-ear.htm
- https://www.fool.com/earnings/call-transcripts/2026/08/07/tenable-tenb-q2-2026-earnings-call-transcript/
