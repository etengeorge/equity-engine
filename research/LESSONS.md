# LESSONS — self-critique that compounds (seeded 2026-08-22; no thesis has matured yet)

No thesis has reached its pinned evaluation window, so there are no scored patterns yet. The
retrospective rewrites this file once theses mature (12-36 month horizons; first grades expected
mid-2027). Until then, these are the STANDING priors the red team should hold the first analyst to:

- Small-cap mean-reversion theses are usually early. A margin trough is not a catalyst; a dated
  event that forces the market to re-price the margin is. Horizon under 12 months on a
  cyclical_mean_reversion call is almost always wrong.
- expectations_sentiment theses have the weakest base rate: "the market is too negative" needs a
  specific, dated reason the negativity resolves, or it is not a thesis.
- A reverse-DCF gap that flips sign inside the +/-15% FCFF band is noise. Conviction is capped
  at 2 mechanically; do not argue it back up.
- The market is usually right about a small-cap with fewer than 3 analysts. Coverage gaps cut both
  ways: less competition for the idea, but also less forced re-rating when you are right.
- One-time items (tariff refunds, legal settlements, insurance recoveries, asset sales) inflate
  normalized FCFF. Every gap over 40% is a data question first.
- Sources: a single uncorroborated story is a lead, not a fact. Two independent sources or an
  8-K is the bar for re-rating.
- A peak can fill the whole window. The peak-cycle flag compares the newest FCF in the window
  to the oldest, so it stays silent when all three years sit at an elevated level — the case
  that matters most. Before accepting a stable FCFF base, check it against the company's
  pre-window history, not just against itself. (Added 2026-08-31 from the BBW pass: three flat
  years at ~$38M, no flag, against a fiscal 2018 pre-tax LOSS and $1.6M of pre-tax income in
  fiscal 2019. Flat is not the same as normal.)
- The balance sheet is as stale as the fiscal year end, and nothing flags it. Three of ten names
  on 2026-08-31 had an enterprise value or a share count invalidated by a transaction that closed
  AFTER the last 10-K: ACR's manager internalization (share count +88% three days after the
  `shares_asof` date), SSRM's $1.49B Çöpler sale (EV overstated ~$2.2B, and the non-controlling
  interest still in the extract belongs to an asset that was sold), ALKS's Avadel acquisition
  ($1.525B of term loans drawn six weeks after the year end, so the model reports EV *below*
  market cap). `fundamentals_age_days` is printed but not acted on. Read the 8-K list before
  trusting any EV: items 2.01, 1.01 and 3.02 in the last two quarters are the tell.
- A gap on a financial is a bug until the equity line is decomposed — but decompose it against
  the FILING, not by assuming. `justified_pb` computed tangible common equity as equity −
  goodwill − intangibles and deducted neither non-controlling interests nor preferred. Preferred
  always belongs out. NCI only sometimes does, and which it is depends on the XBRL concept the
  extractor happened to pick: `StockholdersEquity` is parent-only and already excludes NCI,
  while `StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest` and IFRS
  `Equity` include it. JXN's carries $533M preferred and $389M NCI (TBV/share $146.95 against a
  correct $133.34) and needs both deducted. MFIN's does not: its balance sheet reads "Total
  stockholders' equity 408,617" with "Non-controlling interest 99,429" listed SEPARATELY below,
  and its $10.46 was right all along — deducting would have understated tangible book 41%.
  **This is the correction to a claim previously recorded here, that the omission "silently
  overstates cheapness across all 338 Financials". It does so only for the subset whose extract
  used an including-NCI concept, and on 2026-09-01 an analyst acting on the broad version of
  this lesson published a wrong verdict on MFIN — asserting a 71% overstatement of tangible book
  that did not exist.** A prior lesson is a hypothesis to test against the filing, not a
  conclusion to apply. `fundamentals()` now records `equity_concept` and `justified_pb` deducts
  NCI only when the concept includes it, flagging the name when the concept is unknown rather
  than guessing in either direction.
- GAAP net income is not a return for anything whose earnings are a mark. `justified_pb` averages
  three GAAP ROTCE ratios into a "sustainable" return; for JXN one of the three is 0.3%, because
  2025 GAAP was a $(17)M loss to common against $22.67 of adjusted operating EPS on non-economic
  hedge and MRB marks. The `unstable_rotce` flag names the symptom and the model averages the
  artifact in anyway. When one defensible input choice moves the answer from −48% to +77%, the
  output is not a valuation.
- Convertible notes are invisible to the debt extractor, and the error always reads as cheapness.
  `FIELDS["total_debt"]` covers the LongTermDebt* / Borrowings family and `debt_current` covers
  DebtCurrent and LongTermDebtCurrent; neither touches the `ConvertibleNotesPayable*` /
  `ConvertibleDebt*` concepts a convertible issuer actually tags. TDOC on 2026-09-01 reported
  total_debt of $42.4M against $996.7M of 2027 convertible notes sitting on the balance sheet —
  enterprise value understated 3.4x ($413M vs ~$1.41B), which moved the growth the market implies
  from −43.0% to −15.8%, and to −2.0% with stock comp expensed. The whole +220% gap that won it an
  opportunistic slot was missing debt. Missing debt lowers EV, lowers implied growth and
  manufactures a positive gap every time, so this bug does not produce noise, it produces false
  buys. A scan for non-financial FCFF names whose interest expense cannot be serviced by the debt
  the model can see returned 142 of them, with gaps like BIPC +1962%, COLL +1702%, RPD +413%,
  UPBD +202%. Treat any large positive gap on a known convertible issuer as this bug until proven
  otherwise, and check interest_expense / total_debt as the cheap detector.
