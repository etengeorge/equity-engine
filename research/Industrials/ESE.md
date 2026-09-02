# ESE — ESCO TECHNOLOGIES
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-02 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $267.63 · fair value $153.44 · gap -42.7%
- **Growth:** market implies +41.1%, analyst says +8.0% (delta -33.1%)
- **FCFF base overridden** by the analyst to $205.6M

**Scenarios.** Fair value at each growth case, across the discount rate.

| case | growth | 6.8% | 7.8% | 8.8% | 9.8% | 10.8% |
|---|---|---|---|---|---|---|
| bear | +2.0% | $168.73 | $139.48 | $118.86 | $103.53 | $91.69 |
| base | +8.0% | $219.63 | $180.80 | $153.44 | $133.13 | $117.47 |
| bull | +13.0% | $271.21 | $222.60 | $188.37 | $162.98 | $143.41 |

At the point WACC of 8.8%: bear -55.6%, base -42.7%, bull -29.6%
Across the whole grid the gap ranges -65.7% to +1.3% — that spread is the honest precision of this model, not the point estimate.

**The case for the price.** ESCO is a quality industrial compounder in the middle of the best stretch in its history, and it is priced like one. Q3 FY2026 sales rose 14% to $339M with 8% organic growth plus $23M from the Maritime acquisition, EPS of $1.26, and record backlog. Management raised full-year FY2026 guidance to $1.30-1.33B of sales and $8.30-8.40 of adjusted EPS — up 38-39% on fiscal 2025. The end markets behind that are aerospace and defence test, navy/maritime, and utility grid equipment, all of which have multi-year funded demand rather than order-to-order cyclicality. Low leverage gives it capacity for the pending Megger acquisition, expected to close in Q1 fiscal 2027. At $267.63 the stock is on roughly 32x that raised guidance, which is what the market pays for a defence-and-grid compounder growing earnings at nearly 40% with a record backlog and an accretive deal pending.

**What changed.** Q3 FY2026 results (2026-08-06): sales $339M (+14%, 8% organic), EPS $1.26, record backlog, full-year guidance raised to $1.30-1.33B sales and $8.30-8.40 adjusted EPS. The Megger acquisition is pending and expected to close in Q1 fiscal 2027. Two 8-Ks in the last two quarters carry structural items the model does not see: 2026-04-16 under items 1.01 and 3.02 (a material agreement and an equity issuance) and 2026-06-03 under items 1.01, 1.02 and 2.03 (a material agreement, its termination, and a new direct financial obligation) — consistent with financing arranged around the Megger transaction.

**Base case.** ESCO's underlying businesses grow high single digits organically and management is compounding on top of that with bolt-on acquisitions like Maritime and Megger. Utility grid investment and naval programmes are genuinely multi-year. Eight percent is roughly the organic rate the company just reported and close to its own five-year revenue CAGR of 8.4%, and I am not willing to underwrite acquisition-driven growth as if it were free — Megger has to be paid for. Where I differ most from the model is not the growth rate but the base it is applied to.

**Devil's advocate.**
- Strongest counter: The counter is that I am rescuing an expensive stock from the model's verdict by swapping in a better cash-flow base, and I should check whether the model was closer to right than I am giving it credit for. Even on the newest and best year of $205.6M, the enterprise value of $6.9B is 33.6x FCFF. Growing 8% for five years and then 2% forever does not come close to supporting that — the price still needs something like 25% compound growth. A 32x multiple on a company whose sales are $1.3B, in businesses where the customer is a government or a regulated utility with a procurement cycle, is a high price for predictability. So 'the base was wrong' does not rescue the name; it only moves it from absurdly expensive to expensive.
- What would prove it: Whether free cash flow actually runs at the $205.6M level or reverts toward the $91.4M and $54.5M of the two prior years. That spread — the peak-cycle flag says the newest year is 3.8x the oldest — is the whole question, and one good year is not a base.
- Already visible today: Yes, and it partly favours the devil's advocate. The peak-cycle flag is not noise here: the FCFF series is $54.5M, $91.4M, $205.6M and I am choosing to build on the highest of the three. The standing lesson that 'a peak can fill the whole window' cuts the other way too — but here the flag fired precisely because the newest year is an outlier, and I have not verified that $205.6M is repeatable rather than a working-capital release. What supports me instead is the reported 38-39% EPS growth and record backlog, which are independent of the cash-flow series.
- Left unresolved: Whether the FY2025 free cash flow of $205.6M is a run rate or a one-off, and what the Megger acquisition costs and adds — the price was not in anything I read. Both matter, and neither is resolved, which is why this is no_edge and not rich. I did not fetch ESCO's filings; the 8-K items 3.02 and 2.03 in April and June would tell me how Megger is being financed and whether the share count is about to change.

**Key risks.** Roughly 32x raised adjusted EPS guidance leaves no room for a guidance miss; the -15.9% 21-day move on no news shows the multiple is unsupported by yield; The FCFF history is $54.5M, $91.4M, $205.6M — one strong year is being treated as a base; Megger acquisition closing in Q1 FY2027 at an undisclosed price and undisclosed financing; An 8-K under item 3.02 in April 2026 means an equity issuance the share count in this model may not reflect
**Watch for.** Q4 FY2026 results and the first FY2027 guide; Megger deal terms, price and financing structure when it closes; Whether free cash flow holds near $200M or reverts toward the prior two years; Backlog conversion versus the record level reported

**Data quality.** Two flags, one raised and one not. The raised flag — possible peak-cycle base, newest FCF 3.8x oldest — is real and I engaged with it directly rather than dismissing it: the series is $54.5M, $91.4M, $205.6M, and I have nonetheless set fcff_base_override to the newest year because the two older years predate the Maritime acquisition and a materially smaller, lower-margin ESCO, so the three-year mean of $104.0M describes a company that no longer exists. That override is a judgement, not a correction, and it is the weakest input in this file. The flag the brief did NOT raise is staleness: fundamentals_age_days is 337, by far the oldest of today's ten and nearly a full year, because ESCO's fiscal year ends in September. So the annual cash-flow data predates three quarters of the 14%-growth year the company has just reported, while the balance sheet is current to 2026-06-30 — the same instant-versus-duration mismatch this engine has been bitten by before, in a milder form. Separately, the 2026-04-16 8-K carries item 3.02, an unregistered equity issuance, which may mean the share count underlying the $6.9B market cap is understated; I did not verify it and I am recording that I did not. The -70.6% gap and the 16th-percentile cohort rank should not be read as a signal on this name.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.stocktitan.net/news/ESE/esco-reports-third-quarter-fiscal-2026-fkj7cpqy58xu.html
- https://www.investing.com/news/company-news/esco-q3-2026-slides-record-backlog-drives-guidance-raise-93CH-4844810
- https://www.investing.com/news/transcripts/earnings-call-transcript-esco-technologies-posts-strong-q3-2026-results-93CH-4844616
- https://www.sec.gov/Archives/edgar/data/866706/000110465926092033/tm2621646d1_ex99-1.htm
