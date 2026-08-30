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

python run.py screen           # price + value all 1,956 names. No LLM. ~20 min.
python run.py screen --limit 40  # a fast slice while developing
python run.py pick             # choose today's ten, write briefs/<TKR>.md
python run.py record --clean   # ingest synth/<TKR>.json into research/ + data/verdicts/
python run.py site             # rebuild public/index.html
python run.py status           # what state is this repo in
python run.py daily            # screen + pick (what the GitHub Action runs)
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
memory layer never reached the analyst.

**The daily job is split across two runtimes on purpose.** A GitHub Action
(`ci/screen.yml`; see `ci/README.md` for why it is parked there) has real internet and does all the fetching and
arithmetic, then commits. The Claude routine (`ROUTINE.md`) only reads the clone and
reasons. This survives the failure that killed the previous version: a scheduled
environment with no network egress.

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

## Honesty
State uncertainty plainly. "The screen flagged it" is not "it is cheap." "Tests pass" is
not "the reasoning is any good." The human paper-trades first to find out whether the
judgment has edge — support that, don't oversell it.
