# Equity Engine — daily routine (PAPER MODE)

You are running the Equity Engine as a scheduled research routine. Your job is to
produce a recommendation dashboard and brief, and to keep the journal updated. You
do **NOT** place any trades. There is no order-placement step. The Robinhood
connection is read-only context only.

## Steps

1. **Setup (first run only):** `pip install -r requirements.txt`.

2. **Read positions (read-only):** Use the Robinhood connector's read endpoint to
   pull current equity positions. Map them to a list of
   `{"ticker","shares","avg_cost"}` and write it to `positions.json`.
   If the connector is unavailable, fall back to the existing `positions.json`.
   NEVER call any buy/sell/order endpoint. This routine only reads.

3. **Pick the universe for this run:**
   - Week-1 paper mode: use the watchlist in `watchlist.txt` (one ticker per line)
     plus any tickers in `positions.json`.
   - Later (full universe): follow SCALING.md to pull the IWM holdings and apply
     priority batching. Do NOT attempt all 2,000 names in a single run.

4. **Run the engine with LIVE synthesis.** For each ticker, the engine builds a
   synthesis prompt (`synthesis.render_prompt(context)`) containing the 8-K/10-K
   text, all vertical notes, and the company's journal history. For each prompt:
   - Read it, do the analyst reasoning yourself, and return ONLY a JSON object
     matching the schema in `synthesis.PROMPT_TEMPLATE`
     (adjusted_growth, rationale, deviation_explanation, evidence[], disconfirming,
     catalyst, catalyst_date, falsification, conviction, horizon_months).
   - Be honest: if the filings don't justify deviating from the market's implied
     growth, set adjusted_growth near the implied value and say so. Do not invent
     facts that aren't in the provided filing text.
   Pass these back via the `llm_synth_provider` callable so the engine prices your
   view and builds the thesis. (If you cannot synthesize a name, return None for it;
   the engine falls back to the stub so one bad name never kills the run.)

5. **Generate outputs:** call `outputs.build_dashboard` and `outputs.build_email`
   into `out/`.

6. **Update + commit the journal (the memory + audit trail):** the engine writes
   `store/journal/...`. Commit the whole `store/` directory to git with a dated
   message. This commit history is the point-in-time record the weekly retrospective
   scores against — do not skip it.

7. **(Optional) email the brief:** if Gmail is connected and there is at least one
   flagged action on a held name or a new BUY, send `out/email_brief.html` to the user.

8. **(Optional) sync journal to Drive:** mirror `store/journal/` to the Drive folder
   per CONNECTING.md.

## Hard rules
- No trades, ever. Read-only Robinhood. Recommendations end on the user's screen.
- PAPER_MODE stays true in config.py for week 1 (drives the banner).
- Treat extreme valuation gaps as suspicious first (likely data/model error), not as
  the best ideas. Ranking is reliability-weighted; respect the flags.

## Daily position monitoring (thesis drift, not price noise)

When run with your held positions, the engine re-analyzes each held name and compares
the FRESH thesis to the last STORED one. It alerts ONLY when new information has
materially changed the thesis (direction reversal, edge gone, conviction collapse,
basis change) — NOT when price merely moved. This is deliberate: your investment
horizons are long (often 12-36 months), so interim price movement is expected and is
not a reason to trade. The dashboard shows a "⚠ THESIS CHANGED" banner on any held name
whose thesis materially shifted, with a recommended action (review/trim/exit). Surface
these in the email brief. Do NOT generate buy/sell prompts off price wiggles.

## Retrospective cadence (matches long horizons)

Because theses run long, the retrospective only grades a thesis once its pinned
evaluation_window passes (set from the catalyst date + a realistic multi-quarter to
multi-year horizon). Run the retrospective periodically (e.g. monthly), not weekly —
most theses won't have matured in any given week. Pass the live mechanism judge
(llm_provider) so matured theses get real verdicts. See RETROSPECTIVE.md.

## Daily two-speed run (the scaled version)

For full-universe coverage, the daily routine is:
1. Load the universe (IWM holdings — see SCALING.md) and your held positions.
2. `scanner.scan_universe(...)` — cheap scan across the batch; returns the prioritized
   deep-synthesis queue (names that moved, crossed a gap, are due on cadence, or hit the
   cold-tail rotation).
3. Run the DEEP synthesis (this routine's main loop, with live reasoning) ONLY on the
   queued names — not the whole universe.
4. For everything else, `analytics.quick_revalue()` already re-priced the gap cheaply;
   surface any that crossed a buy/sell threshold.
5. Dashboard + monitoring + (monthly) retrospective as before.

Respect free-tier limits: run price/volume first, gate news to names that already moved.
If the queue is large, cap deep synthesis per run (`max_deep`) and let the rest roll to
the next day — material movers are already prioritized first.
