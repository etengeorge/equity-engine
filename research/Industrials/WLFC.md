# WLFC — WILLIS LEASE FINANCE
*Industrials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-08-31 — NO_MODEL (conviction: medium)

- **Verdict:** no_model · price $53.42
- **Not repriced:** not a repriceable fcff name or no growth supplied

**The case for the price.** Willis Lease owns and leases spare commercial aircraft engines into an aftermarket that has been structurally short of capacity since the pandemic: OEM new-engine deliveries are late, shop-visit turnaround times are long, and airlines are flying older airframes longer, all of which raises the lease rate and residual value of a spare CFM56 or V2500. That drove 2025 revenue of $730.2M, up 28.3% on 2024's $569.2M, and net income of $113.8M. The market's price reflects a levered spread business — $2.70B of debt against $662M of book equity — where each incremental engine bought at a spread over funding cost compounds book value, and it reflects the Q2 2026 crack in that story: EPS fell 53.4% year over year to $1.31, maintenance reserve revenue fell 8.4% to $46.5M with short-term reserves down 22%, and utilisation eased to ~85% as older engines flew less. The equity has de-rated roughly a third from its all-time high accordingly.

**What changed.** Three things since the last 10-K. (1) A three-for-one forward stock split: approved by shareholders 2026-06-23, record date 2026-07-06, implemented 2026-07-17, trading split-adjusted from 2026-07-20. (2) Q2 2026 results on 2026-08-04 showed the first material earnings decline of the cycle — EPS $1.31 vs $2.81, net income to common $28.7M vs $59.0M, driven by lower short-term maintenance reserve revenue as older engines saw reduced flying. (3) An 8-K on 2026-08-25 under item 2.01 (completion of an acquisition or disposition of assets) which I could not read. The stock is down roughly 16% since the Q2 print and about 23% over August.

**Base case.** I will not supply one, because the FCFF base the growth rate would be applied to is not a real number. See below.

**Devil's advocate.**
- Strongest counter: The counter to declaring this unmodellable is that WLFC is not a bank — it owns hard assets with observable residual values, reports EBIT and interest expense cleanly, and a normal FCFF model ought to handle a lessor the same way it handles a railroad or a shipping company. On that view I should fix the capex input rather than abandon the model, and the answer would be that a business earning $114M of net income on $662M of equity, marked at $1.1B of market cap, is not obviously mispriced either way.
- What would prove it: Reading the 2025 10-K cash flow statement and substituting the correct equipment-purchase line into the capex series, then re-running the reverse DCF. If corrected FCFF is materially negative — which is what a lessor growing its portfolio 28% a year should produce — the model is structurally inapplicable, not merely mis-parameterised.
- Already visible today: Yes, and it settles it against the model. The committed extract shows capex sourced from PaymentsToAcquirePropertyPlantAndEquipment at $31.1M / $15.6M / $5.1M against revenue of $730M / $569M / $419M. A company that grew its lease portfolio fast enough to add $161M of revenue in one year did not do it on $31M of equipment purchases. Engine purchases are tagged under a separate lessor-specific concept and the alias list misses them entirely, so CFO is being taken net of nothing. The resulting $350.2M FCFF base is roughly 48% of revenue, which no capital-intensive lessor produces.
- Left unresolved: I could not read the 10-K to state the correct equipment-purchase figure, so I cannot say what the corrected FCFF base is — only that it is far below $350M and plausibly negative. I also could not read the 2026-08-25 item 2.01 8-K, so I do not know whether a material asset sale or purchase has changed the balance sheet since Q2.

**Key risks.** The +176.7% baseline gap and the 93rd-percentile cohort rank are both artifacts of the broken capex input and should not be treated as signal; The reported beta of 1.53 and the 14.6% WACC derived from it are computed on a price series containing a fabricated -67% single-day move, so every discount-rate-dependent output for this name is unreliable; Genuine business risk is real and separate: maintenance reserve revenue is rolling over, utilisation is easing, and $2.70B of debt against $662M of equity leaves little room if lease rates normalise; Residual values on CFM56/V2500 assets fall quickly once OEM delivery schedules catch up
**Watch for.** A corrected capex alias covering lessor equipment purchases — until then this name cannot be screened at all; Q3 2026 maintenance reserve revenue and utilisation: a second consecutive decline turns a soft quarter into a cycle turn; The contents of the 2026-08-25 item 2.01 8-K

**Data quality.** Two separate defects, both of which I verified against the committed extract rather than inferring. FIRST, capex: the extract sources capex from PaymentsToAcquirePropertyPlantAndEquipment ($31.1M/$15.6M/$5.1M), which for an engine lessor captures office and shop assets and misses the purchase of equipment held for operating lease — the company's actual capital spending. FCFF is therefore reported as ~$350M when it is far lower and plausibly negative. This is exactly the 'capex tagging is industry-specific' failure already documented in CLAUDE.md, in a sector the alias list does not cover, and it will affect every lessor in the universe, not just this name. SECOND, the price history: the 3-for-1 split of 2026-07-17 was not applied to the pre-split series. The screen reports 63d -69.7% and 252d -64.5%; a -69.7% 63-day move implies a price of ~$176 around 2026-06-01, which is the unadjusted pre-split quote (~$58.8 split-adjusted). The stock's split-adjusted all-time high was $79.78 on 2026-07-06, so the true 63-day move is roughly -9%, not -70%. The 5d (-1.7%) and 21d (-26.2%) windows sit entirely after the split and are real. The share count (21,144,111 as of 2026-07-31) and the current price are both post-split, so market cap is correct; the momentum series, the beta and the WACC are not. The fabricated crash is part of why this name was pulled into an opportunistic slot. NO flags were raised on this name by the screen. I resolved neither defect by reading a filing — SEC egress is blocked from this runtime — but both are demonstrable from the committed extract and from free price data.

*Horizon: 12 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.tipranks.com/news/company-announcements/willis-lease-finance-announces-three-for-one-stock-split-2
- https://finance.yahoo.com/markets/stocks/articles/willis-lease-finance-corporation-shareholders-200100504.html
- https://www.tradingview.com/news/zacks:3c704df9a094b:0-wlfc-s-q2-earnings-fall-y-y-on-lower-maintenance-revenues/
- https://simplywall.st/stocks/us/capital-goods/nasdaq-wlfc/willis-lease-finance/news/willis-lease-finance-wlfc-stock-slips-as-margin-durability-q
- https://finance.yahoo.com/news/willis-lease-finance-corporation-reports-110100040.html
- data/fundamentals.json (committed EDGAR extract, CIK 1018164, fetched 2026-08-30)

**Ingestion notes.** no usable final_growth
