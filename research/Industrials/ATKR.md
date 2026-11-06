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

## 2026-11-06 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $94.96
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** There is no market opinion about Atkore's cash flows to steelman, because Atkore no longer trades. Prysmian S.p.A. completed its acquisition on 2026-10-19 at $95.00 per share in cash under the Agreement and Plan of Merger dated 2026-08-02; Atkore is now a wholly owned subsidiary of Prysmian, has notified the NYSE, requested delisting of its common stock and intends to terminate its Exchange Act registration. The $94.96 the engine priced is a 20-day-stale frozen quote four cents below the deal consideration, and the 5d/21d returns of +0.1%/+0.5% are the tape of a security that has stopped trading, not a market view.

**What changed.** Everything, and exactly as the 2026-09-21 pass on this name predicted. That pass recorded no_model on a pending all-cash deal and put 'delisting, at which point the name should leave universe.csv' on its watch list. The deal closed on 2026-10-19 and the 8-K of that date carries items 1.02, 2.01, 3.01, 3.03, 5.01, 5.02, 5.03 and 9.01 — termination of a material agreement, completion of acquisition, delisting notice, material modification to rights, change in control, departure of officers and amendment of the articles. That is the complete APGE completed-acquisition signature, filed in one document. Andrea Pirondini was appointed President and CEO and Prysmian expects Atkore to be fully consolidated from November 2026.

**Base case.** No FCFF growth rate is supplied because none is operative: the equity has been extinguished for cash. Recording a fair value would be publishing a number for a security that cannot converge to it. For completeness the engine's standalone figure is also wrong on its own terms, and in two ways it did not raise. First, `interest_expense` is absent from the extract entirely (None against $760.2M of recorded total debt), so the $427.9M FCFF base carries no after-tax interest add-back at all — the CON defect. Second, `ebit` reads $23.173M against revenue of $2,850.4M, i.e. 0.81% of revenue, which fails the HP missing-concept test; the newest reported year is a net LOSS of $15.2M. The base is the mean of fiscal 2023-25 cfo-less-capex of [$588.7M, $399.2M, $295.7M], a monotonic decline out of the steel/PVC conduit super-cycle, against revenue that has fallen from $3,913.9M to $2,850.4M.

**Devil's advocate.**
- Strongest counter: That refusing a second time is mechanical, and that the brief's own flags point at a live cyclical question worth answering: `possible_trough_cycle_base_newest_fcf_0.50x_oldest` invites the view that the base is a trough and the business is worth more than $95.00, which would mean Atkore's board sold cheap and the comparison is still instructive for the rest of the electrical-products cohort. The AI-data-centre demand story in this name's own news feed (2026-09-20) supports that reading.
- What would prove it: Whether Atkore common stock still trades and settles. If a Form 25 and Form 15 have been filed and the NYSE has suspended trading, no amount of cyclical analysis produces an investable claim.
- Already visible today: Yes, decisively, and it defeats the counter. The 2026-10-19 8-K carries item 3.01 together with items 2.01 and 5.01 — the ACHR false-positive test is passed, because this is not a de-SPAC warrant expiry but a delisting filed alongside a completed acquisition and a change of control. Prysmian's own press release states the shares will no longer be traded on the NYSE. The adhoc-fetch dispatch for ATKR returned 'no CIK for ticker' and zero documents, which is itself corroboration: the registrant is being deregistered. And the flag reads backwards anyway — the series [$588.7M, $399.2M, $295.7M] newest-last is a decline out of a peak, so the three-year mean OVERSTATES current generation. The counter fails on both limbs.
- Left unresolved: The exact delisting effective date. I could not retrieve the Form 25 or Form 15, so I cannot say on which session the shares stopped trading — only that trading had stopped, which is all the verdict requires.

**Key risks.** This is not a valuation and carries no investment risk: the equity has been acquired for cash and the ticker is being deregistered; The engine will re-rank ATKR as cheap every session until the name is removed from universe.csv, because nothing in the selection path reads a completed merger; The standalone FCFF base is an artifact of the 2022-23 conduit super-cycle and would misprice the name even absent the deal, and it carries no interest add-back because interest_expense is None
**Watch for.** Removal of ATKR from universe.csv — this is the action item, not a market event; Form 25 and Form 15 on EDGAR confirming the delisting and deregistration dates

**Data quality.** Two flags raised and a third defect unflagged. `stale_price_20.0d` is the material one and the engine does not act on it: a price 20 sessions old on a name whose 5d and 21d returns are +0.1% and +0.5% is a frozen quote, and together with items 2.01/3.01/5.01 it is the APGE signature the 2026-09-07 lesson asked to be gated before selection. `possible_trough_cycle_base` is both wrong (the series is a decline out of a peak, so the mean overstates) and irrelevant. UNFLAGGED: `interest_expense` is None against $760.2M of total debt (the CON defect, fifth form of the interest-expense family), so the base has no add-back; and `ebit` of $23.2M is 0.81% of revenue, below the HP 1% missing-concept threshold. `fundamentals_age_days` is 402 with fy_end 2025-09-30. The share count itself is sound (33,772,550 from the dei cover-page concept, dated 2026-07-31). Confirmed from the 8-K item list on the face of the brief plus Prysmian's own completion release; the adhoc-fetch returned no documents because the CIK is being deregistered.

*Horizon: 6 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1666138/000166613826000041/atkr-20261019.htm (8-K 2026-10-19, items 1.02/2.01/3.01/3.03/5.01/5.02/5.03/9.01 — completion, delisting, change in control)
- https://www.prysmian.com/en/media/press-releases/prysmian-completes-atkore-acquisition-to-accelerate-growth-as-an-electrical-solutions-provider
- https://www.sec.gov/Archives/edgar/data/0001666138/000114036126035981/ny20080616x2_defm14a.htm (DEFM14A — merger proxy)
- research/ATKR prior verdict 2026-09-21 (no_model, price $94.32, which nominated delisting as the watch item)
- data/adhoc/ATKR/index.json ('no CIK for ticker' — zero documents returned)

**Ingestion notes.** no usable final_growth
