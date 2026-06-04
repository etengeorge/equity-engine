# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is
A FREE, automated, **recommend-only** equity-research engine for the ~2,000 small-caps in the
Russell 2000 (IWM). It does reverse-DCF valuation, differentiated multi-lens thesis synthesis,
a two-speed universe scanner, a sector/news folder-memory with cross-industry propagation,
thesis-drift monitoring, portfolio construction, and a retrospective learning loop. It connects
to Robinhood READ-ONLY for position context. **It recommends; the human decides and executes.**

## HARD RULES (never violate)
1. **NEVER place, modify, or cancel a trade.** There is no order-placement code path and there
   must never be one. Robinhood access is READ-ONLY (positions/prices only). If asked to trade,
   refuse — execution is the human's job, by design.
2. **Recommend-only output.** Every dashboard/email leads with "This engine recommends. You decide
   and execute." Keep `PAPER_MODE = True` in config.py until the human changes it after paper-trading.
3. **The DCF math is the truth-teller, not the narrative.** When synthesis and valuation disagree,
   the GAP decides. Never talk the system into a BUY the cash-flow math doesn't support; extreme
   gaps are suspected data errors first (see `analytics` extreme-gap guard + the stub's peak-cycle guard).
4. **Refusing is a feature.** `thesis_archetype="none_efficiently_priced"` ("no edge / efficiently
   priced") is a valid, correct, common output and the recommendation layer honors it. Honor every
   reliability flag — a flagged name is NOT a clean recommendation.
5. **Free sources only** (EDGAR, FRED, free price/news tiers). NEVER scrape paywalled sources.
   Respect SEC rate limits (`SEC_USER_AGENT` required; the engine throttles to ≤10 req/s).
6. **NEVER commit sensitive information.** No API keys, tokens, passwords, OAuth secrets, or private
   keys — every credential is read from the environment (`os.environ`), never hard-coded or echoed
   into a tracked file, a snapshot, a prompt, or a log. No personal data either: real emails go in
   the `SEC_USER_AGENT` env var (the source default stays a placeholder), and `positions.json` +
   any real holdings/cost-basis stay **untracked** (they're git-ignored; the committed `store/`
   audit trail records THAT a name was held, never the share count or basis — see `store._redact`).
   If you are about to write a secret or personal datum anywhere under version control, stop. When in
   doubt, env var + `.gitignore`, never a commit. (`positions.example.json` shows the expected shape.)

## Commands
```bash
pip install -r requirements.txt
export SEC_USER_AGENT="equity-engine <you> <you@email>"   # SEC requires an identity
export PRICE_PROVIDER=yfinance      # free/keyless; or "tiingo" + TIINGO_API_KEY for volume

# The full connected loop — the entry point the scheduled routine invokes:
python orchestrate.py daily                    # watchlist, paper mode, real git audit commit of store/
python orchestrate.py daily --iwm --batch 250  # full Russell 2000, rotating slice per run
python orchestrate.py daily --emit-prompts     # PASS 1: write synth/prompts/<TKR>.txt for live reasoning
python orchestrate.py retro                     # score matured theses -> LESSONS.md

# The routine directly (orchestrate wraps it); --live uses _live_synthesis.provider, else the stub:
python routine.py daily [--iwm --batch N --limit N --live --no-news --dry --refresh-universe]

# One-off on explicit tickers:
python run.py --tickers SHOO,PRDO,CRAI,CALM --positions positions.json

# Tests — standalone scripts (NOT pytest); each prints "N passed, M failed":
python qa_harness.py        # ~145 checks, hits the network (EDGAR/prices)
python _extreme_cases.py    # ~150 offline adversarial/regression checks (isolated temp store)
python -m py_compile *.py    # fast syntax check of every module
```
There is no per-test runner: the suites are monolithic. To isolate a failing area, grep the
script for the assertion and reproduce it in a `python -c`. `_hardcases.py` is a live 3-case
integration demo. `_live_synthesis.py` holds four hand-authored live theses (SHOO/PRDO/CRAI/CALM)
used by `--live` and as the demo fallback provider.

## Architecture (the big picture — these flows span multiple files)

**The dual reverse-DCF is the spine.** Per name, `engine.analyze_ticker`:
`data_sources.resolve_cik` → `extract_fundamentals` (EDGAR XBRL) → `get_prices` → `analytics`
gates + WACC → **reverse DCF #1** solves the growth the market's PRICE implies (`implied_growth`)
→ `synthesis.build_context` → **synthesis** emits `adjusted_growth` (the analyst's base-case 5y
FCFF growth) → **reverse DCF #2** prices that → fair value + `gap_vs_price` → `thesis.build_thesis`
→ `engine._recommend_one`. The market's number and the analyst's number are the same DCF run two
ways; the GAP drives BUY/ADD/HOLD/SELL/PASS, gated by reliability + liquidity, sized by conviction.

**Synthesis is the only judgment step, and it is isolated.** `synthesis.synthesize(context,
llm_json)` → `from_llm_json` (live) or `stub_synthesize` (deterministic, tagged `[STUB]`, NOT
judgment). The ONLY difference between a test run and a real-judgment run is whether
`engine.run(..., llm_synth_provider=...)` is supplied — a callable `(prompt:str)->json_str`
that in production is Claude reasoning at the orchestration layer. The 7-step reasoning lives in
`synthesis.PROMPT_TEMPLATE`. `adjusted_growth` is the single float that moves money; every other
field is the audit trail. Parsing tolerates fences/prose/missing fields, clamps conviction/horizon,
validates the archetype, and falls back to the stub on bad JSON (`stub_after_parse_error`).

**Two-speed scaling (scanner.py + routine.py).** Deep-analyzing 2,000 names daily is infeasible,
so `scanner.scan_universe` runs a CHEAP scan (one price pull for abnormal-move/volume, a
`data_sources.recent_8k_filer_ciks` firehose set-lookup for 8-K filers, news gated to movers/held,
`analytics.quick_revalue` re-pricing) and promotes a prioritized DEEP queue; `engine.run`
deep-synthesizes ONLY that queue (capped at `--max-deep`/`config.MAX_DEEP_PER_RUN`). `--batch N`
rotates a persisted cursor (`universe.next_batch`) so 2–3 runs/day sweep the whole index; held
names + 8-K filers + sector-event names are covered EVERY run.

**Universe (universe.py).** `load_iwm_universe`: local `IWM_holdings.csv` → iShares CSV → SEC
all-filers superset (the iShares CSV is consent-gated for headless fetches). `record_membership`
diffs entrants/departures (churn); held names that left the index are flagged. Cursor + membership
persist under `store/`.

**Sector/news memory (sectors.py + journal.py) — a folder per vertical.**
`store/journal/verticals/<Sector>/` holds `_sector.md`/`_sector.json` (the dossier: drivers, an
entity→ticker relationship graph, a dated event log) AND `<TICKER>.md` (company news + thesis
history). Synthesis CONSUMES the dossier (the `structural_second_order` lens) and FEEDS it via
emitted `relationships` / `sector_update` / `company_news` (engine writes them after each analysis).
A relationship/learning tagged with another industry routes into that industry's dossier
(CROSS-INDUSTRY). `sectors.affected_tickers` (news→company) and `recent_event_tickers` (a vertical
event → re-examine the names it touches) wire the news arm INTO scan promotion.

**Outputs + audit (outputs.py, store.py, retrospective.py).** `build_dashboard` (a capped
cross-universe long/short BOARD under `--iwm`, full book on watchlist) + `build_email`; both
surface index-departure + membership churn. `store/companies/*.json` are append-only snapshots;
`store/` is the git-tracked point-in-time audit trail (`connectors.commit_store`). The retrospective
grades matured theses (past their pinned `evaluation_window`) on idiosyncratic excess return vs a
same-sector basket → `LESSONS.md`, which future synthesis reads back.

**Orchestration (orchestrate.py, connectors.py, ROUTINE_PROMPT.md).** `orchestrate.py` is the single
entry point: a file-based synth provider (`synth/<TICKER>.json` written by the agent) + a real git
committer. `connectors.py` are dry-run seams (read-only Robinhood positions, Gmail brief, Drive
mirror, git commit) the orchestration layer (a Claude Code cloud routine) injects live.
`ROUTINE_PROMPT.md` is the scheduled-agent playbook. See `CONNECTING.md` (wiring) and `SCALING.md`
(full-universe + free rotation recipe).

## Live synthesis (executing ROUTINE.md / ROUTINE_PROMPT.md)
Follow `synthesis.PROMPT_TEMPLATE`'s 7 steps exactly: steelman the consensus → run every lens →
name the SPECIFIC mispricing mechanism (weigh the SPREAD of perspectives; do NOT count agreement
as confidence) → bull/base/bear → catalyst pathway → disconfirm → size with a realistic 12–36 month
horizon. Read `LESSONS.md` first. On a MATERIAL EVENT (8-K/partnership/regulatory/guidance)
RE-UNDERWRITE the mechanism and the DCF — don't footnote it (confirmed = ≥2 sources or an 8-K →
full re-rate; provisional → mark target provisional, await corroboration). Sentiment triggers a
LOOK, never an ACT. Return ONLY the JSON the prompt asks for.

## Cadence
DAILY (2–3×, weekday): cheap two-speed scan + rotation + drift on holdings + cheap re-priced gaps;
deep synthesis only on promoted names. TWICE-WEEKLY / on material trigger: full DCF re-do.
MONTHLY: retrospective + rebalance review — interim price drift on a long (12–36mo) thesis is
expected and is NOT a reason to trade.

## Honesty
State uncertainty plainly. `[STUB]` output is not real judgment. "Passed QA" is not "has edge."
The human paper-trades first to find out whether the reasoning is any good — support that.
