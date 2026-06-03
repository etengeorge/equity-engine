# ROUTINE_PROMPT.md — paste this as the scheduled routine's task

You are running the **Equity Engine** as a scheduled, recommend-only research routine. You do
**NOT** place, modify, or cancel any trade — there is no order path, and Robinhood is READ-ONLY.
Keep `PAPER_MODE = True`. Read `CLAUDE.md` first (it pins the hard rules and the 7-step reasoning).

Work in the project directory (clone the repo if needed; the journal in `store/` is the git-tracked
audit trail, so a fresh clone works). One-time per environment: `pip install -r requirements.txt`
and set `SEC_USER_AGENT="equity-engine <you> <you@email>"` and `PRICE_PROVIDER=tiingo` (free key)
or `yfinance`.

## Each run, do exactly this

1. **Positions (read-only).** Pull current equity positions via the Robinhood connector's READ
   endpoint (`get_equity_positions`). Map to `[{"ticker","shares","avg_cost"}]` and write
   `positions.json`. NEVER call a buy/sell/order endpoint. If the connector is unavailable, leave
   `positions.json` as-is.

2. **Pass 1 — emit the synthesis prompts** for the names the scan promotes:
   ```
   python orchestrate.py daily --iwm --batch 250 --emit-prompts
   ```
   This writes `synth/prompts/<TICKER>.txt`, one per promoted name (movers, 8-K filers, cadence-due,
   sector-event re-examines, held names).

3. **Live synthesis — the actual research.** For each `synth/prompts/<TICKER>.txt`: read it, do the
   full 7-step analysis yourself **with web_search** (steelman the consensus → run every lens → name
   the specific mispricing mechanism → bull/base/bear → catalyst path → disconfirm → size), honoring
   the sector dossier and the reporting standards in the prompt. Then write the result to
   `synth/<TICKER>.json` — **only** the JSON object the prompt's schema asks for. If a name has no
   edge, say so (`thesis_archetype:"none_efficiently_priced"`, low conviction) — that is correct and
   common. Skip a name (no file) only if you genuinely cannot analyze it; it falls back to the stub.

4. **Pass 2 — run the loop.** Feed your JSON through the engine and produce outputs + the audit commit:
   ```
   python orchestrate.py daily --iwm --batch 250
   ```
   This re-prices each name at your base-case growth, builds `out/dashboard.html` + `out/email_brief.html`,
   writes the sector dossiers + company news, and commits `store/` (git audit trail; push if a remote is set).

5. **Email the brief (only if actionable).** If `out/email_brief.html` flags an action on a holding,
   a new BUY, or an index departure, send it to the user via the Gmail connector. Otherwise don't email.

6. **Mirror the journal to Drive** via the Drive connector (per CONNECTING.md), if connected.

7. **Report back** in one short message: the new/changed recommendations, any ⚠ thesis-drift or
   index-departure flags, and confirm "recommend-only, no trades placed." Surface the single best
   long and short ideas and the reasoning, not a dump.

## Cadence
- **Daily (weekday), 2–3×/day:** the above with `--iwm --batch 250` so the full Russell 2000 sweeps
  every ~2–3 days while held names + 8-K filers are covered every run.
- **Monthly:** also run `python orchestrate.py retro` to score matured theses and refresh `LESSONS.md`.

## Non-negotiables
- No trades, ever. Read-only Robinhood. The recommendation ends on the user's screen.
- The DCF math governs the narrative — never talk a name into a BUY the cash flow doesn't support.
- Honor every reliability flag; "[STUB]" output is not real judgment.
