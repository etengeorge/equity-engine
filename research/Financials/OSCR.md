# OSCR — OSCAR HEALTH CLASS A
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-02 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $29.83

**The case for the price.** Oscar Health is a bet on ACA exchange policy, not on tangible book. The stock is up 79% in twelve months and 41% in three because the enhanced premium subsidy regime that determines whether its 3+ million members can afford their plans has moved from expiring to being extended, and each step of that political process has re-rated the stock. The market is paying 8.0x tangible book for a technology-led insurer that has been growing membership and revenue fast and is targeting its first year of profitability. Book value is the wrong lens for that: a managed care company's value is its member base, its risk-adjustment competence and its medical loss ratio, and almost none of that sits on the balance sheet. Buying an insurance company at 8x tangible book is a statement about future underwriting margin on a large book, and the price says the market believes the margin is coming.

**What changed.** I could not establish this properly and that is the main limitation of this file. The news store held no company-specific items for the trailing 90 days — a coverage fact, not a company fact, since a name only earns a pull when it moves hard, trades abnormal volume, files an 8-K or is picked. Q2 2026 results were filed 2026-08-06 with the press release as EX-99.1 and the 10-Q on 2026-08-07, and I did not fetch either. What web search establishes is the shape of the policy backdrop: enhanced ACA subsidies were set to expire, an extension has been proposed and reported, and management has warned of elevated churn with paid membership falling from roughly 3.4 million toward 3.0 million as passively enrolled members face higher premiums.

**Base case.** There is no sustainable ROTCE to supply. The model computes -58.8%, and the honest reading of that is not 'a very negative return' but 'the averaging window contains loss years and the ratio has no economic meaning'. Oscar has been loss-making; a return on tangible common equity computed from those losses, on an equity base of $3.73 per share against a $29.83 price, is not a return through the cycle. I will not substitute a number of my own either, because I did not read the Q2 filing and I have no basis for an underwriting margin assumption.

**Devil's advocate.**
- Strongest counter: The counter to no_model is that the model's answer — 2nd percentile of 338 Financials, a -193% gap, actual P/TBV of 8.01 against a NEGATIVE justified multiple — is at least directionally informative: this is one of the most expensive financials in the index on the only measure the engine has. Declining to score it means an 8x-tangible-book loss-making insurer gets exactly the same 'no_model' label as a profitable one whose accounting happens not to fit, which loses real information.
- What would prove it: Two to three quarters of medical loss ratio and membership after the subsidy question resolves. Those two numbers decide the entire valuation and neither is on the balance sheet.
- Already visible today: Not in anything I read. The subsidy outcome is a live political process, and management's own guidance already contemplates membership falling by roughly 400,000. I did not read the Q2 release, so I cannot say what the current medical loss ratio is.
- Left unresolved: The current MLR, the current membership trajectory, and the status of the subsidy legislation. All three are knowable and I did not get them — I prioritised the ad-hoc fetch budget on the five names where a document would change a number rather than confirm a refusal. That is a defensible allocation but it does mean this file rests on search results rather than filings, and I am recording that rather than dressing it up.

**Key risks.** The entire business depends on federal ACA subsidy policy, which is outside management's control and currently unresolved; Adverse selection as healthier members drop coverage when premiums rise — the risk pool worsens exactly as it shrinks; 8.0x tangible book with a history of losses leaves no margin for a bad medical cost year; Membership guided down from roughly 3.4 million to 3.0 million
**Watch for.** Final legislative outcome on the enhanced ACA subsidy extension; Medical loss ratio and membership in the next two quarterly reports; Whether the first full year of profitability is delivered or deferred again

**Data quality.** The justified P/TBV is -7.46 and the sustainable ROTCE is -58.8%. A negative justified multiple is not a cheap or expensive signal, it is the formula reporting that its inputs are outside the domain where it means anything — you cannot capitalise a negative return into a price-to-book multiple and read the sign. The -193.1% gap and 2nd-percentile cohort rank should be discarded rather than interpreted, and I am recording no fair value. The loss_year_in_window flag is the direct cause and it is correct. Two further points the brief does not make. First, the book method is arguably the wrong method for a health insurer in the first place: the sector mapping in universe.csv puts Oscar in Financials and therefore prices it on justified price-to-tangible-book from ROTCE, but a managed care company's economics are premium underwriting margin, not spread on a balance sheet, and debt is not its raw material in the way it is for a bank. That is a universe.csv method question worth raising, not a bug in valuation.py. Second, shares_asof is null for this name — the model has no cover-page share count date at all, so I cannot confirm the $7.8B market capitalisation is struck on a current count. Beta is 0.97 from a regression with an R-squared of 0.051, which is the same failed-regression problem found on GLRE today.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://simplywall.st/stocks/us/insurance/nyse-oscr/oscar-health/news/oscar-health-oscr-is-up-52-after-aca-subsidy-extension-suppo
- https://finance.yahoo.com/news/oscar-health-oscr-13-7-042859951.html
- https://simplywall.st/stocks/us/insurance/nyse-oscr/oscar-health/news/oscar-health-outlines-growth-policy-risks-and-capital-model/amp
- https://thesmartfin.com/blog/oscar-health-deep-dive

**Ingestion notes.** no usable final_growth
