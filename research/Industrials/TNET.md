# TNET — TRINET GROUPINARY
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $69.21 · fair value $80.12 · gap +15.8%
- **Growth:** market implies -4.3%, analyst says +2.0% (delta +6.3%)
- **FCFF base overridden** by the analyst to $266.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 6.4% | 7.4% | 8.4% | 9.4% | 10.4% |
|---|---|---|---|---|---|---|
| bear | -5.0% | $84.63 | $67.40 | $55.51 | $46.80 | $40.15 |
| base | +2.0% | $121.53 | $97.01 | $80.12 | $67.77 | $58.34 |
| bull | +7.0% | $154.53 | $123.45 | $102.04 | $86.40 | $74.48 |

At the point WACC of 8.4%: bear -19.8%, base +15.8%, bull +47.4%
Across the whole grid the gap ranges -42.0% to +123.3% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** TriNet is a margin-recovery story the market has already partly re-rated. After the 2024-25 insurance cost blowout the company repriced its book, and it is working: Q2 2026 adjusted EBITDA of $128M on a 10.9% margin against $105M and 8.5% a year earlier, net income $53M against $37M, attrition improved 36%, and full-year earnings guidance RAISED — all while total revenues fell 5%. The market is paying for stabilised insurance margins on a shrinking revenue base, which is why it implies roughly zero FCFF growth rather than a decline.

**What changed.** Q2 2026 (filed 2026-07-30) raised FY26 guidance: total revenues $4,750-4,900M, professional service revenues $647-663M, adjusted EBITDA margin 8.5-9.0% — i.e. roughly $404-441M of adjusted EBITDA. A quarterly dividend of $0.29 was declared 2026-09-11. Nothing structural: no acquisition, no financing, no management change.

**Base case.** The +134% gap is manufactured by a corrupted revenue series and should be discarded before any thesis is formed. revenue_series reads [$5,010M, $5,053M, $917M, $3,275M, $3,060M, $2,659M] — a company whose revenue does not fall to $917M and then return to $5,053M. That is a concept switch between TriNet's 'Total revenues' (gross, including insurance costs) and a net-service-revenue presentation, the same shape as the HRI predecessor artifact but arising from tagging rather than a spin-off. The '+13.5% five-year revenue CAGR' baseline is computed off that series and means nothing, and the entire +134% gap and 92.7th-percentile rank follow from it. Working the actual economics instead: the FCFF base of $310.7M rests on cfo_series [$303M, $279M, $545M] where the $545M year is a working-capital swing in client payroll and insurance accruals, and interest_expense is recorded as $12M against an actual $27M for six months (~$55M a year) — an implied rate of 1.34%, below the PATK alarm threshold, which understates the add-back. Building the base from the company's own guidance instead — adjusted EBITDA ~$420M less ~$75M capex less ~$46M D&A, taxed, plus D&A back — gives roughly $266M, at which the market implies -0.9%; across every base I can defend the answer runs -6.6% to +5.1%. I take +2%: insurance margin recovery is real but finite, and professional service revenue is still falling 8%.

**Devil's advocate.**
- Strongest counter: That I am treating a 21%-of-FCFF stock compensation charge as free. Expensing it takes the base from ~$266M to ~$205M, at which the market requires +5.1% rather than -0.9% — and TriNet's revenue is shrinking, so a 5% compounding requirement on a declining business is a genuine short case rather than a fair one.
- What would prove it: The net weighted-average share count trend, per the BOX rule — whether buybacks are actually paying for the compensation.
- Already visible today: Partly: TriNet has been reducing its share count and the engine's 45.9M shares are well below the ~50M of prior years, which suggests the compensation is being absorbed. I did not pull the year-over-year weighted-average figures from this quarter's filing, so I cannot state the net rate, and that is why the stock-comp flag stays open rather than resolved.
- Left unresolved: The stock-comp treatment, which is worth six points of required growth and is the difference between 'fair' and 'modestly rich'. The answer was one grep further into the 10-Q than I went.

**Key risks.** total revenues -5% and professional service revenues -8%; the recovery is in margin, not volume; health insurance cost trend is the single swing factor and it broke the model once already in 2024-25; stock compensation is 21% of the reported cash-flow base; cfo swings violently with the timing of client payroll and insurance accruals, so any single-year base is unreliable
**Watch for.** worksite employee volumes turning positive — the bull case is volume, not margin; the FY2027 insurance cost trend assumption at the Q4 print

**Data quality.** RESOLVED: possible_trough_cycle_base is real but the flag's advice is backwards per the AMR rule — the $545M year is the OLDEST and is a working-capital swing, so the three-year mean is inflated rather than depressed. NEW AND UNFLAGGED: (1) revenue_series carries a concept-switch artifact (a $917M year between $3,275M and $5,053M) which makes the +13.5% baseline and therefore the entire +134% gap meaningless; (2) interest_expense of $12M against total_debt of $896M is an implied 1.34%, versus $27,058k reported for six months in the 10-Q — the PATK understated-add-back defect. OPEN: the stock_comp_is_21% flag is NOT resolved — I did not obtain the year-over-year weighted-average share count, and it is worth six points of required growth.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/937098/000093709826000048/tnet-063026xexhibit991.htm (Q2 2026 EX-99.1: total revenues, adjusted EBITDA, FY26 guidance table)
- https://www.sec.gov/Archives/edgar/data/937098/000093709826000050/tnet-20260630.htm (10-Q, 2026-06-30: interest expense, bank fees and other)
- https://www.sec.gov/Archives/edgar/data/937098/000093709826000056/exhibit991q32026dividend.htm (dividend declared 2026-09-11)
