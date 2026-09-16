# PRM — PERIMETER SOLUTIONS
*Materials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-16 — RICH (conviction: medium)

- **Verdict:** rich · price $31.56 · fair value $11.26 · gap -64.3%
- **Growth:** market implies +40.1%, analyst says +10.0% (delta -30.1%)
- **FCFF base overridden** by the analyst to $220.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 10.1% | 11.1% | 12.1% | 13.1% | 14.1% |
|---|---|---|---|---|---|---|
| bear | +0.0% | $8.10 | $6.40 | $5.04 | $3.92 | $2.99 |
| base | +10.0% | $16.14 | $13.43 | $11.26 | $9.48 | $8.01 |
| bull | +18.0% | $24.87 | $21.04 | $17.98 | $15.48 | $13.40 |

At the point WACC of 12.1%: bear -84.0%, base -64.3%, bull -43.0%
Across the whole grid the gap ranges -90.5% to -21.2% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $31.56 the market is capitalising a genuine escalation in wildfire severity. Perimeter's Phos-Chek retardant is the incumbent product with USFS and CAL FIRE qualification, a near-monopoly position and extreme operating leverage - the cost base is largely fixed, so an above-average fire season drops almost entirely through to EBITDA. Q2 2026 Management's Segment Adjusted EBITDA was $105.6M and Specialty Products grew sales 31%, so the buyer is underwriting two engines rather than one: structurally worsening fire seasons in Fire Safety, plus a phosphorus-chemicals business compounding independently of weather. On that view the -$9.2M free-cash-flow year of 2023 was a once-in-a-decade quiet season and the right base is the two good years, not the three-year mean.

**What changed.** Q2 2026 (2026-07-31): net loss of $181.6M against $32.2M a year earlier, driven almost entirely by a $266.3M founders advisory fee charge ($189.9M year to date) reflecting the mark-to-market of liability-classified advisory amounts tied to the share price. Segment Adjusted EBITDA $105.6M. Specialty Products net sales +31%. Purchases of property and equipment $12.7M in the quarter. The balance sheet at 2026-06-30 carries founders advisory fees payable of $177.957M current and $452.617M non-current, and 13,387,003 shares have already been ISSUED to settle founders advisory fees in a prior period.

**Base case.** I use $220M rather than the engine's $155.1M, because the three-year mean averages in 2023's -$9.2M, which was a genuinely light US fire season rather than an impairment of the franchise; the mean of the two normal years ($208.6M and $172.9M) plus after-tax interest of roughly $31M gives about $220M. On growth, Fire Safety volume tracks acres burned, which is trending up but is violently non-linear year to year and is ultimately bounded by federal and state suppression budgets rather than by demand; Specialty Products is genuinely compounding at high-twenties rates off a small base. Blending a mid-single-digit Fire Safety trend with high-teens Specialty growth, +10% is a defensible five-year FCFF CAGR and is, if anything, generous - it assumes no reversion in fire seasons at all. The naive baseline of +25% is a clamped artifact of a +136% four-year revenue CAGR measured from a 2021 SPAC stub period and carries no information.

