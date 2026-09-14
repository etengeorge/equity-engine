# WLTH — WEALTHFRONT
*Financials · Russell 2000*

Append-only research log. Newest entries at the bottom.

## 2026-09-14 — NO_MODEL (conviction: high)

- **Verdict:** no_model · price $10.38

**The case for the price.** At $10.38 the market is paying ~$1.6B of market capitalisation, roughly $1.15B net of $450M+ of cash, for a debt-free automated wealth platform that crossed $100 billion in total platform assets in August, grew funded clients 14% to 1.5 million, and has now posted sixteen consecutive quarters on the Rule of 40. It is GAAP profitable, generates $47.3M of operating cash flow a quarter, is buying back stock, and is extending from cash management and advisory into mortgage origination. At roughly 7.6x an annualised adjusted EBITDA of ~$152M for a business with that client growth, the price is not obviously stretched.

**What changed.** Fiscal Q2 2027 (quarter ended 2026-07-31, reported 2026-09-09): total revenue $91.9M, up just 1% year over year, while platform assets rose 12% to $99.0B — revenue is decoupling from assets as cash-management yield compresses. GAAP diluted net income POSITIVE $17.6M, down 49% from $34.7M. Adjusted EBITDA $38.1M, DOWN 15%, margin 41% from 49%. Stock-based compensation $16.4M against $1.6M a year earlier, from dual-trigger awards recognised after the December 2025 IPO. Repurchased 3.3 million shares for ~$30M. Wealthfront Home Lending launched in California, Colorado and Texas.

**Base case.** I am not supplying a growth rate or a return, because the model being applied to this company is the wrong model. Wealthfront is priced by the `book` method — justified price-to-tangible-book from sustainable ROTCE — and that frame assumes the balance sheet is the constraint on earnings, as it is for a bank. Wealthfront's tangible book is $4.12 a share of mostly corporate cash; its productive asset is a software platform and 1.5 million client relationships, neither of which is on the balance sheet. Supplying a ROTCE would launder that category error into a fair value.

**Devil's advocate.**
- Strongest counter: That a -145.1% gap and the 7th percentile of 338 Financials is the engine shouting that this is one of the most expensive names in the index, and refusing to model it lets an overvalued stock off the hook. There is something to that: revenue growing 1% against a $1.6B market capitalisation is a real concern, and adjusted EBITDA is falling.
- What would prove it: Whether the -145% gap contains any information about the price. It does not, and five independent defects say so.
- Already visible today: Yes, all five on the face of the data. (1) The sustainable ROTCE of -6.8% comes from ONE observation: equity_series has length 1 and net_income_series is a single -$42.1M — the AII n=1 problem, where a one-observation return is silently the most confident-looking input on the brief. (2) That single observation is the fiscal year ended 2026-01-31, which contains the December 2025 IPO and a one-time stock-compensation charge of $259.8M against revenue of $365.0M — the GAAP loss IS the IPO award recognition, and operating cash flow in the same year was POSITIVE $152.2M. (3) The company is GAAP profitable right now: $17.6M of net income this quarter. (4) The negative ROTCE produces a justified price-to-tangible-book of -1.14, i.e. the model asserts the equity is worth less than nothing — the same arithmetic breakdown recorded for BETR, CD, MQ and FLYW. (5) The beta is the sector median because there is insufficient price history, the company having listed nine months ago. On top of all five, the book method is a category error here for the PIPR reason: this is a fintech whose capital is not its balance sheet.
- Left unresolved: Whether Wealthfront is actually expensive. I record explicitly that refusing to model it is NOT a judgment that it is cheap — revenue growing 1% while adjusted EBITDA falls 15% is a genuine concern, and at ~7.6x adjusted EBITDA that EXCLUDES $65M a year of run-rate stock compensation, the real multiple is closer to 13x. I cannot convert that into a defensible fair value with the tools here.

**Key risks.** Revenue +1% against platform assets +12% — the cash-management spread is compressing and advisory has not yet replaced it; Adjusted EBITDA -15% year over year with margin down 8 points; the Rule of 40 streak is being carried by growth, not profitability; Stock compensation stepped from $1.6M to $16.4M a quarter post-IPO and is permanent dilution excluded from every adjusted figure
**Watch for.** Revenue growth re-accelerating toward asset growth as advisory mix rises; Adjusted EBITDA margin stabilising above 40%; Home Lending origination volume and whether it carries its own cost base

**Data quality.** NO FAIR VALUE AND NO ROTCE SUPPLIED, deliberately. Flags raised were `loss_year_in_window`, `beta_from_sector_median_0.87(insufficient_history)` and `volume_3.3x_its_60d_average`; all three are correct and all three understate the problem. The -145.1% gap and 7th-percentile cohort rank are produced by a single-observation ROTCE of -6.8% drawn from an IPO year whose $42.1M GAAP loss is a $259.8M one-time dual-trigger stock-compensation charge, against $152.2M of positive operating cash flow in the same year and $17.6M of GAAP net income in the most recent quarter. The resulting justified price-to-tangible-book is NEGATIVE (-1.14). Per the standing PIPR lesson I report no_model and decline to supply a ROTCE, because supplying one would convert a category error into a published fair value. Note also that this row sits inside the cohort distribution every other Financial is ranked against, including RDN's 96th percentile in the same session.

*Horizon: 24 months — re-evaluate no earlier than that unless something on the watch list fires.*

**Sources.**
- https://www.sec.gov/Archives/edgar/data/1524566/000162828026061131/wlth-20260909.htm
- https://www.sec.gov/Archives/edgar/data/1524566/000162828026042874/wlth-20260430.htm
- https://www.sec.gov/Archives/edgar/data/1524566/000162828026027232/wlth-20260131.htm

**Ingestion notes.** no usable final_growth
