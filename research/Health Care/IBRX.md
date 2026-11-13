# IBRX — IMMUNITYBIO INC
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-11-13 — NO_MODEL (conviction: low)

- **Verdict:** no_model · price $6.07
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** ImmunityBio is a commercial-stage immunotherapy company whose approved product ANKTIVA is growing fast - Q3 revenue rose 53% year over year - and which has just reported positive late-stage data in BCG-naive non-muscle-invasive bladder cancer with an FDA label expansion widening the eligible population. The founder is pursuing sepsis trials in the US and Europe and controls a large affiliated platform. Holders are underwriting an option on a platform and a founder with deep pockets, not a discounted cash flow, and the stock is still up 183.6% over twelve months even after a 38.7% drawdown in twenty-one days.

**What changed.** Q3 results, 2026-11-09, and the stock fell roughly 18-19% on the print and extended to four consecutive down days, closing at $6.07. Revenue grew 53% year over year but ANKTIVA sales declined SEQUENTIALLY, the loss was wider than expected and expenses rose. Most importantly, the 10-Q filed 2026-11-09 carries an explicit going-concern paragraph: 'we believe that substantial doubt exists regarding our ability to continue as a going concern without additional funding or financial support.' Management states the doubt is alleviated 'based primarily upon our Founder, Executive Chairman and Global Chief Scientific and Medical Officer's intent and ability to support our operations with additional funds, including loans from affiliated entities, as required', alongside an S-3ASR shelf. Positive BCG-naive data and an FDA label expansion were also announced in the same window.

**Base case.** There is nothing here a free cash flow model can value, and the engine is right to refuse. There is no FCFF base at all - the normalised series is computed over zero years - no enterprise value and no implied growth. The multiples table is the only populated path and it must be disregarded rather than read: ev_sales of 53.6x and ev_gross_profit of 54.0x against Health Care cohort medians of 4.4x and 6.4x produce a blended $0.91 against a $6.07 price, but CLAUDE.md's own standing caution applies with full force - a sales multiple on a company whose product revenue has only just arrived, and which is building commercial infrastructure ahead of it, is close to meaningless, and the cohort is explicitly 'not ranked - too few comparable Health Care names'. An 85% 'discount' computed that way is not a valuation. Above all, a going-concern paragraph whose mitigation is the personal intent of one individual to lend is a statement that the enterprise's ability to fund itself is unresolved; no growth rate applied to any base survives that.

**Devil's advocate.**
- Strongest counter: That a going-concern paragraph is close to routine for a commercial-stage biotech and that I am treating boilerplate as a verdict. Revenue is growing 53%, the drug is approved and the label just widened, and the market capitalisation is $6.4 billion - the market plainly does not think this company is about to fail.
- What would prove it: Sequential ANKTIVA revenue in Q4 and Q1, and the terms and size of the next financing - whether it is an arm's-length equity raise or another affiliated loan.
- Already visible today: The sequential sales decline is visible now, and it is the reason the stock fell on a quarter with 53% growth. What is NOT routine is the mitigation: the doubt is alleviated by one person's stated intent to lend through affiliated entities, which is a related-party dependency rather than committed capital.
- Left unresolved: Everything that decides the equity. I have no basis for an opinion on ANKTIVA's peak sales and I will not manufacture one from a cohort multiple the brief itself says is unrankable.

**Key risks.** Explicit going-concern doubt, alleviated only by the founder's stated intent to fund through affiliated entities; ANKTIVA sales declined sequentially in Q3 despite 53% year-over-year growth; S-3ASR shelf available for dilution at a price already down 38.7% in twenty-one days; A $6.4 billion market capitalisation resting on one approved product and one supporter
**Watch for.** Sequential ANKTIVA revenue in Q4 - whether the Q3 decline was channel timing or demand; The size, pricing and counterparty of the next financing: an arm's-length raise would materially change the going-concern picture; Any partnership or licensing transaction that funds the company independently of affiliated entities

**Data quality.** The engine refused correctly (`status: model_failed`, no FCFF base, no enterprise value) and the two flags it raised - `interest_expense_implies_6888%_on_reported_debt_debt_likely_understated` and `speculative_cost_of_debt_but_only_0%_debt_weight` - are symptoms of a capital structure the extractor cannot read, not of anything about the business. Beta is 2.23 at R-squared 0.101, giving a 17.4% cost of equity that is at least directionally honest for this risk but is not a measurement. The multiples table is the only populated valuation path and I am recording explicitly that it should be DISREGARDED, not read as -85%: the cohort is unranked for insufficient comparables, and both rows divide by a trailing revenue line for a product in its first full commercial year, which is the MXL defect in its sharpest form - an inflecting denominator makes every trailing multiple an artefact. Refusing is not a judgment that the name is cheap or expensive; on this one it is a statement that a going-concern dependency on a single related party cannot be priced by this engine.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1326110/000132611026000099/ibrx-20260930.htm
- https://finance.yahoo.com/healthcare/articles/ibrx-q3-earnings-miss-anktiva-140300738.html
- https://www.proactiveinvestors.com/companies/news/1101446/immunitybio-shares-slump-19-as-revenue-misses-and-going-concern-warning-hits-sentiment-1101446.html

**Ingestion notes.** no usable final_growth