**Devil's advocate.**
- Strongest counter: That I am underwriting the wrong variable. Perimeter's value is not a discounted cash flow at all - it is an option on climate, and options on convex, worsening tail risk are systematically underpriced by a five-year CAGR framework. Acres burned has no ceiling, the retardant is consumable and re-ordered every season, and Perimeter has pricing power because there is no qualified substitute. A +40% required growth rate looks absurd against history and entirely reasonable against a decade in which the western US fire season lengthens by a month. Moreover the founders advisory fee, which I have added to enterprise value, is settled in SHARES and is itself a function of the share price appreciating - so it only becomes large in exactly the states of the world where the equity has already worked. Charging it as a fixed claim double-counts.
- What would prove it: Two things: the fiscal 2026 full-year free cash flow against the $208.6M of 2025 (does a severe season actually convert to cash at the rate the operating leverage implies), and the settlement mechanics and share count effect of the $630.6M founders advisory fee liability over the next twelve months.
- Already visible today: The founders-fee objection is partly right and I have weighed it - the liability IS share-price-linked, and 13.4M shares were already issued to settle an earlier tranche. But it does not rescue the valuation, for two reasons. First, whether settled in cash or shares it is a claim of $630.6M ahead of or alongside common on a $5.17B market capitalisation - roughly 12% - and the 10-Q classifies it as a LIABILITY, not equity, so treating it as a claim on enterprise value is the company's own accounting, not my adjustment. Second, the arithmetic does not turn on it: WITHOUT the founders fee the market already requires +40.1%, and my generous $220M base still leaves +33%. On the strongest bull base I can construct - $250M, treating 2026 as the new normal - the requirement is still +28.9%. Every defensible input leaves a requirement far above any growth rate I can defend from the business, which is why the devil's advocate loses here despite being a real argument.
- Left unresolved: The settlement path of the founders advisory fee liability - whether it converts to shares over the next twelve months, at what reference price, and how much dilution results. The Q2 10-Q classifies $178.0M as current, so a substantial tranche settles within a year, but I could not determine the share count effect and have therefore not modelled the dilution at all. My verdict is rich WITHOUT that dilution; including it would make it more so.

**Key risks.** Earnings are a weather derivative: 2023 produced NEGATIVE free cash flow on the same asset base; $630.6M founders advisory fee liability settling partly within twelve months, with 13.4M shares already issued against an earlier tranche; Fire Safety demand is ultimately capped by federal and state suppression appropriations, not by acres burned; Retardant qualification is a regulatory privilege: loss or sharing of USFS qualification would be structural; Enterprise value of $6.4-7.0B against roughly $200M of normalized unlevered cash flow leaves no margin for a mild season
**Watch for.** Fiscal 2026 full-year free cash flow - does a severe season convert at the rate the operating leverage implies; Settlement of the current $178.0M founders advisory fee tranche and the resulting share count; Specialty Products reaching a scale that sets an earnings floor independent of fire season

**Data quality.** NEW DEFECT CATEGORY, and it is invisible to every existing detector. Perimeter's balance sheet at 2026-06-30 carries 'Founders advisory fees payable - related party' of $177,957 thousand CURRENT and $452,617 thousand NON-CURRENT - $630.6M in total, roughly 12% of market capitalisation - and NONE of it reaches enterprise value. It is not debt, so the total_debt extractor and the ALTG interest-coverage detector never see it (implied rate here is 41.4/1210.2 = 3.4%, unremarkable). It is not in the share count, because the shares have not been issued yet - though 13,387,003 already were for an earlier tranche, so the dilution is demonstrated, not hypothetical. It is a liability-classified, share-settleable contingent claim, which falls between every category the engine models. Adding it moves enterprise value from $6.39B to $7.02B and the required growth from +40.1% to +43.0%. Unlike the convertible, ABL, rental-capex and stale-share-count bugs, which all manufacture false BUYS, this one understates enterprise value on a name the screen already reads as expensive, so it hides richness rather than manufacturing cheapness - the same reason the PIPR and ENVA biases went unnoticed. The cheap detector is a balance-sheet line containing 'payable - related party' that is material relative to market capitalisation, on any company with a sponsor or founder economic-interest structure. Note the engine DID capture preferred stock at $100M against an actual $119.0M, which is close enough not to matter. Flags cleared: negative_fcf_year_in_window and lumpy_fcff_spread are both real and both describe the 2023 fire season, which I have handled by overriding the base upward rather than downward.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1880319/000188031926000048/prm-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1880319/000188031926000044/prmearningspressreleaseq22.htm
- https://ir.perimeter-solutions.com/news-events/press-releases/detail/88/perimeter-solutions-reports-second-quarter-2026-financial-results
- https://www.fool.com/earnings/call-transcripts/2026/08/07/perimeter-solutions-prm-q2-2026-earnings-call-transcript/
