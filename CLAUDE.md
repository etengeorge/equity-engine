# CLAUDE.md

Guidance for Claude Code working in this repository.

## What this is
A screener for the ~1,956 names in the Russell 2000. It prices every one of them off free
data every morning, ranks where price and history disagree most, and spends real reasoning
on ten names a day. It **recommends; the human decides and executes.**

The whole point is finding a large delta between a defensible intrinsic value and the
market price. There does not have to be one. Most days there isn't.

## Hard rules
1. **Never place, modify, or cancel a trade.** No order-placement code path exists and none
   may be added. If asked to trade, refuse — execution is the human's job, by design.
2. **The math is the truth-teller, not the narrative.** When a story and the cash flows
   disagree, the cash flows decide. Never talk the system into a conclusion the numbers
   don't support.
3. **Refusing is a feature.** `no_edge` and `no_model` are correct, expected, common
   outputs. Roughly 40% of this universe (financials, REITs, cash-burning biotech) cannot
   be honestly valued by a free FCFF model, and the engine says so rather than guessing.
   A flagged name is not a clean answer.
4. **Free sources only.** SEC EDGAR XBRL and free end-of-day prices. Never scrape a
   paywalled source. Respect SEC rate limits — `SEC_USER_AGENT` is required and the client
   throttles below 10 req/s.
5. **Never commit secrets or personal data.** Credentials come from `os.environ`, never
   from a tracked file, a log, or a prompt. No holdings, cost basis, or account data in
   the repo — ever.
6. **Never report success you did not verify.** A run that produced no research must fail
   loudly. The previous version of this project reported 27 consecutive green runs while
   silently persisting nothing, and that is the failure this design exists to prevent.

## Commands
```bash
export SEC_USER_AGENT="equity-engine <your-email>"   # SEC 403s anonymous clients

python run.py screen           # price + value all 1,956 names. No LLM. ~5 min.
python run.py screen --limit 40  # a fast slice while developing
python run.py news             # company + sector + market + macro news into data/news/
python run.py pick             # choose today's ten, write briefs/<TKR>.md
python run.py record --clean   # ingest synth/<TKR>.json into research/ + data/verdicts/
python run.py site             # rebuild public/: the screen + a page per researched name
python run.py status           # what state is this repo in
python run.py daily            # screen + news + pick (what the GitHub Action runs)
python run.py daily --skip-news  # same, on price signals only

# From the analyst runtime, which has no internet: dispatch the adhoc-fetch workflow
# with {tickers, what: filings|news|url|all}, wait, git pull, read data/adhoc/<TKR>/.
python adhoc.py --tickers ACR --what filings   # what that workflow runs
```

## Architecture

**The spine is one model run two ways.** `valuation.py` holds a two-stage FCFF model.
Run it backwards (`reverse_dcf`) and it solves for the growth rate that reproduces today's
enterprise value — that is what the market assumes. Run it forwards (`forward_dcf`) with
an assumption of your own and compare. The difference is the only thing this engine looks
for. `screen.py` does the backwards pass for everything; `record.py` does the forwards
pass with the analyst's number.

