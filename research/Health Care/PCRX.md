# PCRX — PACIRA BIOSCIENCES
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-10-09 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $36.39
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** There is no consensus about cash flows to steelman: the price is an administered number. On 2026-10-08 Pacira signed an Agreement and Plan of Merger with Viatris Inc. and Peach Purchaser Sub Inc. under which Purchaser will commence a cash tender offer, within no more than 15 business days, for all outstanding shares at $36.50 per share in cash, an aggregate equity value of $1.65 billion. At $36.39 the stock trades at a 0.30% DISCOUNT to the offer. That spread, not a growth rate, is what the market is pricing: roughly 0.3% over an expected close 'by the end of 2026', i.e. a market-implied probability of completion close to certainty, against the 8-K's stated conditions (a minimum of one share more than 50% tendered, HSR expiry, and a Section 251(h) DGCL back-end merger needing no shareholder vote).

**What changed.** Everything. 8-K filed 2026-10-08 under items 1.01, 7.01 and 9.01 — the merger agreement itself — with EX-99.1 the joint Viatris/Pacira press release. Viatris acquires all outstanding shares at $36.50 cash; both boards approved; close expected by end of 2026 subject to regulatory review. The release discloses Pacira LTM revenue to 2026-06-30 of approximately $746 million and adjusted EBITDA of approximately $177 million, and names EXPAREL and ZILRETTA as the assets. Viatris says it will fund primarily from excess cash with the remainder from short-term borrowings. This 8-K is dated the same session as the screen's price date, so the entire +45.5% five-day move, the 6.8x volume and the 'filed an 8-K' signal are one event: the announcement.

**Base case.** I do not produce a base case. A company under a signed all-cash tender offer has no free-cash-flow valuation that the market is expressing; its price is the offer less a completion discount. Supplying a growth rate here would be answering a question nobody is asking.

**Devil's advocate.**
- Strongest counter: The strongest case for engaging rather than refusing is that a deal spread is itself a tradable, analysable proposition: 0.30% to an expected close inside three months is roughly 1.3% annualised, which is BELOW the risk-free rate, so the arbitrage is priced for certainty and an informed analyst could argue it is too tight given that the HSR waiting period has not yet run on a transaction that consolidates non-opioid pain management with Viatris' own fast-acting meloxicam programme — an overlap the acquirer's own press release advertises as 'synergistic'. If the antitrust risk is real, the correct verdict is 'rich', not 'no_model'.
- What would prove it: The HSR outcome: expiry of the initial waiting period versus a second request, and the tender's initial expiration date and tendered percentage once the Schedule TO and SC 14D9 are filed (due within 15 business days of 2026-10-08).
- Already visible today: Partially, and it cuts against the counter. The 8-K conditions the Offer on HSR expiry but imposes no antitrust-specific regulatory covenant that I read, and the complementarity Viatris describes is between an acute post-surgical injectable (EXPAREL), an intra-articular steroid (ZILRETTA) and an oral NSAID — adjacent rather than overlapping therapeutic forms, which is a weak Clayton Act theory. The market's 0.30% discount is the collective view of exactly that question and I have no better information than it does.
- Left unresolved: I cannot independently price the antitrust risk, and I did not read the Schedule TO or the SC 14D9 because neither has been filed yet. I also did not verify whether a go-shop or matching-rights provision exists, because no fair value turns on it: on either answer the name is not a free-cash-flow valuation.

**Key risks.** Deal break on HSR or on the minimum tender condition — downside to roughly the $25.20 pre-announcement close; The engine will keep pricing this name as a free-cash-flow opportunity, and keep ranking it in the cheapest decile of Health Care, every session until it delists; Holding past the close converts an equity position into cash at $36.50 with no further upside
**Watch for.** Schedule TO and SC 14D9 filings, due within 15 business days of 2026-10-08; HSR second request, which would widen the spread and is the only event that makes this name interesting again; An 8-K under items 2.01, 3.01 or 5.01 completing the merger and delisting the shares

**Data quality.** Both engine flags are real but irrelevant, and that is the point. `volume_6.8x_its_60d_average` IS the announcement. `stock_comp_is_34%_of_fcff_reported_cash_flow_treats_it_as_free` is a genuine defect on the $164.7M base (expensing stock comp moves the implied growth from -11.3% to -3.2%) and it no longer matters, because neither number describes the price. UNRESOLVED and more serious than either: `beta 0.24 at R-squared 0.014, marked yahoo_rescaled` gives a 7.82% WACC and a 6.55% cost of equity for a single-product specialty pharma company — the standing yahoo_rescaled defect, and it alone would have manufactured a large positive gap on this name even without the deal. The +192.1% baseline gap, the 93rd percentile of 91 Health Care peers and the -11.3% implied growth are all void.

*Horizon: 3 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- data/adhoc/PCRX/2026-10-08-8-K-tm2627240d2_8k.htm.txt (merger agreement, items 1.01/7.01/9.01, fetched via adhoc-fetch)
- data/adhoc/PCRX/2026-10-08-EX-99.1.txt (joint Viatris/Pacira press release)
- https://www.sec.gov/Archives/edgar/data/1396814/000110465926114571/tm2627240d2_8k.htm
- https://www.sec.gov/Archives/edgar/data/1396814/000110465926114571/tm2627240d2_ex99-1.htm
- https://www.benzinga.com/m-a/26/10/62253774/viatris-bets-big-on-non-opioid-painkillers-with-pacira-buyout
- data/picks.json row for PCRX (screen 2026-10-09, prices as of 2026-10-08)

**Ingestion notes.** no usable final_growth
