# v2: make the scheduled routine actually persist, and make its research defensible

## Why
An audit of the "Equity Engine — daily research" routine (28 runs, Jun 3 to Aug 22) found that
27 "succeeded" while **nothing was persisted after Jun 5**. Root causes, each reproduced:

| # | Failure | Cause | v2 fix |
|---|---|---|---|
| 1 | 27 green runs, zero commits on `main` | `git push` output discarded; every fresh clone started from the last pushed state and was destroyed | push result captured; manifest records it; **exit 2** if not pushed; git identity supplied inline; routine does `git push --dry-run` at setup |
| 2 | Universe was ~10,000 names | iShares CSV is consent-walled headlessly; silent fallback to all SEC filers | Vanguard VTWO holdings API (headless, ~1,950 names); SEC superset opt-in only (`ALLOW_SEC_SUPERSET=1`) |
| 3 | Research prompt truncated at 90k chars mid-string | 8k-char filing heads consumed the budget; dossier/history/LESSONS never reached the analyst | `CONTEXT_BUDGET` per section; targeted `filing_sections` (MD&A, liquidity, 8-K items); `_fit_context` trims whole sections, always valid JSON |
| 4 | `[STUB]` placeholders in the journal | stub output journaled like judgment | engine journals `synthesis_source == "llm"` only; `scripts_scrub_stub_journal.py` removed the 10 historical ones |
| 5 | No way to tell a silent failure from success | exit 0 == success | `store/runs/<date>_<mode>.json` manifest + `_check_manifest` |

## What else is new
- **Red team** as a separate, binding pass (`RED_TEAM_TEMPLATE` → `parse_red_team` → `apply_red_team`):
  DEAD → `none_efficiently_priced`/conviction 1; WOUNDED → conviction cut; SURVIVES → +1 max.
  Never touches `adjusted_growth` (the DCF input). Actionable names without a verdict fail the run.
- **Street consensus seam** (`synth/consensus/<TKR>.json`): Capital IQ via the S&P Global connector when it
  works, web-sourced fallback otherwise. The red team's STREET CHECK reconciles against it.
- **Short side**: `SHORT CANDIDATE` (gap ≤ -30%, ≥ $5M ADV, reliable, live thesis, conviction ≥ 3).
- **Modes**: `daily` (monitor: held + 8-K filers + sector events, deep cap 8, no universe price sweep),
  `sweep` (rotating 300-name slice, deep cap 25), `retro`.
- Held names are cap-exempt and first in the deep queue; gate-failed names sort last.
- Board never carries forward stub-sourced or extreme-gap (> 150%) stale rows.
- Email leads with deltas vs the last stored run; red-team verdicts on the dashboard.
- Mechanical conviction cap (≤ 2) when the gap's sign flips inside the ±15% FCFF band.
- Same-day journal entries are replaced, not duplicated, on a re-run.
- Stooq price cross-check (now behind a JS wall) replaced with a yfinance alternate read.
- `qa_harness.py` no longer `rmtree`s the real `store/`.

## Tests
`_v2_cases.py` 78/78 · `_extreme_cases.py` 184/184 · `qa_harness.py` 145/145 (network) ·
fresh-clone verification of this commit: compiles, both offline suites pass, pass 1 emits valid ~45k-char prompts.
Full three-pass flow run live on the watchlist with a real held-name thesis, red-team verdict,
drift detection ("EDGE GONE"), and `commit.pushed: true`.

## Not included
- Position economics, emails, or keys: none in the repo (scanned). The store records *that* a name was
  held, never share counts or cost basis (`store._redact`).
- The S&P Global connector is currently failing upstream; the code path is in place and the routine
  falls back to web-sourced consensus until it works.

## Deployment checklist (see `DEPLOY_v2.md`)
1. Merge, then confirm the routine's GitHub connection has **push** permission (Issue #push-permission).
2. Routine Instructions ← `ROUTINE_PROMPT.md`. Connectors: Robinhood, S&P Global, Gmail, Drive only.
3. Trigger: weekdays 5:30 PM ET. Notifications on.
4. First run: read `store/runs/<date>_daily.json`; want `commit.pushed: true`.
