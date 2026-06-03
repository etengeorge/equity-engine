# SCALING.md — going from a watchlist to the full 2,000-name universe

The engine runs today on whatever tickers you pass. This is how to scale it to the
whole Russell 2000 without hitting rate-limit walls or burning hours per run.

## The core constraint (why you don't just loop over 2,000)

A scheduled run cannot deeply analyze 2,000 small-caps every time — SEC EDGAR
asks for ≤10 requests/second, each name needs several filing fetches plus prices,
and the synthesis step has real cost. A naive full loop would take hours and trip
throttling. The fix is **priority-driven coverage**: refresh the names where
something changed, rotate slowly through the rest.

## Step 1 — load the real universe

Replace the `--tickers` list with the IWM holdings pull. `config.IWM_HOLDINGS_URL`
is the official iShares CSV (refreshes daily). Parse the `Ticker` column, drop
cash/derivative lines, and resolve each to a CIK with `data_sources.resolve_cik`.

```python
import csv, io, urllib.request, config, data_sources as ds
raw = urllib.request.urlopen(config.IWM_HOLDINGS_URL, timeout=60).read().decode("utf-8","ignore")
# iShares CSV has preamble lines before the header row "Ticker,Name,..."
lines = raw.splitlines()
start = next(i for i,l in enumerate(lines) if l.startswith("Ticker"))
rows = list(csv.DictReader(lines[start:]))
tickers = [r["Ticker"].strip() for r in rows
           if r.get("Ticker") and r.get("Asset Class","Equity")=="Equity"]
```

**Implemented in `universe.py`.** Reality check: the iShares `.ajax` CSV endpoint above is
now gated behind a browser consent wall — a headless fetch returns a 3 MB HTML page, not CSV.
So `universe.load_iwm_universe()` is source-robust and tries, in order: (1) a **local holdings
file** you drop in — `IWM_holdings.csv` / `russell2000.csv` in iShares CSV format, or
`universe.txt` one-ticker-per-line; (2) the iShares URL, used only if it actually returns CSV
(HTML is rejected, never parsed to an empty list); (3) the SEC `company_tickers.json` all-filers
list — a labeled SUPERSET so the engine is never dead-in-the-water (the reliability/liquidity
gates still apply). **The faithful path:** download the IWM holdings CSV from ishares.com in a
browser (or via the Cowork/Chrome connector), drop it in the project, and the loader reads it.

## Step 2 — assign a review priority (don't touch everyone every run)

Add a `review_priority` per name, recomputed each run from cheap signals **before**
doing the expensive deep analysis:

- **High:** a new 8-K since last look, an earnings date within ~5 days, an insider
  cluster, or a prior thesis whose falsification condition may have triggered.
- **Medium:** stale coverage (not analyzed in N days).
- **Low:** everything else.

Checking "is there a new 8-K" is one cheap submissions call per name (or use the
EDGAR full-text/RSS firehose to get the day's filers in one shot, then intersect
with your universe — far fewer calls).

## Step 3 — batch each run

Each scheduled run processes: **all High-priority names + a rotating slice of the
cold tail** (e.g. 1/20th of the universe, so everything gets a deep refresh roughly
monthly even with no news). That keeps any single run bounded to a few hundred
names at most, which fits comfortably in the rate limits.

```python
todays_batch = high_priority + cold_tail_rotation(universe, fraction=1/20)
results = engine.run(todays_batch, llm_synth_provider=synth_provider, positions=positions)
```

## Step 4 — respect the limits in code

- Keep the built-in EDGAR throttle (the engine already paces ≤10 req/s).
- Add Tiingo (`PRICE_PROVIDER=tiingo`) instead of yfinance — far sturdier at volume,
  and free-tier/academic friendly.
- Cache the market series once per run (the engine already does).
- On any `429`/`503`, back off and skip that name for the run rather than failing
  the batch. Record the skip so it's high-priority next time.

## Step 5 — the cadences (three, distinct)

- **Daily (weekday):** the priority batch above → dashboard + email.
- **Per-earnings:** a name reporting gets force-promoted to High that day.
- **Weekly retrospective:** read theses whose `evaluation_window` has passed and
  score them on idiosyncratic excess (return vs a same-sector basket built from
  your own universe membership, not just vs zero). This is the "did it actually
  work" loop, and it's what the paper-trade gate uses.

## Reminder: the gate still applies at scale

Scaling to 2,000 names multiplies the multiple-comparison problem — more names
means more apparent mispricings by chance, and the most extreme gaps are
disproportionately data errors. Ranking stays reliability-weighted, extreme gaps
are treated as suspicious first, and **you paper-trade before funding.** More names
is more sourcing, not more edge; edge is proven on out-of-sample results.

## The two-speed model (how "watch all 2,000 every day" actually works)

A deep synthesis on one name (multi-source filings + live reasoning + web search) costs
30-90s and many API calls. Times 2,000 daily = infeasible on free tiers, AND overkill for
12-36 month theses. So the engine runs at two speeds (`scanner.py`):

