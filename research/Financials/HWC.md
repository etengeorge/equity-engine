# HWC — HANCOCK WHITNEY
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-04 — NO_EDGE (conviction: low)

- **Verdict:** no_edge · price $75.60 · fair value $63.56 · gap -15.9%
- **Sustainable ROTCE:** screen said +13.9%, analyst says +14.0%
- **P/TBV:** justified 1.47 vs actual 1.75 on tangible book of $43.23/share

**The case for the price.** Hancock Whitney is a $6.1B Gulf South commercial bank compounding tangible book at a mid-teens return on tangible common equity, and at 1.75x tangible book the market is paying a modest premium for a franchise with genuine deposit quality across Louisiana, Mississippi, Alabama, Florida and Texas. It has just completed the all-cash acquisition of One Florida Bank, extending into the fastest-growing deposit market in its footprint. A bank earning ~14% on tangible equity against a ~10% cost of equity is worth more than book; the argument is only about how much more, and 1.75x is close to where profitable regional banks of this size trade. Nothing about the price requires an error.

**What changed.** The material event is an acquisition that closed AFTER the balance sheet the model uses. On 2026-05-15 (8-K item 1.01, 2026-05-19) Hancock Whitney agreed to acquire OFB Bancshares, parent of One Florida Bank. Regulatory and shareholder approvals followed in July (8-K item 8.01, 2026-07-20), and the transaction CLOSED EFFECTIVE 2026-08-01, announced 2026-08-03 (8-K item 8.01). Consideration was approximately $377.6M in CASH for common stock and options; systems conversion is scheduled for Q4 2026. Because it is cash, the share count is unaffected — but roughly $377.6M leaves the balance sheet and a substantial portion of it will be capitalised as goodwill and core deposit intangibles, which come straight out of tangible common equity. The model's 2026-06-30 balance sheet predates all of this. No company-specific news in the store for the last 90 days, which for a $6.1B bank means the wire was quiet rather than that nothing happened — the acquisition is evidence of exactly that gap.

**Base case.** Book-method name; my number is a sustainable ROTCE and it is in rotce_override. I use 14%, essentially agreeing with the engine's 13.9%. The engine computed it correctly from three years of net income to common ($486.1M, $460.8M, $392.6M) against tangible common equity of roughly $3.47B, $3.24B and $2.90B — a stable, mildly improving mid-teens return with no trough or peak distortion of the kind that broke VLY. I see no reason to override it. Directionally, One Florida Bank should be accretive to earnings and dilutive to tangible book, which roughly cancels in the ratio; I have not tried to model that precisely because the goodwill allocation is not yet disclosed.

**Devil's advocate.**
- Strongest counter: The case that the -16% gap is a real short signal rather than model noise: this is a bank that just paid $377.6M of cash — roughly 11% of its tangible common equity — for a bank in a market where deposit franchises are expensive, at a point in the cycle when Florida commercial real estate is deteriorating. That transaction reduces tangible book per share on day one, so the 1.75x actual multiple in the model is understated and today's true multiple is closer to 1.83x. On unchanged earnings power that makes the stock roughly 20% expensive rather than 16%, and the deal adds integration risk into a Q4 systems conversion.
- What would prove it: The Q3 2026 10-Q, which will show the purchase-price allocation: how much of the $377.6M became goodwill and core deposit intangibles, and therefore the real tangible book per share post-close. Then the Q4 conversion and the first two quarters of combined ROTCE.
- Already visible today: The acquisition and its cash consideration are visible and confirmed. The purchase-price allocation is not — it will not be until the Q3 filing. So the direction of the tangible-book effect is certain and its size is not.
- Left unresolved: Whether -16% (or -20% adjusted) is a signal at all. The justified P/TBV formula is (ROTCE - g) / (ke - g), and its sensitivity to the cost of equity dominates everything else here: at the model's 10.16% cost of equity the justified multiple is 1.46 and the gap is -16%; at 9.5%, entirely defensible for a bank with a 0.98 beta and an R-squared of 0.511, the justified multiple is 1.59 and the gap narrows to about -9%. A 66bp change in an unobservable input moves the answer by half. I cannot call a name rich on that.

**Key risks.** One Florida Bank integration and the Q4 2026 systems conversion; $377.6M of cash consideration is dilutive to tangible book per share on day one; Gulf South commercial credit — energy services, CRE, hospitality — normalising from benign levels; Deposit beta on the way down: NIM compression if funding costs lag rate cuts; Hurricane exposure across the deposit and lending footprint
**Watch for.** Q3 2026 10-Q purchase-price allocation for OFB Bancshares — the actual goodwill and intangibles created, and the resulting tangible book per share; Q4 2026 systems conversion completing without customer attrition; Any move in the provision or in criticised-asset balances across the commercial book

**Data quality.** The one flag on this name is a FALSE ALARM and I want that on the record, because it looked like the most serious defect in today's ten before I checked it. `last_10k_5361d_old` reads as though Hancock Whitney's fundamentals come from a 2011 annual report — the extract's fy_end is literally '2011-12-31' and fundamentals_age_days is 5,361. It does not. The underlying series are current and correct: net income to common of [$486.1M, $460.8M, $392.6M] and equity of [$4,460.1M, $4,127.6M, $3,803.7M] are recent-year figures, goodwill of $925.4M matches the post-Whitney franchise, and tangible book per share of $43.23 reconciles exactly to the 2026-06-30 balance sheet ($3.468B over 80.2M shares). I reproduced the 13.9% ROTCE from those numbers by hand and it is right. So `fy_end` is being mislabelled by the extractor on this filer while the data it drives are fine — a cosmetic bug in the flag, not a stale extract, and no verdict should be capped on it. What IS a genuine, unflagged staleness problem is the One Florida Bank close on 2026-08-01, one month after the 2026-06-30 balance sheet the model prices: $377.6M of cash out, goodwill and core deposit intangibles in, and therefore a tangible book per share that is overstated in the model by roughly 4-5% at a plausible allocation. This is the ACR/SSRM/ALKS pattern in research/LESSONS.md — read the 8-K list before trusting any book value — and it pushes the name further rich rather than rescuing it. The beta is the one genuinely reliable input here: 0.98 on an R-squared of 0.511, the best fit in today's ten.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.businesswire.com/news/home/20260803843833/en/Hancock-Whitney-Completes-One-Florida-Bank-Acquisition
- https://www.sec.gov/Archives/edgar/data/0000750577/000119312526329625/d118362dex991.htm
- https://www.sec.gov/Archives/edgar/data/0000750577/000119312526308486/d63138d8k.htm
- https://finance.yahoo.com/markets/stocks/articles/hancock-whitney-receives-regulatory-approval-130200316.html
- data/adhoc/HWC/ (8-K and 10-Q set fetched via adhoc-fetch)
- data/fundamentals.json CIK 750577 (stored EDGAR extract, v5)

**Ingestion notes.** no usable final_growth
