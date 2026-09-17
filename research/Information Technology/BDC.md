# BDC — BELDEN
*Information Technology · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $112.52
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Belden reported record Q2 2026 on AI data-centre and industrial-automation demand and has just bought RUCKUS Networks for ~$1.9 billion, roughly 40% of its own pre-deal enterprise value. The market is paying for a materially larger, more software- and wireless-weighted business than the one the engine's three-year cash-flow history describes, which is why a standalone reverse DCF reports a +22% growth requirement.

**What changed.** ON 2026-07-01 — THREE DAYS AFTER THE BALANCE SHEET THE ENGINE PRICED — BELDEN ACQUIRED RUCKUS NETWORKS FOR APPROXIMATELY $1.9 BILLION, funded entirely by a new Term Loan Credit Facility at SOFR+2.25% maturing 2033. The 10-Q states explicitly: 'We are in the preliminary phase of the purchase accounting process... As such, we cannot provide the estimated fair value of the assets and liabilities acquired for this business combination at this time.' Separately, in H1 2026 Belden issued EUR450M of 4.250% 2033 notes and repurchased the 3.375% 2027 notes.

**Base case.** No fair value is supplied because the enterprise changed size by roughly 36% three days after the balance sheet date and the company itself has not yet published what it bought. Enterprise value is recorded as $5.28B from market cap plus $1,230.6M of balance-sheet debt less $348.7M of cash; adding the ~$1.9B term loan that funded RUCKUS gives a true EV of about $7.18B. The cash-flow base is standalone Belden and contains not one dollar of RUCKUS, so any reverse DCF here divides a combined-company enterprise value by a single-company cash flow. The sensitivity is the whole answer: at the corrected EV against the standalone base the market implies +22.2%, and allowing a plausible RUCKUS contribution it falls to about +10% — and I have no disclosed figure for that contribution, so I will not invent one. There is also a second, independent defect that I did verify and that has its own direction: interest_expense is recorded as NEGATIVE $33,625,000 against an actual net interest expense of $27,058k for six months (~$54M a year), so the after-tax add-back SUBTRACTS about $27M from the base instead of adding about $43M. Correcting that alone takes the standalone requirement from +22.1% to +14.1% — i.e. most of the -51.4% gap is a sign error, not an opinion about Belden.

**Devil's advocate.**
- Strongest counter: That I am refusing a name the model calls expensive and therefore costing nothing — the lazy refusal. If the honest correction is that Belden must grow FCFF +22% standalone to justify today's price, that is a defensible SELL and no_model buries it.
- What would prove it: RUCKUS's standalone revenue and EBITDA, and the completed purchase price allocation.
- Already visible today: No. The company states in terms that it cannot yet provide the fair value of assets and liabilities acquired, and the 10-Q was filed 2026-07-30, four weeks after closing. There is no public combined figure to reason from.
- Left unresolved: Whether the combined entity requires +10% or +22%. That is the entire question and it turns on a number nobody has published yet. Refusing is NOT a judgment that Belden is cheap — at 4.25x sales and a leveraged balance sheet it may well be expensive; it is a statement that no row on this page can be believed.

**Key risks.** ~$1.9B of new floating-rate term debt on a company that previously carried $1.23B of fixed low-coupon subordinated notes; purchase accounting incomplete, so goodwill and intangible amortisation are unknown; the acquired business competes with far larger enterprise-networking vendors; the engine will keep pricing a standalone Belden against a combined enterprise value every session until the extract refreshes
**Watch for.** the 3Q26 10-Q with the preliminary purchase price allocation and the first consolidated RUCKUS quarter; total debt on the next balance sheet — the term loan should take recorded debt from $1.23B to roughly $3.1B

**Data quality.** RESOLVED: 'none raised' was wrong on both counts. (1) interest_expense is NEGATIVE $33,625,000 — a sign-inverted or net-interest-income concept — against an actual ~$54M/yr. This is a NEW direction on the ALTG/PATK implied-rate detector: the recorded implied rate is MINUS 2.73%, and because normalized_fcff adds after-tax interest back, a negative value SUBTRACTS ~$27M from the base and manufactures a false SELL rather than a false buy. The existing detector screens for rates above 12% and below 2% and does not test for a negative. (2) The RUCKUS acquisition closed 2026-07-01, three days after the 2026-06-28 balance sheet, adding ~$1.9B of debt invisible to enterprise value — the ALKS/balance-sheet-staleness lesson, and fundamentals_age_days looks unremarkable throughout. OPEN: RUCKUS's contribution to cash flow, which the company has not disclosed.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/913142/000091314226000063/bdc-20260628.htm (10-Q for the quarter ended 2026-06-28: Note 8 long-term debt, Note 14 subsequent events — RUCKUS ~$1.9B and the Term Loan Credit Facility, interest expense net $27,058k for six months)
- Q2 2026 EX-99.1 filed 2026-07-30
- company news in brief: record Q2 on AI data-centre demand, RUCKUS acquisition

**Ingestion notes.** no usable final_growth
