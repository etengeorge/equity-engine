# CONNECTING.md — wiring the live, free, hands-off loop

The Python engine runs fully on its own with the deterministic synthesis stub.
This guide connects the four live seams so it becomes the autonomous, free loop
you asked for. **All of it runs on your Anthropic subscription — no metered API
key, no paid data tier.**

The pattern throughout: **the Python holds no credentials.** The orchestration
layer (a Claude Cowork scheduled task, or a Claude Code routine) holds the
connections and calls into the engine. That keeps secrets out of the codebase and
is why everything here is free — the reasoning is Claude doing the work inside
your subscription, not an API bill.

---

## 1. Live synthesis (the research brain) — free

The engine exposes `engine.run(tickers, llm_synth_provider=...)`. The
`llm_synth_provider` is a callable `(prompt: str) -> json_str`. When you pass one,
the engine uses real Claude reasoning instead of the stub; when you don't, it
falls back to the stub. Nothing breaks either way.

**In a Cowork task / Code routine**, the loop is:

1. For each name, the engine builds the prompt via `synthesis.render_prompt(context)`.
   The context already contains the 8-K and 10-K text, all vertical notes, and the
   company's journal history.
2. You (the agent) read that prompt, do the synthesis reasoning, and return JSON
   matching the schema in `synthesis.PROMPT_TEMPLATE`.
3. `synthesis.from_llm_json()` parses it into the same `SynthesisResult` the stub
   produces — so the thesis, valuation, and journal all work unchanged.

Because the agent *is* Claude running in your subscription, this step costs nothing
beyond your normal usage. The engine is structured so the only difference between
"test mode" and "live judgment" is whether `llm_synth_provider` is supplied.

> Tip: keep the stub as a fallback in the routine (wrap the live call in try/except
> → stub) so a single bad name never kills the whole run.

---

## 2. Google Drive journal (the compounding memory)

The engine writes the journal locally as a folder tree:

```
store/journal/verticals/<Sector>.md          # all sector notes (read together)
store/journal/companies/<Sector>/<TICKER>.md  # one doc per company (read one-at-a-time)
```

To mirror this to Google Drive so it's the living set of docs you described:

1. **One-time:** create a Drive folder "Equity Engine". Inside it, a "Verticals"
   subfolder and one subfolder per sector.
2. **Each run**, after `engine.run(...)`, the routine uses your **Google Drive**
   connector to, per company analyzed: find-or-create that ticker's Doc in its
   sector folder and append the new dated entry (the same Markdown the engine wrote
   locally). Same for the vertical notes.
3. `journal.push_to_gdoc()` is the stub seam to implement with your connector calls.

The local tree is the source of truth and the git history is the audit trail;
the Drive copy is the human-readable mirror. Read model to preserve: **all vertical
notes get read together** (cheap, ~11 files, catches cross-sector exposure), while
**company docs are read individually** for the name being analyzed.

---

## 3. Gmail alerts (the brief)

`outputs.build_email(results, path)` writes `email_brief.html` — the actionable
items on names you hold plus top buy candidates, each with the full reasoning and
deviation-from-market. To send it:

- The routine reads the file and uses your **Gmail** connector to email it to
  yourself after each run.
- Suggested cadence: send only when there's at least one flagged action on a
  holding or a new BUY, so you're not emailed noise.

---

## 4. Robinhood read-only positions (context, never execution)

The engine takes `positions=[{"ticker","shares","avg_cost"}]` and uses them to
decide SELL/TRIM/ADD/HOLD on names you own. To feed your *real* book:

1. Each run, the routine calls your **Robinhood** connector's read endpoints
   (`get_equity_positions`) to pull current holdings.
2. Map them to the `positions` list and pass into `engine.run(...)`.

**The engine has no order-placement code path and never will.** Robinhood is read
context only. Every recommendation ends on your screen (dashboard + email); you
open Robinhood and place any trade yourself. This is the deliberate safety line.

---

## Putting it together (pseudo-routine)

```
positions = robinhood.get_equity_positions()        # connector, read-only
tickers   = load_universe()                          # watchlist or IWM (see SCALING.md)

def synth_provider(prompt):
    try:
        return claude_reason(prompt)                 # you, in-subscription -> JSON
    except Exception:
        return None                                  # engine falls back to stub

results = engine.run(tickers, llm_synth_provider=synth_provider, positions=positions)
outputs.build_dashboard(results, "out/dashboard.html")
outputs.build_email(results, "out/email_brief.html")
gmail.send(to=me, html=open("out/email_brief.html").read())   # connector
drive.sync(local="store/journal", folder="Equity Engine")     # connector
git_commit_and_push("store/")                                  # point-in-time audit trail
```

Schedule that routine daily (weekdays). Done — free, autonomous research; you keep
the decision and the click.
