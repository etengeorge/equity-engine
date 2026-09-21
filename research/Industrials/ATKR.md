# ATKR — ATKORE
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-21 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $94.32
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** There is no market opinion about Atkore's cash flows to steelman. On 2026-08-03 Atkore signed a definitive agreement to be acquired by Prysmian S.p.A. for $95.00 per share in ALL CASH, an enterprise value of about $3.8bn, unanimously approved by both boards, targeted to close by calendar year end 2026. At $94.32 the stock is a 0.72% gross spread to a fixed number roughly three months away — an annualised ~3% return for taking deal risk. That, and not a view on electrical conduit, is what the price is.

**What changed.** Everything. The engine ran a standalone reverse DCF on a company that has contracted to stop existing. The 8-K of 2026-08-03 (items 1.01, 7.01, 9.01) carries the merger agreement and the joint press release as EX-99.1; a further 8-K on 2026-09-15 (items 8.01, 9.01) is merger-communications traffic, and it is what triggered the 'filed an 8-K in the last few sessions' selection term. The deal followed a public strategic review announced around 2025-09-29; $95.00 is a ~30% premium to the $72.96 close of 2026-07-31 and ~57% to $60.69 pre-review.

**Base case.** No FCFF growth rate is supplied because none is operative. The equity is a claim on $95.00 of cash conditional on shareholder approval and regulatory clearance, not on five years of free cash flow. Recording a fair value here would be publishing a number the market has no reason to converge to. For completeness the engine's standalone figure is also wrong on its own terms: the $427.9M FCFF base is the mean of fiscal 2023-25 cfo-capex of [$588.7M, $399.2M, $295.7M], the tail of the steel/PVC conduit super-cycle, against an LTM EBITDA the same brief reports as $147.7M and a revenue line that has fallen from $3,913.9M to $2,850.4M. `interest_expense` is also absent from the extract entirely, so there is no add-back at all. The +123.2% gap and the 91st-percentile rank are an artifact of a closed window on a collapsed cycle, and would be wrong even if there were no deal.

**Devil's advocate.**
- Strongest counter: That refusing is lazy — a merger-arb spread is still an investable claim and I could price it. I ran that: at $94.32 against $95.00 closing by year end, the gross spread is 0.72%, roughly 3% annualised, against a ~23% downside to the undisturbed price. To make that attractive you need better than 88% confidence of closing, which is a regulatory judgment about a transatlantic combination in electrical infrastructure, not an output of a free-cash-flow model. This engine's job is finding a delta between intrinsic value and price; there is no such delta here, only deal risk, and pretending otherwise would smuggle a merger-arb bet in through a DCF.
- What would prove it: The HSR waiting period and any EU Phase I/II decision, and whether Prysmian pulls and refiles its notification — the PATK tell from 2026-09-15, which is the standard move when the agencies are preparing a Second Request.
- Already visible today: Not yet. The 8-K of 2026-09-15 is item 8.01/9.01 merger-communications traffic and the proxy statement was still pending as of the 2026-08-03 filing. I could not find a filed HSR milestone in the documents fetched.
- Left unresolved: Whether the transaction clears antitrust without remedies, and whether Atkore shareholders approve. Neither is knowable from the filings I have.

**Key risks.** this is a deal stock, not a valuation — the only material risk is deal break, which costs roughly 23%; the engine will re-rank ATKR as cheap every session until it delists, because nothing in the model reads a merger agreement; the standalone FCFF base is itself an artifact of the 2022-23 conduit super-cycle and would misprice the name even absent the deal
**Watch for.** an HSR pull-and-refile by Prysmian, or a Second Request — the tell that the 0.72% spread is mispriced; the Atkore proxy statement and the shareholder vote date; delisting, at which point the name should leave universe.csv

**Data quality.** The only flag raised was `possible_trough_cycle_base` and it is both wrong and irrelevant. Wrong: the flag reads newest-FCF-0.50x-oldest and advises that a trough base understates value, when the series [$588.7M, $399.2M, $295.7M] is a monotonic DECLINE out of a super-cycle peak, so the three-year mean OVERSTATES current generation — the AMR rule (never read the flag's recommendation on a cyclical) applying in the peak direction. Irrelevant: the name is under a signed all-cash merger agreement. Unflagged and unresolved by the engine: `interest_expense` is absent from the extract, so the FCFF base carries no add-back; and no merger detector exists. Confirmed from the primary document, not from the wire.

*Horizon: 6 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1666138/000166613826000016/atkr-20260803.htm (8-K 2026-08-03, items 1.01/7.01/9.01 — merger agreement)
- https://www.sec.gov/Archives/edgar/data/1666138/000166613826000016/atkr_991xpressrelease.htm (EX-99.1: '$95.00 per share in cash', ~$3.8bn EV, unanimous board approval, targeted close by calendar year end 2026, 30% premium to $72.96)
- https://www.sec.gov/Archives/edgar/data/1666138/000166613826000027/atkr-20260915.htm (8-K 2026-09-15, items 8.01/9.01)
- https://www.businesswire.com/news/home/20260802368964/en/Atkore-Inc.-to-be-Acquired-by-Prysmian-for-$95.00-per-Share-in-Cash
- company news in brief: Trefis 2026-08-04, StockStory 2026-08-04 (+28.1% on announcement)

**Ingestion notes.** no usable final_growth
