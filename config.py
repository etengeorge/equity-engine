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
TERMINAL_GROWTH = 0.025         # long-run nominal growth; must stay below WACC
EQUITY_RISK_PREMIUM = 0.055
MARGINAL_TAX_RATE = 0.23
WACC_BAND = 0.01                # +/- band used for the sensitivity triple
FCFF_YEARS = 3                  # years averaged for the normalized FCFF base
BETA_LOOKBACK_WEEKS = 104
BETA_CLAMP = (0.30, 2.50)       # wide: only reject economically absurd point estimates
BETA_MIN_R2 = 0.04              # below this the regression explains nothing -> use 1.0, flagged
IMPLIED_GROWTH_BOUNDS = (-0.50, 1.00)

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
