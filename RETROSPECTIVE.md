# RETROSPECTIVE.md — the learning loop

This is what makes the system compound. It does **not** make the model intrinsically
smarter — there is no fine-tuning, no weight update from your wins and losses. It makes
the **journal wiser**: it scores matured theses, writes down where the reasoning was
right or wrong, finds patterns across many theses, and feeds those lessons back into
future synthesis. The model reasons over a richer, self-critical record each run. That's
how good discretionary investors actually improve — and it's the honest version of
"gets better over time."

## The strict scoring definition (your choice)

A thesis is **"right" (correct_idiosyncratic)** only if BOTH hold:
1. The named **mechanism** played out within the pinned evaluation window, AND
2. The **idiosyncratic return** was positive in the thesis direction — the stock beat a
   **same-sector basket**, not just the market.

This separates skill from luck. The verdicts:

| Verdict | Meaning |
|---|---|
| `correct_idiosyncratic` | Mechanism played out AND beat the sector. The real win. |
| `right_mechanism_wrong_outcome` | Mechanism happened but didn't pay (priced in / timing). |
| `correct_but_wrong_reason` | Made money, but the mechanism did NOT play out → **luck, not edge**. |
| `idio_correct_mechanism_unverified` | Beat the sector; mechanism not assessed (no live judge). |
| `wrong` | Mechanism failed and underperformed. |
| `no_call` | We took no view (efficiently priced) — nothing to grade. |

It also flags `likely_early`: catalyst date passed, mechanism not yet in, return flat —
the most common real failure mode (right thesis, wrong timing).

## The two scoring components

- **Idiosyncratic excess** (computed, deterministic): stock return minus a same-sector
  basket built from your own universe membership (equal-weight, trimmed so one peer's
  corporate action can't impersonate the sector). Needs ≥2 sector peers in the store.
- **Mechanism played out** (judgment): in a live retro run, Claude reads the original
  thesis + what actually happened (new filings, price action) and judges whether the
  SPECIFIC mechanism played out. Without a live judge it's recorded `unknown`, and the
  verdict is flagged as resting on the idiosyncratic component only.

## Running it

```python
import retrospective as retro

# pass a live mechanism judge from the orchestration layer (Claude reads thesis + outcome):
def mechanism_judge(thesis_dict, ctx):
    # Claude assesses: did the specific mechanism in thesis_dict['mispriced_mechanism']
    # actually play out, given ctx and fresh filings? -> ('played_out'|'did_not'|'partial', why)
    ...

out = retro.run_retrospective(mechanism_judge=mechanism_judge)
```

Run it **weekly** (and at the end of your paper period). It:
1. Scores every thesis whose pinned evaluation_window has passed.
2. Writes a **RETROSPECTIVE verdict** into each company's journal doc (closing the loop
   on that name).
3. Aggregates **patterns** by archetype, sector, and direction — e.g. "cyclical_mean_
   reversion: frequently early; widen horizons" or "expectations_sentiment: low hit-rate."
4. Writes `store/journal/LESSONS.md`.

## How the lessons compound

Every synthesis run reads `LESSONS.md` into its context (`retrospective_lessons`) and the
prompt instructs it to **adjust horizon, conviction, or view** when a lesson warns about
the archetype it's about to use. So next week's theses are informed by this week's errors
— the journal accumulates self-knowledge the model reasons against.

## The paper-week payoff

At the end of your paper period, run the retrospective over all the theses generated. The
**overall mean idiosyncratic excess** line is your verdict on the whole system: if it's
net positive across a meaningful sample AND mechanisms actually played out, there's edge
worth funding. If it's flat/negative, the system told you — for free — not to fund it yet.
No amount of additional data sources substitutes for this evidence.

## Wiring the live mechanism judge (resolves "unverified" into real verdicts)

Without a judge, mechanism stays `unknown` and verdicts rest on idiosyncratic return
only. To get REAL verdicts, pass a live judge at the orchestration layer:

```python
import retrospective as retro

# llm_provider is callable(prompt)->json_str — Claude reasoning in your subscription
out = retro.run_retrospective(llm_provider=claude_provider)
```

What happens: for each matured thesis, the engine builds a judge context containing the
ORIGINAL thesis (the specific mechanism + the what-must-happen checklist) plus every
filing made AFTER the thesis was created (real 8-Ks/10-Qs/10-Ks). Claude reads the new
filings and judges whether the mechanism actually materialized — explicitly separate
from the price. If the stock rose but the mechanism did NOT play out, the judge flags it
`was_outcome_luck` and the verdict becomes `correct_but_wrong_reason` (luck, not edge).
That is the distinction that makes the hit-rate honest.

Run the judge as part of your weekly retrospective routine in Claude Code (ROUTINE.md
can call it). The resolved verdicts then flow into LESSONS.md and back into synthesis.
