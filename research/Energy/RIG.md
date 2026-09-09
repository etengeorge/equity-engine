# RIG — TRANSOCEAN
*Energy · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $5.76
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Transocean is a levered option on ultra-deepwater dayrates, and the market prices it as one. Total contract backlog was $6,732M at 2026-06-30, down from $7,128M six months earlier, against total debt of $5,107M and a market capitalisation of $6.4B - so the enterprise is worth roughly $11B and the entire equity stub sits behind that debt. The company is still selling rigs (Deepwater Champion and Discoverer India went for $27M of net proceeds in the first half). At $5.76 the stock is up 87.6% over twelve months on the offshore recovery, but backlog is shrinking rather than growing, and the equity's value depends almost entirely on whether dayrates on the high-specification floater fleet stay high enough for long enough to service and then de-lever that balance sheet. That is an option, and options are priced on volatility, not on discounted cash flow.

**What changed.** Only two filings in the window the brief covers: the 2026-08-07 10-Q and an 8-K on 2026-08-20 (items 7.01, 9.01). Contract backlog declined to $6,732M from $7,128M. Rig disposals of Deepwater Champion and Discoverer India completed in the first half for $27M net. No company-specific news in the store for the last 90 days, which is a fact about coverage rather than about the company - I lower my confidence in 'nothing happened' accordingly, and I could not find a Q2 earnings press release among the 8-K exhibits.

**Base case.** There is no base to grow. The engine reports a normalized FCFF base of n/a computed over ZERO years of usable data, an enterprise value of n/a, and no implied growth at any of the three WACC points. There is nothing here to form a base case against, and I will not invent one.

**Devil's advocate.**
- Strongest counter: That the multiples table is not nothing and I am discarding usable information. It gives a blended midpoint of $8.16 against a $5.76 price - a +41.7% gap - and the price-to-tangible-book row in particular is coherent: Transocean trades at 0.8x tangible book against a cohort at 1.2x/1.7x/2.9x, which on an asset-heavy driller with real, marketable rigs is the most defensible of the three multiples and implies $8.62 to $20.54.
- What would prove it: A cohort of genuinely comparable offshore drillers - Valaris, Noble, Seadrill, Diamond - priced on the same three multiples, rather than a 99-name Energy bucket containing E&Ps, midstream and services companies whose capital intensity and revenue quality have nothing in common with a floater fleet.
- Already visible today: Yes, and it defeats the counter. The brief states the cohort is 'not ranked - too few comparable Energy names to define a distribution honestly'. The three rows straddle the price in opposite directions - ev_sales puts it at $0.57 at p25 (below the price) while p_tbv puts it at $8.62 at p25 (above it) - and the ev_sales p25 of $0.57 against a $5.76 price is a tenfold disagreement with the p_tbv row on the same page. Under the standing rule established on RIOT and EPRT, rows that straddle the price in opposite directions on an unranked cohort mean the blend is noise with a decimal point. The devil's advocate loses on its own evidence.
- Left unresolved: I did not build an independent dayrate-and-backlog model of the fleet, which is the only honest way to value this equity. That is a substantial piece of work and it is not what a rotation slot buys.

**Key risks.** $5.1B of debt against a shrinking $6.7B backlog - the equity is the residual; Backlog fell 5.6% in six months; contract awards are lumpy and cancellable; 44% debt weight with a cost of debt the engine itself flags as speculative
**Watch for.** Quarterly backlog additions against roll-off - the single number that decides this equity; Ultra-deepwater dayrate prints on new fixtures; Any refinancing or exchange of the 2027-2030 maturities

**Data quality.** This name is unmodellable and both flags say so honestly. `negative_ebitda_valued_on_revenue_or_gross_profit_only` and `speculative_cost_of_debt_at_44%_debt_weight_wacc_unreliable` are both correct, and the DCF returned no base at all - 'mean of CFO-capex over 0y'. I checked the SND precedent (a D&A concept understated by an order of magnitude manufacturing a false negative EBITDA) and it does not obviously apply here: Transocean genuinely runs near or below breakeven at the EBIT line on a $20B+ rig fleet with enormous depreciation, and the 10-Q confirms continued rig disposals rather than a company being mis-extracted into looking unprofitable. The multiples fallback must be DISREGARDED rather than averaged, on all three of the tests in LESSONS.md at once: the cohort is explicitly not ranked, the rows straddle the price in opposite directions ($0.57 at ev_sales p25 versus $8.62 at p_tbv p25), and the 99-name Energy bucket is not a comparable set for an offshore driller. The blended +41.7% is therefore not evidence of anything and should not be read as a gap. No fair value recorded.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1451505/000145150526000061/rig-20260630x10q.htm
- https://www.sec.gov/Archives/edgar/data/1451505/000145150526000064/rig-20260820x8k.htm

**Ingestion notes.** no usable final_growth
