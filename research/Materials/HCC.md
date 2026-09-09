# HCC — WARRIOR MET COAL INC
*Materials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $105.58 · fair value $100.96 · gap -4.4%
- **Growth:** market implies +6.3%, analyst says +3.0% (delta -3.3%)
- **FCFF base overridden** by the analyst to $420.0M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 8.6% | 9.6% | 10.6% | 11.6% | 12.6% |
|---|---|---|---|---|---|---|
| bear | -8.0% | $81.08 | $71.39 | $63.92 | $58.00 | $53.18 |
| base | +3.0% | $130.81 | $113.92 | $100.96 | $90.70 | $82.37 |
| bull | +9.0% | $167.75 | $145.43 | $128.31 | $114.77 | $103.79 |

At the point WACC of 10.6%: bear -39.5%, base -4.4%, bull +21.5%
Across the whole grid the gap ranges -49.6% to +58.9% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** Warrior has just finished a $1.02 billion mine and the market is paying for the result, not waiting for it. Blue Creek's development capital is complete, Q2 2026 delivered record sales of 3.7 million short tons (+65% y/y), adjusted EBITDA of $156.9M (+193%), net income of $87.4M, cash cost of sales down 9% to $92.53 per short ton on Blue Creek's structurally lower cost base plus the 45X credit, and free cash flow of $103.4M in the quarter after two years of negative free cash flow. Full-year guidance was RAISED by 0.5Mt to 13.0-14.0 million tons. The stock is up 74.6% over twelve months. At an enterprise value of $5.43B the market is asking for +6.3% five-year FCFF growth - which is roughly the remaining Blue Creek ramp, and no more. That is a coherent view: buy the volume step-up, do not extrapolate the met coal price that is making it look good.

**What changed.** Q2 2026 (2026-08-05): record 3.7Mt sales, adjusted EBITDA $156.9M vs $53.6M, FCF +$103.4M vs -$56.7M, cash cost $92.53/t vs $101.17/t. Blue Creek development capital complete at $1,022.9M total, in line with guidance; project capex for the rest of 2026 falls to $50-75M and sustaining capex is $105-115M. Full-year volume guidance raised. Liquidity $452.9M including $302.3M cash. Three longwall moves scheduled before year-end (two Q3, one Q4), which will make Q3 optically weaker.

**Base case.** I override the base upward and the growth rate downward, and the two roughly cancel. The engine's $383.9M is the mean of [$147.3M, $336.4M, $668.0M], which is contaminated at both ends - the $668.0M is a 2022-23 met coal super-cycle year and the $147.3M is a Blue Creek construction year - so it is not a normalized number in either direction. Building it forward instead: at the guided 13.0-14.0Mt and Q2's realised ~$42 per ton of adjusted EBITDA, EBITDA runs near $570M; less $105-115M of sustaining capex, less roughly $17M of net cash interest, plus after-tax interest added back, gives an FCFF base near $420M. From there I take +3%. The volume ramp is a one-time step to full Blue Creek rate, largely captured within two years, not a perpetual growth rate - and beyond it Warrior is a price-taker on the premium low-vol HCC index with no control over the variable that decides everything. At $420M and +3% the model returns an enterprise value of $5.18B against a market $5.43B: a 4-5% difference, which is noise.

**Devil's advocate.**
- Strongest counter: The strongest bear case is that Q2 2026 is a peak dressed as a trough. The flag on this brief says the opposite - `possible_trough_cycle_base` - and LESSONS.md records from the AMR pass on 2026-09-08 that this flag's advisory text is backwards on cyclicals: it compares only the newest year to the oldest, calls a 0.22x ratio a trough, and tells the analyst that 'growth applied to a trough understates value' while the base is actually a three-year mean containing a super-cycle year. Applied here, the argument is that $42/ton of EBITDA and a 74.6% twelve-month share price move are the peak, the 45X credit is a policy subsidy that may not persist, and the market's +6.3% is therefore too generous, not too harsh.
- What would prove it: Q3 and Q4 2026 realised prices and EBITDA per ton against Q2's, with the three scheduled longwall moves stripped out, plus the FY2027 capital and cost guidance that shows what sustaining Warrior looks like with Blue Creek in steady state.
- Already visible today: Partly, and this is where HCC genuinely differs from AMR. AMR's depressed cash flow was a price trough with negative first-half free cash flow and no offsetting asset; Warrior's was a $1.02 BILLION construction programme that is now finished and producing - Q2 free cash flow was positive $103.4M with capex already down to $28.9M in the quarter from $94.3M a year earlier. So the trough flag points in a defensible direction here for a reason the flag itself does not know. What is NOT visible is any evidence about the forward met coal price, and that is the whole bear case.
- Left unresolved: The met coal price. I have no edge on the premium low-vol HCC index and neither the flag nor my override tells me anything about it. That single input swings EBITDA per ton by a factor of nearly two on the last twelve months' evidence, which is far wider than the 4-5% by which my fair value differs from the market's. That is why this is no_edge and not a call.

**Key risks.** A single-commodity, single-basin producer with no control over the premium low-vol HCC index; The 45X Advanced Manufacturing Production Tax Credit is inside the reported cash cost per ton and is a policy input, not an operating one; Three longwall moves before year-end will depress reported Q3/Q4 volumes and invite a misreading of the ramp
**Watch for.** FY2027 capital and cost guidance - the first clean look at Warrior in steady state post-Blue Creek; Realised price per ton against the HCC index in Q3/Q4; Any change to the 45X credit's applicability to metallurgical coal

**Data quality.** One flag, `possible_trough_cycle_base_newest_fcf_0.22x_oldest`, and I treated it as a live objection rather than advice - LESSONS.md records that its advisory sentence points the wrong way on cyclicals. Here the flag's DIRECTION happens to be defensible, but not for the reason the flag gives: the depressed 2025/H1-2026 free cash flow is a completed $1,022.9M growth capital programme, verified against the Q1 and Q2 press releases, not a price trough. The base is nevertheless wrong in both directions and I overrode it - $383.9M is the mean of a super-cycle year and two construction years. Beta 1.09 with R-squared 0.178 is our own regression and adequate for a met coal producer, so the WACC of 10.6% is not a defect on this name. Share count is dated 2026-08-03 and the balance sheet 2026-06-30; no acquisition, financing or equity issuance sits between them. Enterprise value of $5.43B against a $5.57B market cap reconciles to the disclosed $302.3M of cash and low debt (3% debt weight), so the EV is sound. Nothing here is a data artifact; the residual uncertainty is the coal price, which is an honest uncertainty rather than a bug.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1691303/000119312526335017/hcc-ex99_1.htm
- https://www.sec.gov/Archives/edgar/data/1691303/000119312526335324/hcc-20260630.htm
- https://www.sec.gov/Archives/edgar/data/0001691303/000119312526197165/hcc-ex99_1.htm
- https://www.fool.com/earnings/call-transcripts/2026/08/12/warrior-met-coal-hcc-q2-2026-earnings-call-transcript/