- The EX-99 exhibit path has never returned anything, and the brief says so in language that reads
  like a fact about the company. `filing_documents` keys off `item["type"]` from EDGAR's directory
  `index.json`, but that endpoint carries no exhibit type and no description — its `type` field is
  the icon filename (`"text.gif"`, `"compressed.gif"`). So `d["type"].startswith("EX-99")` is never
  true for any filing, and every brief prints "No EX-99 exhibits filed under a material 8-K item"
  regardless. All ten names on 2026-09-01 printed it while filing 8-Ks under items 2.02 and 9.01.
  ANF's Q2 press release was sitting in that same directory as `q22026pressrelease.htm`, 416KB, and
  it contained the fact that decided the name: $100M of one-time IEEPA tariff refunds inside a
  headline EPS beat. `adhoc.py` calls the same function, so the workaround is to fetch the filing
  directory index and then the exhibit URL directly. The exhibit type lives in the SGML header
  (`<accession>-index-headers.html`), not in the directory listing.
- One-time tariff refunds are a 2026 cohort event, not a company story. ANF (~$100M pre-tax in Q2,
  $1.75/share, $120M and $2.10/share guided for the year) and CRI ($132M including interest inside
  H1 operating cash flow, with the tax payable the following quarter) both appeared in the same
  ten. Both flattered headline results while the underlying line went the other way — ANF's
  ex-refund Q2 operating income was ~$153M against $168M adjusted a year earlier. When one name in
  a screen shows an IEEPA refund, check every other importer in the cohort before reading any
  earnings beat as operating improvement.
- Before carrying a prior verdict forward, go and get the observable the last devil's advocate
  nominated. The 2026-08-31 morning pass on BBW named the settling evidence exactly — "revenue
  falling while pre-tax margin compresses" — and then recorded that it was "not yet visible". It
  was visible and one search away: Q2 gross margin −340bp to 54.2% on occupancy deleverage and
  promotions, pre-tax income $11.6M vs $15.3M. The verdict went cheap → no_edge on the afternoon
  pass. A red team that names its own test and never runs it is doing half the work.
- Rental and leasing fleet purchases are invisible to the capex extractor, and the error always reads as
  cheapness. CTOS's `capex_series` is [$0.87M, $3.07M] — under $4M across two years for a company that
  bought $191.6M of rental equipment in the six months to 2026-06-30 and guides $170-200M of NET fleet
  investment for 2026. The extractor takes only non-rental property capex, so every dollar of fleet
  spending stays in CFO. The model therefore reported a $241.5M normalized FCFF base against the
  company's own guidance of levered free cash flow "in excess of $50 million", and the whole +184% gap
  and 95th-percentile cohort rank came from that. ALTG has the same shape ([$9.2M, $15.4M, $12.4M] for a
  dealer with a rental fleet). Understated capex overstates free cash flow and manufactures a positive
  gap every time, so like the convertible bug this produces false buys, not noise. Suspect it on any
  equipment rental, leasing or fleet name; the cheap detector is capex as a percentage of revenue against
  the fleet purchases disclosed in investing activities.
- Revolver and ABL balances get dropped from `total_debt`, and the same interest-coverage detector catches
  it. ALTG's extract records $497.2M — the $500M of second-lien notes net of issuance costs — while the
  2026-06-30 10-Q reports $730.6M of debt and finance leases, because the $209.6M line of credit is
  missing entirely, and $85.2M of used/rental floor plan sits outside both. `interest_expense / total_debt`
  reads 17.8% against stated coupons of 9.00% and 5.3%, which is impossible. Screening the universe for
  an implied rate above 12% together with a gap above +50% returns 25 names, including UPBD, COLL, THRY,
  HOV, ARKO, BXC, STNG and UVV — several already flagged as convertible suspects, which suggests one
  detector is finding two different missing-debt bugs. Missing debt lowers EV, lowers implied growth and
  manufactures cheapness, always in that direction.
- A name under an announced all-cash merger is not a valuation, and nothing in the engine knows it. SLAB
  agreed on 2026-02-04 to be acquired by Texas Instruments at $231.00 cash, closing H1 2027; at $219.12 it
  is a 5.4% merger spread. The reverse DCF dutifully reported +48% implied growth and an -80.9% gap, and
  will keep reporting it every session until the name delists. The tape says it plainly without any news
  at all: 5d/21d/63d returns of +0.3%/+0.5%/+0.2% are a price pinned to a fixed number, not a market
  opinion about cash flows. Treat near-zero dispersion across all three return windows as a deal-stock
  tell and check for a pending acquisition before spending a slot.
