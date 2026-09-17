# PJT — PJT PARTNERS CLASS A
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $152.60

**The case for the price.** PJT Partners is a premier independent advisory franchise — restructuring, strategic advisory and placement — whose earnings have compounded from $81.8M to $180.1M across the recorded window. Advisory firms are valued on earnings and on the quality of their bankers, never on book value, and the market is doing exactly that. The 34.7x price-to-tangible-book the model computes is not a valuation signal; it is a category error.

**What changed.** Nothing that changes the conclusion. PJT filed its 10-Q for the quarter ended 2026-06-30 on 2026-07-30 and reports 25,564,818 Class A shares outstanding as of 2026-07-27, against the 24,800,541 the engine carries from 2023-04-24.

**Base case.** No fair value and no ROTCE are supplied, because supplying either would launder a category error into a number. This is the PIPR case verbatim, and PJT was named explicitly in that standing lesson. Price-to-tangible-book is the wrong frame for an advisory firm: PJT's productive asset is a roster of bankers, expensed through compensation and carrying no balance-sheet value, so its $4.40 of tangible book per share is a working-capital balance rather than a capital constraint on revenue. The model reports an actual P/TBV of 34.66x against a justified 1.85 and a -46.7% gap; the cheap detector from that lesson — actual P/TBV above roughly 4x on a book-method name — fires at more than eight times the threshold. The goodwill_and_intangibles_64%_of_book flag is the model fighting itself: those intangibles are the acquired advisory franchises that generate the fees, and stripping them to reach 'tangible' book deletes the productive asset before dividing by it. No ROTCE rescues this: the recorded 152% return is arithmetic on a denominator that has been defined away.

**Devil's advocate.**
- Strongest counter: That refusing on a -46.7% gap costs nothing and hides a real signal — if PJT genuinely is expensive, no_model buries a useful sell.
- What would prove it: A valuation on the right frame: fee revenue, compensation ratio and earnings, which is how the market actually prices advisory firms.
- Already visible today: The inputs for that exist in the filings, but this engine has no path to it — method is assigned per GICS sector and 'Financials' routes every name to justified price-to-tangible-book. Note that refusing is NOT a judgment that PJT is cheap; on 34.7x tangible book and a cyclical fee stream it may well be expensive, and I decline to smuggle that conclusion in through inputs I have just argued are unusable.
- Left unresolved: Everything about the valuation, by construction. The correct fix is a method assignment, not an analyst override.

**Key risks.** advisory revenue is cyclical and lumpy; compensation ratio above 60% limits operating leverage; the engine will re-run this category error every rotation until the method assignment changes
**Watch for.** a method reassignment for advisory, payments and fintech names out of the book bucket

**Data quality.** RESOLVED as no_model on the PIPR rule: actual P/TBV of 34.66x is more than eight times the ~4x threshold at which price-to-tangible-book stops describing the business. share_count_1242d_stale is also real and independently disqualifying — PJT is an Up-C, the engine's 24,800,541 is the 2023-04-24 Class A count against 25,564,818 at 2026-07-27, and neither figure includes the PJT Partners Holdings LP units held by partners, so market capitalisation is understated by the unexchanged partnership interest. rotce_override is deliberately left null.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1626115/000162611526000045/pjt-20260630.htm (10-Q, 2026-06-30: cover page share counts, equity)
- 10-K for 2025 filed 2026-02-26
- research/LESSONS.md — the PIPR standing lesson, which names PJT Partners explicitly

**Ingestion notes.** no usable final_growth
