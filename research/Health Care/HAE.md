# HAE — HAEMONETICS CORP
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-15 — RICH (conviction: medium)

- **Verdict:** rich · price $106.31 · fair value $80.06 · gap -24.7%
- **Growth:** market implies +12.5%, analyst says +7.0% (delta -5.5%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 5.2% | 6.2% | 7.2% | 8.2% | 9.2% |
|---|---|---|---|---|---|---|
| bear | +3.0% | $117.58 | $84.32 | $63.92 | $50.13 | $40.18 |
| base | +7.0% | $144.92 | $104.71 | $80.06 | $63.40 | $51.40 |
| bull | +11.0% | $176.54 | $128.27 | $98.68 | $78.70 | $64.31 |

At the point WACC of 7.2%: bear -39.9%, base -24.7%, bull -7.2%
Across the whole grid the gap ranges -62.2% to +66.1% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Haemonetics has been re-rated for a genuine portfolio transformation, and the case is coherent. It has exited low-margin liquid solutions and whole-blood products, bought Vivasure and built an Interventional Technologies franchise, and now guides fiscal 2027 to 5-8% reported and 4-7% organic revenue growth with 50-100bp of adjusted operating margin expansion and adjusted EPS growing comparably to revenue. Q1 fiscal 2027 organic growth was 5.9% with Plasma taking share, Blood Management Technologies sustaining momentum and Interventional returning to growth, and management raised full-year guidance. Free cash flow conversion is guided at roughly 80% of adjusted net income. A buyer at $106.31 — after a 98.8% twelve-month return — is paying for a business that has swapped commodity revenue for durable device and consumable revenue and is still early in the margin programme.

**What changed.** Q1 fiscal 2027 (8-K item 2.02 and 10-Q, 2026-08-06; quarter ended 2026-06-27). Revenue $339.4M, net income $33.0M, organic revenue growth 5.9%. Full-year guidance RAISED: reported revenue to 5-8% from 4-7%, organic to 4-7% from 3-6%, with adjusted operating margin expansion held at 50-100bp and free cash flow conversion held at about 80%. Operating cash flow $52.3M, up $34.9M, and free cash flow $39.1M, up $36.6M — but the company states the primary driver was 'favourable working capital adjustments driven by the timing of collections on receivables', so it is explicitly not a run-rate improvement. A $391.25M shelf registration tied to an ESOP-related stock matter was filed. 2026-08-18 8-K under item 7.01 only.

**Base case.** The company tells you the base is right and the discount rate is wrong. Fiscal 2027 free cash flow conversion of about 80% of adjusted net income lands around $170-185M, which brackets the engine's $187.3M three-year-mean base almost exactly — so the `possible_peak_cycle_base` flag is a false alarm here in the sense that matters: the newest year's $260.4M is the outlier, not the mean, and the company's own Q1 commentary explains it as receivables timing. With the base validated, the entire question becomes the cost of capital, and that input is broken. A beta of 0.51 with an R-squared of 0.027, marked `yahoo_rescaled`, gives a 7.2% WACC to a medical device company carrying 20% debt weight and a conditional-conversion convertible. At that WACC the market implies +12.5% five-year FCFF growth; at a defensible 9% it implies +20.6%, and at 10% it implies +24.4%. Against guided organic revenue growth of 4-7% plus 50-100bp of margin expansion, my base case for FCFF growth is 7% — revenue growth plus modest operating leverage, with buybacks not counted because the reverse DCF is an enterprise-level calculation. Even at the engine's own too-generous 7.2% discount rate, +12.5% required against +7% deliverable is a gap in the wrong direction; at any defensible rate it is a wide one.

**Devil's advocate.**
- Strongest counter: The transformation is real and the market is right to pay for it. Haemonetics has genuinely changed its mix: exiting whole blood and liquid solutions makes reported revenue look worse than the business is, which is why reported revenue fell 2% last year while organic growth was positive. A company with 4-7% organic growth, 50-100bp of annual margin expansion and 80% cash conversion compounds free cash flow well above revenue growth — plausibly 10-13% — and at that rate the engine's +12.5% requirement is roughly met and the stock is fair rather than rich. Simply Wall St publishes a DCF suggesting the shares are 49% BELOW fair value.
- What would prove it: Fiscal 2027 free cash flow landing at or above the 80%-conversion implication (roughly $180M+) on a full-year basis, with organic growth at the top of the 4-7% range and the margin programme delivering 100bp rather than 50bp. Two or three consecutive quarters of that would make low-double-digit FCFF compounding the right base case.
- Already visible today: Not yet, and the one quarter available cuts against it. Q1 free cash flow of $39.1M annualises to roughly $156M, BELOW the $187.3M base and well below what 80% conversion implies — and the company itself attributes the year-over-year improvement to receivables timing rather than to earnings. So the strongest available evidence for the counter is explicitly disavowed by the company that reported it. I take the counter seriously enough to move conviction from high to medium, but it does not win: the gap between 4-7% guided organic growth and the 20%+ the price requires at a defensible discount rate is too wide for margin expansion to bridge.
- Left unresolved: The cost of equity itself, which is the whole quantitative disagreement. I cannot measure Haemonetics' true beta from this runtime, and the engine's 0.51 is a rescaled Yahoo figure rather than our own regression, so its R-squared of 0.027 is not even a meaningful gate on it. My claim is that a medtech with 20% debt weight does not have a 7.2% WACC; I cannot prove the right number is 9% rather than 8%. I also could not read the $391.25M ESOP-related shelf registration to determine whether it implies future share issuance.

**Key risks.** The recorded fair value will UNDERSTATE the richness, because it is computed at the engine's 7.2% WACC and the schema has no field to override cost of equity — the verdict is the output here, the fair value is not; Plasma is the largest business and its customers are a handful of fractionators with an incentive to insource collection; The stock has returned 98.8% in twelve months and 35.9% in three, so positioning is the risk as much as fundamentals; Convertible notes with a conditional conversion feature sit inside the $1,174M debt balance
**Watch for.** Full-year fiscal 2027 free cash flow against the ~80% conversion guide — above ~$180M refutes me; Any change to the 4-7% organic guidance or the 50-100bp margin expansion target; Plasma volume commentary from CSL or Grifols on in-house collection; Use of the $391.25M shelf

**Data quality.** Resolved: `possible_peak_cycle_base_newest_fcf_2.3x_oldest`. The flag fires correctly but the mean is the better number, not the worse one — the company's own fiscal 2027 guidance of roughly 80% free cash flow conversion implies $170-185M against the engine's $187.3M base, and the outlier $260.4M newest year is explained in the Q1 release as receivables timing. So I did not override the base. NOT resolved, and it is the input that decides the name: `beta 0.51 (R-squared 0.027) yahoo_rescaled` produces a 7.2% WACC for a medical device company with a 20% debt weight. This is the failed-beta bias, and note the two errors here point in OPPOSITE directions — the low WACC makes the name look cheaper and the three-year-mean base makes it look more expensive — so the recorded -16.6% gap is not simply too small or too large. On the base I have validated, the implied growth runs from +12.7% at the engine's WACC to +24.4% at 10%; the verdict rests on that range exceeding guided growth at every point in it.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/313143/000031314326000120/hae-20260627.htm
- https://www.sec.gov/Archives/edgar/data/313143/000031314326000118/hae-20260806.htm
- https://finance.yahoo.com/healthcare/articles/hae-stock-gains-q1-earnings-153000000.html
