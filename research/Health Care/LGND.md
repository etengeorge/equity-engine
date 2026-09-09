# LGND — LIGAND PHARMACEUTICALS
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $288.83 · fair value $297.15 · gap +2.9%
- **Growth:** market implies +47.0%, analyst says +18.0% (delta -29.0%)
- **FCFF base overridden** by the analyst to $185.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 6.4% | 7.4% | 8.4% | 9.4% | 10.4% |
|---|---|---|---|---|---|---|
| bear | +6.0% | $267.60 | $219.71 | $186.77 | $162.73 | $144.41 |
| base | +18.0% | $434.79 | $353.20 | $297.15 | $256.30 | $225.24 |
| bull | +28.0% | $634.68 | $512.39 | $428.45 | $367.33 | $320.90 |

At the point WACC of 8.4%: bear -35.3%, base +2.9%, bull +48.3%
Across the whole grid the gap ranges -50.0% to +119.7% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Ligand is a royalty aggregator being priced on the portfolio it is building, not the cash it produced last year. Q2 2026 royalty revenue grew 32% to $48.0M and 42% to $91.0M for the half, driven by Travere's Filspari (newly approved in FSGS), Pelthos's Zelsuvmi and Merck's Ohtuvayre. Adjusted net income was $50.8M ($2.37 per diluted share, +48%) and $85.4M ($4.00, +36%) for the half. Management guides to $225-250M of full-year royalty revenue and $9.00-$9.50 of adjusted EPS, raising the low end. In June it raised $700M of 0.00% convertible notes - free five-year money - used $82M on a call spread, repurchased $60M of stock at ~$262, and closed the XOMA Royalty acquisition on 2026-07-14, adding 120+ commercial, clinical and preclinical assets, with roughly $700M of deployable capital still available. At $288.83 that is about 31x guided adjusted EPS for a business whose royalty base is compounding 30-40% and whose incremental margin on a new royalty is close to 100%.

**What changed.** $700M of 0.00% convertible senior notes due 2031 completed 2026-06-25 (8-K items 1.01, 2.03, 3.02). XOMA Royalty acquisition closed 2026-07-14 (8-K items 1.01, 2.01, 2.03) - AFTER the 2026-06-30 balance sheet this model prices. Cash, cash equivalents and short-term investments of $1.36B at 2026-06-30 versus $733.5M at 2025-12-31. 228,859 shares repurchased at ~$262. FDA approval of Filspari in FSGS. Full-year revenue guidance reaffirmed, adjusted EPS guidance low end raised to $9.00-$9.50.

**Base case.** The engine's $63.9M FCFF base is not this company's economics and I override it. For a royalty aggregator, capital deployed to buy royalties sits in investing activities while the receipts run through operating, so CFO-less-capex understates a business that is buying its own growth and overstates one that has stopped. Adjusted net income is the closer proxy: $9.00-$9.50 of guided adjusted EPS on roughly 20-21M diluted shares is $185-195M. I use $185M. On growth, royalty revenue is guided to $225-250M for 2026 against $91.0M in the first half, and the XOMA portfolio plus ~$700M of undeployed capital is what funds the next leg. Filspari, Ohtuvayre and Zelsuvmi are early in their curves. 18% for five years is below the current 32-42% royalty growth rate but above what an unlevered, non-acquiring royalty book would do, and it reflects that some of this growth is bought rather than organic.

**Devil's advocate.**
- Strongest counter: That 31x adjusted earnings for a royalty aggregator is a full price, and that my base override does most of the work in rescuing it. On the engine's own numbers the market requires +47% five-year FCFF growth, and +77% if stock compensation is expensed - and stock comp really is 60% of the reported FCFF base, which is an extraordinary proportion and means reported cash flow is substantially compensation the shareholders paid for. Correct the enterprise value for the missing $700M convertible and the requirement rises further. A royalty aggregator's growth is bought, its cost of capital is its edge, and Ligand is competing for assets against much larger balance sheets.
- What would prove it: Royalty revenue growth decelerating below 20% while deployable capital is spent, or the 2027 guidance implying that the XOMA assets contribute less than the purchase price implied.
- Already visible today: Partly. Captisol revenue is falling, and the 60% stock-comp share of reported free cash flow is a real and large adjustment that I have not fully charged for - at $185M of adjusted net income I am using a measure that already deducts some but not all of it. On the other side, adjusted EPS guidance was RAISED at the low end, which is not what deceleration looks like.
- Left unresolved: The enterprise value, and therefore the required growth rate, is not determinable from this brief. See the data-quality note: I can bound it between roughly $5.53B and $6.23B, which moves required growth by five points.

**Key risks.** Stock compensation is 60% of reported FCFF - the highest proportion in today's ten; Royalty growth is bought with converts and acquisitions; the model cannot distinguish it from organic; Concentration in a small number of partner-controlled products whose commercial execution Ligand does not control
**Watch for.** The first full quarter including XOMA, which reveals what the acquisition actually contributes; Deployment of the remaining ~$700M and the disclosed economics of what is bought; Filspari FSGS launch trajectory at Travere

**Data quality.** One flag, `stock_comp_is_60%_of_fcff`, is correct and is the largest such proportion in today's ten. Two defects it does NOT flag, both established from the Q2 press release. (1) THE $700M CONVERTIBLE IS ALMOST CERTAINLY MISSING FROM ENTERPRISE VALUE. Ligand completed $700M of 0.00% convertible senior notes on 2026-06-25 and reports $1.36B of cash, cash equivalents and short-term investments at 2026-06-30. The brief's enterprise value of $5,526.8M against a $5,758.0M market cap implies NET CASH of only $231M, which cannot be reconciled with $1.36B of cash unless roughly $1.13B of debt is being counted - and Ligand's only material debt is the $700M convertible. Whichever way the extractor is reading it, the LESSONS.md rule applies: `FIELDS['total_debt']` does not touch the `ConvertibleNotesPayable*` / `ConvertibleDebt*` concepts, and a 0.00% coupon means the `interest_expense / total_debt` detector cannot catch it either - the cheap detector fails silently on a zero-coupon convertible. I bound true EV at roughly $6.23B, which raises the growth the market requires from +47.0% to +50.7% on the engine's base. NOTE THE DIRECTION IS UNUSUAL: on TDOC this bug manufactured a false BUY, whereas here it makes an already-rich-looking name richer, so it is not a false-buy instance - but it is the same bug. (2) The XOMA Royalty acquisition closed 2026-07-14, two weeks AFTER the balance sheet date, so consideration paid and any assumed obligations are absent from the enterprise value while the share count (2026-08-04) is post-deal - the ALKS pattern. Given that the base, the enterprise value and the discount rate are all questionable in the same direction, I am recording no_edge rather than 'rich': the -73.6% gap is directionally believable but it is not a number I would act on, and my +18% is an estimate of the business rather than a reading of this model.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/886163/000088616326000041/lgnd-20260806.htm
- https://www.sec.gov/Archives/edgar/data/886163/000088616326000044/lgnd-20260630.htm
- https://www.sec.gov/Archives/edgar/data/886163/000119312526302660/d108457d8k.htm
- https://www.sec.gov/Archives/edgar/data/886163/000119312526282990/d167360d8k.htm
