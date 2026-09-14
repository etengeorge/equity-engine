# AEO — AMERICAN EAGLE OUTFITTERS
*Consumer Discretionary · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $15.02 · fair value $12.40 · gap -17.5%
- **Growth:** market implies -3.7%, analyst says +0.0% (delta +3.7%)
- **FCFF base overridden** by the analyst to $200.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 9.3% | 10.3% | 11.3% | 12.3% | 13.3% |
|---|---|---|---|---|---|---|
| bear | -7.0% | $11.56 | $10.29 | $9.30 | $8.50 | $7.83 |
| base | +0.0% | $15.62 | $13.81 | $12.40 | $11.25 | $10.31 |
| bull | +8.0% | $21.74 | $19.11 | $17.05 | $15.38 | $14.02 |

At the point WACC of 11.3%: bear -38.1%, base -17.5%, bull +13.5%
Across the whole grid the gap ranges -47.9% to +44.7% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $15.02 the market is paying ~$2.4B of enterprise value for a retailer that just posted RECORD quarterly revenue of $1.38 billion, up 8%, with total comparable sales up 6% and Aerie plus OFFLINE growing 25% including 19% comparable growth. Full-year operating income is guided to $540-550M. On the reported numbers that is roughly 4x EV/EBITDA with a 3% dividend yield, and the Aerie franchise alone — growing 25% with its own margin rate improving — is arguably worth more than the whole enterprise value. The bull case is that the market is applying a dying-mall-retailer multiple to a portfolio where the growth brand is now a majority of the incremental dollar.

**What changed.** Q2 2026 (quarter ended 2026-08-01, reported 2026-09-09) and the stock fell ~13-16%. The reason is in the company's own release. AEO received $196 MILLION of IEEPA tariff refunds including interest during the quarter. The net benefit to gross profit was $179M — 1300 basis points of the 980bp of gross margin expansion — and the net benefit to OPERATING PROFIT was $161M, or 1170bp of operating margin. Operating profit was $211M against $103M last year. And critically: 'The company has received substantially all of the tariff refunds for which it submitted refund claims.' Interest expense rose to $47M because AEO had SOLD certain tariff refund claims to a third-party buyer in the prior fiscal year, of which $45M is that agreement. American Eagle brand comparable sales were MINUS 1%.

**Base case.** Strip the refund and the quarter inverts. Ex-refund operating profit is $211M - $161M = $50M against $103M a year earlier, DOWN 51%. Gross margin expanded 980bp of which 1300bp was the refund, so ex-refund gross margin FELL about 320bp — consistent with the company's own statement that merchandise margins deleveraged 330 basis points. Full-year guidance of $540-550M is explicitly 'inclusive of net tariff refund benefit', so the underlying number is roughly $380-390M. The cash statement says the same thing louder: H1 operating cash flow was $116.3M against capital expenditure of $127.6M, so FREE CASH FLOW WAS NEGATIVE $11.3M for the half — and that is WITH $196M of refunds collected inside it. I therefore override the base to $200M, roughly the ex-refund normalised level and close to the FY2025 actual of $195.4M, and set growth to zero: one brand compounding 25% against a larger brand at -1% comps, with a mechanical $161M headwind in fiscal 2027 that has no offset because the refunds are done.

**Devil's advocate.**
- Strongest counter: That I am punishing AEO for an accounting windfall while ignoring a genuinely improving business. Total comparable sales were +6% — that is not a company in decline. Aerie at +19% comps and 25% total revenue growth is one of the better franchises in specialty retail. Revenue was a record. And the refund is real cash: $196M actually collected, which funds buybacks and the dividend regardless of how it is labelled.
- What would prove it: Whether ex-refund profitability is growing. That is answerable from the company's own disclosure rather than inference, because AEO quantified the benefit at every line.
- Already visible today: Yes, and it decides the name against the bull. Ex-refund operating profit fell 51%, from $103M to $50M. Ex-refund gross margin fell ~320bp. H1 free cash flow was negative $11.3M with the refund cash already inside it. The +6% comp is being bought with markdowns and 'planned investments in advertising' — SG&A rose 19% against revenue up 8%. A retailer growing comps 6% while operating profit ex-windfall halves is not improving, it is buying traffic.
- Left unresolved: Where the ex-refund base really sits. The refund cash and the $35M of associated incentive compensation accrual straddle the income statement and the cash statement in ways I could not fully separate, and AEO also sold refund claims to a third party in the PRIOR year, so some of the economics were recognised before this window. My $200M base could be $170M or $230M, which moves the implied requirement by several points.

**Key risks.** Fiscal 2027 laps $161M of operating profit with no offset — a dated, mechanical headwind the model cannot see; American Eagle, still the larger brand, is at -1% comparable sales while SG&A grows 19%; H1 free cash flow negative $11.3M despite collecting $196M of refunds; capex guided $250-260M
**Watch for.** Q3 gross margin against the guided 'flat YoY' — the first quarter with no refund in it; American Eagle brand comparable sales turning positive; Fiscal 2027 operating income guidance, which must absorb the $161M

**Data quality.** The extract is A QUARTER STALE (cached to the 2026-05-02 balance sheet) and misses the entire tariff event; I worked from the 2026-09-10 10-Q and the 2026-09-09 release instead. This is the IEEPA screening check firing for the third consecutive session after SIG/JILL/BBW on 2026-09-10 and LOVE on 2026-09-11, and it is the largest instance recorded so far — $196M received, $161M of net operating income benefit, against a company with a $2.5B market capitalisation. As in every prior case the company discloses the ex-refund figure itself. `possible_trough_cycle_base_newest_fcf_0.48x_oldest` — the flag's advisory text is backwards again: the FCF series [$195.4M, $254.3M, $406.3M] is a monotonic DECLINE, not a cyclical trough, so treating the base as understated is wrong in the same way it was on AMR. `operating_leases_60%_of_EV` — not added to EV, because FCFF is computed after cash rent and capitalising one side without the other double-counts; recorded as an operating-leverage risk instead. One new observation worth carrying: AEO SOLD tariff refund claims to a third-party buyer, which pulls the cash forward and books $45M of INTEREST EXPENSE against it — so the refund flatters operating profit while degrading the interest line, and a reader looking only at operating income sees none of the cost.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/919012/000119312526387856/aeo-20260801.htm
- https://www.sec.gov/Archives/edgar/data/919012/000119312526386510/aeo-20260909.htm
