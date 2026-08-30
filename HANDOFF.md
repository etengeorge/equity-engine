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

## Session status — 2026-08-30 (read this before assuming the above is fully working)

v2 is code-complete and audit push has been reliable for days, but **the routine has produced no
real research recently** — its data sources are network-blocked in the environment it's currently
scheduled in. That's the one blocker that matters right now; everything below explains why and
what to check first.

### Repo state
- `main` @ `36f8bb3`+ (this commit). Merged this session: PR #7 (2026-08-27 daily audit trail),
  PR #8 (fresh `IWM_holdings.csv`). Closed: issue #2 (stale "push cannot persist runs" report —
  push has worked reliably since v2; PRs #3/#5/#6/#7/#8 all show `commit.pushed: true`).
- **Universe fixed**: `IWM_holdings.csv` was 1,334 days stale (dated 2023-01-01) and flagging
  every run. Replaced with a fresh iShares export — 1,956 tickers, as of 2026-08-28,
  `universe_stale: False`. Verified directly against `universe.parse_holdings_csv`/`_local_asof`.
- An architecture-diagram artifact ("Equity Engine Field Guide") was published this session,
  covering the reverse-DCF pipeline, the 3-pass loop, and an edit-intent -> file:line map. Find
  it via `Artifact action:"list"` if useful; not reproduced here since it's a visual, not a file.

### Blockers, prioritized

**1. [CRITICAL] Network egress blocks every free data source.** The scheduled environment's proxy
allowlist permits only package registries + Anthropic's own infra. Direct-tested and ALL 403'd:
`www.sec.gov`, `data.sec.gov`, `query1.finance.yahoo.com`, `fc.yahoo.com`, `stooq.com`,
`api.tiingo.com`, `finnhub.io`, `www.alphavantage.co`, `api.polygon.io`, `fred.stlouisfed.org`,
`financialmodelingprep.com`, `api.marketaux.com`. Not a "which provider" problem — zero general
internet access. **Fix:** change the network policy on the environment/trigger that runs this
routine (Claude Code on the web -> environment settings -> network access) to allow outbound
HTTPS generally, or add those hosts to a custom allowlist if supported. The user attempted this
"in the app" once already; a live re-check at the end of the 2026-08-30 session showed **no
change** — verify from a genuinely fresh session (the policy is fixed at container creation, a
resumed/existing session will never pick it up), using:
```bash
for h in www.sec.gov data.sec.gov query1.finance.yahoo.com; do
  curl -sS -o /dev/null -w "%{http_code}\n" --connect-timeout 5 "https://$h"
done   # 200-ish = fixed; "CONNECT tunnel failed, response 403" = still blocked
```

**2. [MEDIUM] S&P Global connector not enabled for this chat/routine.** `ListConnectors` shows it
authenticated at the org level but `enabledInChat: false` (also unchanged after the user's
attempted fix). This is the Street-consensus seam (`synth/consensus/<TKR>.json`); currently
always falls back to web search.

**3. [MEDIUM] Robinhood connector exposes no portfolio/positions tools.** Only market-data tools
were available this session (`get_financials`, price/technicals, news, SEC filing lookups) —
`get_equity_positions`/`get_accounts` weren't in the tool list at all, so the routine ran fully
unheld. Check the connector's granted OAuth scopes include read-only portfolio access.

**4. [Informational — don't re-investigate] Robinhood's own SEC data has no small-cap coverage.**
Before concluding (1) needs a network-policy fix, I checked whether Robinhood's SEC filing tools
(reachable via Anthropic's connector infra, unlike direct EDGAR) could substitute. They have full
XBRL coverage for AAPL but returned empty/404 facts and filing content for three real Russell
2000 names (PRDO, CALM, SHOO) — only the bare filing index (form type/date) exists for small
caps. This is a dead end, not a resourcing gap.

### Already ruled out, don't re-litigate
- **Wisesheets**: no MCP connector exists; also a paid service (conflicts with "free sources only").
- **edgartools / "edgartools MCP"**: no such connector exists; the library just calls the same
  blocked `data.sec.gov`/`www.sec.gov` endpoints, so it wouldn't help even if it did.
- **FactSet, Bigdata.com, Zacks Data, viaNexus vAST** (the only other finance connectors in the
  registry): all paid/institutional — using one means deliberately amending the free-sources rule.

### Next steps, in order
1. From a **fresh** session, re-run the `curl` check above. Still 403 -> the policy change didn't
   land on the environment this trigger actually uses.
2. Once open, run `python orchestrate.py sweep --emit-prompts` and confirm it promotes names
   (no "Failed to get ticker... 403" spam) before trusting a full scheduled run.
3. Confirm S&P Global shows `enabledInChat: true` via `ListConnectors`.
4. Separately, chase Robinhood portfolio scope if held-position awareness matters.
5. Only after (1)-(2) are confirmed should the next `daily`/`sweep` run be trusted to produce
   real theses — until then, expect `promoted: 0` or all-failure scans.
