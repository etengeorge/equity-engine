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
- A gap on a financial is a bug until the equity line is decomposed. `justified_pb` computes
  tangible common equity as equity − goodwill − intangibles and never deducts non-controlling
  interests or preferred, though both sit in the same record and are correctly subtracted in
  `enterprise_value`. ACR: $129.8M of NCI plus preferred against a ~$190M common book, giving a
  reported TBV/share of $58.37 against the company's own $26.76. JXN: $533M preferred and $389M
  NCI, TBV/share $146.95 against a correct $133.34. This is not a one-name error — it silently
  overstates cheapness across all 338 Financials.
- GAAP net income is not a return for anything whose earnings are a mark. `justified_pb` averages
  three GAAP ROTCE ratios into a "sustainable" return; for JXN one of the three is 0.3%, because
  2025 GAAP was a $(17)M loss to common against $22.67 of adjusted operating EPS on non-economic
  hedge and MRB marks. The `unstable_rotce` flag names the symptom and the model averages the
  artifact in anyway. When one defensible input choice moves the answer from −48% to +77%, the
  output is not a valuation.
- Before carrying a prior verdict forward, go and get the observable the last devil's advocate
  nominated. The 2026-08-31 morning pass on BBW named the settling evidence exactly — "revenue
  falling while pre-tax margin compresses" — and then recorded that it was "not yet visible". It
  was visible and one search away: Q2 gross margin −340bp to 54.2% on occupancy deleverage and
  promotions, pre-tax income $11.6M vs $15.3M. The verdict went cheap → no_edge on the afternoon
  pass. A red team that names its own test and never runs it is doing half the work.

---

*Carried forward from the previous engine. These are standing priors for the analyst to hold themselves to, not scored results — no thesis has matured yet.*
