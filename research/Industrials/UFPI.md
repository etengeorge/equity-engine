# UFPI — UFP INDUSTRIES
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-15 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $81.03 · fair value $84.07 · gap +3.7%
- **Growth:** market implies -9.0%, analyst says +2.0% (delta +11.0%)
- **FCFF base overridden** by the analyst to $320.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 7.7% | 8.7% | 9.7% | 10.7% | 11.7% |
|---|---|---|---|---|---|---|
| bear | -4.0% | $86.52 | $74.96 | $66.40 | $59.80 | $54.56 |
| base | +2.0% | $111.19 | $95.60 | $84.07 | $75.19 | $68.15 |
| bull | +8.0% | $142.01 | $121.33 | $106.04 | $94.29 | $84.98 |

At the point WACC of 9.7%: bear -18.1%, base +3.7%, bull +30.9%
Across the whole grid the gap ranges -32.7% to +75.3% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** The market pays $81 because it is not capitalising the 2023 lumber-unwind cash flow. The engine's base of $498.4M is the mean of [$276.4M, $410.3M, $779.5M], and the $779.5M year is the working-capital release as lumber prices normalised — cash that came out of inventory once and cannot recur. Against the real run rate the price is ordinary, not capitulatory: 2025 free cash flow was $276.4M, and first-half 2026 operating cash flow was $61M against $87M of capex, i.e. NEGATIVE $26M. Management cut 2026 capex guidance twice, from $300-325M to $250-275M to $175-200M, and Q2 net sales rose 3% 'driven primarily by acquisitions'. A buyer at $81 is paying roughly 14-16x a mid-cycle $270-320M of owner earnings for a business with $1.9B of liquidity, a 3% dividend raise and $142M of first-half buybacks. That is a fair price for a housing-levered manufacturer three years into a downcycle, not a distressed one.

**What changed.** Q2 2026 (8-K/EX-99.1 2026-07-29; 10-Q 2026-08-05): H1 operating cash flow $61M, H1 capex $87M, H1 acquisition spend $122M, three acquisitions closed in the quarter. 2026 capex target cut to $175-200M from $250-275M, which had itself been cut from $300-325M; the release attributes part of the cut to acquiring MoistureShield's operating assets instead of building a greenfield. Net sales +3%, driven primarily by acquisitions, with organic volume gains named in Deckorators, Structural and Protective Packaging, Concrete Forming and Commercial; Surestone sales +37%. $142M of H1 share repurchases; quarterly dividend raised 3% to $0.36. No company-specific news in the 90-day store — the tape and the wire were both quiet, which lowers my confidence in 'nothing else happened' rather than confirming it.

**Base case.** The fix here is the base, not the growth rate. The naive +4.2% five-year revenue CAGR is measured across the 2021-22 lumber spike — revenue peaked at $9.63B in 2022 against $6.32B in 2025 — and revenue has now fallen three years running, so it is a cycle artifact rather than a forward rate. Correcting the FCFF base from the three-year mean of $498.4M to the 2025 actual of $276.4M moves the growth the market implies from -9.0% to +4.7%; at a normalised $320M it implies +1.2%. I use $320M, which is 2025 actual plus a partial credit for the acquired earnings that CFO-less-capex has been charged for but not yet earned from, and a base-case growth of 2% — value-added mix and volume, with no assumption of a lumber-price recovery. That lands within two or three points of what the market already implies, which is why there is no thesis here.

**Devil's advocate.**
- Strongest counter: This IS a genuine cyclical trough and my corrected base is the trough, not mid-cycle. Three consecutive years of revenue decline, capex cut 40% mid-year, $1.9B of liquidity against a $4.5B market cap, and a management team buying back $142M of stock in six months. If housing turns, free cash flow returns above $400M and $81 is cheap. The engine's own `possible_trough_cycle_base` flag says precisely this.
- What would prove it: Full-year 2026 operating cash flow less capex, measured after the $170M of seasonal working capital converts to cash by the start of Q4 as management says it will. If that figure lands above ~$350M, my $320M base is too low and the gap is real.
- Already visible today: Partly, and it points against the counter. H1 operating cash flow of $61M against $87M of capex is negative free cash flow with the seasonal build already inside it, and the company's own '$198M of first-half free cash flow' reaches that figure by adding the build back. More decisively, the standing lesson applies literally: the trough flag fires by comparing newest FCF to oldest, but the base is a three-year MEAN containing a super-cycle year, so it OVERSTATES rather than understates — the flag's advisory sentence is backwards here.
- Left unresolved: I could not separate organic from acquired growth. The release says sales rose 3% 'driven primarily by acquisitions' and gives no organic figure, while $122M of H1 acquisition spend sits in investing activities where CFO-less-capex never charges for it. That is the EFOR roll-up shape, and without an organic disclosure I cannot tell whether even flat revenue is being bought. It caps conviction and it is the reason my base is $320M rather than higher.

**Key risks.** Lumber price deflation compresses both revenue and the commodity spread that drives Retail segment margin; Acquisition spend ($122M in H1 alone) sits outside CFO-less-capex, so reported free cash flow overstates owner earnings on a roll-up; Housing starts are the single variable and there is no dated catalyst that forces a re-rating; Seasonal working capital makes any half-year cash flow reading unreliable in both directions
**Watch for.** Full-year 2026 CFO less capex after the Q4 working-capital conversion — above ~$350M refutes my base; An organic-versus-acquired revenue disclosure in the Q3 release or the 10-K; A third capex guidance revision in either direction

**Data quality.** Resolved: `possible_trough_cycle_base` — the flag fires correctly on newest-vs-oldest but its advisory text ('growth applied to a trough understates value') is backwards, because the base is a three-year mean containing the 2023 super-cycle working-capital release. Corrected the base from $498.4M to $320M; this alone moves the implied growth from -9.0% to +1.2% and closes the +70.9% gap. Open: no organic revenue disclosure, so the acquisition contribution to the 3% sales growth is unquantified; and the share count and balance sheet are current (shares as of 2026-06-27) so no staleness issue. Interest expense of $12.8M on $234.3M of debt implies 5.5%, which is plausible, so no missing-debt suspicion.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/912767/000110465926090859/ufpi-20260627x10q.htm
- https://www.sec.gov/Archives/edgar/data/912767/000091276726000044/ufpi-20260729xex99d1.htm
- https://www.sec.gov/Archives/edgar/data/912767/000110465926056076/ufpi-20260328x10q.htm
