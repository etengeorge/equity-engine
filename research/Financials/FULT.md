# FULT — FULTON FINANCIAL
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-18 — NO_EDGE (conviction: medium)

- **Verdict:** no_edge · price $23.39 · fair value $18.89 · gap -19.3%
- **Sustainable ROTCE:** screen said +13.1%, analyst says +14.0%
- **P/TBV:** justified 1.35 vs actual 1.68 on tangible book of $13.94/share

**The case for the price.** Fulton is a $4.5bn Pennsylvania/New Jersey commercial bank that has compounded scale through two acquisitions in three years — Republic First in 2024 and Blue Foundry Bancorp, completed 2026-04-01 and merged into Fulton Bank on 2026-07-11 — while running an operating return well above its cost of equity. Reported ROATCE was 15.71% in Q2 2026 against 14.76% in Q1, the efficiency ratio improved 60bp to 57.3%, net charge-offs ran 34bp and the tangible common equity ratio rose to 8.81% from 8.00% a year earlier. A bank earning 15% on tangible common equity against a ~10.9% cost of equity should trade at a meaningful premium to tangible book, and 1.5x is that premium, not an excess.

**What changed.** The Blue Foundry Bancorp acquisition CLOSED on 2026-04-01 (8-K items 2.01/7.01/9.01) and the bank merger completed 2026-07-11. Share count rose from 162,988 thousand to 191,461 thousand and tangible common shareholders' equity from $1,963,233 thousand to $2,989,450 thousand. Tangible book value per share at 2026-06-30 is $15.61 ($16.73 excluding AOCI). The 2026-07-21 8-K is an item 5.02 officer change. There is no company-specific news in the store for the last 90 days, which lowers my confidence in 'nothing else happened' rather than confirming it.

**Base case.** Sustainable ROTCE of 14.0%, between the company's GAAP return and its adjusted 15.71%. Fulton's ROATCE is a non-GAAP figure that adds back intangible amortisation, acquisition-related expense and FultonFirst implementation costs. For a bank that has closed two acquisitions in three years, acquisition expense is a recurring cost of the operating model, not a one-off, so adding all of it back overstates the sustainable return — the mirror of the averaging error that understates it. 14.0% credits the genuine operating improvement (efficiency 57.3%, TCE 8.81%, 34bp charge-offs) while charging part of the deal cost the company excludes.

**Devil's advocate.**
- Strongest counter: The 15.71% ROATCE is an ADJUSTED number, and Fulton is a serial acquirer: adding back acquisition-related expense for a company that acquires continuously is precisely how a roll-up manufactures a return it does not earn. On GAAP, Fulton earns roughly 13%, which is what the engine already says — so the engine's -25.1% gap is right and my correction is the analyst talking himself out of a sell.
- What would prove it: Whether the engine's -25.1% survives once the OTHER input is checked independently of the ROTCE — that is, whether the tangible book the model divides by is the current one.
- Already visible today: Yes, and it is what stops the counter. The defect here is not only in the numerator. The engine prices today's share price against tangible book of $13.94, while the Q2 2026 non-GAAP reconciliation reads tangible common shareholders' equity of $2,989,450 thousand over 191,461 thousand shares = $15.61 per share. `equity_series[0]` predates the 2026-04-01 Blue Foundry close. Actual P/TBV is therefore 1.50, not 1.68. At the engine's OWN 13.1% ROTCE the gap is -16.8%, not -25.1%; at 14.0% it is -10.0%; at the reported 15.71% it is -2.6%. The counter wins on the numerator and still cannot rescue the gap, because the denominator is independently stale by 12%.
- Left unresolved: How much of Fulton's acquisition expense is genuinely terminal. If the bank announces a third deal, 14.0% is too generous and the honest number is nearer 13%. I have no information either way.

**Key risks.** Serial acquisition: two deals in three years means 'adjusted' returns systematically exclude a recurring cost; Commercial real estate concentration in a mid-Atlantic footprint, with charge-offs at a benign 34bp that can only go one way; The recorded fair value is understated because the schema has no field to override tangible book — the model will price against $13.94 when the filed figure is $15.61
**Watch for.** Q3 2026 ROATCE with a full quarter of the merged Blue Foundry Bank — the first clean read on the combined return; Any third acquisition announcement, which would settle the adjusted-return question against my base case; Whether `equity_series` refreshes to the post-acquisition tangible book at the next annual extract

**Data quality.** The brief raised NO flags, and there were two defects. First, tangible book per share of $13.94 against the company's own filed $15.61 at 2026-06-30 — the AII/BUR stale-tangible-book bug, now on a name where an acquisition closed inside the gap; this understates tangible book by 12% and overstates actual P/TBV from 1.50 to 1.68. Second, a 13.1% averaged GAAP ROTCE against a reported 15.71%/14.76% in the last two quarters — the VLY direction of the averaging defect. Both run toward a false SELL. Corrected, the gap is about -10%, inside the noise band. I verified the share count independently: 191,461 thousand shares at $23.39 is $4.48bn, matching the engine's $4.5bn, so market capitalisation is current even though the book is not. The recorded fair value will still be built on the stale $13.94, so the printed number is too low by roughly 12% — the verdict is the output here, not the number.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/700564/000070056426000029/exhibit991063026earningsre.htm
- https://www.sec.gov/Archives/edgar/data/700564/000070056426000029/fultinvestorpresentation.htm
- https://www.sec.gov/Archives/edgar/data/700564/000070056426000033/fult-20260630.htm
- https://www.sec.gov/Archives/edgar/data/700564/000119312526135892/d89081d8k.htm

**Ingestion notes.** no usable final_growth
