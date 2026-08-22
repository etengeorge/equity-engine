"""
config.py - all knobs in one place.

Nothing here is a market call. These are the explicit assumptions the engine
runs on. The two genuinely free parameters in the WACC (equity risk premium and
tax rate) live here as overridable values, not buried constants, so when you
disagree with a discount rate you change one line and rerun.
"""
import os

# ---- safety model -----------------------------------------------------------
# The engine NEVER trades. It reads, values, ranks, and recommends. You execute.
# PAPER_MODE is informational only (it cannot place orders either way); it drives
# the banner on every output so you never mistake a backtest-stage rec for a
# funded one.
PAPER_MODE = True

# ---- universe ---------------------------------------------------------------
# Production: the iShares IWM (Russell 2000) holdings CSV, refreshed daily.
# IWM_HOLDINGS_URL is the official iShares fund-holdings export.
IWM_HOLDINGS_URL = (
    "https://www.ishares.com/us/products/239710/ishares-russell-2000-etf/"
    "1467271812596.ajax?fileType=csv&fileName=IWM_holdings&dataType=fund"
)
# For a quick run you can pass an explicit ticker list to run.py instead.

# ---- API keys (read from environment; never hard-code) ----------------------
# Set in your shell:  export TIINGO_API_KEY=...    export FRED_API_KEY=...
TIINGO_API_KEY = os.environ.get("TIINGO_API_KEY", "")
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY", "")
ALPHAVANTAGE_API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY", "")
POLYGON_API_KEY = os.environ.get("POLYGON_API_KEY", "")
MARKETAUX_API_KEY = os.environ.get("MARKETAUX_API_KEY", "")
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")
# Allow AlphaVantage's public "demo" key as a last-resort news source (works for a
# limited set of tickers). Lets the news layer run with zero keys for testing.
AV_ALLOW_DEMO = os.environ.get("AV_ALLOW_DEMO", "1") == "1"

# Price cross-check: flag when two providers' latest close differ by more than this.
PRICE_XCHECK_TOLERANCE = 0.02   # 2%

# SEC requires a descriptive User-Agent with contact info. Put your real email.
SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT", "equity-engine research you@example.com")

# Price provider: "tiingo" (recommended, needs key) or "yfinance" (fallback, flaky).
PRICE_PROVIDER = os.environ.get("PRICE_PROVIDER", "yfinance")

# ---- WACC assumptions -------------------------------------------------------
RISK_FREE_FALLBACK = 0.043     # used if FRED key absent; ~10y UST. Override anytime.
EQUITY_RISK_PREMIUM = 0.047    # single universe-wide ERP (Damodaran-style implied).
MARGINAL_TAX_RATE = 0.23       # 21% federal + ~2% state. Marginal, NOT effective.
WACC_BAND = 0.01               # +/- this is the sensitivity band on the discount rate.

# ---- reverse DCF ------------------------------------------------------------
HIGH_GROWTH_YEARS = 5          # years of explicit growth before terminal
TERMINAL_GROWTH = 0.025        # long-run nominal growth (~ long-run GDP)
FCFF_NORMALIZATION_YEARS = 3   # average FCFF over this many years to smooth noise
FCFF_BAND_PCT = 0.15           # +/- on normalized FCFF -> the FCF sensitivity band

# ---- reliability gates ------------------------------------------------------
MIN_ADV_USD = 1_000_000        # below this, you can't enter/exit cleanly. Flag it.
MIN_PRICE_HISTORY_DAYS = 180   # below this, beta/vol are too thin to trust.
MIN_BETA_R2 = 0.05             # regression too weak -> beta unreliable.

# ---- recommendation thresholds ----------------------------------------------
BUY_GAP = 0.25                 # fair value must exceed price by this to flag BUY.
SELL_GAP = -0.20               # fair value this far below price -> SELL/TRIM a holding.
SHORT_GAP = -0.30              # v2: unheld name this far OVER fair value -> SHORT CANDIDATE (stricter than BUY)
MIN_ADV_SHORT_USD = 5_000_000  # v2: shorts need real liquidity to borrow and cover.
# Ranking is by reliability-weighted gap, never raw gap (multiple-comparison guard).

