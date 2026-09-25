# OPCH — OPTION CARE HEALTH INC
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-25 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $22.94 · fair value $33.20 · gap +44.7%
- **Growth:** market implies -3.7%, analyst says +3.0% (delta +6.7%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 5.4% | 6.4% | 7.4% | 8.4% | 9.4% |
|---|---|---|---|---|---|---|
| bear | -3.0% | $40.95 | $30.50 | $23.88 | $19.31 | $15.96 |
| base | +3.0% | $56.21 | $42.12 | $33.20 | $27.06 | $22.56 |
| bull | +7.0% | $68.48 | $51.45 | $40.68 | $33.26 | $27.83 |

At the point WACC of 7.4%: bear +4.1%, base +44.7%, bull +77.3%
Across the whole grid the gap ranges -30.4% to +198.5% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $22.94 the market is paying about 9.5x guided 2026 adjusted EBITDA and roughly a 6% free-cash-flow yield on enterprise value for a business whose revenue growth has just collapsed from a 13.3% five-year compound rate to 0.5-2.2% guided for 2026, and whose H1 adjusted EBITDA FELL year over year ($222.3M against $225.8M). That is the case: Option Care is the largest independent home-infusion provider with a real site-of-care tailwind, but it is a low-margin distributor of other people's drugs (8.5% adjusted EBITDA margin), its therapy mix is exposed to biosimilar substitution economics it does not control, and a business that grows revenue 2% while EBITDA declines is not a compounder. The stock is down 20% over twelve months for that reason.

**What changed.** Q2 2026 (2026-07-29): revenue $1,442M, +1.9%; GAAP net income $53.9M, +6.7%; adjusted EBITDA $117.5M, +3.0%; adjusted diluted EPS $0.45, +9.8%; Q2 operating cash flow $184M; $150M of stock repurchased in the quarter. Full-year 2026 guidance: revenue $5.675-5.775B, adjusted EBITDA $480-495M, adjusted diluted EPS $1.85-1.92, and cash provided by operating activities of AT LEAST $320M. Q3 guided to low-to-mid single digit sequential revenue growth and mid single digit sequential adjusted EBITDA growth. The guided revenue range against FY2025 revenue of $5,649.5M is +0.5% to +2.2% growth - the single most important number for this name, because it replaces the +13.3% baseline the screen used to generate a +138% gap. Note there was NO company-specific news in the store for the trailing 90 days, so this is the filings alone.

**Base case.** Guided 2026 operating cash flow of at least $320M against capex that has run $36-42M implies free cash flow near $280M, which plus after-tax interest lands almost exactly on the engine's $316.6M base - so the base is sound and I am not overriding it. Forward, I underwrite +3% FCFF growth: low-single-digit revenue growth (management's own 2026 guide is +0.5-2.2%, and the secular shift of infusion from hospital to home supports mid-single-digit volume over a decade) with roughly stable margins. I differ from the naive +13.3% baseline by ten points, because that number is the historical revenue CAGR of a period that included both acquisition and a therapy-mix surge, and the company has just guided to a sixth of it. I also do not underwrite margin expansion: H1 adjusted EBITDA was down year over year, which is the opposite of leverage.

**Devil's advocate.**
- Strongest counter: The recorded fair value is a discount-rate artifact and the name is fair, not cheap. The 7.45% WACC rests on a beta of 0.56 whose R-squared is 0.07 - the regression explains 7% of the variance, and the standing measurement is that betas below an R-squared of ~0.15 are attenuated toward zero, which lowers the cost of equity, lowers the WACC and manufactures exactly this kind of positive gap. Put a defensible healthcare-distribution beta of 1.0 on it and the WACC is ~9.45%, at which the market requires +2.8% growth against my +3.0% - the gap vanishes entirely. The second leg of the counter is independent of the discount rate: a company guiding +0.5-2.2% revenue with H1 EBITDA DOWN year over year does not obviously grow free cash flow at 3% for five years.
- What would prove it: For the beta: an R-squared above ~0.2 on a longer regression, or Yahoo's SPX-based beta rescaled to the IWM convention, neither of which this runtime can reach. For the business: 2027 guidance. Revenue growth reaccelerating above 4% with adjusted EBITDA growing FASTER than revenue would settle it in the bull's favour; another year of 2% revenue and flat EBITDA settles it the other way.
- Already visible today: Yes, and it is what makes me withhold a 'cheap'. H1 2026 adjusted EBITDA of $222.3M against $225.8M is already a year-over-year DECLINE, on revenue up 1.9%. The guided full-year adjusted EBITDA of $480-495M against H1's $222.3M does imply a materially stronger H2, but that is guidance, not a result. On the beta side nothing is visible - I could not test it from this runtime and am recording that.
- Left unresolved: I could not establish the therapy-level gross profit mix, so I cannot say how much of the H1 EBITDA decline is biosimilar economics versus the cost of the 2026 initiatives - the press release attributes the quarter's strength to those initiatives without quantifying either. And I could not resolve the beta, which is the input that decides the verdict. Absent that, the disciplined answer is no_edge rather than cheap.

**Key risks.** H1 2026 adjusted EBITDA declined year over year on higher revenue - margin compression is already in the numbers, not a forecast; Revenue growth has fallen from a 13.3% five-year CAGR to 0.5-2.2% guided; the multiple was set in the faster era; 8.5% adjusted EBITDA margin on drug-distribution economics leaves little absorption for reimbursement change; $1.16B of debt at a 24% weight against a business whose EBITDA is flat
**Watch for.** 2027 revenue and adjusted EBITDA guidance - whether EBITDA grows faster than revenue for the first time in two years; Full-year cash from operations against the 'at least $320M' guide; Whether the H2 adjusted EBITDA step-up implied by $480-495M full year against $222.3M in H1 actually lands; Any change in payer policy on site of care for high-cost chronic infusion therapies

**Data quality.** No flags were raised and the extract is clean on every standing check I can run: interest_expense of $51,248k against total_debt of $1,159,820k is an implied 4.42%, inside the normal band and consistent with the reported interest; capex is positive and steady [$41.3M, $35.6M, $41.9M] with no rental or fleet exposure; there is no convertible debt; shares of 157,027,504 come from the cover page; the FCFF base reconciles to guided 2026 cash flow. Two things remain open. First, the balance sheet in the extract is 2026-03-31 although a 2026-06-30 10-Q was filed 2026-07-29, so total_debt and cash are one quarter stale and the $150M of Q2 buybacks is not reflected in the share count (shares_asof 2026-04-28); this is small here but it is the standing staleness gap. Second and material: beta 0.56 with R-squared 0.07 sets a 7.45% WACC, and the verdict flips on it. At the engine's WACC the market requires -3.7% FCFF growth and my +3.0% gives a fair value of $33.20 (+45%); at a defensible beta near 1.0 the WACC is ~9.45%, the market requires +2.8%, and the same +3.0% gives $22.55 against a $22.94 price - fair. The scenario grid's +2pt WACC column IS that corrected case, so read the recorded fair value as the low-discount-rate end of a range that straddles the price, not as a point estimate. Stock compensation is 13% of the base, which is modest, and expensing it moves the requirement only from -3.7% to -1.1%. The screen's +138.4% headline gap is not a mispricing: it comes from applying the company's 13.3% historical revenue CAGR to FCFF when management has guided 2026 revenue growth of +0.5% to +2.2%.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1014739/000101473926000023/bios-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1014739/000101473926000021/bios-20260729.htm
