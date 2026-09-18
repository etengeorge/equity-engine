# XMTR — XOMETRY CLASS A
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-18 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $95.26
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Xometry is an AI-matched marketplace for custom manufacturing, and the market is paying for a two-sided network approaching profitable scale. Second-quarter 2026 revenue was $229 million, up 41% year over year, adjusted EBITDA was POSITIVE $14.1 million against a $10.2 million improvement year over year, and the net loss attributable to common stockholders narrowed to $5.3 million. A marketplace that has just crossed into positive EBITDA while growing above 40% is priced on the slope, not the level, and a 6x multiple of revenue is an ordinary price for that combination. The stock is up 86% over the last year and 12.3% in the last five sessions.

**What changed.** The most recent 10-Q (2026-08-04, for 2026-06-30) shows 55,562,067 Class A and 1,475,311 Class B shares outstanding — 57,037,378 in total — and adjusted EBITDA that has turned positive. Both contradict inputs the model is still using. No 8-K under items 1.01, 2.01 or 3.02 in the last two quarters other than the 2026-05-08 item 3.02; there is no acquisition or financing that changes the story.

**Base case.** Normalized FCFF is nonpositive and the model returns n/a for the base, the enterprise value and the implied growth at every WACC. There is no discounted-cash-flow answer to give, and inventing one would be exactly the refusal the engine exists to make.

**Devil's advocate.**
- Strongest counter: The multiples table is unusually well-behaved for a refusal: all THREE rows — ev_sales, ev_gross_profit and p_tbv — point the same way and the blended midpoint is $29.24 against a $95.26 price, a 69% gap. Three independent multiples agreeing is corroboration, and refusing to use them discards the only quantitative signal on the name.
- What would prove it: That the three rows are independent — i.e. that they do not all divide by the same denominator.
- Already visible today: Yes, and it defeats the counter outright. All three rows are per-share values derived from the same market capitalisation and the same share count, and that share count is 871 days stale. The engine's implied ~46.2M shares (a $4.4B market capitalisation at $95.26) is against an actual 57,037,378 shares from the 2026-06-30 10-Q cover — 19% too low, understating market capitalisation by roughly $1.0 billion. This is the MXL rule verbatim: three rows agreeing is not corroboration when all three divide by the same wrong denominator. The brief also states the cohort is NOT RANKED — too few comparable Industrials names — which disqualifies the table a second time, and the `negative_ebitda_valued_on_revenue_or_gross_profit_only` flag is itself stale, since Q2 2026 adjusted EBITDA was positive $14.1M.
- Left unresolved: What Xometry is worth. Correcting the share count makes every multiples row LOWER per share, not higher, so the correction does not point toward cheapness — but a disqualified table cannot be used in either direction, so I record no number.

**Key risks.** Share count 871 days stale: 57,037,378 actual against the engine's implied ~46.2M, understating market capitalisation by roughly $1.0 billion and disqualifying all three multiples rows; The `negative_ebitda` flag is out of date — adjusted EBITDA was positive $14.1M in Q2 2026; Dual-class structure (Class A plus Class B) is exactly the population where the stale-share-count bias concentrates; Beta 2.12 with R-squared 0.235 gives a 16.4% WACC, which would dominate any DCF even if a positive base existed
**Watch for.** A full year of positive adjusted EBITDA and the first positive cash from operations less capital expenditure — the condition for this name becoming modellable; Whether the engine refreshes the share count from the next 10-Q cover page

**Data quality.** Five flags raised, and the decisive one is `share_count_871d_stale_market_cap_unreliable`. I resolved it directly against the 2026-06-30 10-Q cover: 55,562,067 Class A plus 1,475,311 Class B. Per the WHD rule of 2026-09-15, a raised stale-share-count flag disqualifies the multiples table wholesale however well its rows agree, and the unranked cohort disqualifies it independently. Recording no_model is NOT a judgment that Xometry is expensive; the corrected share count happens to push the comparables lower, and I am declining to use them either way.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1657573/000119312526332776/xmtr-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1657573/000119312526331547/xmtr-ex99_1.htm

**Ingestion notes.** no usable final_growth
