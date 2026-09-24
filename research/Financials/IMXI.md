# IMXI — INTERNATIONAL MONEY EXPRESS INC
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-24 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $11.43

**The case for the price.** At $11.43 nobody is valuing Intermex's cash flows. The stock is a probability on a contract. On 2025-08-10 the company signed an Agreement and Plan of Merger with The Western Union Company under which every share converts into the right to receive $16.00 IN CASH. The 2026-06-30 10-Q states the outside date is 2026-11-10 (automatically extended for certain regulatory approvals), that Western Union owes a $27.3M termination fee only where the failure relates to ANTITRUST law, and that the remaining closing conditions include consents with respect to 'the Company's or its subsidiaries' money transmitter licenses'. On 2026-08-13 the California Department of Financial Protection and Innovation SUSPENDED the approval extension it had granted on 2026-07-31, 'based on a need to further review the transaction as a result of the intervening six months since approval was originally granted'. At $11.43 against $16.00 the market is paying roughly a coin flip: solving 11.43 = p x 16 + (1-p) x B gives p of about 52% at a $6.50 break price and 43% at $8.00. Given a seven-week outside date and a licensing regulator that has already reversed itself once, that is a reasonable price.

**What changed.** The deal broke down, and the business deteriorated underneath it. (i) NYDFS approved in August with commitments to maintain New York retail locations and limit certain price changes for three years, plus an Assurance of Discontinuance with the New York Attorney General. (ii) California DFPI suspended its approval extension on 2026-08-13; the parties said they would 'engage promptly' and close after reinstatement, and as of 2026-09-23 no reinstatement has been announced - six weeks of silence against a 2026-11-10 outside date. (iii) The stock fell 17.1% in five days and 19.1% in twenty-one. (iv) Underneath, the standalone business is contracting hard: Q2 2026 total revenues $131.2M against $161.1M (-18.6%), H1 $253.1M against $305.4M (-17.1%), Q2 operating income $8.8M against $19.5M (-55%), H1 net income $4.7M against $18.8M (-75%). Buybacks are suspended for the duration of the merger agreement.

**Base case.** No cash-flow base case is appropriate. This is a deal stock with a seven-week binary, and the engine's model is a category error on top of that.

**Devil's advocate.**
- Strongest counter: That the break risk is overpriced. Fifty-one of 51 applicable US states and territories plus every international jurisdiction had approved by June 2026; New York, the hardest one, cleared in August with negotiated commitments; and the DFPI letter does not allege a substantive problem - it says the file has gone stale over six months. Regulators that reopen for staleness usually reinstate. If it closes, $11.43 to $16.00 is 40%.
- What would prove it: A DFPI reinstatement notice, or an 8-K extending the outside date - versus a termination notice.
- Already visible today: The absence is what is visible: six weeks since the suspension and no announced reinstatement, with the outside date seven weeks away. That is the only new information and it is not encouraging. I have no view on California's regulatory calendar, and I should not pretend one.
- Left unresolved: Everything that decides the payoff. I cannot handicap the DFPI. I also cannot pin the break price precisely - my $5-8 range is annualised Q2 earnings at 8-12x, on a revenue line falling 18% a year with an immigration-policy-driven decline in the sending population and digital competitors taking share, and it could be materially lower.

**Key risks.** Binary outcome with a 2026-11-10 outside date and one unresolved state licensing regulator; The Western Union break fee of $27.3M is conditioned on ANTITRUST failure; a money-transmitter licensing failure appears not to trigger it; Standalone business declining 18% year over year in revenue and 75% in half-year net income; Buybacks suspended and capital allocation frozen by merger-agreement covenants for the duration
**Watch for.** California DFPI reinstatement of the approval, or a termination notice - either resolves the name; Any 8-K extending the 2026-11-10 outside date; Q3 2026 revenue: another 18% decline sets the break price lower than my $5-8 estimate

**Data quality.** Both engine flags are correct and both are fatal. `rotce_76%_suggests_asset_light_financial_p_tbv_may_be_the_wrong_model_here` is the engine correctly diagnosing the PIPR category error on itself: Intermex is an agent-network remittance processor whose productive asset is a distribution network, not regulatory capital, and $2.70 of tangible book per share is a working-capital balance. `unstable_rotce_40.0%_to_111.2%` and `goodwill_and_intangibles_48%_of_book` compound it. Per the standing rule I am supplying NO rotce_override, because doing so would launder a category error into a fair value. Beyond that, the price is not an opinion about cash flows at all - it is a merger payoff - so the +96.8% gap and the 96th percentile of 339 Financials are meaningless twice over. Note for the engine: the SLAB return-dispersion tell (near-zero 5d/21d/63d dispersion on a pinned deal price) is defeated here in the OPPOSITE direction. IMXI shows -17.1%/-19.1%/-16.8%, i.e. maximal dispersion, which reads to the selection score as a crashing stock deserving an opportunistic slot when it is actually deal risk repricing. The reliable tell was textual and free: a merger agreement described in plain terms in the 10-Q, and 8-Ks dated 2025-08-11 under items 1.01/5.02/7.01/9.01.

*Horizon: 6 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1683695/000162828026055191/imxi-20260630.htm
- https://ir.westernunion.com/news/archived-press-releases/press-release-details/2026/Western-Union-and-Intermex-Provide-Update-on-Pending-Acquisition/default.aspx
- https://investors.intermexonline.com/news-releases/news-release-details/western-union-and-intermex-provide-update-pending-acquisition-0
- https://www.americanbanker.com/payments/news/western-unions-latam-strategy-faces-pressure

**Ingestion notes.** no usable final_growth
