# BUR — BURFORD CAPITAL LTD
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-07 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $4.35

**The case for the price.** At $4.35 against a tangible book of $3.12 per share, the market pays roughly 1.4x tangible book for a litigation funder whose largest asset was destroyed on appeal in March. That is not a discount to book, it is a premium, and the premium is for the asset-management franchise and the remaining portfolio rather than for the balance sheet. The bear reasons that the remaining book is itself a Level 3 mark: the weighted-average discount rate is 6.7% and the adjusted risk premium rose to 48.6% at 30 June 2026 from 31.1% at year end, so nearly half the modelled value is being given back to risk before a court has ruled. A 10% move in the fair value of capital provision assets and related liabilities moves net assets by $321.4M — a third of the market cap — which is why the equity trades like an option on a small number of binary legal outcomes rather than like a book-value stock.

**What changed.** The single most important fact about this company post-dates the fiscal year the model prices. On 2026-03-27 the US Court of Appeals for the Second Circuit REVERSED the District Court's entry of judgment in favour of Petersen and Eton Park against Argentina and YPF (Judge Cabranes dissenting). Burford's 10-Q for the quarter ended 2026-06-30 records the consequence: the consolidated fair value of the YPF-related assets fell to $160.4M at 30 June 2026 from $2.6B at 31 December 2025, with unrealized gains down $2.4B to an unrealized LOSS of $41.2M. Total Burford Capital Limited equity fell from $2,448.0M to $819.1M in six months; retained earnings went from $1,800.9M to $157.2M. The YPF exposure had been ~46% of the fair value of all capital provision assets at 2025 year end. Further proceedings continue in the US courts and the plaintiffs are likely to pursue international arbitration, so the claim is not worthless — but it is no longer a judgment.

**Base case.** I decline to state one. This is a book-method name whose book value the engine has wrong by a factor of 3.4x, and whose ROTCE is an average of years in which the dominant input was an unrealized mark that has since reversed. Correcting one input without the other would produce a number with no meaning.

**Devil's advocate.**
- Strongest counter: The best case that I am wrong to refuse is that the corrected picture is itself a thesis: at $4.35 against $3.12 of tangible book you are paying 1.4x for a franchise with $733M of cash on hand, a portfolio that generated the strongest cash quarter since 1Q25, and an asset-management business, with a free option on YPF revival. That is a coherent argument, and someone who has read the remaining portfolio matter by matter could make it. I have not read the portfolio matter by matter, and the honest answer is that I cannot value a book that is 100% Level 3 marks on legal outcomes from headline numbers.
- What would prove it: A matter-by-matter roll-forward of the non-YPF portfolio's realizations against cost, and the outcome of the remand and of any petition for rehearing or certiorari in Petersen/Eton Park.
- Already visible today: Partially. The 10-Q shows cost basis and unrealized gains split between YPF and other assets, and shows the adjusted risk premium rising to 48.6% — the company itself is marking the rest of the book more conservatively. What is not visible is any dated event that resolves the YPF residual.
- Left unresolved: Whether the residual $160.4M consolidated ($101.1M Burford-only) YPF carrying value is conservative or optimistic. I could not form a view on that from the filings, and it is roughly 17% of remaining shareholders' equity.

**Key risks.** The engine's entire +178% gap is a stale-book artifact and would have read as the cheapest 1% of 340 Financials; Remaining book value is Level 3 marks on litigation outcomes; a 10% move in those marks moves net assets by $321.4M against a $955M market cap; Debt-to-equity based covenants on incurrence of additional debt and restricted payments tighten as equity falls; Non-controlling interests of $649.3M exceed the $819.1M attributable to Burford itself
**Watch for.** Any ruling on remand, rehearing en banc, or certiorari in Petersen/Eton Park v. Argentina; The 3Q26 tangible book per share — the engine will keep pricing against $10.57 until the extract refreshes

**Data quality.** RESOLVED AND FATAL. The brief prices tangible book at $10.54/share and an actual P/TBV of 0.41. Burford's own non-GAAP reconciliation in the 2Q26 10-Q gives tangible book attributable to Burford Capital Limited of $685.1M on 219,584,503 basic shares = $3.12 per share at 2026-06-30, against $10.57 at 2025-12-31. The engine used the DECEMBER figure. Actual P/TBV is therefore ~1.39x, not 0.41x, and the +177.9% gap and 99th-percentile cohort rank are entirely artifact. This is the AII lesson of 2026-09-04 — 'the engine prices today's share price against LAST fiscal year-end's tangible book' — recurring on a name where the intervening quarter contained a $2.4B write-down, which is the worst case that error can produce. The second input is also unusable: the flagged `unstable_rotce_2.7%_to_28.3%` spans years whose net income was dominated by YPF fair-value marks, so the 12.5% 'sustainable' ROTCE describes a company that no longer exists (the JXN/FG pattern). Both inputs to the justified P/TBV are wrong, so no fair value is recorded. Note also that total shareholders' equity of $1,468.3M includes $649.3M of non-controlling interests against $819.1M attributable to Burford — check which equity concept the extract used before repricing.

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1714174/000171417426000097/bur-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1714174/000171417426000096/bur-20260806xex991.htm
- https://investors.burfordcapital.com/news/news-details/2026/Burford-Capital-Statement-Re-YPF-Appeal-Decision/default.aspx
- https://www.sullcrom.com/insights/memo/2026/April/Second-Circuit-Reverses-18-Billion-Judgment-Against-Argentina

**Ingestion notes.** no usable final_growth
