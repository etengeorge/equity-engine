# TXG — 10X GENOMICS CLASS A
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-02 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $59.98
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** 10x Genomics is up 328% in twelve months because the market believes the instrument cycle has turned. Q2 2026 revenue was $151M including a $1.6M Takara settlement; management raised the 2026 outlook on strong early orders for the new Atera platform, and booked orders for Atera exceeded the 2026 target. The company also won a patent infringement verdict against Parse Biosciences in Delaware and is seeking added damages and a US injunction, which strengthens the moat around single-cell. The bull case is a platform transition: a large installed base of single-cell customers migrating to a new instrument, with consumables pull-through following for years afterward. Against a $7.7B market cap that requires the migration to be large and durable — but that is a genuine, specific mechanism, not a hope, and it is why the stock has re-rated.

**What changed.** Q2 2026 (2026-08-06): revenue $151M, or $149.4M ex-settlement, up just 3% year over year, with the year-over-year decline in instrument sales attributed to the Atera transition. The 2026 revenue outlook was raised on early Atera orders. On 2026-08-28 a Delaware jury found Parse Biosciences infringed, awarding $4.8M, with 10x seeking enhanced damages and an injunction. RBC noted on 2026-09-01 that the two franchises are pulling in opposite directions and that meaningful growth is needed in single-cell.

**Base case.** I cannot set a defensible FCFF growth rate here because there is no defensible FCFF base to grow. The three-year free cash flow series is -$63.8M, -$5.7M and $130.1M, a spread of 9.6x the mean, and the mean of $20.2M is an artefact of averaging across a sign change. Worse, stock compensation is 688% of that base: expensing it gives FCFF of -$118.7M. The single most recent year, $130.1M, is the only figure with any claim to being a run rate, and even that goes negative once the roughly $139M of annual stock compensation is treated as the real cost it is. A business that generates no cash after paying its employees is one where the DCF has nothing to discount.

**Devil's advocate.**
- Strongest counter: The counter is that no_model is the coward's answer on a name where the model actually produced a clear signal — 4th percentile of 91 Health Care peers, an -87.8% gap, and an implied growth rate the solver had to clamp at +100%. Every one of those says the price embeds expectations that essentially cannot be met, and calling that 'unmodellable' rather than 'rich' declines to make the call the evidence supports. And the qualitative picture agrees: revenue grew 3% year over year while the stock rose 328%.
- What would prove it: Whether Atera converts booked orders into recurring consumables revenue, visible in the consumables line over the next two to three quarters, and whether stock compensation moderates as a share of revenue.
- Already visible today: Some of it. Ex-settlement revenue growth of 3% is visible and is weak against a 328% share price move — that genuinely supports the counter. What is not visible is the Atera consumables ramp, which by construction lags instrument placement by several quarters, so the bull case has not yet had a chance to be falsified.
- Left unresolved: Whether $130.1M of free cash flow in the newest year is a durable turn or a working capital release. I did not fetch the 10-Q, and I should be explicit that this was a choice: even with it, the stock-compensation problem would still make the FCFF base non-positive on any honest treatment, so the verdict would not change. The counter loses on the verdict but it wins on tone — I am not calling this cheap or fairly valued, and a reader should take from this file that the model's -87.8% gap points in a direction I consider directionally right, even though I will not underwrite it as a number.

**Key risks.** Stock compensation at 688% of the normalised FCFF base — on any honest treatment the company does not generate free cash flow; Ex-settlement revenue grew 3% year over year against a 328% twelve-month share price move; The Atera platform transition depresses instrument revenue before consumables pull-through arrives, and the transition may not complete on the expected timeline; Academic and pharma research funding is the underlying demand driver and is not under the company's control
**Watch for.** Consumables revenue growth over the next two to three quarters — the test of whether Atera placements convert; Any moderation in stock compensation as a percentage of revenue; The Parse injunction ruling and enhanced damages decision; A share count update: the model is using a 2025-12-31 figure

**Data quality.** All three raised flags are correct and decisive: negative_fcf_year_in_window, lumpy_fcff_spread_9.6x_of_mean, and stock_comp_is_688%_of_fcff. Averaging -$63.8M, -$5.7M and $130.1M into a $20.2M base is arithmetic, not normalisation, and the solver clamping implied growth at +100% is the model telling you it cannot solve this. Expensing stock compensation makes the base -$118.7M and no growth rate exists at all — which is the definition of no_model, so I have recorded no fair value. There is also a flag the brief did NOT raise and should have: TXG's shares_asof is 2025-12-31, eight months stale, and every other name in today's ten carries a July or August 2026 date. A stale share count on a company issuing stock compensation at 688% of its cash-flow base understates both market capitalisation and enterprise value — probably by a low single-digit percentage here, so it does not change this verdict, but it is the stale-share-count error already recorded in LESSONS appearing again on a name where it is most likely to bite. Worth a check on how many names in the universe carry a shares_asof older than their most recent 10-Q.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://finance.yahoo.com/healthcare/articles/10x-genomics-txg-sees-strong-074449509.html
- https://finance.yahoo.com/healthcare/articles/10x-genomics-wins-patent-infringement-183800082.html
- https://www.fool.com/earnings/call-transcripts/2026/08/14/10x-genomics-txg-q2-2026-earnings-call-transcript/
- https://finance.yahoo.com/healthcare/articles/10x-genomics-needs-meaningful-apos-152229814.html
- https://finance.yahoo.com/markets/stocks/articles/5-revealing-analyst-questions-10x-074100628.html

**Ingestion notes.** no usable final_growth
