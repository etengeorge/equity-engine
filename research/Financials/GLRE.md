# GLRE — GREENLIGHT CAPITAL LTD CLASS A
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-02 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $15.26 · fair value $28.75 · gap +88.4%
- **Sustainable ROTCE:** screen said +10.6%, analyst says +8.0%
- **P/TBV:** justified 1.33 vs actual 0.70 on tangible book of $21.69/share

**The case for the price.** Greenlight Re trades at 0.74x fully diluted tangible book because that is what the market pays for a Cayman reinsurer whose investment portfolio is a hedge fund. Q2 2026 was a net LOSS of $29.6M ($0.89 per diluted share) on investment losses in the Solasglas portfolio plus catastrophe and Middle East conflict reserves, with a combined ratio of 100.1% — no underwriting profit at all. Fully diluted book value per share FELL 3.7% in the quarter to $20.61. For the half, net income was $6.2M against $30.0M a year earlier, and book value per share is up 0.9% in six months, an annualised return on equity under 2%. A reinsurer that cannot earn its cost of capital, whose earnings are partly a mark on someone else's fund positions, and which has traded below book for most of a decade, is not obviously mispriced at 0.74x. The company's own response is the clearest signal: it bought back $19.2M of stock in the half, which is what management does when it agrees the shares are the best asset available and still cannot make the returns work.

**What changed.** Q2 2026 (2026-08-04): net loss $29.6M, combined ratio 100.1% versus 95.0%, fully diluted book value per share $20.61 (down from $21.40 at 2026-03-31, up from $20.43 at 2025-12-31). $14.2M of ordinary shares repurchased in the quarter, $19.2M for the half (1,102,065 shares). Greenlight Innovation Syndicate 3456 received 'in principle' approval to progress to a full Lloyd's syndicate (2026-07-30). New independent director appointments announced 2026-09-01.

**Base case.** Sustainable ROTCE, not growth, is the number that prices this name. The model uses 10.6%, averaged across a 6.7%-14.6% range that it flags as unstable. That average is drawn from years when reinsurance pricing was hard and the investment portfolio was working. What is observable now is very different: a 100.1% combined ratio in the quarter, 98.1% for the half, and an annualised return on equity under 2%. Through the cycle I would underwrite Greenlight Re at roughly 8% — the underwriting book at a high-90s combined ratio contributes little, and the return depends on the Solasglas investment result, which is volatile in both directions and is not a franchise return the way a bank's spread income is. I have set rotce_override to 0.08 rather than the model's 10.6%.

**Devil's advocate.**
- Strongest counter: The counter is that I am dismissing a 99th-percentile gap on a name whose tangible book I have personally verified against the filing, which is exactly the situation the engine exists to find. Book value is real, liquid and marked — this is not a bank with opaque loan marks; the assets are securities. The company is buying its own stock below book, which is immediately accretive to book value per share. Buying a verified $20.61 of marked assets for $15.26 is a 26% discount, and my dismissal rests entirely on a judgement about future ROTCE that I have set by looking at the two worst recent quarters.
- What would prove it: Two to three more quarters of combined ratio and Solasglas return. A combined ratio settling below 95% with a positive investment result would put ROTCE back near 10-12% and make the discount to book genuinely attractive; another year near 100% confirms the franchise does not earn its cost of capital.
- Already visible today: Yes, and it is mixed rather than favourable. The negative: Q2 combined ratio 100.1%, a net loss, and book value per share down 3.7% in the quarter. The positive, which I should credit: over six months fully diluted book value per share is still UP 0.9% despite that quarter, and management repurchased $19.2M of stock below book while doing it. The half-year combined ratio of 98.1% is better than the 99.9% of the prior-year half. So the franchise is not deteriorating — it is just not earning much.
- Left unresolved: The right cost of equity, which I cannot set from inside the analyst file and which matters more here than the ROTCE. I also did not read the Solasglas portfolio disclosure, so I cannot say how much of the Q2 investment loss was idiosyncratic positioning versus market beta.

**Key risks.** Earnings depend on the Solasglas investment portfolio, which is a hedge fund result, not an underwriting return; Combined ratio at or above 100% means the underwriting book is currently contributing nothing; Catastrophe and conflict exposure can take book value down several percent in a single quarter, as Q2 2026 did; $2.5M average daily dollar volume — the beta is measured on almost no trading
**Watch for.** Combined ratio below 95% for two consecutive quarters; Quarterly change in fully diluted book value per share — the company's own stated primary financial goal; Progress of Lloyd's Syndicate 3456 from 'in principle' to full approval and its contribution; Continued buyback below book

**Data quality.** I verified the tangible book side and it is essentially sound: the 2026-06-30 10-Q shows total shareholders' equity of $697.682M and 32,641,344 ordinary shares outstanding at 2026-08-03, giving basic book value per share of $21.37 against the model's $21.69 tangible book, and the company's own fully diluted figure is $20.61. So actual P/TBV of 0.70-0.74 is right and the +170.8% gap does NOT come from the book value. It comes from the two inputs on the other side, and both are wrong in the same direction. First, the sustainable ROTCE of 10.6% is an average across a range the model itself flags as unstable (6.7% to 14.6%), and it is contradicted by the current run rate — book value per share up 0.9% in six months is under 2% annualised. Second, and more seriously, the cost of equity of 6.5% is built on a beta of 0.31 carrying an R-squared of 0.068, and the screen records beta_source as 'regression' — meaning a regression explaining 7% of variance was accepted rather than falling through to the sector median. A 6.5% cost of equity for a Cayman reinsurer with a hedge-fund investment portfolio is not defensible under any reading; 11-12% is. Substituting an 8% ROTCE and an 11% cost of equity into the same justified-P/TBV formula gives roughly 0.67x against an actual 0.74x — that is, fairly valued to slightly expensive, not +171% cheap. I have set rotce_override to 0.08, but the analyst file has no field for cost of equity, so the recorded fair value will still be computed against the indefensible 6.5% and will still show this name as cheap. Read the recorded number with that in mind; the verdict is the judgement.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1385613/000138561326000097/pressreleaseearnings2026q2.htm
- https://www.sec.gov/Archives/edgar/data/1385613/000138561326000098/glre-20260630.htm
- https://www.sec.gov/Archives/edgar/data/1385613/000138561326000097/investordeck2026q2final.htm
- https://www.fool.com/earnings/call-transcripts/2026/08/11/greenlight-capital-re-glre-q2-2026-earnings-call/
- https://finance.yahoo.com/markets/stocks/articles/greenlight-innovation-syndicate-3456-progresses-070000878.html

**Ingestion notes.** no usable final_growth
