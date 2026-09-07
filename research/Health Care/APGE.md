# APGE — APOGEE THERAPEUTICS
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-07 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $133.96
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** There is no consensus to steelman, because there is no longer a security. AbbVie completed its acquisition of Apogee Therapeutics on 2026-09-03; Apogee shareholders received $135.11 per share in cash (equity value ~$10.9B) and the common stock ceased trading on Nasdaq before the open that day. The $133.96 the screen priced is a 49-day-stale quote from before the close, and the +57.2% 21d / +249.1% 252d 'returns' are the deal premium, not a market opinion about cash flows.

**What changed.** Everything. The 2026-09-03 8-K carries items 1.02, 2.01, 3.01, 3.03, 5.01, 5.02, 5.03 and 9.01 — termination of a material agreement, completion of acquisition, notice of delisting, suspension of the duty to file, change in control, departure of directors and officers, and amendment of the charter. That combination is a closed merger and a delisting, and it is on the face of the filing list in the brief.

**Base case.** No base case is possible or appropriate. The company does not exist as a separate issuer. Any FCFF growth rate recorded here would be a fiction about an entity that was absorbed into AbbVie four days ago.

**Devil's advocate.**
- Strongest counter: The strongest counter is that this is not a valuation error at all but a universe-maintenance error, and that recording no_model on a dead ticker teaches nothing. I disagree: the engine spent one of ten judgment slots on a company that had already been delisted, and it did so with four independent tells on the face of the brief (a stale-price flag, an 8-K carrying items 2.01/3.01/5.01, a +249% 252d return, and zero modelled fundamentals). That is a live defect in the pipeline, not a footnote.
- What would prove it: Whether the name is still in universe.csv and whether the price puller returns anything for APGE on the next run.
- Already visible today: Yes — `stale_price_49.0d` fired, and the last quote is from before the deal closed. The engine flagged the symptom and ranked the name anyway.
- Left unresolved: Nothing about the company. What I cannot resolve from here is how many other delisted or acquired names remain in the 1,956-name universe; the rotation cursor will reach them one at a time.

**Key risks.** None to an investor — the position was cashed out at $135.11 on 2026-09-03; To the engine: a delisted ticker consumed a rotation slot and will do so again on the next cycle unless the universe is pruned
**Watch for.** APGE removed from universe.csv, and a pre-selection gate that drops any name whose 8-K carries item 3.01 (delisting notice) or 5.01 (change in control), or whose price is more than ~5 sessions stale

**Data quality.** Every quantitative field on this brief is void: no FCFF base, no enterprise value, no implied growth, no cohort rank, and a 49-day-old price. `stale_price_49.0d`, `negative_fcf_year_in_window`, `nonpositive_normalized_fcff` and `no_usable_multiple_for_this_name` all fired and are all correct — collectively they say the model had nothing to work with. This is the SLAB lesson (2026-09-02) carried to completion: SLAB was a PENDING all-cash deal that the engine kept reverse-DCFing; APGE is a CLOSED one that the engine kept ranking after the shares stopped existing.

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1974640/000114036126035537/ef20081397_8k.htm
- https://news.abbvie.com/2026-09-03-AbbVie-Completes-Acquisition-of-Apogee-Therapeutics
- https://finance.yahoo.com/healthcare/articles/abbvie-completes-acquisition-apogee-therapeutics-123400899.html
- https://www.biospace.com/press-releases/abbvie-completes-acquisition-of-apogee-therapeutics

**Ingestion notes.** no usable final_growth
