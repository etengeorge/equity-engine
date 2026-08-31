# CRNX — CRINETICS PHARMACEUTICALS
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-08-31 — NO_EDGE (conviction: high)

- **Verdict:** no_edge · price $84.84
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** There is no valuation case to construct: the price is a contract. On 2026-07-06 Vertex agreed to acquire Crinetics for $85.00 per share in cash (~$10B equity value). At $84.84 the stock trades 0.19% below the deal price, which is a merger-arbitrage discount for a few weeks of closing risk, not an opinion about paltusotine's cash flows. The screen correctly could not model the name (no positive normalized FCFF: PALSONIFY only launched after its September 2025 FDA approval and did $24.0M of net product revenue in Q2 2026), but the reason there is no edge has nothing to do with that.

**What changed.** Everything that matters happened after the last 10-K. FDA approved PALSONIFY (paltusotine) for acromegaly in September 2025; EMA cleared it in 2026; Q1 2026 revenue was ~$10.7M and Q2 2026 net product revenue $24.0M. On 2026-07-06 Vertex agreed to acquire the company at $85.00/share cash. HSR waiting period expired 2026-08-12; Austrian, German and Australian antitrust clearances obtained by late August. The 2026-08-28 8-K (item 5.07) is the special meeting at which shareholders voted on the merger; closing was guided to early September 2026.

**Base case.** I decline to state a standalone growth rate. The equity's payoff between now and closing is $85.00 in cash or, if the deal breaks, an unknown price well below today's. Neither is a function of a five-year FCFF growth assumption, and producing one would be dressing a 3-week arbitrage spread as a valuation.

**Devil's advocate.**
- Strongest counter: The counter to 'no edge' is that a 0.19% spread three weeks from closing is actually a very high annualised return (~3-4% annualised at a two-week close, more if it closes sooner), and that an all-cash strategic deal with HSR expired, three foreign clearances in hand and a completed shareholder vote is about as close to riskless as public equity gets. On that reading the engine should say 'cheap' — you are being paid a positive spread for near-certain closing.
- What would prove it: The merger closing on schedule in early September at $85.00. Conversely, a second-request, a foreign regulator holding out, or a financing or MAC dispute would prove the spread is compensation for real risk.
- Already visible today: The evidence for near-certain closing is already visible: HSR expiry 2026-08-12, Austria/Germany/Australia cleared, an 8-K on 2026-08-28 recording the shareholder vote, and Vertex funding it with cash. I could not confirm the vote's outcome from a primary source — the 8-K itself is unreadable from this runtime — but a company does not schedule and file item 5.07 for a vote that fails without a separate announcement, and I found none.
- Left unresolved: Whether merger-arbitrage spreads are inside this engine's mandate at all. This system exists to find gaps between intrinsic value and price on a 12-36 month horizon; a 3-week event spread is a different product with different risk. I am recording no_edge because capturing 0.19% is not what this engine is for, not because the spread is unattractive. I also could not read the merger agreement, so I cannot speak to termination fees or the break-price.

**Key risks.** Deal break on an unanticipated regulatory or litigation objection would reprice the stock to a standalone value far below $85 — the pre-announcement 52-week high was $57.99; Shareholder suits challenging the merger disclosures were filed; these normally delay rather than block, but I could not read them; If the deal closes, the position simply ceases to exist as cash — there is nothing to hold
**Watch for.** Closing of the Vertex merger in early September 2026 — after which this ticker should be removed from the universe rather than re-screened; Any 8-K disclosing a termination, extension, or amendment of the merger agreement

**Data quality.** The two flags raised (negative_fcf_year_in_window, nonpositive_normalized_fcff) are correct and are simply what a company one year into its first product launch looks like; they are not errors. I resolved nothing by reading filings because SEC egress is blocked from this runtime — every fact above comes from secondary sources, including the fact of the shareholder vote. That is the reason I did not raise conviction on the deal mechanics themselves. Separately: this name should arguably be dropped from the universe on close, and the engine has no mechanism to do that.

*Horizon: 2 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://news.vrtx.com/news-releases/news-release-details/vertex-acquire-crinetics-pharmaceuticals
- https://crinetics.com/press-releases/crinetics-pharmaceuticals-reports-second-quarter-2026-financial-results-and-provides-business-update/
- https://www.tradingview.com/news/tradingview:0ff9b0ceee246:0-vertex-to-acquire-crinetics-after-hsr-clearance-closing-expected-early-sept/
- https://www.investing.com/news/sec-filings/crinetics-pharmaceuticals-merger-with-vertex-pharmaceuticals-advances-after-regulatory-clearances-93CH-4860772
- https://www.tipranks.com/news/company-announcements/crinetics-nears-shareholder-vote-on-vertex-merger

**Ingestion notes.** no usable final_growth
