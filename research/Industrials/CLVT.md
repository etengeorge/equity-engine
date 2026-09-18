# CLVT — CLARIVATE PLC
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-18 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $1.90 · fair value $0.04 · gap -98.1%
- **Growth:** market implies +4.5%, analyst says -2.0% (delta -6.5%)

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 13.4% | 14.4% | 15.4% | 16.4% | 17.4% |
|---|---|---|---|---|---|---|
| bear | -6.0% | $-0.02 | $-0.50 | $-0.91 | $-1.26 | $-1.57 |
| base | -2.0% | $1.12 | $0.54 | $0.04 | $-0.39 | $-0.77 |
| bull | +4.0% | $3.17 | $2.39 | $1.73 | $1.16 | $0.66 |

At the point WACC of 15.4%: bear -147.8%, base -98.1%, bull -9.1%
Across the whole grid the gap ranges -182.7% to +66.9% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** At $1.90 Clarivate's equity is a thin, heavily levered claim on Web of Science, Derwent and ProQuest — subscription assets with high renewal rates — sitting behind $4,251.5 million of debt. The market is pricing the decline it can see: revenue fell 5.5% to $587.3 million in Q2 2026 and 3.5% to $1,172.8 million in the first half, and generative AI is a live substitution threat to exactly the citation- and IP-search workflows the company charges for. Against that, free cash flow of $365-435 million a year on a $1.2 billion market capitalisation is a ~30% equity yield, debt fell $218.4 million in the half, and management has a stated path from 4.0x net leverage to about 2.5x. A stub priced for decline that merely stabilises re-rates violently; a stub priced for decline that accelerates goes to nothing. The price is the market's estimate of that coin flip, and it has fallen 54.7% in a year taking it.

**What changed.** Two structural items, neither in the model. On 2026-07-06 Clarivate agreed to sell its Life Sciences & Healthcare segment to Altaris for $600 million — $500 million cash on completion, $25 million after the transition services agreement and a $75 million seller note — expected to close before the end of 2026, with LS&H classified as DISCONTINUED OPERATIONS from the third quarter and an expected $225-250 million non-cash goodwill impairment. The full-year 2026 outlook was reaffirmed INCLUDING LS&H: revenue $2.30-2.42bn, adjusted EBITDA $980m-$1.04bn, free cash flow $365-435 million, now expected at the LOW end because of transaction and restructuring costs taken to capture 2027 savings; net proceeds are earmarked for debt reduction. On 2026-09-17 a subsidiary commenced a cash tender offer for certain outstanding debt securities (8-K item 8.01). A director bought 900,000 shares for $1.7 million on 2026-08-18.

**Base case.** FCFF roughly flat to slightly declining. Revenue is falling 3.5-5.5%, and the Academia & Government and Intellectual Property segments that remain after the LS&H sale are the slower-growing half of the portfolio, not the faster. Against that, the company is taking real cost out — the restructuring charges depressing 2026 free cash flow are explicitly buying 2027 savings — and adjusted EBITDA of $980m-$1.04bn on $2.3-2.4bn of revenue is a 42% margin that has held while revenue fell. I net those to about -2%: cost programmes offset most but not all of a mid-single-digit revenue decline. I differ sharply from the naive +14.4% baseline, which is not a forecast of anything — it is the ProQuest acquisition of December 2021 rolling through a five-year revenue CAGR, i.e. bought revenue read as organic growth, the EFOR pattern.

**Devil's advocate.**
- Strongest counter: This is a deleveraging story and calling it no_edge misses the only thing that matters. Hold the enterprise value flat at roughly 5.3x EBITDA and pay down $365 million of debt a year: in three years debt is about $3.15 billion and the equity is worth roughly $2.15 billion against $1.2 billion today, a 79% gain, WITHOUT any improvement in the business at all. A director backed that with $1.7 million of his own money in August. The mechanism is named, dated and arithmetic, which is exactly what the standing lessons say a thesis needs.
- What would prove it: Whether adjusted EBITDA holds. The whole argument rests on the enterprise value not shrinking faster than the debt does.
- Already visible today: The evidence points the wrong way for the counter, but not decisively. Revenue fell 3.5% in the first half and 5.5% in the second quarter — decelerating, not stabilising. The LS&H sale raises $600 million for a segment being let go at a price that covers about 14% of the debt, so it is a liquidity event rather than value creation. And free cash flow is guided to the LOW end of its range. On the other side, the 42% adjusted EBITDA margin has genuinely held. I could not settle it: at -3% EBITDA decline the counter wins comfortably; at -8% with any multiple compression the equity is close to worthless. The counter did NOT win, but it stopped me recording this as rich, which is where the 97th-percentile rank and the declining revenue would otherwise have taken me.
- Left unresolved: Whether revenue decline stabilises. That single variable determines whether this equity triples or goes to zero, and nothing I could read settles it. The distribution is genuinely bimodal, which is a reason to record no_edge rather than a midpoint that describes neither outcome.

**Key risks.** The +194.3% gap and the 97th-percentile Industrials rank that won this opportunistic slot come from a +14.4% revenue-CAGR baseline that is the 2021 ProQuest acquisition, on a company whose revenue is now FALLING 3.5-5.5%; WACC of 15.4% at a 78% debt weight is set by a synthetic credit rating derived from an EBIT depressed by roughly $400 million a year of ProQuest intangible amortisation — the cost of debt it implies is far above what Clarivate actually pays, so the printed fair value is unreliable and the verdict is the output, not the number; The FCFF window includes a segment being sold: LS&H goes to discontinued operations in Q3 2026, so the base and the debt it is compared against both change; 4.0x net leverage on a declining revenue base — the denominator can fall faster than the numerator is repaid; Beta 0.72 with R-squared 0.044 is at the very bottom of the fit distribution
**Watch for.** Q3 2026 organic revenue growth for Academia & Government and Intellectual Property, reported for the first time without LS&H — the single number the thesis turns on; Completion of the Altaris sale and the actual application of the $500 million cash to debt; The outcome of the 2026-09-17 tender offer and the post-tender maturity schedule; Any evidence of AI substitution in renewal rates rather than in commentary

**Data quality.** The brief raised NO flags. Enterprise value checks out: $1.2bn of market capitalisation plus $4,251.5 million of debt from the Q2 release, less cash, reconciles to the engine's $5.3bn, so there is no missing-debt bug here. The FCFF base of $628.4 million is arithmetically sound — a three-year mean of $408.2 million plus roughly $220 million of after-tax interest on $4.25bn. The two real problems are the ranking baseline (bought revenue read as growth) and the discount rate (a synthetic rating built on an amortisation-depressed EBIT), and neither is flagged. I could not override the WACC — the schema has no field for it — so the recorded fair value understates what the model would produce at a defensible cost of capital. LS&H moving to discontinued operations in Q3 makes the entire base provisional.

*Horizon: 36 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1764046/000176404626000090/ex991q22026earningsrelease.htm
- https://www.sec.gov/Archives/edgar/data/1764046/000095010326014070/dp253474_ex9901.htm
- https://clarivate.com/news/clarivate-announces-sale-of-life-sciences-healthcare-segment-for-600-million/
- https://www.sec.gov/Archives/edgar/data/1764046/000176404626000091/clvt-20260630.htm
- https://www.fool.com/earnings/call-transcripts/2026/08/07/clarivate-clvt-q2-2026-earnings-call-transcript/
