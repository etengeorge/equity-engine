# START HERE — integrating the engine into Claude Code

This is the shortest path from the zip to a live run. It covers BOTH ways to run Claude Code
(desktop app or command line) — pick the one that matches your machine. Deeper detail lives in
SETUP_CLAUDE_CODE.md (full setup), ROUTINE.md (the daily/monthly flow), CONNECTING.md (Robinhood
+ email + Drive), SCALING.md (full 2,000-name universe), PORTFOLIO.md, RETROSPECTIVE.md, SOURCES.md.

Your week-1 goal: **do not trade. Watch it run, read the calls, tune, build trust.** The engine
is recommend-only and ships in PAPER_MODE — keep it there until you've judged the reasoning.

---

## STAGE 0 — one-time install (~5 min)

You need **Node.js 18+** first (check: `node --version`). Then install Claude Code one of two ways:

- **Desktop app (Mac / Windows)** — easiest, has a built-in terminal: download from
  claude.com/download, sign in, open the Code tab. *(The desktop app is not available on Linux.)*
- **Command line (any OS, incl. Linux)** — `npm install -g @anthropic-ai/claude-code`, then run
  `claude` and authenticate in the browser on first launch. *(Don't use `sudo` with npm — that's
  the usual cause of permission errors.)*

Either way it runs on your Claude subscription — no separate API key, which is what keeps the
synthesis free.

**Unzip the project** somewhere permanent, e.g. `~/equity_engine`.

---

## STAGE 1 — first local run, see it work (~10 min)

Open a terminal **in the project folder**:
- Desktop app: open the folder as your project, then use the integrated terminal.
- CLI: `cd ~/equity_engine`.

```bash
git init && git add -A && git commit -m "initial"     # the journal-as-git design needs this
pip install -r requirements.txt
export SEC_USER_AGENT="equity-engine yourname you@email.com"   # SEC requires an identity
export PRICE_PROVIDER=yfinance                                 # free, no key, fine for week 1
python run.py --tickers PLAB,SHOO,UFPT,CALM,PRDO,CRAI --positions positions.json
```

Open `out/dashboard.html`. Expand a few theses. **The reasoning will say `[STUB]`** — that's the
deterministic placeholder, not real judgment. You're confirming the machinery runs and seeing the
shape of the output. (`positions.json` ships with a sample; edit it to your real holdings later.)

---

## STAGE 2 — the real thing: live synthesis (this is the point)

In Claude Code (desktop Code tab, or `claude` in the project folder), paste this as your task:

> Read ROUTINE.md and execute it for tickers PLAB, SHOO, UFPT, CALM, PRDO, CRAI using
> positions.json. For each name, when the engine produces a synthesis prompt, do the analyst
> reasoning yourself using web_search, and return the JSON the prompt asks for. Then generate the
> dashboard and commit the journal.

Claude Code reads `CLAUDE.md` automatically (it's in the project root — it pins the recommend-only
rules and the 7-step reasoning), then runs the engine and does the *real* deep synthesis per name:
steelmanning the consensus, running the lenses, building bull/base/bear, searching for news and
filings, then handing JSON back. The dashboard will now show real reasoning, not `[STUB]`.

**The week-1 loop:** read a thesis, disagree with it, find where it went wrong (the deviation from
the market and the evidence are on the card), tune `config.py` (BUY_GAP, SELL_GAP, MIN_ADV_USD, the
caps), re-run. You're calibrating your judgment against the system's.

---

## STAGE 3 — automate it (only after you trust the output)

In Claude Code, create a **routine** pointing at the project with `ROUTINE.md` as the prompt,
scheduled for a weekday morning. Routines run in Anthropic's cloud, so they fire whether your
laptop is on or not (the git-based journal makes the fresh-clone model work). Two cadences:
- **Daily** — two-speed scan over the universe + drift monitoring on your positions.
- **Monthly** — retrospective with the live mechanism judge + rebalance review.
Check the current per-plan routine limits in the Claude Code docs before you lean on the schedule.

---

## STAGE 4 — connect your data (when ready)

See CONNECTING.md for specifics. The shape: connect **Robinhood (READ-ONLY** — positions/prices
only; the engine has no trade path), **Gmail** (to send the brief), **Google Drive** (to mirror the
journal). You also have **S&P Global** available as the sanctioned Capital-IQ-adjacent source. Once
connected, the routine pulls your real positions each run so monitoring and the portfolio panel
work against your actual book. Worst case is ever a missed email — never an unwanted trade.

---

## SCALING to all ~2,000 names

Don't loop all 2,000 through deep synthesis daily (rate limits + overkill for long horizons).
SCALING.md describes the two-speed model that's already built: a cheap daily scan over the whole
universe (price/volume/news/sentiment + re-priced gap) that promotes only material names into deep
synthesis, with a cold-tail rotation so quiet names still refresh ~monthly. Material 8-K events
fast-track to the top of the queue the day they happen.

---

## The honest line, kept

The QA hardening means the engine won't hand you a garbage number — degenerate inputs refuse or
flag rather than emit false signals. That is a floor, not edge. Whether the *reasoning* is good
only shows in live results. That's what your paper-trade week is for. Bring back one real thesis
(bull/base/bear + catalyst + mechanism) and the portfolio panel on your real book, and judge the
quality before you ever switch PAPER_MODE off.
