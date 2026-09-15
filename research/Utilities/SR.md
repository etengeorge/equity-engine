# SR — SPIRE INC
*Utilities · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-15 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $81.36
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Spire is a rate-regulated natural gas utility, and the price is what a regulated utility trades at: a function of allowed return on equity, rate base growth and the ten-year Treasury, not of discounted free cash flow. At $81.36 with a 0.3 beta and the tape flat (-0.6% / -0.9% / +3.9% over five, twenty-one and sixty-three days) in a week when the macro feed leads with 'Rising Bond Yields' and 'A Rate Hike Could Be the First of Many', the market is expressing a yield-spread view. A buyer is underwriting Missouri, Alabama and now Tennessee regulators allowing recovery on a growing rate base. That question cannot be asked of a DCF on free cash flow.

**What changed.** Spire completed the acquisition of the Piedmont Natural Gas Tennessee business on 2026-03-31 (8-K item 2.01, 2026-04-30), and on 2026-06-30 filed a further item 2.01 8-K whose EX-99.1 describes a transaction whose 'proceeds help fund Spire's previously completed acquisition of the Piedmont Natural Gas Tennessee business'. A further item 1.01 8-K followed on 2026-09-01. The engine's fiscal-year end is 2025-09-30, so the entire three-year cash flow history predates the Tennessee acquisition and the financings that funded it.

**Base case.** No growth rate is supplied, because free cash flow to the firm is not a meaningful measure for this business and the engine has correctly declined to compute one. CFO less capex over the three years available is [-$344.4M, +$51.1M, -$222.3M], a mean of about -$172M — and negative free cash flow is the NORMAL, healthy state of a rate-regulated utility, which funds rate base growth with debt and equity issuance and earns a return on it. That is the standing BKH lesson and it applies here without qualification: capex of $922.4M, $861.3M and $662.5M against operating cash flow of $578.0M, $912.4M and $440.2M is a utility investing ahead of its cash generation, which is what regulators pay it to do. Manufacturing a positive base to force a DCF would invert the meaning of the accounting.

**Devil's advocate.**
- Strongest counter: The multiples table exists precisely so that 'a DCF cannot value this' does not collapse into 'no answer'. It blends to $89.48 against an $81.36 price, a +10.0% gap, on cohorts of 13 to 30 Utilities names — and unlike the RIOT and EPRT cases the cohort IS ranked and no row is negative. A modest discount to the sector on a utility with a freshly acquired Tennessee franchise is a usable, if unexciting, observation.
- What would prove it: Whether the four multiple rows describe the same company. If they cluster, the blend means something; if they straddle the price in opposite directions, the blend is averaging disagreement rather than corroborating anything.
- Already visible today: Yes, and they straddle badly, so the counter fails the standing refusal test. Against an $81.36 price, ev_ebitda gives $31.80 / $73.55 / $120.76, ev_sales gives $12.48 / $74.25 / $121.35, ev_gross_profit gives $81.36 / $166.80 / $335.46 and p_tbv gives $36.12 / $43.33 / $48.94. The p_tbv row says the stock is worth roughly HALF the price at every percentile while the ev_gross_profit row says it is worth up to four times the price, and the ev_sales p25-to-p75 range spans a factor of ten. That is the RIOT/EPRT signature verbatim: rows pointing in opposite directions mean the blend is noise with a decimal point. Note also that the ev_gross_profit p25 value of $81.36 equals the price exactly because Spire's own 7.7x multiple equals the cohort p25 of 7.7x — a coincidence of rounding, not a valuation.
- Left unresolved: I did not attempt to build the correct model for this name, which would be a regulated-utility framework: allowed ROE, equity ratio, rate base and the approved capital structure in each of Missouri, Alabama and Tennessee. That is outside what this engine computes and outside what one session could assemble from the filings I have. I also could not size the Tennessee acquisition's effect on rate base or on the share count.

**Key risks.** Negative normalised free cash flow is structural for a rate-regulated utility, not a distress signal — and it makes the DCF inapplicable rather than merely imprecise; The multiples fallback fails the standing refusal test: rows straddle the price in opposite directions by a factor of four; Three-year cash flow history predates the Piedmont Natural Gas Tennessee acquisition completed 2026-03-31; Rate-sensitive in a week when the macro feed is leading with the possibility of Fed hikes
**Watch for.** Rate case outcomes in Missouri, Alabama and Tennessee; The first full fiscal year including the Tennessee franchise, which will reset the rate base; Any equity issuance funding the acquisition, which would change the share count; Long-end Treasury yields, which set the comparator for a 0.3-beta regulated name

**Data quality.** Three flags raised and all three are correct and mutually reinforcing: `negative_fcf_year_in_window`, `lumpy_fcff_spread_2.3x_of_mean` and `nonpositive_normalized_fcff`. The engine did the right thing in refusing a DCF; my contribution is to confirm that the multiples fallback must ALSO be disregarded rather than used as a substitute, on the straddle test set out in the RIOT/EPRT lesson. Two further items neither flagged nor resolved: the fiscal-year end is 2025-09-30 so the entire cash flow history predates the Piedmont Natural Gas Tennessee acquisition that closed 2026-03-31 (an item 2.01 8-K on 2026-04-30, with a second item 2.01 on 2026-06-30 and an item 1.01 on 2026-09-01), and interest expense of $204.1M against $6,249.5M of recorded debt implies 3.3%, which is low for current coupons and suggests the debt balance may include recently issued paper not yet reflected in the expense, or that the acquisition financing is only partly captured. Recording explicitly that refusing is NOT a judgment that Spire is expensive or cheap — I have no view on its value.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1126956/000119312526334335/sr-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1126956/000119312526290674/sr-ex99_1.htm
- https://www.sec.gov/Archives/edgar/data/1126956/000119312526333825/sr-ex99_1.htm

**Ingestion notes.** no usable final_growth
