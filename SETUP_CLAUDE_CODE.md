# SETUP_CLAUDE_CODE.md — running the engine in Claude Code

Your week-1 plan: **don't trade. Watch it run, read the calls, edit, build trust.**
This guide does exactly that — first a local on-demand run so you can *see it run
normally* today, then promotion to a scheduled cloud routine once it behaves.

There are two layers:
- **The engine** (the Python) runs anywhere.
- **The routine** is the Claude Code wrapper that schedules it, does the live
  synthesis, and pushes outputs. You don't need the scheduled routine for week 1 —
  run locally on demand first.

---

## Part A — first run, locally, on demand (do this now)

1. **Put the project in a git repo** (the journal-as-git design needs this for the
   point-in-time audit trail):
   ```bash
   cd equity_engine
   git init && git add -A && git commit -m "initial engine"
   ```

2. **Install deps:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set your identity for SEC (required) and pick the price provider:**
   ```bash
   export SEC_USER_AGENT="equity-engine yourname you@email.com"
   export PRICE_PROVIDER=yfinance      # free, no key, fine for week 1
   # (optional, sturdier) export PRICE_PROVIDER=tiingo ; export TIINGO_API_KEY=...
   # (optional, better risk-free rate) export FRED_API_KEY=...
   ```

4. **Run it on the watchlist** (stub synthesis — this is the "see it run normally"
   baseline, no live reasoning yet):
   ```bash
   python run.py --tickers PLAB,SHOO,UFPT,CALM,PRDO,CRAI --positions positions.json
   ```
   Open `out/dashboard.html`. Expand a few theses. This is the shape of what you'll
   get daily. Note the `[STUB REASONING]` tag — that's the placeholder; Part B turns
   on real judgment.

5. **In Claude Code, do a LIVE-synthesis run** (this is the real thing). Open the
   project in Claude Code and give it `ROUTINE.md` as the task. Claude Code will:
   read each name's synthesis prompt, do the analyst reasoning itself, hand the JSON
   back to the engine, and write the dashboard/email/journal. This is free — it's
   Claude reasoning inside your subscription, not an API bill.

6. **Read, judge, edit.** This is the week-1 loop:
   - Disagree with a growth number or a thesis? The reasoning, the deviation from
     the market, and the evidence are all on the card — find where it went wrong.
   - Tune knobs in `config.py` (BUY_GAP, SELL_GAP, MIN_ADV_USD, the WACC/FCFF bands).
   - Re-run. Watch how the calls change. Commit when you like a config.

---

## Part B — promote to a scheduled routine (after it behaves)

Once you trust the output, make it run on its own. In Claude Code:

1. **Connect the services** you want the routine to use: Robinhood (read-only),
   Gmail, Google Drive. (Robinhood read is for pulling positions; see CONNECTING.md.)

2. **Create a routine** pointing at this repo with `ROUTINE.md` as the prompt.
   Configure it to run on a weekday-morning schedule (e.g., 7:30am pre-market).
   - Routines run in Anthropic's cloud, so they fire whether or not your laptop is
     on. Confirm the current per-day routine limits for your plan in the Claude Code
     docs before relying on cadence.
   - Routines clone the repo fresh each run and don't keep local state — which is
     fine here because the journal lives in git and gets committed each run. That's
     the whole point of the git-as-store design.

3. **Keep PAPER_MODE = true** in `config.py` for the entire first week. Every output
   carries the paper banner. You are only reading.

---

## Part C — going live (only after the paper week earns it)

When you've watched a meaningful sample and the calls hold up:
- Run the weekly retrospective (SCALING.md, step 5): score matured theses on
  idiosyncratic excess — return vs a same-sector basket, not vs zero. If there's no
  edge net of sector beta, do not fund it.
- If it clears, you start placing trades **yourself** in Robinhood off the dashboard.
  The engine still never executes. Flip PAPER_MODE only to change the banner — it
  has no power to trade either way.

---

## What you'll watch for in week 1
- Are the implied-growth numbers sane vs each company's history?
- When the engine deviates from the market, is the *reasoning* sound and grounded in
  the actual filings (not hand-wavy)?
- Are reliability flags firing on the names that deserve them (thin/illiquid/neg-EBIT)?
- Do the BUY/SELL calls match what you'd conclude after reading the thesis yourself?
- Does the journal accumulate useful context day over day?
The goal of the week is calibrating *your* judgment against the system's — that
calibration is the actual product.
