# ABCB — AMERIS BANCORP
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $84.99 · fair value $63.06 · gap -25.8%
- **Sustainable ROTCE:** screen said +12.9%, analyst says +14.1%
- **P/TBV:** justified 1.41 vs actual 1.90 on tangible book of $44.79/share

**The case for the price.** Ameris is a high-performing Southeast franchise and is priced as one. Q2 2026 adjusted net income was $107.3M ($1.60 per diluted share, flat on a strong year-ago quarter), adjusted ROTCE 14.08%, return on assets 1.53% adjusted, net interest margin stable at 3.88%, earning assets growing 8.5% annualised, tangible common equity above 11% of tangible assets and 30% of deposits non-interest-bearing. Tangible book value per share rose to $45.10. At $84.99 that is 1.88x tangible book and about 13x annualised adjusted earnings, with the company expanding into Nashville. For a bank earning 14% on tangible equity with a fortress funding mix, 1.9x book is the market's ordinary price, not an aggressive one - the cohort agrees, placing this at the 52nd percentile of 339 Financials, which is the median.

**What changed.** Q2 2026 (2026-07-23): GAAP net income $51.4M ($0.77) depressed by a litigation accrual, against adjusted net income of $107.3M ($1.60). GAAP ROTCE 6.75% versus adjusted ROTCE 14.08%. Tangible book value per share up $0.92 in the first half to $45.10, held back by a $24.8M decline in AOCI. 226,600 shares repurchased in the quarter. Announced expansion into the Nashville market. 8-K of 2026-06-18 (items 5.03) and 2026-02-24 (item 5.02, officer change). No acquisition, financing or equity issuance in the last two quarters.

**Base case.** See rotce_override. I use 14.1%, the company's own adjusted ROTCE for Q2 2026, which also reconciles independently: adjusted net income of $107.3M annualised is $429M against tangible common equity of roughly $3.02B ($45.10 x ~67.1M shares), or 14.2%. The engine's 12.9% is a three-year GAAP average and understates the current franchise for the same structural reason recorded on VLY and AUB - a GAAP average absorbs one-off charges (here a litigation accrual worth 7.3 points of ROTCE in a single quarter) and describes a company that is not the one being priced today.

**Devil's advocate.**
- Strongest counter: That 1.88x tangible book is genuinely too much, and correcting the ROTCE upward does not rescue it. Even at the company's own 14.08%, the justified multiple is 1.41 against an actual 1.88 - a 25% overvaluation - and the engine's cost of equity of 10.6% rests on a beta of 1.05 with an R-squared of 0.608, which is the best-fitted regression in today's ten. So unlike most large gaps in this engine, this one is NOT a measurement artifact: the discount rate is well measured and the answer still says rich.
- What would prove it: Sustained adjusted ROTCE materially above 14%, or tangible book compounding fast enough that the multiple compresses without the price falling.
- Already visible today: Tangible book grew only 4.2% annualised in the first half - well below the 8.5% earning-asset growth - because AOCI took $24.8M out of equity. A bank cannot sustain a 1.9x multiple on 4% book compounding unless the AOCI drag reverses. That is a real point against the name and I could not dismiss it.
- Left unresolved: The terminal growth constant. The Gordon justified-P/TBV model uses 2.0% forever, and Ameris is growing earning assets at 8.5%. At a 4% terminal growth the justified multiple rises to 1.53 and the gap narrows from -25% to -19%; the sign never changes, but the magnitude is governed by a constant that is a choice rather than a fact. That is exactly why I am not calling this rich.

**Key risks.** Southeast commercial real estate concentration at a benign point in the credit cycle; AOCI drag on tangible book if long rates rise; The Q2 litigation accrual - I could not determine what it relates to or whether it recurs
**Watch for.** Whether adjusted ROTCE holds at or above 14% for two more quarters; Tangible book per share growth once the AOCI drag abates; Any disclosure on the nature of the litigation accrual

**Data quality.** The single flag, `goodwill_and_intangibles_26%_of_book`, is real but not disqualifying: the company reports book value per share of $60.96 against tangible book of $45.10, and the model correctly prices the tangible figure. I ran the AII/BUR stale-tangible-book cross-check and the engine PASSES here - it uses $44.79 against the company's reported $45.10 at 2026-06-30, a 0.7% difference consistent with share-count timing rather than a period lag, and equity is the current figure ($4.09B at 2026-06-30). The defect I did find is in the numerator: the 'sustainable' ROTCE of 12.9% is a three-year GAAP average, and Q2 2026 GAAP ROTCE was 6.75% against an adjusted 14.08% because of a litigation accrual. Correcting to 14.1% moves the justified P/TBV from 1.27 to 1.41 and the gap from -33.0% to about -25%. The verdict does not change sign, which is why this is no_edge rather than a correction that matters: at the 52nd cohort percentile this name is the definition of the median, and a -25% gap on a model whose terminal growth constant alone is worth six points of that gap is not a thesis. Beta 1.05 with R-squared 0.608 is the soundest cost of capital in today's ten, so none of the failed-beta bias applies here.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/351569/000035156926000139/exhibit991pressreleasedate.htm
- https://www.sec.gov/Archives/edgar/data/351569/000035156926000143/abcb-20260630.htm
- https://www.sec.gov/Archives/edgar/data/351569/000035156926000139/a2q26earningspresentatio.htm

**Ingestion notes.** no usable final_growth
