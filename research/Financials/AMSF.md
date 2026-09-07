# AMSF — AMERISAFE INC
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-07 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $25.99 · fair value $27.31 · gap +5.1%
- **Sustainable ROTCE:** screen said +24.2%, analyst says +12.0%
- **P/TBV:** justified 2.01 vs actual 1.91 on tangible book of $13.57/share

**The case for the price.** The market pays 1.9x tangible book — a premium, not a discount — for a specialist workers' compensation underwriter of hazardous-industry risk that has out-earned its cost of capital for two decades and returns essentially all of its capital. The bear side of the same price, and the reason the shares are down 41% over twelve months, is that the underwriting cycle has turned. Q2 2026 net combined ratio was 95.4% against 91.7% a year earlier and 94.3% year-to-date against 90.5%; the net loss ratio rose to 62.6% from 58.6%; EPS of $1.12 missed by 17% and fell 16% year over year; book value per share of $13.49 is DOWN 3.4% from $13.96 a year ago. Management's own language is that workers' comp remains profitable but is showing gradual softening — rate reductions, rising medical costs, moderating reserve redundancies and heightened competition. Nine consecutive quarters of premium growth into a softening market is volume bought at a worse price. The market is pricing the end of the redundancy cycle, and it is right to.

**What changed.** Q2 2026 (2026-07-21) was the break. Net premiums earned rose 11.4% but the combined ratio deteriorated 370bp to 95.4%. Critically, the current accident year loss ratio is 72.0% and the prior accident year loss ratio contributed -9.4 points, i.e. $7.3M of favourable development on accident years 2023 and prior. Strip the development out and the accident-year combined ratio is roughly 104.8% — an underwriting LOSS on business written today. Favourable development also shrank year over year, from $8.6M in Q2 2025 to $7.3M. Claim frequency was up from the prior accident year at six months, returning toward 2023 levels, with severity down.

**Base case.** For a financial the number that matters is the sustainable return, not a growth rate. See rotce_override.

**Devil's advocate.**
- Strongest counter: The best case that 12% is too low: releasing reserves is not an accident at AMERISAFE, it is the business model. The company has deliberately set conservative initial loss picks on hazardous-industry workers' comp for twenty years and has harvested favourable development in almost every one of them. Calling that unsustainable is calling the franchise unsustainable, and there is no evidence of that — the redundancies are still coming, just smaller. Add that AMERISAFE pays out essentially everything it earns through regular and extraordinary dividends, which structurally holds equity down and lifts ROE, so a mid-to-high-teens reported return is a repeatable feature of the capital policy rather than an artefact. On that reading the engine's 24.2% is too high but 15-16% is defensible, which would put justified P/TBV near 2.7 against an actual 1.91 and make the shares genuinely cheap after a 41% decline.
- What would prove it: The size and direction of prior-year development over the next three to four quarters, and whether the current accident year loss ratio pick comes down below 72%. A single quarter of adverse development would settle it against the bulls; two more years of $7M-plus releases would settle it for them.
- Already visible today: The evidence is mixed and slightly against the bulls. Development is still favourable but shrinking ($7.3M from $8.6M), the current-year pick has risen, frequency is deteriorating back toward 2023 levels, and book value per share fell 3.4% year over year — a company that is out-earning its payout does not shrink its book. Against that, the accident-year loss ratio of 72% is a management estimate set conservatively by design, and history says it comes down.
- Left unresolved: Whether the deterioration is cyclical (soft market, price it through) or structural (medical severity inflation permanently raising the loss cost of hazardous-industry comp). I cannot separate those from two quarters of data, and it is the whole question.

**Key risks.** Ex-development accident-year combined ratio of roughly 104.8% — the current book is written at an underwriting loss; Softening workers' comp pricing with rate reductions into rising medical severity; Nine consecutive quarters of premium growth in a softening market is a warning, not a strength; Small, single-line, concentrated in hazardous industries; no diversification to absorb a bad accident year
**Watch for.** Prior accident year development turning below ~$5M a quarter, or turning adverse; The current accident year loss ratio pick in Q3/Q4 2026; Any move to a special dividend below the recent run rate — that would say management sees the redundancy running out

**Data quality.** The brief raised no flags and one of its two inputs is fine while the other is not. Tangible book per share of $13.57 is essentially current — the company reports $13.49 at 2026-06-30 — so this name does NOT have the stale-book problem that voided BUR and AII. The sustainable ROTCE of 24.2% is the problem: it is a GAAP return that depends on 9.4 points of favourable prior-year reserve development, on accident years 2023 and prior, in a market the company itself describes as having moderating redundancies. Ex-development the accident-year combined ratio is ~104.8%, so the underwriting contribution to the return is currently negative and the rest is the after-tax yield on the float. I have overridden to 12%, which allows for AMERISAFE's genuine long-run record of conservative initial picks without underwriting the 24% that only the release cycle produces. Second, the cost of equity of 7.0% rests on a beta of 0.40 with an R-squared of 0.094, which is the BETA_MIN_R2 defect recorded on 2026-09-03 — a failed regression attenuates the slope toward zero, lowers the discount rate and manufactures a positive gap. There is no field in this schema to override cost of equity, so the recorded fair value is still built on a 7.0% discount rate that is probably 100-200bp too low; at a defensible 8.5-9% the justified multiple falls below the actual and the name reads slightly expensive rather than slightly cheap. That two-sided uncertainty on a gap of a few points is why this is no_edge rather than a call in either direction. The +133.7% gap and 98th-percentile cohort rank are artefacts of the two bad inputs and should be disregarded entirely.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1018979/000119312526314074/amsf-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1018979/000119312526310328/d122285dex991.htm
- https://www.theinsurer.com/ti/news/amerisafe-combined-ratio-worsens-to-954-in-q2-earnings-miss-2026-07-22/
- https://www.insurancebusinessmag.com/us/news/workers-comp/amerisafe-net-premiums-rise-11-as-underwriting-profit-falls-in-q2-583276.aspx

**Ingestion notes.** no usable final_growth
