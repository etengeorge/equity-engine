# VSEC — VSE CORP
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-07 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $203.91
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** VSE has become a pure-play aviation aftermarket platform and is being priced as one. Q2 2026 revenue rose 65% to a record $449.1M with roughly 14% organic growth, net income from continuing operations doubled to $28.5M, adjusted EBITDA from continuing operations rose 98% to $86.0M and the margin reached a record 19.2%, up about 320bp. Full-year guidance was raised twice-over: revenue growth of 61-64% (from 57-61%) and adjusted EBITDA margin of 18.7-19.0% (from 18.1-18.5%). On that guide the company earns roughly $330M of adjusted EBITDA in 2026 against an enterprise value of about $6.6B — call it 20x — which is the multiple the market pays for HEICO- and TransDigm-adjacent aftermarket compounders with mid-teens organic growth and a repeatable acquisition engine. The bear case is the balance sheet that bought it: $966.7M of debt, adjusted net leverage of 2.4x, and $19M of free cash flow in a quarter that produced $86M of EBITDA.

**What changed.** The company was rebuilt. VSE completed the acquisition of Precision Aviation Group for approximately $2 billion, plus Aero 3 and NorthStar, and divested the Fleet segment into discontinued operations. Repair revenue rose 149.4% and distribution 17.2% year over year. In February 2026 it issued common stock and tangible equity units (including 5.93% senior unsecured amortizing notes) and refinanced its term loan, writing off $3.2M of unamortized issuance costs. At 2026-06-30: 28,064,972 shares outstanding (as of 2026-07-31), $75.4M of cash, $966.7M of total debt, $871.6M of net debt, about $500M available under the revolver.

**Base case.** I decline to state a five-year FCFF growth rate because there is no FCFF base to grow. The three-year window the model uses spans the Fleet divestiture and three acquisitions; operating cash flow for the first half of 2026 was negative, and the free cash flow that does exist ($18.7M in Q2, on $86.0M of adjusted EBITDA) is being consumed by the inventory build that a distribution business requires when it grows revenue 65%. That is a real economic feature of the model, not an accounting artefact, and it means a discounted cash flow on this company would be a statement about working-capital timing rather than about earning power.

**Devil's advocate.**
- Strongest counter: The best case against refusing: I have enough to say something. I computed a corrected forward multiple of roughly 20x EV to 2026 adjusted EBITDA, which sits squarely inside the aviation-aftermarket comparable range, so 'roughly fairly valued' is a defensible conclusion and no_model looks like evasion. I take the point, and I have recorded the corrected multiple above rather than hiding behind the refusal. What I will not do is convert it into a fair value. Twenty times EBITDA on a business two quarters into integrating a $2B acquisition, where the guided margin depends on synergies management describes as 'meaningful' but has not quantified, and where the cash conversion is currently 22% of EBITDA, spans a range too wide to call. A point estimate would claim precision this does not have.
- What would prove it: Second-half 2026 free cash flow. Management explicitly expects it to be stronger and to support deleveraging; if it is not, the working-capital drag is structural rather than growth-related and the 20x multiple is on an EBITDA that never becomes cash.
- Already visible today: Partially, and it favours the company: Q2 free cash flow of $18.7M improved significantly from Q1 on better profitability and working capital, and adjusted net leverage of 2.4x is not stressed. But one improving quarter after a negative half is not a trend.
- Left unresolved: Whether the 18.7-19.0% adjusted EBITDA margin survives the full PAG integration, and how much of the reported margin expansion is mix rather than synergy. I could not separate those from the disclosure.

**Key risks.** Two quarters into integrating a ~$2B acquisition, with synergies described but not quantified; Cash conversion: $18.7M of free cash flow on $86.0M of quarterly adjusted EBITDA, after a negative first-half operating cash flow; $966.7M of debt at 2.4x adjusted net leverage on an acquisition-built platform; Roughly 20x forward EBITDA leaves no room for a commercial aftermarket slowdown
**Watch for.** Second-half 2026 free cash flow and the deleveraging management has promised; Organic growth ex-acquisition holding in the low-to-mid teens; Quantified PAG synergy targets

**Data quality.** Two of the three flags are correct and the third is the reason this is no_model. `nonpositive_normalized_fcff`, `negative_fcf_year_in_window` and `lumpy_fcff_spread_2.0x_of_mean` all describe the same thing: a three-year window spanning the Fleet divestiture and three acquisitions, during which a distribution business scaling revenue 65% consumed cash in inventory. There is no usable FCFF base and the reverse DCF correctly returns n/a. The multiples table is worse than useless and must be disregarded, exactly per the standing lesson of 2026-09-03. Its rows straddle the price in opposite directions — ev_ebitda median $35.42, ev_sales median $35.74, ev_gross_profit median $136.34, p_tbv median $21.44, against a price of $203.91 — and the cohort is explicitly 'not ranked'. The blended midpoint of $57.24 and its '-71.9% gap' are noise with a decimal point. The specific defect: 'its own' EV/EBITDA reads 50.9x, which is trailing EBITDA that predates PAG measured against a post-PAG enterprise value. Corrected: enterprise value is roughly $6.59B (28,064,972 shares at $203.91 = $5.72B, plus $871.6M of net debt) against 2026 guided adjusted EBITDA of approximately $326-336M — about 20x, not 50.9x. Share count and debt both reconcile to the 10-Q, so the market cap on this brief is right; it is the earnings denominator that is wrong.

**Sources.**
- https://www.sec.gov/Archives/edgar/data/102752/000010275226000064/vsec-20260630.htm
- https://www.stocktitan.net/sec-filings/VSEC/8-k-vse-corp-reports-material-event-3f7f4e02eb59.html
- https://www.fool.com/earnings/call-transcripts/2026/08/12/vse-vsec-q2-2026-earnings-call-transcript/

**Ingestion notes.** no usable final_growth
