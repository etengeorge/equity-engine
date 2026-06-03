# PORTFOLIO.md — construction, monitoring, and reweighting

The engine analyzes names in isolation; `portfolio.py` looks at the BOOK as a whole —
where the real risks of running money live. It runs automatically whenever you pass
positions, and renders a "Portfolio overview" panel on the dashboard.

## What it monitors

**Concentration / overexposure.** Flags any single name over the cap and any sector
over the cap. Critically, winners grow into oversized positions WITHOUT a trade — a
name can drift from 5% to 20% on price alone — so this is checked every run. (Research:
most pros treat >10% in one name as concentration risk.)

**Hidden / structural concentration.** Your universe is all small-caps, so the whole
book shares one size factor — in a small-cap drawdown everything falls together
regardless of name diversification. The panel says this out loud, every time.

**Effective diversification (correlation-aware).** "20 names" is not 20 bets if they
move together. The panel reports naive effective positions (1/HHI of weights) AND a
correlation-adjusted effective-bets number. High average pairwise correlation shrinks
your real diversification and triggers a warning.

## Sizing & reweighting (half-Kelly, capped)

Target weights use single-asset Kelly — expected return (annualized to fair value over
the thesis horizon) ÷ variance — scaled by the Kelly fraction and capped at the
single-name limit. (We deliberately do NOT use the matrix-inversion multi-asset Kelly:
small-cap correlation estimates are too noisy, and inverting a noisy covariance matrix
overfits. Single-asset Kelly + caps + a fractional scale is the robust choice.)

Suggestions follow strict discipline (the research's core rule — "never sell just
because it went up"):
- **TRIM (over cap)** — position exceeds the single-name cap. Concentration trim.
- **TRIM (harvest)** — overweight AND fair value reached (upside gone). A real harvest.
- **TRIM (fair value reached)** — upside gone even if not over cap.
- **hold (let winners run)** — overweight target BUT thesis still has upside; Kelly says
  hold. This is the discipline that stops you cutting winners early.
- **ADD (under target, thesis intact)** — underweight a name whose thesis still has edge.

And symmetric with exits: when the daily monitor sees a held long's thesis MATERIALLY
STRENGTHEN (conviction surge on new facts), it recommends **CONSIDER ADDING** — size up
toward target, subject to your concentration cap.

## Cadence

Reweighting is a **monthly** activity, not daily. Interim price drift on a long-horizon
thesis is expected and is NOT a reason to trade. The daily run is for monitoring (thesis
drift, overexposure alerts); the monthly run is when you actually rebalance.

## The knobs (config.py — all editable, nothing hardcoded)

```
MAX_SINGLE_NAME_WEIGHT  0.10   # conservative 0.05 · moderate 0.10 · high-conviction 0.15
MAX_SECTOR_WEIGHT       0.30   # conservative 0.20 · moderate 0.30 · high-conviction 0.40
KELLY_FRACTION          0.50   # quarter 0.25 · half 0.50 (real-money standard) · full 1.0
REBALANCE_DRIFT_TRIGGER 0.05   # suggest rebalance when weight drifts >5pp from target
HIGH_AVG_CORRELATION    0.50   # above this -> "fewer real bets" warning
```

Everything is ADVISORY. The engine never trades. You place every order yourself.