# ---- portfolio construction & risk limits ----------------------------------
# Editable, NOT hardcoded assumptions. Tiers from the research:
#   conservative 0.05/0.20 · moderate 0.10/0.30 · high-conviction 0.15/0.40
MAX_SINGLE_NAME_WEIGHT = 0.10   # flag any position above this fraction of the portfolio
MAX_SECTOR_WEIGHT = 0.30        # flag any sector above this aggregate weight
# Kelly fraction: quarter 0.25 (most conservative) · half 0.50 (standard for real money)
# · full 1.0 (aggressive, not advised — overestimating edge 10% can double the bet)
KELLY_FRACTION = 0.50
REBALANCE_DRIFT_TRIGGER = 0.05  # suggest rebalance when a weight drifts >5pp from target
HIGH_AVG_CORRELATION = 0.50     # above this avg pairwise correlation -> "fewer real bets" warning
SINGLE_FACTOR_WARN = 0.80       # if >80% of book is one factor (e.g. all small-cap), warn

# ---- end portfolio limits ---------------------------------------------------

# ---- two-speed scanner & dynamic revaluation --------------------------------
# The cheap DAILY scan watches the whole universe on price/volume/news/sentiment
# and promotes names into the deep-synthesis queue. Thresholds = what counts as
# "material enough to re-analyze." Your knobs.
SCAN_ABNORMAL_RETURN_Z = 2.0       # |1-day return| beyond this many daily-vol sigmas -> trigger
SCAN_ABNORMAL_RETURN_FLOOR = 0.07  # OR an absolute 1-day move beyond this (7%) -> trigger
SCAN_VOLUME_SPIKE_MULT = 2.5       # today's volume vs 20-day average beyond this -> trigger
SCAN_NEWS_TRIGGER = True           # a fresh news cluster -> trigger a look
SCAN_SENTIMENT_TRIGGER = True      # a sentiment spike -> trigger a look (look, never act)
SCAN_GAP_BUY = 0.25                # cheap re-priced gap crossing this -> promote (now a buy?)
SCAN_GAP_SELL = -0.20              # held name whose re-priced gap crosses this -> promote
SCAN_GAP_SHORT = -0.30             # v2: any liquid name whose re-priced gap crosses this -> promote (short side)

# Dynamic DCF cadence: the full re-do (new assumptions -> new target price).
FULL_REVALUE_INTERVAL_DAYS = 3     # twice a week even with no news
COLD_TAIL_REFRESH_FRACTION = 0.05  # also rotate ~1/20th of the no-signal universe daily
TARGET_PRICE_MOVE_NOTABLE = 0.10   # flag when a re-done target moves >10% vs prior
# Cap deep synthesis per daily run when scanning the FULL universe — the rest roll to
# the next day (material movers / events are prioritized first). Watchlist runs leave
# max_deep unset (cover everything). Raise as your rate-limit headroom allows.
MAX_DEEP_PER_RUN = 30
# Full-universe (--iwm) dashboard shows a capped cross-universe long/short BOARD — today's
# deep names + held + the best stored recommendations accumulated over the rotation cycle —
# not all ~2,000 rows. Raise for a longer board.
MAX_BOARD_ROWS = 60
BOARD_MAX_ABS_GAP = 1.50   # v2: stale board rows with |gap| beyond this are data errors, not ideas
# ---- end scanner / revaluation ----------------------------------------------

# ---- congressional-trade sourcing (STOCK Act disclosures) -------------------
# A new free SOURCING signal: when a member of Congress discloses a large stock
# trade, promote that name to deep research to investigate WHY (policy edge,
# contracts, sector tailwind). This is a LOOK trigger, NEVER an ACT — the engine
# still recommends and the DCF still governs; a politician's trade is evidence to
# explain, not a position to copy. Source is the OFFICIAL, free, no-key House
# Clerk disclosure feed (disclosures-clerk.house.gov, refreshed daily) + a
# best-effort Senate pass; nothing paywalled. (Honors the free-sources hard rule.)
CONGRESS_TRADES_TRIGGER = os.environ.get("CONGRESS_TRADES_TRIGGER", "1") == "1"
CONGRESS_MIN_AMOUNT = int(os.environ.get("CONGRESS_MIN_AMOUNT", "50000"))  # lower bound of the
# disclosed amount RANGE must reach this ($) to count as a "big" trade worth promoting.
CONGRESS_LOOKBACK_DAYS = int(os.environ.get("CONGRESS_LOOKBACK_DAYS", "10"))  # disclosure window
CONGRESS_MAX_PTRS_PER_RUN = int(os.environ.get("CONGRESS_MAX_PTRS_PER_RUN", "60"))  # cap PDF parses/run
# Marquee filers whose trades get a priority bump (well-followed; market reacts).
CONGRESS_HIGH_SIGNAL_NAMES = [
    "Pelosi", "Crenshaw", "Gottheimer", "Khanna", "Greene", "McCaul", "Tuberville",
]
# ---- end congressional-trade sourcing ---------------------------------------

STORE_DIR = os.environ.get("STORE_DIR", "store")
