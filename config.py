"""Every tunable number in one place. Nothing here is secret; secrets live in os.environ."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"          # gitignored: raw EDGAR payloads, restored by actions/cache
DATA = ROOT / "data"            # committed: small derived files the agent + site read
RESEARCH = ROOT / "research"    # committed: the memory, one markdown file per company
PUBLIC = ROOT / "public"        # committed: the static site Vercel serves

# --- identity -----------------------------------------------------------------
# SEC requires a real contact string. No default that looks real: a fake UA gets you 403'd
# or blocked, and hard-coding a personal email into a tracked file breaks the secrets rule.
SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT", "").strip()

# --- valuation ----------------------------------------------------------------
EXPLICIT_YEARS = 5              # explicit forecast horizon before the terminal value
TERMINAL_GROWTH = 0.02          # long-run nominal growth; must stay below WACC
EQUITY_RISK_PREMIUM = 0.055
MARGINAL_TAX_RATE = 0.25
WACC_BAND = 0.01                # +/- band used for the sensitivity triple
FCFF_YEARS = 3                  # years averaged for the normalized FCFF base
BETA_LOOKBACK_WEEKS = 104
BETA_CLAMP = (0.30, 2.50)       # wide: only reject economically absurd point estimates
BETA_MIN_R2 = 0.04              # below this the regression explains nothing -> fall back
IMPLIED_GROWTH_BOUNDS = (-0.50, 1.00)

# When the beta regression fails (286 of 1,956 names on 2026-08-31), fall back to the
# MEDIAN beta of that name's own sector, computed from the names in this same universe
# whose regressions did work. A flat 1.0 was badly wrong at both ends: utilities run a
# 0.44 median and health care 1.24, so 1.0 overstated a utility's cost of equity by
# ~300bp and understated a biotech's by ~130bp. The sector median is free, uses data
# already in hand, and is measured on the same benchmark and lookback as every other
# beta here — which an externally sourced beta would not be.
# Tried in order once the regression fails. "yahoo" is company-specific but measured
# against a different index on a different frequency, so it is rescaled (see
# prices.yahoo_betas) rather than mixed in raw; "sector_median" is measured exactly the
# way our own betas are but is not specific to the company. Company-specific first.
BETA_FALLBACK_ORDER = ("yahoo", "sector_median")
BETA_FALLBACK = "sector_median"     # kept for the last step of the chain
BETA_SECTOR_MIN_NAMES = 8           # below this the median is not meaningful -> use 1.0
BETA_YAHOO_MAX_LOOKUPS = 400        # one request each, only for names the regression lost
BETA_YAHOO_BUDGET_SECONDS = 240     # hard stop so a slow Yahoo cannot eat the job
BETA_SPX = "^GSPC"                  # Yahoo quotes beta against this; we discount vs IWM

# --- multiples: the second opinion, and the only one for cash-burning names ----
# A two-stage DCF cannot value negative cash flow, but "unmodellable" and "worthless"
# are different claims. Where FCFF fails, price the name against what its own sector
# cohort actually trades at. Reported as a RANGE across the cohort quartiles, never a
# point estimate, because a comparables valuation is a statement about the cohort.
MULTIPLE_MIN_COHORT = 8         # a cohort thinner than this cannot define quartiles
MULTIPLE_METRICS = ("ev_ebitda", "ev_sales", "ev_gross_profit", "p_tbv")

# --- scenarios ----------------------------------------------------------------
# Every thesis is priced three ways. The analyst supplies bear and bull alongside the
# base case, so the output is a range with named drivers rather than a single number
# carrying false precision.
SCENARIO_WACC_STEPS = (-0.02, -0.01, 0.0, 0.01, 0.02)

# --- screen gates -------------------------------------------------------------
MIN_MARKET_CAP = 50e6           # below this, price is noise and the float is untradeable
MIN_DOLLAR_VOLUME = 250e3       # 60-day average; you cannot act on what you cannot buy
MAX_ABS_GAP = 3.0               # |gap| > 300% is a data error until proven otherwise

# --- daily selection ----------------------------------------------------------
DAILY_SLOTS = 10
ROTATION_SLOTS = 6              # blind sweep: guarantees full coverage over ~326 sessions
OPPORTUNISTIC_SLOTS = 4         # whatever today's screen says is most urgent
RICH_WEIGHT = 0.4               # overvalued names still get slots, at lower priority:
                                # this is a long-oriented screen, and a very negative gap
                                # is more often a broken input than a short candidate
REVISIT_COOLDOWN_DAYS = 45      # don't burn a slot on a name we just did...
MATERIAL_EVENT_OVERRIDE = True  # ...unless something NEW happened since
MIN_REVISIT_DAYS = 7            # ...and never sooner than this, whatever happened.
                                # Without a floor, a 21-day return that barely changes
                                # day to day re-triggered the override every session and
                                # starved fresh names out of the opportunistic slots.
FACTS_MAX_AGE_DAYS = 30         # refresh a company's XBRL facts at most this often

# --- news ---------------------------------------------------------------------
NEWS_LOOKBACK_DAYS = 90         # the window the analyst asks about per company
NEWS_RETENTION_DAYS = 120       # what the store keeps, with margin over the lookback
NEWS_MAX_COMPANY_PULLS = 450    # per-company requests per run; sector feeds cover the rest
NEWS_BUDGET_SECONDS = 600       # hard stop on the company sweep so it cannot eat the job
NEWS_ITEMS_PER_TICKER = 10
NEWS_RECENT_DAYS = 5            # "in the news lately", for the selection score
NEWS_SECTOR_HOT_ITEMS = 6       # sector article count in NEWS_RECENT_DAYS that counts as hot
