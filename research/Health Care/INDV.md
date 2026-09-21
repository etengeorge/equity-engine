# INDV — INDIVIOR PHARMACEUTICALS INC
*Health Care · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-21 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $34.88
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** At $34.88 the buyer is not pricing five years of Indivior's free cash flow. $8.13 of that price — 23% of it — is a special cash dividend already declared, payable on or about 2026-11-06 to holders of record 2026-10-30, contingent only on the Supernus merger closing (expected around 2026-11-02). The residual ~$26.75 buys 56.5% of a combined Indivior/Supernus on a fully diluted basis, funded in part with a $650M Citibank term loan. The case for the price is that SUBLOCADE is still growing, the cost-reset programme is real, and bolting on Supernus's CNS portfolio reduces single-product dependence — but none of that is a claim on the standalone entity the engine modelled.

**What changed.** Everything material, and none of it is in the model. On 2026-08-03 Indivior agreed to merge with Supernus Pharmaceuticals (1.5401 INDV shares per SUPN share; legacy Indivior holders ~56.5%, Supernus ~43.5% fully diluted; $650M term loan from Citibank, remainder from combined cash). On 2026-09-17 Indivior declared the $8.13 special cash dividend contingent on closing, which Supernus holders do not receive. An S-4 has been filed. Operationally, first-half 2026 operating cash flow was $220M against $233M, after $34M of litigation settlement payments; capex ran $27M with another $10-15M guided for the second half, mostly the new Raleigh, North Carolina manufacturing facility.

**Base case.** No fair value. Two independent reasons, either sufficient. First, the price contains a contracted cash payment six weeks away and a share of a company that does not exist yet; a standalone five-year FCFF growth rate is not the question the market is answering. This is a fifth variant of merger blindness and a genuinely new one — SLAB covers a pending all-cash TARGET, APGE a completed deal, BKH/LCII an all-stock target, PATK an all-stock ACQUIRER, and this is an all-stock acquirer whose own price carries a declared contingent special dividend. The tell is cheap and specific: a dividend press release whose headline says 'Payment of Special Dividend Contingent upon Closing of the Pending Merger Transaction'. Second, the engine could not value it anyway and said so: `status` is model_failed on `nonpositive_normalized_fcff` because `cfo_series` holds only TWO years, [-$27M, $36M], against `capex_series` [$66M, $29M], giving cfo-capex of [-$93M, +$7M] and a mean of -$43M. That two-year window is unrepresentative in both directions — the negative year reflects litigation settlement outflows, and the company generated $220M of operating cash flow in the first half of 2026 alone, more than the entire window suggests it earns in a year. Refusing here is not a judgment that Indivior is cheap or expensive; it is a statement that neither the engine's inputs nor a standalone frame can answer the question.

**Devil's advocate.**
- Strongest counter: That a stub valuation is perfectly possible and I am refusing work rather than a valuation. Strip the $8.13 and you are paying $26.75 for 56.5% of a combined entity; value Supernus separately, add the $650M of new debt, apply the guided synergies, and you have a number. That is the correct analysis and I agree it is the one a buyer should do.
- What would prove it: The S-4 pro-forma condensed combined financial statements, which give the combined balance sheet, the purchase accounting and the pro-forma cash flow the stub claim actually attaches to.
- Already visible today: The S-4 exists (Indivior filed one) and I did not read it — it was not in the filings the adhoc fetch returned and I chose not to spend a second dispatch on a name whose verdict it would not change. That is a limit on this note, not on the argument: the stub analysis needs a valuation of Supernus, which is outside this universe, outside this brief, and outside anything the engine holds.
- Left unresolved: What the combined entity is worth. I did not attempt it and I am recording that rather than gesturing at it. Also unresolved: whether the two-year cash-flow window's negative year is fully explained by litigation settlements — the 10-Q attributes $34M of the 2026 half to settlements and $65M to the 2025 half, which does not by itself bridge a -$27M annual CFO.

**Key risks.** 23% of the share price is a special dividend contingent on a merger closing; if the deal fails that payment does not happen; the engine will keep running a standalone DCF on a two-year cash-flow window until this closes or delists; SUBLOCADE concentration and an unresolved litigation history on the standalone entity; $650M of new term debt at the combined company
**Watch for.** the record date of 2026-10-30 and payment on or about 2026-11-06 — the dividend is the near-dated fact; shareholder votes at both companies and the S-4 going effective; post-close, whether the combined entity should re-enter this universe under new economics

**Data quality.** Three flags raised — `negative_fcf_year_in_window`, `lumpy_fcff_spread_2.3x_of_mean`, `nonpositive_normalized_fcff` — and the model correctly refused. They understate the problem in one direction and overstate it in another: the window is only TWO years long, which no flag says, and the negative year is litigation-driven rather than operational (H1 2026 CFO alone was $220M). Additional unflagged defects: `dep_amort_series` of [$10M, $29M] is 0.81% of revenue, an order of magnitude too small for a company building a manufacturing plant, so the multiples table's ev_ebitda of 16.1x is unreliable (the SND shape); and beta is 0.575 at an R-squared of 0.046, barely above the engine's own 0.04 gate. None of it matters against the merger, which no flag could have caught.

*Horizon: 6 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1625297/000162828026051895/indv-20260630.htm (10-Q 2026-06-30: net cash provided by operating activities 220 vs 233; litigation settlement payments $34M and $65M; capital expenditures and the Raleigh NC facility with $10-15M more guided for H2; forward-looking statements reference 'the proposed merger with Supernus')
- https://www.sec.gov/Archives/edgar/data/1625297/000110465926103278/tm2623753-1_s4.htm (Form S-4 — identified but NOT read; see devil's advocate)
- https://ir.indivior.com/news-releases/news-release-details/indivior-pharmaceuticals-inc-declares-special-cash-dividend (2026-09-17: $8.13 special cash dividend, record 2026-10-30, payable on or about 2026-11-06, contingent upon closing; Supernus stockholders do not receive it)
- merger terms (1.5401 INDV per SUPN share; ~56.5%/43.5% fully diluted; $650M Citibank term loan) from the 2026-08-03 8-Ks at https://www.sec.gov/Archives/edgar/data/1625297/000119312526329513/d28447d8k.htm and their EX-99.1/99.2 in data/adhoc/INDV, corroborated by TipRanks and Investing.com coverage of the 2026-09-17 release
- https://www.sec.gov/Archives/edgar/data/1625297/000162529726000028/indv-20260909.htm (8-K 2026-09-15)
- company news in brief: Zacks 2026-08-04 'INDV to Merge With Supernus, Beats on Q2 Earnings, Raises '26 Outlook'; Zacks 2026-08-21 on the Supernus merger and SUBLOCADE reliance; GlobeNewswire 2026-09-17 special dividend release

**Ingestion notes.** no usable final_growth
