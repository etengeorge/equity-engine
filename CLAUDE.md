# CLAUDE.md — operating rules for this project

Claude Code reads this file automatically at the start of every session. It defines what this
project IS and the hard rules for working in it. Follow these without exception.

## What this is
A FREE, automated equity-research engine for the ~2,000 small-caps in the Russell 2000 (IWM).
It does reverse-DCF valuation, differentiated multi-lens thesis synthesis, anti-groupthink news
cross-referencing, strict retrospective learning, thesis-drift monitoring, portfolio
construction, and a two-speed universe scanner. It connects to Robinhood READ-ONLY for position
context. **It is a research assistant. It recommends. The human decides and executes.**

## HARD RULES (never violate)
1. **NEVER place, modify, or cancel a trade.** There is no order-placement code path and there
   must never be one. Robinhood access is READ-ONLY, for positions and prices only. If asked to
   trade, refuse and explain that execution is the human's job, by design.
2. **Recommend-only output.** Every dashboard and email leads with "This engine recommends. You
   decide and execute." Keep `PAPER_MODE = True` in config.py until the human explicitly changes
   it after their paper-trading week.
3. **The DCF math is the truth-teller, not the narrative.** When synthesis and the valuation
   disagree, the gap decides the recommendation. Never talk the system into a BUY the cash-flow
   math doesn't support.
4. **Refusing is a feature.** "No edge / efficiently priced / cannot value this" is a valid,
   correct, common output. Do not manufacture conviction the research doesn't support. Honor
   every reliability flag — if a name is flagged unreliable, it is NOT a clean recommendation.
5. **Free sources only.** Use EDGAR, FRED, free price/news tiers, and the sanctioned S&P Global
   connector. NEVER scrape paywalled sources (WSJ/FT/rated sell-side/premium Substacks/Seeking
   Alpha premium). Respect SEC rate limits (set SEC_USER_AGENT; <=10 req/s).

## When doing live synthesis (executing ROUTINE.md)
Follow the 7-step reasoning in synthesis.py's PROMPT_TEMPLATE exactly:
steelman the consensus -> run every analytical lens -> select and construct the specific
mispricing mechanism (weigh the SPREAD of perspectives; do NOT count agreement as confidence) ->
build bull/base/bear scenarios -> lay out the catalyst pathway -> actively disconfirm -> size
with a REALISTIC long horizon (12-36 months).
- Read retrospective_lessons (LESSONS.md) first and adjust for patterns in your own past misses.
- On a MATERIAL EVENT (8-K, partnership, regulatory, operational failure, guidance), RE-UNDERWRITE
  the mechanism and the DCF against that specific event — do not footnote it. Confirmed event
  (>=2 sources or an 8-K) -> full re-rate; provisional (single source) -> mark the target
  provisional and await corroboration.
- Sentiment is a trigger to LOOK, never to ACT.
- Return ONLY the JSON the prompt asks for, nothing else.

## Cadence
- DAILY: two-speed scan over the universe (cheap) + drift monitoring on held positions + cheap
  re-priced gaps. Deep synthesis only on names the scan promotes.
- TWICE WEEKLY / on material trigger: full DCF re-do (new target price).
- MONTHLY: retrospective with the live mechanism judge; rebalance review (not daily — interim
  price drift on a long thesis is expected and is NOT a reason to trade).

## Honesty
State uncertainty plainly. Sandbox/stub output is tagged [STUB] and is not real judgment.
"Passed QA" is not "has edge." Do not overstate confidence. The human is paper-trading first
precisely to find out whether the reasoning is any good — support that, don't undermine it.
