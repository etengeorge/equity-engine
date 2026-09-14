# CNX — CNX RESOURCES
*Energy · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $35.91 · fair value $53.11 · gap +47.9%
- **Growth:** market implies -4.3%, analyst says +2.0% (delta +6.3%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 4.3% | 5.3% | 6.3% | 7.3% | 8.3% |
|---|---|---|---|---|---|---|
| bear | -8.0% | $63.37 | $40.01 | $27.57 | $19.83 | $14.55 |
| base | +2.0% | $112.96 | $73.90 | $53.11 | $40.20 | $31.41 |
| bull | +10.0% | $168.95 | $112.03 | $81.75 | $62.97 | $50.19 |

At the point WACC of 6.3%: bear -23.2%, base +47.9%, bull +127.7%
Across the whole grid the gap ranges -59.5% to +370.5% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $35.91 the market is paying ~$7.5B EV for a low-cost Appalachian gas producer with a long reserve life, a large hedge book, a genuine environmental-attributes business and the balance sheet to keep buying back stock. Gas demand is being repriced upward by data-centre load growth and LNG export capacity, and CNX sits on cheap Marcellus and Utica acreage close to that demand. The stock is +22.6% over twelve months. Paying roughly 14x a ~$520M free cash flow run rate for that optionality is not obviously wrong.

**What changed.** Q2 2026 (2026-07-30): quarterly operating cash flow of $279.5M against $277.5M, $297.0M, $233.8M and $282.5M in the four prior quarters — remarkably stable. Full-year capital expenditure guidance of $540-570M base, $556-586M total. No transaction, no guidance change, no financing event found in the filing list beyond ordinary course. Nothing material found that alters the business.

**Base case.** CNX's free cash flow run rate is ~$1,090M of operating cash flow less ~$570M of guided capex, i.e. roughly $520M — close to the newest year in the series ($534M) and well above the three-year mean of $422.3M the engine uses, because the two older years sit in the 2023-24 gas price trough. So the `possible_peak_cycle_base` flag is pointing at a recovery, not a peak. For a mature Appalachian producer with flat production and no growth capital programme, the defensible long-run FCFF growth is inflation-like: +2%. Gas price is the entire swing factor and I will not forecast it.

**Devil's advocate.**
- Strongest counter: That I am dismissing a genuine +154% gap by blaming the beta. If CNX really does generate $520M of free cash flow against a $5.3B market cap — a 9.8% free cash flow yield — with flat capex and a shareholder-return programme, then the name IS cheap and the discount rate argument is me talking myself out of it.
- What would prove it: Whether a 6.3% WACC is defensible for this company. That is an input question, not a market question, and it is answerable: the cost of equity comes from a beta of 0.34 with an R-squared of 0.041 — the regression explains 4% of the variance and sits barely above the engine's own 0.04 gate.
- Already visible today: Yes, and it settles it. At the engine's 6.3% WACC the market implies -4.3% growth (hence the +154% gap). At a defensible 10% WACC for a levered gas producer with $2.2B of debt, the same price and the same cash flows imply +10.0% growth — the name goes from very cheap to expensive on the discount rate alone. On the current run-rate base of $520M at 10% it implies +4.9%. The gap is not a business fact; it is the failed-beta bias LESSONS.md measures across the whole screen, and Energy is the sector where it concentrates.
- Left unresolved: I cannot correct it in the record: the analyst schema has no field to override the cost of equity, so the fair value this verdict produces will still be computed at a 6.3% WACC and should be disregarded. The verdict is the output; the fair value is not.

**Key risks.** Henry Hub and Appalachian basis are the entire thesis and I have no edge on either; $2.2B of debt against a beta the regression cannot measure; Revenue series is unusable for trend: [$2,239M, $1,267M, $3,435M, $1,261M, $757M, $1,258M] is dominated by unrealised commodity derivative marks, not sales
**Watch for.** 2027 capital and production guidance against the $540-570M base capex run rate; Hedge book roll-off schedule and realised versus NYMEX netback; Any data-centre or behind-the-meter power agreement

**Data quality.** `possible_peak_cycle_base_newest_fcf_3.9x_oldest` — checked and it points the WRONG way, the AMR/LPG lesson again: the newest year ($534M) matches the current quarterly run rate, and it is the two OLDER years ($275M, $135M) that are the anomaly, being the 2023-24 gas trough. The base is if anything conservative. `ebit_derived_from_pretax_plus_interest` — immaterial here. The defect that decides the name is NOT flagged: beta 0.34 at R-squared 0.041, giving a 6.3% WACC for a levered E&P. The naive +12.2% revenue CAGR baseline that generates the +154% gap is also meaningless, because CNX's 'revenue' line includes unrealised derivative gains and losses and swings between $757M and $3,435M year to year.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1070412/000107041226000058/cnx-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1070412/000107041226000056/cnx-20260730.htm
