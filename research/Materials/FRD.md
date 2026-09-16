# FRD — FRIEDMAN INDUSTRIES INC
*Materials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-16 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $40.80 · fair value $49.94 · gap +22.4%
- **Growth:** market implies +13.4%, analyst says +3.0% (delta -10.4%)
- **FCFF base overridden** by the analyst to $28.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 8.4% | 9.4% | 10.4% | 11.4% | 12.4% |
|---|---|---|---|---|---|---|
| bear | -8.0% | $40.21 | $35.15 | $31.30 | $28.25 | $25.79 |
| base | +3.0% | $65.45 | $56.64 | $49.94 | $44.66 | $40.40 |
| bull | +10.0% | $87.75 | $75.56 | $66.30 | $59.02 | $53.15 |

At the point WACC of 10.4%: bear -23.3%, base +22.4%, bull +62.5%
Across the whole grid the gap ranges -36.8% to +115.1% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $40.80, up 94.5% over twelve months, the market is paying for a transformed Friedman: the Century Metals acquisition roughly doubled the business, the June 2026 quarter delivered record sales volumes with sales of $240.0M up 78% year on year, net earnings of $12.8M and EBITDA of $19.3M, and the US-Canada trade escalation to 50% steel tariffs hands a domestic processor both higher realised prices and inventory holding gains. On that reading the stock is roughly 6x an annualised run-rate EBITDA, which is not demanding for a company taking share in a protected market.

**What changed.** Q1 fiscal 2027 (2026-08-06, quarter ended 2026-06-30): sales $240.0M up 78%, record quarterly sales volume up 9% sequentially and 28% year on year, net earnings $12.8M, EBITDA $19.3M, operating cash flow only $7.3M. At 2026-06-30 the company had approximately $91.5 MILLION drawn on its asset-based lending facility at 5.3%, plus a $3.5M seller's note from the Century acquisition. On 2026-09-03 it entered a Seventh Amendment increasing aggregate commitments under the JPMorgan A&R Credit Agreement from $140M to $200M, stated as aligning the facility with growth in the underlying borrowing base - i.e. inventory and receivables are absorbing more cash as steel prices rise. Sector context: US-Canada trade war escalation to 50% tariffs.

**Base case.** Friedman's reported free cash flow is not owner earnings, it is a steel-price derivative: the three-year series of -$8.4M, -$0.8M and +$47.4M tracks working capital, which absorbs cash when hot-rolled coil rises and releases it when coil falls, and tells you almost nothing about earning power. I therefore discard the engine's $15.0M three-year mean and use a mid-cycle construction instead: mid-cycle EBITDA of roughly $50M for the combined Friedman-Century business, less maintenance capex near $10M and cash taxes near $12M, gives about $28M of unlevered cash flow. On growth I underwrite +3%, essentially steel-price inflation on a flat volume base. I explicitly do NOT underwrite the +25% naive baseline: that is a clamped +25.6% five-year revenue CAGR which is the Century acquisition plus steel price inflation, not organic volume, and a metals processor does not compound at 25%. Q1 fiscal 2027 is a record quarter on tariff-driven pricing and is a peak, not a base.

**Devil's advocate.**
- Strongest counter: That I am calling a peak far too early on a company that has genuinely changed size. Friedman's record volumes are up 28% year on year - that is TONNAGE, not price - so the Century acquisition and share gains are producing real physical growth independent of the steel cycle. The tariff regime is not a one-quarter event: 50% duties on Canadian steel structurally advantage a Texas processor for as long as they stand, and the company just upsized its credit facility by $60M precisely because it is growing the borrowing base to support that volume. At $294M of market capitalisation against an annualised $77M of EBITDA, the stock is cheap even if I haircut the run rate substantially.
- What would prove it: The September and December 2026 quarters: whether record volumes hold once the initial tariff-driven restocking passes, and whether operating cash flow converts. Q1's $7.3M of operating cash flow against $19.3M of EBITDA is the number to watch - conversion that poor in a record quarter is the tell.
- Already visible today: Yes, and it is the thing that keeps me from calling this cheap despite a 24-point range of outcomes. In the company's own record quarter, EBITDA of $19.3M converted to just $7.3M of operating cash flow, because inventory and receivables absorbed the rest - and the September facility upsize confirms that pattern is continuing rather than reversing. A processor whose best quarter in history produces $7.3M of cash is not compounding owner earnings at anything like the rate the earnings line suggests. The counter's volume point is real and I have credited it in the bull case, but it cannot resolve the valuation because the required growth swings from +20.7% on the engine's base to -3.5% on the current run rate depending on which base I pick, and both are defensible for a business this cyclical. That is not a valuation.
- Left unresolved: Mid-cycle EBITDA for the combined Friedman-Century entity. Century closed in August 2025 so there is no full cycle of combined data, and my $50M mid-cycle figure is an estimate rather than something I could derive from a filing. It is the assumption the whole verdict rests on and I want it flagged as such.

**Key risks.** Earnings are a levered bet on the hot-rolled coil spread, which the company does not control; Tariff-driven pricing is a policy artifact and reverses on exemption, negotiation or litigation; Working capital consumes cash in exactly the up-cycle that produces the earnings - $19.3M EBITDA converted to $7.3M operating cash flow in a record quarter; Century integration is barely a year old with no combined-cycle track record; Market capitalisation of $294M with $3.3M of average daily volume - position-size risk independent of the thesis
**Watch for.** Operating cash flow conversion in the September and December 2026 quarters; Whether record volumes hold after tariff-driven restocking passes; ABL drawn balance against the new $200M commitment - the direct read on working-capital absorption

**Data quality.** CRITICAL - THE RECORDED FAIR VALUE ON THIS NAME IS OVERSTATED AND THE VERDICT, NOT THE NUMBER, IS THE OUTPUT. The flag interest_expense_implies_no_debt_found_on_reported_debt is correct and the engine's total_debt of ZERO is wrong: Note 5 of the 2026-06-30 10-Q states the company had approximately $91.5 million drawn on its ABL Facility at a 5.3% rate, plus a $3.5M Century seller's note - $95.0M in total. This is the ALTG revolver bug in its purest form (an asset-based facility invisible to the LongTermDebt concept family) and on a company this small it is enormous: $95.0M against 7.2M shares is $13.19 PER SHARE of debt the model does not see, against a $40.80 price. True enterprise value is roughly $384M, not the $289M recorded - a 33% understatement. Because the analyst JSON has no field to override debt, record.py will compute equity value per share by subtracting a zero debt balance, so the fair value written to disk is approximately $13 per share too HIGH. Read the verdict, not the gap. Correcting enterprise value alone moves the required growth from +13.4% to +20.7% on the engine's own base, and the +54.2% gap at the 90th percentile of 41 Materials names does not survive it. The other three flags are all real and all point the same way: last_10k_534d_old, negative_fcf_year_in_window and lumpy_fcff_spread_4.4x_of_mean together describe a cash-flow series (-$8.4M, -$0.8M, +$47.4M) that is a working-capital signal rather than an earnings signal, which is why I overrode the base rather than averaging it.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/39092/000143774926026305/frd20260630_10q.htm
- https://www.sec.gov/Archives/edgar/data/39092/000143774926030072/frd20260910_8k.htm
- https://www.sec.gov/Archives/edgar/data/39092/000143774926026319/ex_1000391.htm
- https://www.sec.gov/Archives/edgar/data/39092/000143774926020323/frd20260331_10k.htm