**Speed 1 — cheap daily scan, whole universe.** For every name: one price/volume pull
(abnormal-move z-score + volume spike) and a re-priced DCF gap against the stored target
(pure arithmetic, no data pull). News/sentiment is checked only for names that already
moved, are held, or are uncovered — so the call budget stays bounded. This catches the
moves that matter ANY day (a short report, a pre-announcement, a sentiment spike), not
just scheduled filings/earnings.

**Speed 2 — deep synthesis, gated.** A name is promoted into the expensive queue ONLY
when: the scan found something material (abnormal move, volume spike, news/sentiment
trigger, or the re-priced gap crossed a buy/sell threshold), OR it's due on cadence
(twice a week), OR it's a held position whose gap crossed. Plus a cold-tail rotation
(~1/20th of no-signal names per day) so quiet stocks still refresh periodically.

So: **every name is WATCHED daily; only the ones where something moved get deeply
RE-ANALYZED.** That's daily responsiveness without the rate-limit wall.

## Dynamic DCF (twice a week, or on news)

The reverse DCF updates at two speeds too:
- **Daily (free):** the market-implied growth and the gap to your target re-price with
  the day's price — `analytics.quick_revalue()`. A 12% drop swings the gap immediately,
  which can flip a name into a buy on price alone. The TARGET is held fixed here.
- **Twice a week + on material triggers:** the full re-do re-pulls financials (a new
  10-Q changes the FCFF base), re-runs the synthesis (new growth/margin assumptions),
  and produces a NEW target price. `FULL_REVALUE_INTERVAL_DAYS` (default 3) sets the
  cadence; a material scan trigger overrides it. When a re-done target moves more than
  `TARGET_PRICE_MOVE_NOTABLE` (10%), that's surfaced as a notable revaluation — the kind
  of fundamentals-driven move that could justify a new buy.

Honest note: sentiment is a trigger to LOOK, never a reason to ACT. Social spikes are
often noise; the deep synthesis decides if the spike reflects something real, and the
anti-overtrading logic still gates whether your position changes. The scan widens
attention, not trading.

## Run it (implemented)

```bash
# Full universe. Drops to the SEC all-filers superset if no IWM_holdings.csv is present.
python routine.py daily --iwm --max-deep 30      # scan all; deep-synth the top 30 by priority
python routine.py daily --iwm --limit 200        # staged rollout: first 200 names only
python routine.py daily --iwm --refresh-universe # force a fresh holdings re-pull (ignore today's cache)
```

`--iwm` loads the universe via `universe.py`, fires ONE EDGAR daily-index **8-K firehose**
(`data_sources.recent_8k_filer_ciks`) so material filers are flagged by a set lookup instead of a
submissions call per name (Step 2, at scale), runs the cheap two-speed scan over everything, and
deep-synthesizes ONLY the promoted queue — capped at `--max-deep` (default `config.MAX_DEEP_PER_RUN`,
30); the rest roll to the next day, material movers first. Any name that errors mid-scan is skipped,
not fatal. On free yfinance the whole-universe price scan is slow and flaky; set
`PRICE_PROVIDER=tiingo` (free tier) for volume. Schedule the daily run as a Claude Code routine /
Cowork task (which also injects the live synthesis provider and the read-only Robinhood / Gmail /
Drive connectors — see CONNECTING.md). Everything stays recommend-only; there is no order path.

### Free, full coverage without cutting names (rotating batches)

To cover all ~2,000 on free tiers, don't price every name every run — **rotate**. `--batch N`
cheap-scans N names per run from a PERSISTED cursor that advances each run, so the universe
completes one full sweep every `ceil(2000/N)` runs. Schedule **2-3 runs/day** to shorten the cycle:

```bash
python routine.py daily --iwm --batch 300        # ~250-300 price pulls/run, free-tier friendly
```

- **Every run, regardless of the slice:** your **held names** are scanned, and the day's **8-K
  filers** (the firehose — one cheap EDGAR call) are fast-tracked straight to deep synthesis. So
  material events drive timely long/short recs without a universe-wide price pull.
- **Cycle math:** `--batch 300` × **3 runs/day** sweeps all ~2,000 every **~2-3 days**; held +
  event coverage is **daily**. Lower N to stay further inside free price/news limits.
- **The dashboard is a rolling board:** with `--iwm` it shows today's deep names + your holdings
  + the best **actionable recommendations accumulated in the store over the cycle** (capped at
  `config.MAX_BOARD_ROWS`), so it reads as a live long/short feed, not a 2,000-row dump. Stored
  rows are marked "scan only" until their slice comes round again.
- **Honest trade-off:** a name's price is only re-checked when its slice comes up (every ~2-3
  days) — a 1-day move on a cold-tail name can wait a couple days. Fine for 12-36 month theses,
  and anything that files an 8-K is caught the SAME day via the firehose. The cursor persists in
  `store/universe_cursor.json`; new index entrants and held names are always covered.

Run as 2-3 weekday Claude Code routines (e.g. 7am / 1pm / 6pm). Fully free: EDGAR + yfinance +
free news tiers, with news gated to names that moved / are held / are uncovered.
