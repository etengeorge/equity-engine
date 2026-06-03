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
- git is initialized locally (branch `main`); `store/` is tracked as the audit trail.

**IMMEDIATE NEXT STEP — finish the CLOUD schedule so it runs on Anthropic's servers (laptop-off):**
1. I will create an **EMPTY private GitHub repo** `equity-engine` under username **`nathan1-gif`**
   (no README/license/.gitignore — an initialized repo rejects the existing history). Then push:
   ```
   git remote add origin https://github.com/nathan1-gif/equity-engine.git
   git push -u origin main
   ```
   Help me if the push errors — HTTPS needs a Personal Access Token, or use SSH
   (`git@github.com:nathan1-gif/equity-engine.git`). You can run `git remote add` for me, but I
   may have to run the push myself if it needs a fresh credential prompt.
2. Connect that repo in **claude.ai/code**.
3. Run **`/schedule`** to create a cloud routine: name "Equity Engine — daily research",
   weekday ~7am ET, task = the contents of **`ROUTINE_PROMPT.md`**. (The earlier `/schedule` attempt
   failed on a transient claude.ai connection — just retry.)
4. Set the routine's env: `SEC_USER_AGENT`, optionally `TIINGO_API_KEY` + `PRICE_PROVIDER=tiingo`.
5. (Optional) commit a real `IWM_holdings.csv` for the faithful R2000 (the cloud can't pass the
   iShares browser consent wall — otherwise it falls back to the SEC all-filers superset); connect
   the read-only **Robinhood / Gmail / Drive** connectors (they dry-run until then).

**CONSTRAINTS (do not break):** never add an order path (Robinhood is read-only); keep
`PAPER_MODE=True`; the DCF gap governs the narrative; `none_efficiently_priced` is a valid output;
free sources only. After it's scheduled, trigger one manual run and confirm it clones, runs
`orchestrate.py daily`, pushes a journal commit, and reports recommend-only.

---
