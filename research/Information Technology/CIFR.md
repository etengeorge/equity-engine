# CIFR — CIPHER DIGITAL INC
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-11 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $15.94
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Cipher is being valued on gigawatts, not on earnings. In the week before the screen it announced development of natural gas lateral pipelines to support 2.5 GW of BEHIND-THE-METER generation across its Texas high-performance-computing sites — a route to power that bypasses the ERCOT interconnection queue for more than 55% of its pipeline while limiting direct generation capital expenditure, and Rosenblatt kept a $30 target on it. It also received Batch Zero conditional classifications alongside the other former miners, and benefits from the PUCT transmission approval in West Texas. The bull case is simple and does not require any trailing multiple to work: in a market where the binding constraint on AI compute is interconnected power, a company with 2.5 GW of behind-the-meter generation in development owns the scarce input. At $15.94 for a $6.6 billion market capitalisation with $611 million of daily dollar volume, the marginal buyer is trading that scarcity.

**What changed.** Power strategy and rates, not financials. (1) 2026-09-03/04: Cipher began development of natural gas lateral pipelines supporting 2.5 GW of behind-the-meter generation across its Texas HPC sites; the shares rose 10-12% on the announcement and Rosenblatt maintained a $30 target, noting the strategy could power more than 55% of the pipeline while limiting direct generation capital expenditure. (2) 2026-09-04: ERCOT sorted Batch Zero large-load projects, with CIFR among those receiving provisional classifications. (3) 2026-09-01: PUCT transmission approval in West Texas. (4) 2026-09-01/03: CIFR and Applied Digital fell together as the 10-year Treasury yield reached 4.79% — the clearest possible statement that these are duration assets. (5) The stock fell 30.6% in August and rebounded in September; it is -24.2% over 63 days but +72.9% over twelve months. Last financial filing was the Q2 10-Q on 2026-08-04.

**Base case.** I will not supply one. There is no usable FCFF base, EBITDA is negative, and the multiples table returns negative implied equity values on both revenue-based rows. Inventing a growth rate would be manufacturing a valuation the model has correctly declined to produce.

**Devil's advocate.**
- Strongest counter: The strongest counter to refusing is that one row of this table is NOT negative and is not obviously nonsense: price to tangible book gives $2.98 to $12.60 against a $15.94 price, on a 158-name cohort, and says the stock trades at 13.6x tangible book against a cohort median of 5.2x. On the only multiple whose denominator is a real balance sheet, Cipher is expensive. Refusing to say so could be read as hiding behind the tooling.
- What would prove it: Signed power and hosting contracts against the 2.5 GW, with megawatts, counterparties, tenor and rates — and the capital expenditure and financing plan for the pipelines. Those turn a development announcement into a cash flow.
- Already visible today: Only the announcement, not the contracts. And the financing question is already visible and large: $172.5 million of 1.75% convertible notes due 2030, $1,300.0 million of 0.00% convertible notes due 2031, and a $200 million revolving credit facility entered in March 2026 with a springing maturity tied to the 2030 notes. A 2.5 GW gas build is not funded out of negative EBITDA, so the equity story and the financing story are the same story. The 10-year at 4.79% moving this stock 4% in a session is the market saying the same thing.
- Left unresolved: The capital cost of 2.5 GW of behind-the-meter generation and how it will be funded, and whether any of the pipeline is contracted. I obtained neither, so I cannot assess whether the announcement is worth anything approaching the $6.6 billion market capitalisation. The engine's `speculative_cost_of_debt` flag is also unresolvable by construction here: a 0.00% coupon convertible's true cost is its embedded option value, which no coupon-based WACC can capture.

**Key risks.** Refusing to model this is not a judgment that it is cheap — at 13.6x tangible book against a 5.2x cohort median it may be very expensive and I decline to put a number on it; $1.47 billion of convertible notes, of which $1.3 billion carries a 0.00% coupon and is therefore invisible to the interest-coverage detector; The $200 million revolver has a springing maturity tied to the 2030 convertible notes; Beta 2.5 on a pure duration asset: the shares moved 4% on the 10-year reaching 4.79%, and the Fed is expected to raise on 16 September; 2.5 GW of behind-the-meter generation is an announcement, not a contract or a financing plan
**Watch for.** Signed hosting or power contracts against the 2.5 GW with megawatts, counterparties and tenor; Capital expenditure and financing plan for the gas lateral pipelines; Final ERCOT classification beyond the provisional Batch Zero designation; Any further convertible issuance, and the 2030 notes' springing-maturity trigger on the revolver

**Data quality.** Two flags, and the multiples table fails the LESSONS.md refusal test on the decisive rows. (1) `negative_ebitda_valued_on_revenue_or_gross_profit_only` with no usable FCFF years: the reverse DCF is entirely n/a. (2) The ev_sales and ev_gross_profit rows both return NEGATIVE implied equity values at every percentile (-$10.30 to -$7.50 and -$9.87 to -$6.72), while p_tbv returns $2.98 to $12.60 — rows straddling the price in opposite directions AND a negative row AND an explicitly UNRANKED cohort. That is all three RIOT/EPRT refusal conditions at once, so the blended -$4.09 and the -125.7% gap should be disregarded entirely. (3) `speculative_cost_of_debt_at_46%_debt_weight_wacc_unreliable` is correct and is worse than the flag knows. From the 10-Q the capital structure is $172.5 million of 1.75% convertible notes due 2030, $1,300.0 million of 0.00% convertible notes due 2031 (carried at $885.9 million after a $414.1 million equity-component discount), and a $200 million revolver. A zero-coupon convertible's economic cost is its option value, not its coupon, so no coupon-derived cost of debt can be right — and it is also invisible to the interest-coverage detector in LESSONS.md for exactly the same reason the LGND notes were. (4) Not flagged and worth noting: the brief's entity name reads 'CIPHER DIGITAL INC' while the extract and filings use the Cipher Mining CIK 1819989; the company appears to have rebranded within the window. I did not chase whether that affects any concept lookup.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- data/adhoc/CIFR/2026-05-05-10-Q-cifr-20260331.htm.txt (convertible note and revolver terms; fetched via adhoc-fetch)
- https://blockspace.media/insight/cipher-natural-gas-generation-plan-ercot/
- https://blockspace.media/short/cipher-digital-plans-2-5-gw-worth-of-gas-pipelines-here-are-the-sites-most-likely-to-benefit/
- https://finance.yahoo.com/technology/ai/articles/applied-digital-cipher-just-sank-195427638.html
- https://blockspace.media/insight/ercot-sorts-batch-zero-large-load-projects/
- https://www.fool.com/investing/2026/09/04/why-cipher-digital-stock-plummeted-306-last-month/

**Ingestion notes.** no usable final_growth
