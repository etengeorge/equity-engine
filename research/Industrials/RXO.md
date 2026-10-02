# RXO — RXO INC
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-10-02 — NO_MODEL (conviction: low)

- **Verdict:** no_model · price $21.36
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** RXO is an asset-light truck brokerage at the bottom of the longest freight recession in modern records, and the market is paying for the recovery rather than the trough. Q2 2026 revenue rose 25% to $1.77bn with adjusted EBITDA of $40M, above the top of guidance; truckload volume turned positive at +2% y/y and truckload gross profit per load rose 11% sequentially, the strongest sequential improvement in four years. The 2026-09-09 update went further: gross profit per load up more than 10% in August against July, better than the prior outlook, with spot at roughly 50% of full-truckload volume and contract rates phasing in higher, and Q3 truckload volume still expected up low-to-mid single digits. Brokerage earnings are enormously operationally geared - in a tightening market gross profit per load and volume rise together - so a buyer at $21.36 is paying roughly 25x trough EBITDA for a business that earned several times this in the last upcycle, with the Coyote integration cost base already absorbed.

**What changed.** Q2 2026 (filed 2026-08-06): revenue $1.77bn +25% on higher rates, fuel and the inclusion of Coyote Logistics; adjusted EBITDA $40M, above the high end of guidance; GAAP net loss $9M, a $0.05 diluted loss per share, unchanged y/y. Truck brokerage was 73% of revenue at a 10.7% gross margin. Q3 2026 adjusted EBITDA guided to $35-45M. On 2026-09-09 RXO issued an unscheduled positive brokerage update (item 7.01): August truckload gross profit per load up more than 10% against July, ahead of the prior outlook, spot around 50% of full-truckload volume through two months of the quarter, Q3 truckload volume still expected to rise low-to-mid single digits. That release is behind the +7.2% five-day move.

**Base case.** Neither of the engine's two routes produces a usable number, and the multiples route fails the standing refusal test outright. The DCF route is correctly refused: cfo_series [51, -12, 89] against capex [59, 45, 64] gives cfo-capex of [-8, -57, +25], a mean of minus $13.3M, so normalized FCFF is non-positive and no growth rate can be solved for. Correcting the unflagged null interest expense does not rescue it - the extract carries interest_expense = None against total_debt of $495M while the Q2 10-Q reports net interest expense of $18M for six months, about $36M annualised, so the after-tax add-back is roughly $27M and the corrected base is about +$14M, a rounding error against a ~$4.0bn enterprise value. The multiples route fails the RIOT/EPRT test on its face: the ev_ebitda row returns per-share values of MINUS $0.73 to $1.47 while the ev_sales row returns $27.06 to $111.59 against a $21.36 price. Rows that straddle the price in opposite directions, one of them negative, with the cohort explicitly 'not ranked', are not a valuation - and averaging them to a $26.98 blended midpoint averages a nonsense input away. REFUSING IS NOT A CLAIM THAT RXO IS CHEAP. Enterprise value is roughly $4.0bn (market cap $3.52bn plus $495M debt less $15M cash) against adjusted EBITDA annualising near $160M on the Q2 actual and Q3 guide - about 25x, with GAAP net losses of $100M and $290M in the last two years and $1.11bn of goodwill plus $432M of intangibles from Coyote. That is a full price for a cyclical recovery that has started but is two quarters old.

**Devil's advocate.**
- Strongest counter: That refusing on 'non-positive trailing cash flow' is exactly the wrong call at a cyclical trough - the whole point of a trough is that trailing cash flow is bad, and an owner buys the mid-cycle. On mid-cycle brokerage economics the combined RXO-Coyote footprint could plausibly earn $400-500M of adjusted EBITDA, at which $4.0bn of enterprise value is 8-10x and the stock is cheap.
- What would prove it: Gross profit per load sustaining its gains into Q4 and 2027 while volume grows - the two have to rise together, because volume bought with margin is what brokers do in a bad market and it looks identical to a recovery.
- Already visible today: Genuinely encouraging and genuinely early: +2% truckload volume, +11% sequential gross profit per load in Q2, and a further +10% in August per the 2026-09-09 release. But Q3 adjusted EBITDA is guided to $35-45M against $40M in Q2 - the midpoint is flat sequentially, which is not yet an inflection in earnings however good the per-load statistics look.
- Left unresolved: Mid-cycle earnings power for the combined entity. RXO has never reported a full upcycle with Coyote included, so there is no observed mid-cycle to anchor on, and the difference between $160M and $450M of normalised EBITDA is the entire valuation. I could not resolve it from free sources and will not manufacture it.

**Key risks.** Three consecutive years of negative or near-zero free cash flow and GAAP losses of $100M and $290M; About 25x annualised trough adjusted EBITDA - the recovery is already in the price; $1.11bn of goodwill and $432M of intangibles from Coyote against $1.51bn of equity; Freight has produced several false dawns since 2023; idled capacity returns quickly when rates rise
**Watch for.** Q3 and Q4 adjusted EBITDA against the $35-45M guide - earnings, not per-load statistics, are the test; Whether gross profit per load and volume rise together, or volume is being bought with margin; Any disclosure of mid-cycle or normalised earnings power for the combined Coyote footprint

**Data quality.** Flags raised (negative_fcf_year_in_window, lumpy_fcff_spread_6.1x_of_mean, nonpositive_normalized_fcff) are correct and the DCF refusal is right. One UNFLAGGED defect confirmed: interest_expense is None against total_debt of $495,000,000, the fifth form of the interest-expense family recorded on CON; the Q2 10-Q reports 'Interest expense, net 9 8 18 17' - $18M for six months, about $36M a year at an unremarkable 7.3%. It cost nothing here because the base is non-positive either way (correcting it moves the base from about -$13M to about +$14M against a ~$4.0bn EV), but on a ranked name it would be a false sell. The multiples table is refused under the standing RIOT/EPRT test: ev_ebitda returns negative per-share values (-$0.73 at p25) while ev_sales returns $27.06-$111.59, the rows straddle the price in opposite directions, and the cohort is 'not ranked'. No number recorded.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1929561/000192956126000036/rxo-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1929561/000192956126000041/rxo-20260909.htm
- https://www.sec.gov/Archives/edgar/data/1929561/000192956126000033/rxo-20260806.htm
- https://www.investing.com/news/company-news/rxo-q2-2026-presentation-shows-early-recovery-amid-tight-capacity-93CH-4842864

**Ingestion notes.** no usable final_growth
