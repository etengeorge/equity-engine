# RLGT — RADIANT LOGISTIC INC
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $9.10 · fair value $8.80 · gap -3.3%
- **Growth:** market implies -2.0%, analyst says +11.0% (delta +13.0%)
- **FCFF base overridden** by the analyst to $20.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 7.9% | 8.9% | 9.9% | 10.9% | 11.9% |
|---|---|---|---|---|---|---|
| bear | +4.0% | $8.85 | $7.68 | $6.81 | $6.14 | $5.60 |
| base | +11.0% | $11.60 | $10.00 | $8.80 | $7.87 | $7.13 |
| bull | +18.0% | $15.11 | $12.93 | $11.31 | $10.06 | $9.06 |

At the point WACC of 9.9%: bear -25.1%, base -3.3%, bull +24.3%
Across the whole grid the gap ranges -38.5% to +66.0% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Radiant is a debt-free, asset-light freight forwarder at the bottom of a freight cycle with a founder-CEO, a newly extended $200M revolver to 2031, a $100M acquisition accordion and visibly accelerating momentum — Q4 revenue +18.5%, adjusted EBITDA +31.6%, adjusted EBITDA margin +240bp. Buying a cyclical forwarder on trough earnings before the cycle turns is a reasonable thing to pay up for, and the +10% five-day move on 5x volume is the market doing exactly that after the 2026-09-14 results.

**What changed.** EVERYTHING THE ENGINE IS PRICING PREDATES A 10-K FILED THREE DAYS AGO. Radiant filed its FY2026 10-K (year ended 2026-06-30) on 2026-09-14 with the Q4 8-K; the engine's extract carries fy_end 2025-06-30 and fundamentals_age_days 444. The new actuals: revenue $934.4M (from $902.7M), net income attributable $18.8M ($0.40 basic), adjusted net income $25.3M — DOWN from $30.9M — and adjusted EBITDA of $36.7M, DOWN 5.4% from $38.8M. Operating cash flow was $17.5M against $4.3M of capex, i.e. free cash flow of $13.2M. Also new: an amended and restated $200M secured revolver (2026-08-07) extending maturity to 2031 with the accordion raised from $75M to $100M; $25.0M drawn at 2026-06-30 against $25.6M of cash, so no net debt; and a new COO appointed 2026-08-31.

**Base case.** The +12.7% gap is an artifact of a cash-flow base that is 2.7x the company's actual free cash flow. The engine's $35.7M base is the mean of three cfo-less-capex years of [$8.1M, $8.7M, $90.3M], where the $90.3M is fiscal 2023 — the tail of the freight super-cycle, when revenue collapsed from $1,459M to $1,085M and released an enormous slug of working capital. That is a one-off liquidation of receivables, not earning power, and no flag fired on it. Against the FY2026 actual of $13.2M, a three-year mean of genuine recent free cash flow of ~$10M, and an EBITDA-less-capex-and-tax normalisation of ~$25M, I take $20M as a defensible normalised base: above the current depressed print because working capital is consuming cash as revenue reaccelerates, and well below the engine's number. Enterprise value is also understated — the engine nets off $39.7M of stale cash and carries zero debt, while the 10-K shows $25.0M drawn on the revolver against $25.6M of cash, so true EV is ~$426M against the recorded $387M. On corrected inputs the market requires +14.4% five-year FCFF growth at a $20M base (and +8.8% to +25.3% across the defensible base range), not the -2.0% the brief reports. I can underwrite roughly +11% from a genuine freight recovery plus agent-network and acquisition growth — which is BELOW what the price already asks.

**Devil's advocate.**
- Strongest counter: The base I chose is a trough, and applying an ordinary growth rate to a trough understates a cyclical — the exact error the brief's own flag language warns about. If FY2026's $13.2M of free cash flow is the bottom and normalised mid-cycle free cash flow is $40M+, then the required +14% is being measured off the wrong starting point and the name is cheap, not fair. Q4 is genuine evidence for this: revenue +18.5%, adjusted EBITDA +31.6%, margin +240bp, with international airfreight and domestic surface both cited.
- What would prove it: Whether adjusted EBITDA growth converts into cash. The FY2027 cash flow statement — operating cash flow against the $36.7M-and-rising EBITDA line — settles it, because the gap between the two has been the whole story for two years.
- Already visible today: Partly, and it cuts against the bull. FY2026 adjusted EBITDA was $36.7M and operating cash flow was $17.5M; FY2025 was $38.8M and $13.3M. Radiant has now converted roughly 40% of adjusted EBITDA into operating cash in each of two years, so a recovery in EBITDA does not mechanically become free cash flow — working capital in a forwarder consumes cash precisely when revenue accelerates.
- Left unresolved: I could not settle mid-cycle free cash flow with any confidence, and the answer spans +8.8% to +25.3% of required growth across bases I can defend. That range is the honest precision here and it is too wide to call the name either way.

**Key risks.** adjusted EBITDA fell 5.4% in FY2026 and adjusted net income fell 18%, so the 'recovery' has not yet shown up in the full-year numbers; EBITDA-to-cash conversion has run near 40% for two years and worsens as growth accelerates; the 10-K's own forward-looking section references a prior material weakness in internal control over financial reporting; an agent/station model means operating partners can leave and take volume with them
**Watch for.** FY2027 Q1 (December filing) operating cash flow against adjusted EBITDA — the conversion test above; use of the $100M accordion: a large acquisition changes both the base and the enterprise value at once

**Data quality.** RESOLVED: the only flag raised was volume_5.0x_its_60d_average, and the two defects that matter were unflagged. (1) The extract is a FULL YEAR stale — fy_end 2025-06-30, fundamentals_age_days 444 — against a 10-K filed 2026-09-14; every input below is from the new filing. (2) The FCFF base is one-third a freight-super-cycle working-capital release ($90.3M of $107.1M across three years) and no peak/trough flag fired. (3) Enterprise value misses the $25.0M revolver draw and uses $39.7M of stale cash against an actual $25.6M — the ALTG revolver bug again, small here (~10% of EV) but in the cheap direction. Corrected base and EV together move the growth the market requires from -2.0% to +14.4% and the +12.7% gap inverts.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1171155/000119312526390768/rlgt-20260630.htm (FY2026 10-K filed 2026-09-14: operating cash flow $17.5M, capex $4.3M, acquisitions $5.2M)
- https://www.sec.gov/Archives/edgar/data/1171155/000119312526390772/rlgt-ex99_1.htm (Q4/FY2026 EX-99.1: revenue, adjusted EBITDA $36.7M, adjusted net income, $200M revolver, no net debt)
- https://www.sec.gov/Archives/edgar/data/1171155/000119312526347070/rlgt-ex99_1.htm (2026-08-12 EX-99.1: amended and restated $200M secured revolving credit facility)
