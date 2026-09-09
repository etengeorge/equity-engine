# BKH — BLACK HILLS CORP
*Utilities · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $74.19
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Black Hills is not being priced as a standalone discounted cash flow at all. It is nine-tenths of the way through an all-stock merger with NorthWestern Energy - the Q2 2026 release says the deal has 'only one regulatory approval remaining' and is expected to close by year-end 2026, and the company filed NorthWestern's own Q2 10-Q as an exhibit to its 2026-08-17 8-K. Underneath that, the standalone story is a regulated utility guiding $4.25-$4.45 of 2026 adjusted EPS and the upper half of a 4-6% long-term EPS growth target, with a large-load pipeline of more than 3 GW in Wyoming (Microsoft expansion, a new Meta AI data centre, 600 MW in plan by 2030) and a prospective 1.8 GW Cheyenne data centre that has already posted $377M of refundable advances against long-lead generation equipment. At $74.19 that is roughly 17x guided adjusted EPS - an ordinary multiple for a utility with an above-ordinary load-growth story.

**What changed.** Q2 2026 (2026-08-05): adjusted EPS $0.54 vs $0.38; year-to-date adjusted EPS $2.33 vs $2.24; 2026 adjusted EPS guidance of $4.25-$4.45 reaffirmed, explicitly excluding the NorthWestern merger. Wyoming Electric set four new all-time load peaks, the most recent 439 MW on 2026-07-20, up 16% year over year. The 1.8 GW generation reservation agreement was amended in July to raise refundable customer advances from $285M to $377M. 8-K of 2026-08-17 attaches NorthWestern Energy's Q2 2026 financial statements - a merger disclosure obligation, not a Black Hills event.

**Base case.** No FCFF growth rate is meaningful for this name. The base is the mean of [-$146.4M, -$24.9M, $388.8M] - two of the three years are negative, and negative free cash flow is the NORMAL and correct state of a rate-regulated utility funding rate-base growth, because the capex is the investment on which the allowed return is earned. Growing that mean at any rate values nothing.

**Devil's advocate.**
- Strongest counter: That I am hiding behind 'no_model' when a real question exists: even in a merger, the exchange ratio makes this a claim on the combined entity, and if the combined entity is mispriced then so is BKH. And the data-centre load growth is not priced into a 17x multiple - 1.8 GW in Cheyenne would be transformational rate base for a utility this size.
- What would prove it: A signed definitive agreement on the 1.8 GW project with tariff terms, plus the merger closing so that the security being valued is stable and the combined rate base and capital plan are disclosed.
- Already visible today: The customer has posted $377M of REFUNDABLE advances and the parties are still 'negotiating definitive agreements'. Refundable is the operative word: money that comes back is not a commitment. So the biggest single upside item is real but not yet contracted, which is precisely why I will not put a number on it.
- Left unresolved: I did not attempt to value the combined Black Hills / NorthWestern entity. That is a different security from the one this brief priced and it is not what a rotation slot on BKH asks.

**Key risks.** The final regulatory approval for the NorthWestern merger - the whole equity is a claim on a deal closing; Data-centre load is concentrated in a handful of counterparties in one Wyoming service territory; Heavy capex funded partly with equity; adjusted EPS growth of 4-6% depends on regulatory lag staying manageable
**Watch for.** Closing of the NorthWestern merger, expected by year-end 2026; Conversion of the 1.8 GW Cheyenne generation reservation agreement into a definitive tariff contract, or the return of the $377M of refundable advances; The combined company's first capital plan and rate-base growth disclosure

**Data quality.** Both flags - `negative_fcf_year_in_window` and `lumpy_fcff_spread_7.4x_of_mean` - are correct and together they invalidate the model rather than qualify it. The -78.0% gap and the '+20.5% implied growth' are arithmetic on a base that means nothing. The more important defect is the one nothing flagged: BKH is under a PENDING ALL-STOCK merger with NorthWestern Energy, and this is a third variant of a failure already twice in LESSONS.md. The SLAB entry covers a pending CASH merger, whose tell is near-zero dispersion across the 5d/21d/63d return windows because the price is pinned to a fixed number; the APGE entry covers a COMPLETED acquisition, whose tell is a stale price plus 8-K items 3.01 and 5.01. Neither tell fires here, and that is the point: in a stock-for-stock merger the price FLOATS with the acquirer, so BKH shows perfectly ordinary dispersion (+3.5% / +0.3% / +3.8%) and no items 2.01, 3.01 or 5.01 anywhere in the filing list. The only signal in the machine-readable data is an 8-K under item 8.01 carrying another registrant's 10-Q as EX-99.1. The engine has no way to see this, and it will keep pricing a standalone DCF on BKH every session until the deal closes. Recommend gating on that pattern before selection.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1130464/000119312526335259/bkh-20260805.htm
- https://www.sec.gov/Archives/edgar/data/1130464/000119312526354167/bkh-20260817.htm
- https://www.sec.gov/Archives/edgar/data/1130464/000119312526337444/bkh-20260630.htm

**Ingestion notes.** no usable final_growth
