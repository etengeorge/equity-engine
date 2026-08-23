# HANDOFF — Equity Engine v2 (continue in a new Claude Code instance)

Open a fresh Claude Code session **in this repo** and paste the block below as your first message.

---

I'm continuing work on the **Equity Engine v2** (this repo), a FREE, **recommend-only** Russell 2000
research engine. **Read `CLAUDE.md` first** (hard rules, architecture, and the "v2 changes" section
that explains what broke in v1), then `ROUTINE_PROMPT.md` (the scheduled-agent playbook).

**WHAT v1 GOT WRONG (Aug 2026 audit, all reproduced):** the cloud routine reported 27 green runs while
(1) `git push` failed silently in every fresh clone so nothing persisted after June 5, (2) the universe
was the 10k SEC all-filers superset, (3) the synthesis prompt was truncated at 90k chars so the memory
layer never reached the analyst, (4) stub output polluted the journal, (5) there was no run manifest.

**WHAT v2 IS:** three passes per run (`orchestrate.py <mode> --emit-prompts` -> agent writes
`synth/<TKR>.json` -> `--emit-redteam` -> agent writes `synth/redteam/<TKR>.json` -> final pass),
a binding devil's-advocate verdict, a street-consensus seam (`synth/consensus/`), a run manifest
(`store/runs/`), loud push, and `exit 2` on any silent-failure condition. Modes: `daily` (monitor),
`sweep` (rotating research slice), `retro`.

**TESTS (all must stay green):** `python _v2_cases.py` (78), `python _extreme_cases.py` (184, offline),
`python qa_harness.py` (145, network), `python -m py_compile *.py`. Never `rmtree("store")` in a test;
`store/` is the git-tracked audit trail and `store/journal/LESSONS.md` lives there.

**CONSTRAINTS (do not break):** never add an order path (Robinhood is read-only); keep
`PAPER_MODE=True`; the DCF gap governs the narrative and the red team governs conviction;
`none_efficiently_priced` is a valid output; the stub never writes to the journal; free sources only;
the routine's GitHub connection MUST have push permission or every run is lost.

---