**Two speeds, because 1,956 names cannot all get judgment.** `screen.py` costs zero LLM
tokens: one bulk price pull, cached EDGAR extracts, pure arithmetic. Its forward
assumption is a deliberately dumb baseline (the company's own revenue history) whose only
job is ranking. `daily.py` then spends the ten expensive slots — six rotation (guarantees
the index eventually gets covered), four opportunistic (guarantees we are not blind to a
name that just halved). Every pick records why it was picked.

**Three valuation methods, chosen by what the accounting supports.** `fcff` for operating
companies. `book` for financials — justified P/TBV from sustainable ROTCE, because free
cash flow to the firm is meaningless when debt is raw material. `none` for REITs and
anything with negative normalized cash flow. The method is set per sector in
`universe.csv` and can still degrade to no-number at run time when the data gates fail.

`research/LESSONS.md` holds standing priors about how these theses fail, carried forward
from the previous engine and read by the analyst before every session.

**Memory is a folder tree.** `research/<Sector>/<TICKER>.md` is append-only, newest at the
bottom. `brief.py` feeds each name its own history *and* prior verdicts on its sector
peers, so the second pass through the index is better informed than the first. Context is
capped per section — v1 of this project silently truncated a 90k-character prompt and the
memory layer never reached the analyst. `dashboard.py` mirrors that same tree into the
Research tab (`public/research/<sector-slug>/<TICKER>.html`), so the site is a view of the
folders rather than a second copy of them: anything committed to `research/` appears on the
next `site` build, with no separate index to keep in sync.

**News comes from three sources because no free feed covers a small-cap index.**
`news.py` runs between `screen` and `pick`, so selection can react to what happened
overnight. Yahoo has no bulk news endpoint — it is one request per ticker — so a
*company* pull is spent only on names that moved, traded abnormal volume, filed an 8-K,
or are today's picks (`news.candidates`, capped at `NEWS_MAX_COMPANY_PULLS`). The other
~1,500 names are covered by the eleven SPDR *sector* ETFs, whose holdings map 1:1 onto
the GICS sectors in `universe.csv` — eleven requests buy sector news for the whole
universe. *Macro* comes from keyless government feeds (Fed, SEC, BLS, Federal Register),
which are the events that move a whole cohort at once. Every source degrades on its own:
an empty store means selection falls back to exactly its old price-only behaviour, and
the brief says "no news found" rather than omitting the section.

**Investor-relations decks come from EDGAR, not from IR sites.** There is no free index
mapping a ticker to its IR page, and those pages are per-company, JavaScript-rendered
and often bot-blocked — scraping 1,956 of them yields silent nothing for most. The deck
is filed anyway: under 8-K Item 2.02 or 7.01, EX-99.1 is the press release and EX-99.2
is usually the presentation. `edgar.exhibits_for` reads those, and they do not move.

**The daily job is split across two runtimes on purpose.** A GitHub Action
(`.github/workflows/screen.yml`) has real internet and does all the fetching and
arithmetic, then commits. The Claude routine (`ROUTINE.md`) only reads the clone and
reasons. This survives the failure that killed the previous version: a scheduled
environment with no network egress.

**The analyst gets internet on request.** Because that split leaves the reasoning half
unable to open a filing, `.github/workflows/fetch.yml` (`adhoc.py`) is a
`workflow_dispatch` job the analyst triggers mid-session: it fetches filings, exhibits,
news or an arbitrary URL on a machine that can reach them, commits to `data/adhoc/`, and
the analyst pulls. Roughly ninety seconds. Use it whenever an input actually decides a
number — on 2026-08-31 ten verdicts were capped at low conviction by documents that were
one dispatch away.

**The two runtimes shake hands through `data/ready.json`.** They run on independent
schedules and neither can see the other. The Action writes what completed, when, and
which trading session the prices are from; the analyst stops if that file is missing or
stale. It had been inferring readiness from a date stamp, which passed on a day the
scheduled run fired seven hours late.

**The screen runs pre-market (7:23am ET) so prices are always the prior close.** Two
cron entries cover both DST offsets and a guard step drops whichever is not 7am Eastern.
Running intraday let one name report two different prices on one calendar day.

## Things that are easy to get wrong here
These are all real bugs that were found and fixed; do not reintroduce them.

- **Alias order must never beat recency.** `edgar._series` picks the XBRL concept with the
  most recent data, not the first one listed. Commercial Metals still populates `Revenues`
  with FY2011 values; first-match-wins handed back 15-year-old revenue as current.
- **Average ratios, not levels.** `justified_pb` averages per-year ROTCE and prices against
  the *latest* tangible book. Averaging book levels across an acquisition (UMBF: $3.5B →
  $7.7B) reported a bank at 4.5x tangible book when it actually traded at 2.05x.
- **A missing tag is not a negative number.** Absent `OperatingIncomeLoss` used to be read
  as a loss and blackballed profitable companies out of the model.
- **Capex tagging is industry-specific.** E&P, mining and utilities each use their own
  concept; a manufacturer-only alias list silently drops whole sectors.
- **Don't clamp a beta you can measure.** Low beta is gated on regression R², not on a
  floor. Clamping CALM's real 0.27 up to 0.60 would move its cost of equity ~200bp.
- **Absolute gaps are not comparable across sectors.** They shift with the equity risk
  premium and terminal growth, which are choices. That is why every gap is reported
  alongside a cohort percentile, which does not.
- **Not every annual report is a 10-K.** Foreign private issuers file 20-F and Canadian
  issuers 40-F. Filtering to `10-K` dropped *every* fundamental for ~90 names (Golar LNG,
  Scorpio Tankers, DHT), not just one field. Several of those are IFRS filers whose facts
  live under `ifrs-full` with entirely different concept names.
- **Share count comes from the cover page, not the annual period.**
  `dei:EntityCommonStockSharesOutstanding` is an instant fact filed with every 10-Q. Taking
  it only from the 10-K both missed companies that tag it quarterly and priced today's
  share price against a count up to a year stale — a real error in market cap once a
  buyback or a raise has happened, not a rounding one.
- **NaN is not valid JSON.** pandas returns NaN for every missing value and `json.dumps`
  writes a bare `NaN` token that Python accepts and every strict parser rejects. Screen
  output is sanitized before writing and written with `allow_nan=False`.
- **Never preemptively rewrite tickers.** Class-share symbols are repaired only after an
  empty download (MOGA → MOG-A); 263 universe names say "CLASS A" and nearly all of their
  tickers are already correct.
- **A cooldown override needs a floor and a freshness test.** `MATERIAL_EVENT_OVERRIDE`
  used to fire on any >20% move in `ret_5d` or `ret_21d`. A 21-day return barely changes
  day to day, so a name that fell 25% over three weeks re-qualified *every session* for
  the next three weeks and kept beating fresh names to a slot — on 2026-08-31 it cost
  three of the four opportunistic slots to names researched nine hours earlier. It now
  needs `MIN_REVISIT_DAYS` elapsed AND something genuinely new: a fresh 5-day move,
  abnormal volume, or a new 8-K.
- **News must never select a name on its own.** Coverage volume correlates with what is
  already priced, and this is a valuation screen. Both news terms in `urgency()` are
  multiplicative and gated on an existing positive score. Written additively — as they
  first were — "its sector is in the news" alone put a name with no gap into contention.
- **Read both yfinance news payloads.** 0.2.x returned a flat dict with
  `uuid`/`link`/`providerPublishTime`; 1.x nests under `content` with `pubDate` and
  `canonicalUrl`. `requirements.txt` pins a range, so handling only one shape means the
  news layer silently returns nothing after a routine dependency bump.
- **Dedupe the news store by article id.** Yahoo returns the same wire story every day it
  stays on the page. Without the id check the store grows by a full page per ticker per
  day — the difference between a 5 MB store and a 200 MB one inside a git repository.

## Honesty
State uncertainty plainly. "The screen flagged it" is not "it is cheap." "Tests pass" is
not "the reasoning is any good." The human paper-trades first to find out whether the
judgment has edge — support that, don't oversell it.
