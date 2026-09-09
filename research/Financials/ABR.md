# ABR — ARBOR REALTY TRUST REIT
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-09 — NO_MODEL (conviction: low)

- **Verdict:** no_model · price $5.01

**The case for the price.** The market is not valuing Arbor's book, it is discounting it. At $5.01 against a reported $10.95 of book value per share the stock trades at roughly 0.46x, and the reason is on the face of the Q2 2026 release: a GAAP net loss of $(37.3)M, distributable earnings down to $0.10 per diluted share from $0.25 a year earlier, a $38.2M net CECL provision in the quarter, nineteen non-performing loans with $428.8M of unpaid principal balance carried against only $31.1M of reserves, $545.9M of real estate owned (up from $498.9M six months earlier) with $13.6M of fresh impairments on two properties, and a portfolio yield falling to 7.21% from 7.50% because default and back interest are no longer being collected. Total non-performing assets are roughly $1.07 billion. Against $2.88B of total equity that is a credible reason to mark the book down by half, and the equity has returned -53% over twelve months while management guides to reducing the legacy book below $1B only by the end of 2027.

**What changed.** Q2 2026 (2026-07-31): net loss $(37.3)M vs $24.0M profit a year earlier; distributable earnings $21.7M ($0.10/sh) vs $52.1M ($0.25/sh); $38.2M CECL provision; total allowance $163.4M; REO $545.9M; total equity down to $2,881.0M from $3,067.2M at 2025-12-31. Subsequent 8-Ks on 2026-08-03 (investor presentation on the multifamily portfolio and NPL resolution plan) and 2026-08-11 (item 1.01/2.03, new debt obligation). Non-performing loan count is flat at nineteen quarter over quarter while reserves against them rose from $16.1M to $31.1M.

**Base case.** I am not supplying a sustainable ROTCE, because on this name the choice of that input IS the answer and I cannot defend any single value. See the devil's-advocate and data-quality notes.

**Devil's advocate.**
- Strongest counter: The bull case is genuinely strong and I want to state it properly. Arbor is not a bank marking to model: it has an agency business (Fannie Mae DUS) that is a real, separately valuable servicing franchise with a $24B+ servicing portfolio, and the CECL allowance on loss-sharing obligations is only 0.34% of it. If the legacy bridge book resolves at or near carrying value - and nineteen NPLs is a flat count, not a growing one - then book is roughly real, the company earns back toward a high-single-digit ROTCE as REO is sold, and 0.46x book is a large discount to a franchise that is not going away. Management is buying stock back (pro forma book rises to $11.59 after the buyback), which is what you do when you believe your own marks.
- What would prove it: REO and non-performing loans actually converting to cash at or near carrying value over two or three quarters, with distributable earnings recovering toward $0.20+ per quarter, and the total non-performing asset balance falling rather than rotating from delinquency into REO.
- Already visible today: The evidence available cuts both ways and does not settle it. NPL count is flat at nineteen and UPB fell from $481.5M to $428.8M, which supports the bull. But REO ROSE from $498.9M to $545.9M over the same six months, which is what it looks like when delinquent loans are foreclosed rather than repaid, and $26.2M of REO impairments have been taken year to date. Reserves against $428.8M of NPL UPB are $31.1M, or 7.3%, which is a thin mark on assets already in default. I cannot tell from outside which reading is right.
- Left unresolved: Everything that matters. The value of this equity is the recovery on roughly $1.07B of non-performing assets, and I have no basis on which to mark them that the market does not also have. The devil's advocate did not lose here - it fought to a draw, and that is why the verdict is no_model.

**Key risks.** Roughly $1.07B of non-performing assets against $2.88B of equity, reserved at 7.3% of NPL unpaid principal balance; REO growing while NPL balances fall - foreclosure, not repayment; Distributable earnings of $0.10 per quarter against a $0.17 dividend: the payout is not currently covered
**Watch for.** Realised proceeds on REO dispositions against carrying value - the single observable that settles whether book is real; Total non-performing assets falling in absolute terms rather than rotating between delinquency and REO; Any further dividend action, which would tell you what management thinks distributable earnings normalise at

**Data quality.** This name won an opportunistic slot at the 98th percentile of 339 Financials on a +127.3% gap, and the gap is not a valuation. Two flags fired and both are fatal. (1) `unstable_rotce_4.8%_to_13.6%`: the 'sustainable' 9.3% is a three-year average of a range that spans a factor of nearly three, and the most recent quarter is a LOSS - trailing distributable earnings are running at $0.40 annualised on ~$12 of book, i.e. about 3.3%. (2) `rotce_numerator_includes_minority_interest_earnings`: the balance sheet carries $103.1M of non-controlling interest inside $2,881.0M of total equity, so the numerator and denominator are not the same entity. The sensitivity is total and it is the JXN test verbatim: at the engine's 9.3% the justified P/TBV is 0.95 against an actual 0.42, a +127% gap; at 6.5% it is 0.58; at 5.0% it is 0.39, i.e. fair; at the current 3.3% run rate it is 0.17, which says the stock is nearly three times too EXPENSIVE. One defensible input choice moves the answer from +127% to -60%, so the output is not a valuation and I am recording no fair value. Separately, tangible book per share is close but not exactly reconcilable: the engine reads $12.03 while the company reports $10.95 at 2026-06-30 (pro forma $11.59 after buyback), a difference that looks like preferred and OP-unit treatment rather than the AII/BUR stale-book bug - equity of $2,881.0M is the current 2026-06-30 figure, not the December one. Note also that ABR is a mortgage REIT priced by the `book` method because it is classified in Financials; CLAUDE.md's own rule assigns REITs to `none`, and this name is a good argument for that rule.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1253986/000125398626000048/abr-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1253986/000125398626000047/abr-20260731.htm
- https://www.sec.gov/Archives/edgar/data/1253986/000125398626000051/abr-7312026x8k.htm
- https://www.stocktitan.net/news/ABR/arbor-realty-trust-reports-second-quarter-2026-results-and-declares-76bhegwkjyjd.html

**Ingestion notes.** no usable final_growth
