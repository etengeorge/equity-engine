# VRNS — VARONIS SYSTEMS
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — RICH (conviction: low)

- **Verdict:** rich · price $45.12 · fair value $20.11 · gap -55.4%
- **Growth:** market implies +37.6%, analyst says +14.0% (delta -23.6%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 8.0% | 9.0% | 10.0% | 11.0% | 12.0% |
|---|---|---|---|---|---|---|
| bear | +2.0% | $16.73 | $14.61 | $13.02 | $11.78 | $10.78 |
| base | +14.0% | $26.54 | $22.86 | $20.11 | $17.97 | $16.26 |
| bull | +22.0% | $35.67 | $30.53 | $26.68 | $23.69 | $21.30 |

At the point WACC of 10.0%: bear -71.1%, base -55.4%, bull -40.9%
Across the whole grid the gap ranges -76.1% to -20.9% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $45.12 the market is paying ~$5.0B EV for a data-security platform whose SaaS ARR reached $726.0M, up 52% year over year and up 25% excluding conversions, with new-logo SaaS ARR growing more than 20% and management raising the full-year SaaS ARR outlook to $769-775M excluding conversions. The bull case is straightforward: Varonis is roughly through a term-licence-to-SaaS conversion that mechanically suppresses reported cash flow, AI adoption is forcing enterprises to classify and govern unstructured data, and newer products (Atlas, Interceptor, Database Activity Monitoring) are adding to the motion. Post-conversion, a security platform at 20%+ ARR growth should convert 25-30% of revenue to free cash flow, which is a much larger number than today's.

**What changed.** Q2 2026 (2026-07-28 release): SaaS ARR $726.0M, +52% (+25% ex-conversions). Full-year SaaS ARR guidance RAISED to $819.0-850.0M. But free cash flow for the six months ended 2026-06-30 was $69.1M against $82.7M in the prior-year period — DOWN 16% — and full-year free cash flow is guided to $105.0-110.0M against $134.8M actually generated in FY2025. ARR is accelerating while cash flow is guided down.

**Base case.** The honest steady-state: if Varonis exits FY2026 at ~$850M of SaaS ARR growing ~20% and eventually converts at a mature security-software margin of ~26%, owner earnings are roughly $220M — about double the $101.6M base and double the $105-110M the company guides this year. Compounding ARR at 20% for five years and holding that margin gives roughly $550M, i.e. ~14% annual growth off my corrected base. That is my base case and it is deliberately generous: it assumes the conversion drag unwinds immediately and in full. It is still well below the +37.6% the current price requires on the reported base, and below the +16.3% it requires even on the generous $220M base.

**Devil's advocate.**
- Strongest counter: I argued this side first and it is the real case: the SaaS conversion genuinely depresses reported cash flow, because customers move from multi-year upfront term payments to annual SaaS billing, so the FCFF base I am dividing by describes the transition and not the business. On that reading the +37.6% requirement is an artifact of a temporarily suppressed denominator, exactly as MXL's multiples were an artifact of a suppressed revenue denominator.
- What would prove it: Free cash flow re-accelerating above the FY2025 level of $134.8M once conversions annualise, and stock compensation falling as a share of revenue.
- Already visible today: It points the other way so far. FY2026 free cash flow is guided to $105-110M, BELOW the $134.8M of FY2025, and H1 free cash flow already fell 16% year over year. The conversion argument predicts a trough, and the company's own guidance says the trough is this year and deeper than last — but it does not yet show the recovery.
- Left unresolved: How much of the FY2026 FCF decline is conversion mechanics versus spending. I ran the steelman anyway: even granting the full post-conversion margin TODAY on a $220M base, the price still requires +16.3% compounding for five years. The counter did not rescue the price, which is why the verdict is rich rather than no_edge.

**Key risks.** Stock compensation is 133% of the FCFF base — on an expensed basis FCFF is -$30.7M and no growth rate can be solved at all; Microsoft bundling Purview into E5 removes the budget line rather than the competitor; GAAP net losses of $129M/$96M/$101M across the window; this has never been GAAP profitable
**Watch for.** FY2027 free cash flow guidance against the $134.8M FY2025 high-water mark; Stock compensation as a percentage of revenue trending below 20%; SaaS ARR growth ex-conversions holding above 20%

**Data quality.** The flags are real and I resolved them rather than dismissing them. `stock_comp_is_133%_of_fcff`: confirmed, sbc_series [$130.2M, $126.7M, $139.8M] against a $101.6M base — this is the single most important fact on the name and it means the two defensible treatments (add back / expense) give answers 40 points apart. I underwrite the RICH call on the reported base because the expensed base is worse, not better: both treatments say the price is demanding, so unlike the EVI precedent the ambiguity does not straddle the decision. `possible_peak_cycle_base_newest_fcf_2.5x_oldest`: confirmed and real — FCF ran $54.3M -> $108.5M -> $134.8M and is now guided DOWN to $105-110M, so the 3-year mean of $101.6M happens to sit almost exactly on FY2026 guidance. `speculative_cost_of_debt_but_only_8%_debt_weight`: immaterial. Beta 0.87 at R-squared 0.086 is in the weak-fit bucket LESSONS.md warns about, but here it would make the name look CHEAPER, so it does not support the rich call — the call survives it.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1361113/000162828026050630/vrns-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1361113/000117184326004948/f8k_072826.htm
- https://www.sec.gov/Archives/edgar/data/1361113/000162828026005450/vrns-20251231.htm
