# ASB — ASSOCIATED BANCORP
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-17 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $29.76 · fair value $19.75 · gap -33.6%
- **Sustainable ROTCE:** screen said +8.2%, analyst says +12.5%
- **P/TBV:** justified 1.12 vs actual 1.69 on tangible book of $17.59/share

**The case for the price.** Associated Banc-Corp has finished a multi-year balance-sheet repositioning and is now earning a normal regional-bank return: net income available to common of $121M in Q2 2026 against $108M a year earlier, and a return on average tangible common equity the company reports at 12.1-13.0% across recent quarters. At 1.46x tangible book for a 12.5% return against an 11.4% cost of equity, the market is paying a modest premium for a clean, recovered franchise.

**What changed.** Q2 2026 (2026-07-23): net income available to common $121M, $0.63 per share, up from $108M and $0.65 a year earlier; H1 net income available to common $237.5M against $207.2M, +15%. The company's own ROATCE series runs 12.54%/12.66%/12.12%/13.03%/15.04%/14.02%/12.96% across the disclosed periods. Nothing structural since.

**Base case.** The -60.8% gap is roughly two-thirds defect. The engine's 'sustainable ROTCE' of about 8.2% is a three-year GAAP average of [13.94%, 3.79%, 6.85%], and the 3.79% year is the one containing the balance-sheet repositioning the company announced in Q4 2024 — the loss on the mortgage portfolio sale, which its own non-GAAP reconciliation strips out as an 'announced initiative'. Averaging a return across a deliberate one-time repositioning describes a bank that no longer exists, which is the AX/EBC/AUB/VLY pattern for at least the sixth time. Associated's own return on average tangible common equity is 12.1% to 13.0%; I use 12.5%. The stale-book defect is present too: justified_pb prices against equity_series[0] of $4,975.3M while equity_now is $5,638.1M, so tangible book per share reads $17.59 against a true $20.38 and actual P/TBV reads 1.69 against a true 1.46. Correcting both, the justified multiple of 1.12 against an actual 1.46 leaves a gap of about -23%, not -61%. That residual richness is real but it rests almost entirely on the model's fixed 2% terminal growth in a Gordon form — the ENVA bias — and on an ROTCE choice inside a 12.1-13.0% band, so it is not a thesis.

**Devil's advocate.**
- Strongest counter: That I have over-corrected. The engine's average includes the repositioning loss because the repositioning was real cash: Associated destroyed several hundred million dollars of shareholder value selling mortgages at a loss, and a 'sustainable' return that excludes every such decision flatters serial repositioners. If ASB repositions again — and banks that do it once often do it twice — the through-cycle return is nearer 10% than 12.5%, at which the justified multiple is 0.86 and the stock is 40% rich.
- What would prove it: Whether the securities and loan portfolios are now positioned such that no further restructuring is needed — i.e. whether the AFS book still carries material unrealised losses that would have to be crystallised to redeploy.
- Already visible today: Not from what I read. The Q2 release gives the adjusted ROATCE series and names the Q4 2024 mortgage portfolio sale as the adjusting item, but I did not obtain the AFS unrealised loss position, which is where the answer to a repeat repositioning lives.
- Left unresolved: The repeat-repositioning risk, which is the difference between a -23% gap and a -40% one. Also unresolved: the model's fixed 2% terminal growth does more work here than the business does, and I have no way to override it in this schema.

**Key risks.** a three-year GAAP return history containing a deliberate loss-taking repositioning, which may recur; commercial real estate concentration typical of a $18B Midwest regional; $525M of preferred sits ahead of the common; the recorded fair value is computed on a tangible book 14% below the current figure and therefore overstates the richness
**Watch for.** any further announced balance-sheet repositioning or securities restructuring; ROATCE holding above 12% for four consecutive quarters, which would confirm the recovery is the run rate

**Data quality.** RESOLVED: last_10k_991d_old is COSMETIC, the HWC pattern — fy_end reads 2023-12-31 but the underlying series are current and the balance sheet is the 2026-06-30 10-Q. unstable_rotce_3.8%_to_13.9% is the real defect and, per the EBC rule, it should disqualify the model output rather than be reasoned past: the 3.8% year is the Q4-2024 repositioning. goodwill_and_intangibles_25%_of_book is ordinary for an acquisitive regional. Preferred of $525M is correctly deducted and net_income_common_series differs from net_income_series by exactly the $11.5M annual preferred dividend, so the AX numerator check PASSES. OPEN AND MATERIAL: the stale-tangible-book bug — equity_now $5,638.1M against equity_series[0] $4,975.3M — means the RECORDED fair value is built on $17.59 of tangible book against a true $20.38, so the published discount is roughly ten points too rich. The verdict, not the number, is the output.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/7789/ (Q2 2026 EX-99.1 filed 2026-07-23: net income available to common, ROATCE series, adjusted net income reconciliation, repositioning footnote)
- 10-Q for the quarter ended 2026-06-30 filed 2026-08-04
- data/fundamentals.json (equity_now vs equity_series, preferred, goodwill and intangibles as recorded)

**Ingestion notes.** no usable final_growth
