# SND — SMART SAND INC
*Energy · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-04 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $5.35
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Smart Sand is a Northern White frac sand producer that has just had the best quarter in its history, and the market has repriced it accordingly — the stock is up 201% over twelve months. Q2 2026 tons sold were ~1,864,000 (+31% year on year, +25% sequentially) and adjusted EBITDA was $18.7M against $3.8M in Q1 2026 and $7.8M in Q2 2025. The price says: this is a small, structurally challenged Northern White producer competing against in-basin sand, whose earnings swing by 5x from quarter to quarter, and which is being valued off a peak quarter. At $5.35 the market is paying roughly 3.5x an annualised peak EBITDA and considerably more than that on any through-cycle number — that is a normal, not a depressed, multiple for a business with this volatility.

**What changed.** Q2 2026 (2026-08-11): record quarterly volumes and revenue, adjusted EBITDA $18.7M, net income $10.2M ($0.26/share), and management's own framing was 'one of the best quarters in the Company's history'. H1 2026 adjusted EBITDA is $22.5M in total, i.e. Q1 contributed $3.8M — the swing between two consecutive quarters is 5x. Special dividend of $0.10/share declared 2026-07-16, paid 2026-08-12; ~$12.1M of capital returned year to date via buybacks and dividends. On 2026-09-01 (8-K filed 2026-09-03, items 1.01/2.03) the company entered Amendment No. 2 to its First-Citizens credit agreement, raising total revolving commitments by $20M to $50M and extending the term to 2031, with a $20M sublimit against the Oakdale, Wisconsin facility. That is a commitment increase, not a drawdown — it does not change enterprise value today.

**Base case.** Northern White frac sand is a share-loss business at the industry level: in-basin Permian sand has taken structural volume from Wisconsin-origin sand for a decade, and the economics of hauling sand from Wisconsin only work when basin supply is tight. Smart Sand has offset that by taking share, adding logistics and terminal services, and buying distressed assets — its revenue series runs [$122M, $127M, $256M, $296M, $311M, $330M] over six years. The engine's naive baseline of +22% is that series' CAGR measured from the 2020-21 COVID trough, which is not a growth rate, it is a recovery. Forward, I underwrite roughly flat volumes with modest logistics mix improvement: 2% FCFF growth. I would not underwrite more from a base that is itself a record quarter.

**Devil's advocate.**
- Strongest counter: The strongest case against my dismissal is that the +296% gap might survive a corrected discount rate. Smart Sand is debt-light (total debt $14.7M against $238M of book equity), returns cash, trades at roughly book value (P/TBV 1.09), and has just demonstrated 1.86Mt of quarterly throughput — if that is the new normal rather than a peak, annualised EBITDA near $60-75M against a $258M enterprise value is genuinely cheap and no discount-rate correction closes that gap.
- What would prove it: Q3 and Q4 2026 volumes holding above 1.7Mt with contribution margin per ton stable — two consecutive quarters, because one is what we already have. A single additional quarter near $18.7M of adjusted EBITDA would move this from a peak to a run rate.
- Already visible today: No — the opposite is visible, and it is the reason I am not persuaded. Q1 2026 adjusted EBITDA was $3.8M. Q2 2025 was $7.8M. The $18.7M quarter is one observation surrounded by observations a fifth its size, and the company itself called it a record. On the discount rate the evidence is also one-sided: the screen's 6.32% WACC comes from a beta of 0.31 with an R-squared of 0.039, and at any defensible beta for a frac sand microcap the market is already implying growth, not discounting it.
- Left unresolved: I could not establish what fraction of Q2's volume was contracted versus spot, which is what would distinguish a durable share gain from a one-quarter completion surge. The 10-Q was fetched but I did not find a contracted-volume disclosure that settles it.

**Key risks.** Northern White sand is losing structural share to in-basin Permian supply; Quarterly adjusted EBITDA swung 5x between Q1 and Q2 2026 — there is no stable earnings base to value; Completion activity is levered to oil price and E&P capital discipline; The stock is up 201% in twelve months; the re-rating has already happened; $1.7M average daily dollar volume — position size cannot be exited into a downturn
**Watch for.** Q3 2026 tons sold and adjusted EBITDA — anything near 1.8Mt / $18M would materially change this view; Any drawdown on the enlarged $50M revolver, which would be the tell for an acquisition or for working-capital stress; Permian in-basin sand pricing, which is the variable that decides Northern White's relevance

**Data quality.** I have deliberately left final_growth null, and that is the finding. The +296% gap is manufactured by the discount rate, and the schema has no field that can correct it. The screen assigns beta 0.31 with an R-squared of 0.039 (source `yahoo_rescaled`, raw Yahoo 0.33), producing a cost of equity of 6.48% and a WACC of 6.34% for a $227M-market-cap frac sand producer whose stock tripled in a year. Re-running the engine's own reverse DCF across defensible betas: at 0.31 the market implies -7.6% growth (the screen's number); at 0.90 it implies +4.0%; at 1.20, +8.7%; at 1.40, +11.6%; at 1.60, +14.4%. In other words, at any beta a reasonable person would assign to this business, the market is already paying for growth and the stock is not cheap — at beta 1.4 the fair value at my 2% base case is roughly $3.30 against a $5.35 price. Because record.py reprices from the screen's stored beta, supplying a final_growth here would publish a fair value built on the 6.34% WACC I have just shown to be indefensible, so I have supplied none. This is the BETA_MIN_R2 defect documented in research/LESSONS.md, and SND is a textbook instance: worst-fit bucket, sub-1.0 beta, large positive gap, Energy sector. Second flag, resolved and IMPORTANT to record as a false alarm: the brief's EBITDA of -$2.07M is wrong. The extract's dep_amort_series reads [$2.39M, $2.60M, $2.54M] for a company with mines, plants and terminals — the concept picked up is a fraction of true depreciation, so EBIT + D&A understates EBITDA by an order of magnitude. Actual Q2 adjusted EBITDA was $18.7M. I initially read the negative EBITDA as evidence the business was losing money; it is an extraction error and I withdraw that reading. Third flag, `possible_peak_cycle_base_newest_fcf_4.1x_oldest`: CONFIRMED by the company's own words. Fourth, `stock_comp_is_20%_of_fcff`: real; expensing it moves implied growth from -7.5% to -2.7% at the screen's WACC and I would expense it.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.prnewswire.com/news-releases/smart-sand-inc-announces-second-quarter-2026-results-302848832.html
- https://www.sec.gov/Archives/edgar/data/0001529628/000152962826000096/a2026q2exhibit991.htm
- https://www.sec.gov/Archives/edgar/data/0001529628/000152962826000104/snd-20260901.htm
- data/adhoc/SND/2026-08-11-EX-99.1.txt (fetched via adhoc-fetch)
- data/adhoc/SND/2026-08-11-10-Q-snd-20260630.htm.txt
- data/adhoc/SND/2026-09-03-8-K-snd-20260901.htm.txt
- research/LESSONS.md (BETA_MIN_R2 entry, 2026-09-03)

**Ingestion notes.** no usable final_growth
