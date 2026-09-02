# SLAB — SILICON LABORATORIES
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-02 — NO_EDGE (conviction: high)

- **Verdict:** no_edge · price $219.12 · fair value $53.77 · gap -75.5%
- **Growth:** market implies +48.0%, analyst says +5.0% (delta -43.0%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 9.0% | 10.0% | 11.0% | 12.0% | 13.0% |
|---|---|---|---|---|---|---|
| bear | +0.0% | $55.58 | $49.89 | $45.45 | $41.90 | $38.99 |
| base | +5.0% | $66.64 | $59.40 | $53.77 | $49.26 | $45.58 |
| bull | +10.0% | $79.87 | $70.76 | $63.68 | $58.03 | $53.41 |

At the point WACC of 11.0%: bear -79.3%, base -75.5%, bull -70.9%
Across the whole grid the gap ranges -82.2% to -63.6% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** There is no cash-flow case to steelman. Silicon Labs agreed on 2026-02-04 to be acquired by Texas Instruments for $231.00 per share in cash, an all-cash deal at roughly $7.5B enterprise value, unanimously approved by both boards and expected to close in the first half of 2027 subject to regulatory approval and a shareholder vote. At $219.12 the stock is trading at a 5.4% gross discount to the deal price. That discount, not any view on IoT connectivity growth, is what sets the price: it is the market's estimate of deal risk and the time value of money over roughly nine months to close.

**What changed.** The company suspended forward guidance because of the pending TI acquisition. Q2 2026 (reported 2026-08-11) revenue $228M, up 18.3% year over year, with Industrial & Commercial $135M (+23%) and Home & Life $93M (+12%); GAAP net loss $10.6M, non-GAAP net income $23.8M ($0.71/share). Underlying IoT demand is recovering, but none of it is priceable while a fixed cash price is on the table.

**Base case.** A five-year FCFF growth rate is the wrong question for this security and I am recording one only because the schema requires it. The payoff is a fixed $231.00 in cash on a date, not a stream of cash flows. If the deal closes, the fundamental growth rate is irrelevant to the holder; if it breaks, the relevant starting point is the unaffected price, which was roughly 69% below the deal price ($137), not today's $219.12. Any DCF run on today's price is measuring the merger spread and calling it a growth expectation.

**Devil's advocate.**
- Strongest counter: The counter is that I am dismissing the model's output rather than testing it, and the model might still be telling me something: it says the price implies +48% FCFF growth (+75% with stock compensation expensed), which would be a genuine warning if SLAB were a standalone company. If the deal breaks on antitrust grounds — a real possibility given both parties sell embedded wireless connectivity into overlapping industrial and consumer sockets — then that standalone valuation becomes the live one immediately, and it says the business is worth far less than $219. So the DCF is not irrelevant; it is the downside case, and it is severe.
- What would prove it: The regulatory calendar: second-request or Phase 2 filings in the US, EU and China, and whether TI is required to divest anything. A widening spread would price rising break risk.
- Already visible today: Yes, and it points the other way for now. The 5d/21d/63d returns are +0.3%/+0.5%/+0.2% — the price has been pinned essentially flat for a quarter, which is the signature of a market that regards the deal as very likely to close. A market pricing real break risk would show a widening, volatile spread. I did not find any reported regulatory objection.
- Left unresolved: I could not establish the current status of the regulatory reviews, the outside date in the merger agreement, or whether a break fee exists. I did not read the DEFM14A. That is the document that would size the downside properly, and I did not fetch it because it does not change the verdict — no_edge holds whether break risk is 3% or 15%.

**Key risks.** Antitrust review of TI's largest acquisition in fifteen years; a break returns the stock toward its ~$137 unaffected price, roughly -37%; Merger arbitrage is a different discipline from valuation and is not what this engine screens for; The screen will keep flagging this name as -81% 'rich' every day until it delists, because nothing in the model knows a deal exists
**Watch for.** Regulatory clearance or a second request in any of the US, EU or China reviews; The shareholder vote on the merger; Any widening of the spread beyond ~8%, which would mean the market has started pricing real break risk

**Data quality.** Both flags in the brief are real but immaterial to the verdict. Stock compensation at 57% of the FCFF base and the trough-cycle flag (newest FCF 0.46x oldest) would both matter for a standalone valuation; neither matters when the price is a fixed cash number. The important data-quality point is one the brief cannot raise: no field in this engine records that a company is subject to a definitive cash merger agreement, so the reverse DCF is being run on a price that is not a market opinion about cash flows. This is a repeatable class of error — any Russell 2000 name under an announced cash deal will screen as extremely rich and consume a rotation slot for no reason.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.ti.com/about-ti/newsroom/news-releases/2026/2026-02-04-texas-instruments-to-acquire-silicon-labs.html
- https://investor.silabs.com/news-releases/news-release-details/texas-instruments-acquire-silicon-labs
- https://www.cnbc.com/2026/02/04/texas-instruments-to-buy-chip-designer-silicon-laboratories.html
- https://news.silabs.com/2026-08-11-Silicon-Labs-Reports-Second-Quarter-2026-Results
- https://www.sec.gov/Archives/edgar/data/1038074/000103807426000027/slab-20260811q2earningsrel.htm