- A failed beta regression still gets used, and on a financial it is the whole gap. GLRE's cost of equity
  of 6.5% comes from a beta of 0.31 whose R-squared is 0.068, recorded with `beta_source = regression` —
  the gate did not fire. Combined with a "sustainable" ROTCE of 10.6% averaged over a range the model
  itself flags as unstable (6.7%-14.6%), against a company whose book value per share rose 0.9% in six
  months, that produced a justified P/TBV of 1.91 against an actual 0.74 and a +170.8% gap. The tangible
  book was right — I verified it against the 10-Q — so this is the JXN pattern again: on a financial, check
  BOTH inputs to the justified multiple, not just the book value. OSCR carries the same defect (R-squared
  0.051). Note that the analyst JSON has no field to override cost of equity, so a name whose gap is
  produced by a bad beta cannot be corrected in the record — only the verdict can say so.
- **The failed-beta problem is not a handful of names, it is a ranking bias across the whole screen, and
  `BETA_MIN_R2 = 0.04` is why.** The GLRE and OSCR entries above treated a bad regression as a per-name
  defect where "the gate did not fire". The gate fired correctly; the threshold is the bug. An R² of 0.04
  means the regression explains 4% of the variance, so essentially every regression passes and is stamped
  `beta_source = regression`. A noisy regression attenuates its slope toward zero (classic errors-in-
  variables), so the worse the fit, the lower the beta, the lower the cost of equity, the lower the WACC,
  the lower the implied growth, and the larger the positive gap. Measured across the 1,644 regression betas
  in the 2026-09-03 screen, median gap by R² bucket: 0.00-0.10 → **+6.0%** (median beta 0.81, n=373);
  0.10-0.20 → −7.1% (beta 1.08); 0.20-0.30 → −28.1% (beta 1.10); 0.30+ → −33.4% (beta 1.01). That is a
  39-point swing in apparent cheapness driven by fit quality alone, monotonic across four buckets. 246 of
  the 373 worst-fit names carry a beta below 1.0, and 57 have beta < 0.9 together with a gap above +50%.
  Do not read this as "low-beta names look cheap": the top sector in that 57 is **Energy** (15 names —
  CRC, REPX, CRGY, TK, NVGS among them), which is the highest-beta cohort in the index, so this is
  measurement error and not genuine defensiveness. On 2026-09-03 it took ALL THREE Energy opportunistic
  slots — TDW (β 0.70, R² 0.082), RES (β 0.73, R² 0.085), PTEN (β 0.69, R² 0.061) — with gaps of +118%,
  +221% and +189%. Correcting TDW to a defensible OSV beta of ~1.4 moves the growth the market implies
  from +5.6% to roughly +16%, i.e. from cheap to rich. Like the convertible, ABL and rental-capex bugs,
  this error has a direction: it manufactures false buys, never false sells. Treat any large positive gap
  on a name with R² below ~0.15 as this bug until proven otherwise, and check `beta_r2` before the thesis,
  not after.
- **Averaging a ratio across a credit trough understates a recovered bank, the mirror of the acquisition
  case.** The `justified_pb` lesson above warns against averaging book LEVELS across an acquisition. VLY
  on 2026-09-03 is the same error running the other way in the numerator: sustainable ROTCE of 9.08% is a
  three-year average spanning the 2024-25 CRE provisioning trough, while the actual quarterly series runs
  9.07% → 10.02% → 11.56% → 11.91% (12.05% adjusted), improving monotonically over four quarters with
  tangible book per share compounding ~8% annualized. A reserve release flatters earnings while book value
  stagnates; rising ROTCE *and* rising tangible book together is an operating recovery. Overriding to 11.5%
  moves the gap from −36.4% to roughly −15%. The general rule: before accepting an averaged ratio on a
  financial, look at the quarterly path — a monotonic trend means the average is describing a company that
  no longer exists, in whichever direction it is trending.
- **The multiples fallback is not a weak signal on a transforming or non-operating company, it is noise
  with a decimal point, and its own internal disagreement is the tell.** CLAUDE.md already says to treat
  a multiples number on a pre-revenue name with suspicion. Two names on 2026-09-03 show the sharper test:
  when the three rows disagree by a factor of three, the blend is meaningless. RIOT blends to $10.12 vs a
  $18.64 price (−45.7%) while its own p_tbv row says $27.34 (+47%) and its ev_gross_profit row returns
  $-1.00 at every percentile because gross profit is negative — and the whole table prices bitcoin-mining
  revenue for a company that has just signed a 20-year, ~$9.1B power lease that has produced almost no
  revenue yet. EPRT blends to $21.40 from components of $26.63, $32.00 and $5.57, where the $5.57 is
  EV/sales applied to a REIT's rental revenue against a cohort median built from operating companies in
  the same Real Estate bucket. Both briefs also said "not ranked — too few comparable names". Rule: if the
  rows straddle the price in opposite directions, or any row is negative, or the cohort is unranked, report
  no_model and say the multiples number should be disregarded — do not average a nonsense input away.

---

*Carried forward from the previous engine. These are standing priors for the analyst to hold themselves to, not scored results — no thesis has matured yet.*
