# ASO — ACADEMY SPORTS AND OUTDOORS
*Consumer Discretionary · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-15 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $54.25 · fair value $54.95 · gap +1.3%
- **Growth:** market implies +0.7%, analyst says +1.0% (delta +0.3%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 7.3% | 8.3% | 9.3% | 10.3% | 11.3% |
|---|---|---|---|---|---|---|
| bear | -3.0% | $63.35 | $53.17 | $45.76 | $40.13 | $35.71 |
| base | +1.0% | $76.43 | $63.99 | $54.95 | $48.09 | $42.70 |
| bull | +5.0% | $91.62 | $76.54 | $65.60 | $57.30 | $50.78 |

At the point WACC of 9.3%: bear -15.7%, base +1.3%, bull +20.9%
Across the whole grid the gap ranges -34.2% to +68.9% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $54.25 the price requires only +0.7% FCFF growth for five years, which is a low bar and a defensible one. Academy earns $265-330M of free cash flow a year on a $3.5B enterprise value, opened 24 stores in fiscal 2025 and plans more than a dozen in the back half of 2026, and is retiring roughly 5% of its shares a year — $182.1M of buybacks in the first half alone, up 82%. Diluted share count guidance fell from 66.0M to 64.5M in one quarter. A buyer at $54 does not need comps to grow; they need Academy to hold roughly flat cash flow while the share count shrinks. Given 327 stores, a 4.4% inventory build against 4.7% sales growth, and $298M of cash against $494M of long-term debt, that is a reasonable thing to underwrite.

**What changed.** Q2 fiscal 2026 (8-K/EX-99.1 and 10-Q, both 2026-09-09; quarter ended 2026-08-01), which the screen's extract does not yet contain — its balance sheet is dated 2026-05-02, a quarter stale. Net sales +3.0% to $1,647.3M, comparable sales NEGATIVE 0.4%, eCommerce +12.8%, GAAP diluted EPS $2.17 (+17.3%). Gross margin 40.4% against 36.0%, up 440bp. The company discloses the net tariff refund impact to EPS as $0.06 including reinvestments, and books a 'Loss on tariff refund monetization' of $61,759 thousand with a 'Remittance of tariff refund claims' of $(72,224) thousand — i.e. Academy SOLD its IEEPA refund claims to a third party at a discount, and that loss is already inside the GAAP result. Guidance: full-year net sales UNCHANGED at $6,230-6,355M, GAAP net income UNCHANGED at $390-415M, adjusted net income UNCHANGED at $420-445M, gross margin rate RAISED 100bp to 35.5-36.0%, adjusted free cash flow raised to $300-350M from $250-300M. The CEO flags pressure on lower-income households.

**Base case.** Academy is a low-single-digit-growth retailer whose unit economics are flat and whose per-share compounding comes from buybacks rather than the business. Comps were -0.4% in the quarter and +1.1% year to date against a 7% larger store base, so sales per store are falling; inventory per store is down 5.6% in units and 2.3% in dollars, which is disciplined but not expansionary. The engine's $265.7M base is the mean of [$222.1M, $328.5M, $328.0M] and is slightly understated because the extract tags interest as NEGATIVE $36.2M (net interest income) and subtracts the after-tax figure rather than adding it — worth about $27M, under one point of implied growth. Against the company's own $300-350M adjusted free cash flow guide, which includes the refund cash, an ex-refund $250-300M is the honest forward number, so the engine's base is about right. I take +1% real FCFF growth: new stores roughly offsetting negative comps, with no credit for a consumer recovery.

**Devil's advocate.**
- Strongest counter: The stock is up 20.7% in five days on 2.3x volume, and my own reading says the quarter contained no incremental profit. That is an argument for RICH, not no_edge: the EPS guidance raise is arithmetic on the denominator, fiscal 2027 laps a quantified margin benefit, and comps are negative. If the market has re-rated a retailer for a buyback, the re-rating should unwind.
- What would prove it: Q3 and Q4 gross margin ex-refund against the 34.8% fiscal 2025 base, and whether the unchanged $390-415M net income guide is met at the low or high end. A Q3 gross margin below ~34.5% ex-refund with comps still negative would confirm that the margin structure is deteriorating underneath.
- Already visible today: The guidance table settles the profit question and it is unambiguous. Sales guidance unchanged, GAAP net income guidance unchanged at both ends, adjusted net income guidance unchanged at both ends — and the EPS raise reconciles EXACTLY to the share count: $390-415M over 64.5M diluted shares is $6.05-6.43 against the new $6.05-6.45 guide, where 66.0M gave $5.91-6.29 against the old $5.95-6.35. Not one incremental dollar of profit was guided. What I could NOT establish is that this makes the stock rich, because the reverse DCF only asks for +0.7% growth, and a retailer retiring 5% of its shares a year clears that bar on buybacks alone.
- Left unresolved: I could not size the gross tariff benefit. Academy discloses the NET EPS impact ($0.06, 'including reinvestments') and the $61.8M monetisation loss, but not the gross refund, so I cannot compute an ex-refund gross margin the way AEO, SIG and JILL permitted. The 100bp gross-margin guidance raise against an unchanged net income guide is the best available proxy and it is indirect.

**Key risks.** Fiscal 2027 laps roughly 100bp of tariff-driven gross margin with no offset — a dated, mechanical headwind; Comparable sales are negative against a 7% larger store base, so sales per store are declining; Management explicitly flags pressure on lower-income households, which is Academy's core customer; The five-day +20.7% move discounts an EPS raise that contains no incremental profit dollar
**Watch for.** Q3 gross margin ex-refund against the 34.8% fiscal 2025 rate; Whether GAAP net income lands at the low or high end of the unchanged $390-415M guide; Comp trend turning positive, or the buyback pace slowing below ~5% of shares a year; Disclosure of the gross IEEPA refund amount in the 10-K

**Data quality.** No flags were raised on this brief and the inputs are broadly sound, but two things are worth recording. First, the extract is a quarter stale — balance sheet 2026-05-02 against a 10-Q for the quarter ended 2026-08-01 filed 2026-09-09 — so the enterprise value predates the quarter that caused the move; the balance-sheet items moved little ($298.2M cash, $494.2M long-term debt) so the effect is immaterial here. Second, `interest_expense` is tagged NEGATIVE $36,214,000, i.e. net interest income captured under an expense concept, so the FCFF base SUBTRACTS about $27M after tax instead of adding it. That understates the base by ~10% and therefore overstates the implied growth by under a point — conservative, and it does not change the verdict. The IEEPA screening check was run and Academy is a genuine but only partial instance: the refund is real and was monetised at a $61.8M loss, but the company's own net EPS impact of $0.06 means the headline beat is mostly not the refund.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1817358/000181735826000102/aso-20260801.htm
- https://www.sec.gov/Archives/edgar/data/1817358/000181735826000100/aso-20260909.htm
- https://www.fool.com/earnings/call-transcripts/2026/09/10/academy-sports-aso-q2-2027-earnings-call-transcript/
- https://finance.yahoo.com/markets/stocks/articles/academy-sports-aso-turns-tariff-105619595.html
