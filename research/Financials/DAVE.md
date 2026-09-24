# DAVE — DAVE CLASS A
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-24 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $326.19

**The case for the price.** Dave is a consumer fintech, not a balance-sheet lender, and the market prices it as one. At $326.19 it trades at 13.93x tangible book because tangible book is not the constraint on its earnings - the ExtraCash product turns over in days, the member base and the underwriting model (CashAI) are the productive assets, and neither appears on the balance sheet. Recent product news is consistent with that: raised ExtraCash limits, the Flex spending product, CashAI V6 underwriting, and marketing spend scaling with flat customer acquisition cost. A buyer at this price is underwriting monetisation per member, not return on equity.

**What changed.** Nothing that changes the verdict. Q2 2026 reported 2026-08-05 with the stock up 7% since; product expansions announced through August (ExtraCash limit increases, Flex, CashAI V6); an item 5.02 officer change on 2026-08-14. In March 2026 there were items 1.01/2.03/3.02 (a financing and an equity issuance) that would matter if the model were usable, and it is not.

**Base case.** Not applicable and deliberately not supplied. The justified price-to-tangible-book model is the wrong instrument for this business, and the engine's own numbers say so at maximum volume.

**Devil's advocate.**
- Strongest counter: That -96.0% is not noise, it is a warning, and refusing lets an obviously expensive stock off the hook. Dave trades at 13.93x tangible book and 13th percentile of 339 Financials - the most expensive decile - on a business whose three-year GAAP return series spans MINUS 65.7% to POSITIVE 57.8% and contains an outright loss year. If the justified-P/TBV model is wrong about the level it may still be right about the direction.
- What would prove it: Sustained GAAP profitability across several quarters with credit losses disclosed through a full consumer cycle, and a return measure that is stable enough to price against something.
- Already visible today: The instability is visible and it is the point: an 8.7% 'sustainable' ROTCE averaged across a range of -65.7% to +57.8% is not a return, it is three unrelated numbers. The counter is directionally plausible and I cannot convert it into a fair value without committing the exact error this record already documents.
- Left unresolved: Whether Dave is expensive. I suspect it is; I have no defensible way to say so from this model, and the standing rule is explicit that supplying a ROTCE here would launder a category error into a number.

**Key risks.** Regulatory risk to earned-wage-access and overdraft-alternative products; Credit performance of the ExtraCash book through a consumer downturn - never yet observed at this scale; 13.93x tangible book leaves no valuation support if growth stalls; A three-year return series containing a loss year and a 123-point range
**Watch for.** Several consecutive quarters of stable GAAP return on tangible equity - the only thing that would make this name modellable at all; Any CFPB or state action on earned-wage-access products; ExtraCash loss rates disclosed alongside the raised limits

**Data quality.** Refused on the standing PIPR rule rather than on a broken input. `method` is assigned by GICS sector and Financials is not a sector of banks: an actual price-to-tangible-book of 13.93x is the documented signature of a business whose capital is not its balance sheet, and above roughly 4x the justified-P/TBV model is a category error rather than a calibration problem. `unstable_rotce_-65.7%_to_57.8%` and `loss_year_in_window` compound it, and per the EBC entry the unstable-ROTCE flag should be treated as DISQUALIFYING the model output rather than as a caution to reason past. Averaging -65.7%, a loss year and +57.8% into an 8.7% 'sustainable' return and pricing it through a Gordon form with terminal growth fixed at 2% produces the -96.0% gap and the 13th percentile of 339 Financials; both are arithmetic, not analysis. No rotce_override supplied, by design. One minor extract oddity noted and not pursued because it changes nothing: balance_sheet_form reads 10-K with balance_sheet_asof 2026-06-30 on a December-year-end filer, the same provenance anomaly recorded on SLG.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1841408/000119312526335154/dave-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1841408/000119312526335119/dave-ex99_1.htm

**Ingestion notes.** no usable final_growth
