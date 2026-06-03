# HANDOFF — continue in a new Claude Code instance

Open a fresh Claude Code session **in this repo** and paste the block below as your first message.

---

I'm continuing work on the **Equity Engine** (this repo) — a FREE, **recommend-only** Russell 2000
research engine. **Read `CLAUDE.md` first** (hard rules + architecture), then `CONNECTING.md` and
`SCALING.md` as needed. Here's the state and what I need next.

**WHAT'S BUILT & WORKING** (everything committed; tests pass — `python _extreme_cases.py` ~150/0 and
`python qa_harness.py` ~145/0; `python -m py_compile *.py` clean):
- The full connected loop runs as ONE command:
  `python orchestrate.py daily [--iwm --batch 250]` →
  positions (read-only) → universe + churn → 8-K firehose → two-speed scan + **sector-event
  propagation** → deep synthesis (reverse-DCF dual-pass) → recommendation → dashboard/email →
  **git audit commit of `store/`**. Recommend-only, `PAPER_MODE=True`, no order path.
- **Sector/news folder-memory:** `store/journal/verticals/<Sector>/` holds a dossier
  (`_sector.md/.json`: drivers, entity→ticker graph, event log) + per-company `<TICKER>.md`.
  Synthesis consumes AND feeds it; **cross-industry routing** (a tech name's FDA/CMS edge lands in
  Healthcare) and **news→company propagation** are wired into the scan.
- Four hand-authored live theses (SHOO/PRDO/CRAI/CALM) in `_live_synthesis.py` (used by `--live`
  and as the demo provider). `ROUTINE_PROMPT.md` is the scheduled-agent playbook.
  `out/dashboard.html` is the latest routine output. `git log` shows the audit trail working.
- **Pushed to GitHub: `nathan1-gif/equity-engine` (private), branch `main`** — `store/` tracked as the audit trail, so the cloud fresh-clone model works.

**STATE OF SETUP:** code + repo are done. The ONLY thing left is creating the CLOUD schedule, and
that's been blocked by a transient Anthropic-side issue — `/schedule` repeatedly returns "trouble
connecting with your remote claude.ai account." It is NOT a setup problem and nothing got
half-created; just retry when the service is back.

**TO FINISH (when the scheduling service is reachable):**
1. Connect the `equity-engine` repo in **claude.ai/code** (GitHub connector) so the cloud routine can clone the private repo.
2. Create the routine — retry **`/schedule`**, OR use the **claude.ai/code → Routines / Scheduled tasks** web UI (often works when the CLI skill's connection is flaky):
   - name: **Equity Engine — daily research**
   - schedule: weekday (Mon–Fri) ~7am ET
   - repo / working dir: `nathan1-gif/equity-engine`
   - task: paste the contents of **`ROUTINE_PROMPT.md`**
3. Set the routine env: `SEC_USER_AGENT="equity-engine you@example.com"`, optionally `TIINGO_API_KEY` + `PRICE_PROVIDER=tiingo` (volume).
4. (Optional) commit a real `IWM_holdings.csv` for the faithful R2000 (the cloud can't pass the
   iShares browser consent wall — otherwise it falls back to the SEC all-filers superset); connect
   the read-only **Robinhood / Gmail / Drive** connectors (they dry-run until then).
5. Trigger ONE manual run; confirm it clones, runs `orchestrate.py daily`, pushes a journal commit, and reports recommend-only.

**CONSTRAINTS (do not break):** never add an order path (Robinhood is read-only); keep
`PAPER_MODE=True`; the DCF gap governs the narrative; `none_efficiently_priced` is a valid output;
free sources only. After it's scheduled, trigger one manual run and confirm it clones, runs
`orchestrate.py daily`, pushes a journal commit, and reports recommend-only.

---
