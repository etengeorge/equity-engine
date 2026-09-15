# BOX — BOX INC CLASS A
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-15 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $34.86 · fair value $42.31 · gap +21.4%
- **Growth:** market implies -7.2%, analyst says +6.0% (delta +13.2%)
- **FCFF base overridden** by the analyst to $225.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 4.7% | 5.7% | 6.7% | 7.7% | 8.7% |
|---|---|---|---|---|---|---|
| bear | +1.0% | $58.81 | $42.99 | $33.88 | $27.96 | $23.80 |
| base | +6.0% | $74.02 | $53.89 | $42.31 | $34.79 | $29.51 |
| bull | +11.0% | $92.31 | $66.98 | $52.42 | $42.96 | $36.33 |

At the point WACC of 6.7%: bear -2.8%, base +21.4%, bull +50.4%
Across the whole grid the gap ranges -31.7% to +164.8% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Box is a mature, high-retention content platform growing revenue 9% with billings up 17%, guiding to about $1.29B of fiscal 2027 revenue, and converting most of that into operating cash flow ($356.5M last year against $6.1M of capex). The distinguishing fact is what it does with the cash: weighted-average basic shares fell from 144,896 thousand to 137,379 thousand year over year — a 5.2% net reduction AFTER absorbing all stock compensation — funded by $185.7M of repurchases in the first half alone, more than double the prior year's $89.6M. A buyer at $34.86 is underwriting flat-to-modestly-growing free cash flow compounding into a share count that shrinks 5% a year, which produces high-single-digit per-share growth with no revenue acceleration required. Enterprise Advanced and AI-driven bookings are optionality on top, not the case.

**What changed.** Q2 fiscal 2027, reported 2026-08-25/26 (8-K item 2.02; 10-Q 2026-08-26 for the quarter ended 2026-07-31). Revenue $321.1M, +9%; billings +17%; net income $19.2M; adjusted EPS $0.40, +21%; record Enterprise Advanced adoption. Full-year guidance raised to roughly $1.29B of revenue with a higher GAAP operating margin. UBS raised its target to $37 with a Neutral rating and wants more proof the momentum sustains. Financing detail from the 10-Q that is not in any summary: H1 repurchases of common stock $185,662 thousand against $89,583 thousand a year ago, employee payroll taxes for net settlement of stock awards $36,845 thousand, preferred dividends $7,500 thousand, and $426.7M of unrecognised stock compensation still to be recognised over a weighted-average 2.67 years.

**Base case.** The brief's headline gap of +106.9% and its 89th-percentile rank are a stock-compensation artifact, and the flag's two endpoints are both wrong. Treating $224M of stock compensation as free gives a base of $339.1M and an implied growth of -7.2%, which flatters the name; expensing it entirely gives $122.0M and +15.9%, which penalises it. Neither is the economics. The right construction is operating cash flow less capex less the cash actually required to hold the share count flat. Box repurchased roughly $371M annualised and SHRANK the count 7.5M shares net, so gross buybacks of about 10.9M shares offset roughly 3.4M shares of dilution — about $118M a year. Owner earnings are therefore approximately $350M less $118M, or $232M, less $15M of preferred dividends, call it $217-232M. At that base the market implies +0.9% to +2.4% at the engine's WACC, against a business growing 9%. I use +6% as my base case: revenue growth decelerating toward mid-single digits, partly offset by continuing margin expansion.

**Devil's advocate.**
- Strongest counter: This was my starting position and it is the obvious one: stock compensation is 66% of the FCFF base and about 19% of revenue, with $426.7M more still unrecognised. On a fully-expensed base the market requires +15.9% growth from a company growing 9%, which is rich. The buyback is not evidence against this — it is the cash cost of the compensation becoming visible, and Box is funding roughly $371M of annualised repurchases out of roughly $356M of operating cash flow, i.e. spending more than it earns, supported by $342.9M of cash and $452.2M of debt. That is not sustainable, and when it stops the share count stops shrinking.
- What would prove it: The net share count trend over the next four quarters, and whether repurchases fall back toward the dilution-offsetting level of roughly $120M a year once the cash balance is drawn down.
- Already visible today: Yes, and it beat my original reading, which is why the verdict moved. The weighted-average share counts are in the 10-Q and they are unambiguous: 144,896 thousand to 137,379 thousand, a 5.2% net reduction achieved WHILE absorbing every dollar of stock compensation. That is the fact the 66%-of-FCFF flag cannot see, and it defeats the simple 'expense it and call it rich' conclusion I began with. The counter's own strongest point — that buybacks exceed operating cash flow — is real and is why I did not swing the other way to cheap; it caps the sustainable shrink well below 5% a year, which is exactly why my base uses the $118M dilution-offset cost rather than the full $371M.
- Left unresolved: The cost of capital. Box's beta is 0.35 with an R-squared of 0.044, barely above the engine's own 0.04 gate, giving a 6.7% WACC to an enterprise software company. At a defensible software beta near 1.0 the WACC is roughly 9%, and at 8.5% my own $232M base implies +8.5% growth rather than +0.9% — i.e. fair rather than cheap. The whole remaining answer sits on a regression that explains 4% of the variance, and the schema has no field to override it. That is what holds this at no_edge instead of cheap.

**Key risks.** Beta of 0.35 with R-squared 0.044 produces a 6.7% WACC; at a defensible ~9% the implied growth rises to roughly +10% and the name is fair, not cheap; Repurchases are running above operating cash flow and are drawing on cash and debt — the 5% annual share shrink is not indefinitely fundable; $426.7M of unrecognised stock compensation still to be expensed over ~2.67 years; Core content management is a mature market; the AI/Enterprise Advanced uplift is one cycle of evidence, not a trend
**Watch for.** Net weighted-average share count over the next four quarters — a stall confirms the bear; Repurchase pace falling toward ~$120M a year (dilution offset only); Net revenue retention disclosure, and whether billings growth of 17% converts into revenue growth above 9%; Any debt raise to fund further buybacks

**Data quality.** Resolved: `stock_comp_is_66%_of_fcff_reported_cash_flow_treats_it_as_free`. Neither endpoint the flag offers is the economics; I constructed owner earnings as CFO less capex less the cash cost of holding the share count flat ($118M/yr, derived from the 5.2% net shrink against roughly $371M of annualised gross repurchases) and overrode the base to $225M. This moves the implied growth from -7.2% to about +1.6% and removes the +106.9% gap as an artifact. Open and material: the cost of capital. `beta_r2` is 0.044 against an engine gate of 0.04, which is the failed-beta bias at close to its worst reading, and correcting the base WITHOUT correcting the WACC would make this name look cheap for the wrong reason — the two corrections point in opposite directions and roughly cancel, which is why the verdict is no_edge. Also noted: Box carries preferred stock paying $15M a year which does not appear in the enterprise value.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1372612/000119312526368289/box-20260731.htm
- https://www.sec.gov/Archives/edgar/data/1372612/000119312526365121/d87668d8k.htm
- https://www.fool.com/earnings/call-transcripts/2026/09/01/box-box-q2-2027-earnings-call-transcript/
