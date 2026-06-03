"""
data_sources.py - every external input, behind clean functions.

EDGAR is the source of truth for anything in a filing (the precedence rule).
Vendor APIs and price feeds are convenience and cross-check, never the authority
on a reported number.

Free / keyless here: EDGAR (ticker map + CompanyFacts), FRED needs a free key,
prices come from Tiingo (key) or yfinance (fallback).
"""
import json
import time
import urllib.request
import urllib.parse
from functools import lru_cache

import config

_SEC_HEADERS = {"User-Agent": config.SEC_USER_AGENT}
_last_sec_call = [0.0]


def _sec_get(url):
    # SEC asks for <=10 req/s. We keep a simple global throttle.
    gap = time.time() - _last_sec_call[0]
    if gap < 0.12:
        time.sleep(0.12 - gap)
    req = urllib.request.Request(url, headers=_SEC_HEADERS)
    out = urllib.request.urlopen(req, timeout=30).read()
    _last_sec_call[0] = time.time()
    return out


# ---- ticker -> CIK ----------------------------------------------------------
@lru_cache(maxsize=1)
def _ticker_map():
    d = json.loads(_sec_get("https://www.sec.gov/files/company_tickers.json"))
    # keys are arbitrary indices; value has cik_str, ticker, title
    return {v["ticker"].upper(): (int(v["cik_str"]), v["title"]) for v in d.values()}


def resolve_cik(ticker):
    """Return (cik_int, name) or (None, None)."""
    return _ticker_map().get(ticker.upper(), (None, None))


# ---- CompanyFacts (XBRL) ----------------------------------------------------
# Different filers tag the same concept differently. We try aliases in order and
# take the first that has data. This is the small fallback list the critic flagged.
_ALIASES = {
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
        "RevenueFromContractWithCustomerIncludingAssessedTax",
        "SalesRevenueNet",
    ],
    "ebit": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment",
              "PaymentsForCapitalImprovements"],
    "interest_expense": ["InterestExpense", "InterestExpenseDebt"],
    "total_debt": ["LongTermDebtNoncurrent", "LongTermDebt", "DebtCurrent",
                   "LongTermDebtAndCapitalLeaseObligations"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
    "shares": ["CommonStockSharesOutstanding",
               "WeightedAverageNumberOfDilutedSharesOutstanding",
               "EntityCommonStockSharesOutstanding"],
    "dep_amort": ["DepreciationDepletionAndAmortization",
                  "DepreciationAmortizationAndAccretionNet",
                  "DepreciationAndAmortization"],
}


def get_company_facts(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    return json.loads(_sec_get(url))


def _annual_series(facts, concept):
    """Pull annual (FY) values for one concept, newest first: [(fy, val, end, form)]."""
    node = facts.get("facts", {}).get("us-gaap", {}).get(concept)
    if node is None:
        node = facts.get("facts", {}).get("dei", {}).get(concept)
    if node is None:
        return []
    out = []
    for unit_vals in node.get("units", {}).values():
        for r in unit_vals:
            if r.get("fp") == "FY" and r.get("form") in ("10-K", "10-K/A") and "val" in r:
                out.append((r.get("fy"), r["val"], r.get("end"), r.get("form")))
    # de-dup by fiscal year, keep latest end date
    by_fy = {}
    for fy, val, end, form in out:
        if fy is None:
            continue
        if fy not in by_fy or end > by_fy[fy][2]:
            by_fy[fy] = (fy, val, end, form)
    return sorted(by_fy.values(), key=lambda x: x[0], reverse=True)


def _latest(facts, key):
    for concept in _ALIASES[key]:
        s = _annual_series(facts, concept)
        if s:
            return s[0][1], concept
    return None, None


def _series(facts, key, n):
    for concept in _ALIASES[key]:
        s = _annual_series(facts, concept)
        if s:
            return [v for _, v, _, _ in s[:n]], concept
    return [], None


def extract_fundamentals(cik):
    """Normalize the messy XBRL into the handful of numbers the engine needs."""
    facts = get_company_facts(cik)
    nyrs = config.FCFF_NORMALIZATION_YEARS
    cfo, cfo_c = _series(facts, "cfo", nyrs)
    capex, capex_c = _series(facts, "capex", nyrs)
    intex, _ = _latest(facts, "interest_expense")
    ebit, _ = _latest(facts, "ebit")
    debt, _ = _latest(facts, "total_debt")
    cash, _ = _latest(facts, "cash")
    shares, _ = _latest(facts, "shares")
    rev, _ = _latest(facts, "revenue")
    rev_series, _ = _series(facts, "revenue", 6)  # newest first, for historical CAGR
    return {
        "cik": cik,
        "revenue": rev,
        "revenue_series": rev_series,
        "ebit": ebit,
        "interest_expense": intex,
        "total_debt": debt or 0.0,
        "cash": cash or 0.0,
        "shares": shares,
        "cfo_series": cfo,        # newest first
        "capex_series": capex,    # newest first (reported positive = cash out)
        "provenance": {"source": "SEC EDGAR XBRL companyfacts", "cfo_concept": cfo_c,
                       "capex_concept": capex_c},
    }


# ---- risk-free rate ---------------------------------------------------------
def risk_free_rate():
    """10y UST from FRED if a key is set, else the config fallback."""
    if not config.FRED_API_KEY:
        return config.RISK_FREE_FALLBACK, "config_fallback"
    try:
        url = ("https://api.stlouisfed.org/fred/series/observations?series_id=DGS10"
               f"&api_key={config.FRED_API_KEY}&file_type=json&sort_order=desc&limit=5")
        d = json.loads(urllib.request.urlopen(url, timeout=20).read())
        for obs in d["observations"]:
            if obs["value"] not in (".", ""):
                return float(obs["value"]) / 100.0, "FRED:DGS10"
    except Exception:
        pass
    return config.RISK_FREE_FALLBACK, "config_fallback"


# ---- prices -----------------------------------------------------------------
def get_prices(ticker, lookback_days=420):
    """
    Return (dates, closes, highs, lows, volumes) newest-last, or None.
    Tiingo is the recommended production source; yfinance is a flaky fallback
    that we only lean on because it needs no key.
    """
    if config.PRICE_PROVIDER == "tiingo" and config.TIINGO_API_KEY:
        return _tiingo_prices(ticker, lookback_days)
    return _yfinance_prices(ticker, lookback_days)


def _tiingo_prices(ticker, lookback_days):
    import datetime as dt
    start = (dt.date.today() - dt.timedelta(days=lookback_days)).isoformat()
    url = (f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start}"
           f"&token={config.TIINGO_API_KEY}")
    req = urllib.request.Request(url, headers={"Content-Type": "application/json"})
    rows = json.loads(urllib.request.urlopen(req, timeout=30).read())
    if not rows:
        return None
    d = [r["date"][:10] for r in rows]
    # adjClose accounts for splits/dividends -> required for clean beta/vol.
    c = [r["adjClose"] for r in rows]
    h = [r.get("adjHigh", r["adjClose"]) for r in rows]
    lo = [r.get("adjLow", r["adjClose"]) for r in rows]
    v = [r.get("adjVolume", r.get("volume", 0)) for r in rows]
    return d, c, h, lo, v


# ---- submissions: SIC sector + recent filings (8-K, 10-K, 10-Q) -------------
# Coarse SIC-range -> vertical map. Enough to bucket the Russell 2000 into the
# ~11 sectors the vertical-notes layer reasons over. Refine ranges as needed.
def sic_to_sector(sic):
    try:
        s = int(sic)
    except (TypeError, ValueError):
        return "Unknown"
    if 100 <= s <= 999:   return "Agriculture"
    if 1000 <= s <= 1499: return "Energy & Materials"
    if 1500 <= s <= 1799: return "Industrials"
    if 2000 <= s <= 2199: return "Consumer Staples"
    if 2200 <= s <= 2799: return "Consumer Discretionary"
    if 2800 <= s <= 2899: return "Materials & Chemicals"
    if 2900 <= s <= 2999: return "Energy & Materials"
    if 3000 <= s <= 3299: return "Industrials"
    if 3300 <= s <= 3499: return "Materials & Chemicals"
    if 3500 <= s <= 3599: return "Industrials"
    if 3600 <= s <= 3699: return "Technology"
    if 3700 <= s <= 3799: return "Consumer Discretionary"
    if 3800 <= s <= 3899: return "Healthcare"          # instruments/medical devices
    if 3900 <= s <= 3999: return "Consumer Discretionary"
    if 4000 <= s <= 4799: return "Industrials"
    if 4800 <= s <= 4899: return "Communications"
    if 4900 <= s <= 4999: return "Utilities"
    if 5000 <= s <= 5199: return "Industrials"
    if 5200 <= s <= 5999: return "Consumer Discretionary"
    if 6000 <= s <= 6499: return "Financials"
    if 6500 <= s <= 6999: return "Real Estate"
    if 7000 <= s <= 7372: return "Technology"
    if 7373 <= s <= 7399: return "Technology"
    if 7400 <= s <= 7999: return "Consumer Discretionary"
    if 8000 <= s <= 8099: return "Healthcare"
    if 2833 <= s <= 2836: return "Healthcare"          # pharma (also caught above)
    if 8100 <= s <= 8999: return "Industrials"
    return "Other"


def get_submissions(cik):
    return json.loads(_sec_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))


def company_meta(cik, subs=None):
    subs = subs or get_submissions(cik)
    sic = subs.get("sic")
    return {"name": subs.get("name"), "sic": sic,
            "sic_desc": subs.get("sicDescription"),
            "sector": sic_to_sector(sic)}


def recent_filings(cik, forms=("8-K", "10-K", "10-Q"), limit_per_form=4, subs=None):
    """Return recent filings of the given forms, newest first, with doc URLs."""
    subs = subs or get_submissions(cik)
    rec = subs.get("filings", {}).get("recent", {})
    form, date = rec.get("form", []), rec.get("filingDate", [])
    accn, doc = rec.get("accessionNumber", []), rec.get("primaryDocument", [])
    items = re.compile if False else None  # noqa (keep imports minimal)
    out, counts = [], {f: 0 for f in forms}
    for i in range(len(form)):
        f = form[i]
        if f in counts and counts[f] < limit_per_form:
            a = accn[i].replace("-", "")
            url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/{a}/{doc[i]}"
                   if doc[i] else None)
            out.append({"form": f, "date": date[i], "accession": accn[i], "url": url})
            counts[f] += 1
    return out


# 8-K item codes -> the material event each one discloses. A filed 8-K is a
# legally-required, CONFIRMED disclosure of a material event (reliability-first).
EIGHTK_ITEM_EVENTS = {
    "1.01": ("material_agreement", "Entry into a material definitive agreement (e.g. partnership, major contract)"),
    "1.02": ("agreement_termination", "Termination of a material definitive agreement"),
    "1.03": ("bankruptcy", "Bankruptcy or receivership"),
    "2.01": ("m_and_a", "Completion of acquisition or disposition of assets"),
    "2.02": ("earnings", "Results of operations / earnings"),
    "2.03": ("new_obligation", "Material direct financial obligation incurred"),
    "2.04": ("debt_acceleration", "Triggering events accelerating a financial obligation"),
    "2.05": ("restructuring_costs", "Costs associated with exit or disposal activities"),
    "2.06": ("impairment", "Material impairment"),
    "3.01": ("delisting", "Notice of delisting or failure to satisfy listing rule"),
    "4.01": ("auditor_change", "Changes in registrant's certifying accountant"),
    "4.02": ("restatement", "Non-reliance on previously issued financials (restatement)"),
    "5.01": ("control_change", "Changes in control of registrant"),
    "5.02": ("exec_change", "Departure/appointment of directors or officers"),
    "5.07": ("shareholder_vote", "Submission of matters to a vote of security holders"),
    "7.01": ("reg_fd", "Regulation FD disclosure"),
    "8.01": ("other_material", "Other material event"),
}
# weight: which events are MOST likely to be thesis-changing (for prioritization)
HIGH_IMPACT_ITEMS = {"1.01", "1.02", "1.03", "2.01", "2.06", "3.01", "4.02", "5.01", "5.02"}


def recent_material_events(cik, since_date=None, subs=None):
    """Confirmed material events from recent 8-K filings (filing-backed). Returns each
    8-K's item codes mapped to event categories, newest first, optionally only those
    filed on/after since_date."""
    subs = subs or get_submissions(cik)
    rec = subs.get("filings", {}).get("recent", {})
    form = rec.get("form", [])
    date = rec.get("filingDate", [])
    items = rec.get("items", [])
    accn = rec.get("accessionNumber", [])
    doc = rec.get("primaryDocument", [])
    out = []
    for i in range(len(form)):
        if form[i] != "8-K":
            continue
        if since_date and date[i] < since_date:
            continue
        codes = [c.strip() for c in (items[i] if i < len(items) else "").split(",") if c.strip()]
        evs = [{"item": c, "category": EIGHTK_ITEM_EVENTS.get(c, ("other", c))[0],
                "description": EIGHTK_ITEM_EVENTS.get(c, ("other", c))[1],
                "high_impact": c in HIGH_IMPACT_ITEMS} for c in codes]
        a = accn[i].replace("-", "")
        url = (f"https://www.sec.gov/Archives/edgar/data/{cik}/{a}/{doc[i]}"
               if i < len(doc) and doc[i] else None)
        out.append({"date": date[i], "url": url, "items": codes, "events": evs,
                    "any_high_impact": any(e["high_impact"] for e in evs)})
    return out


def recent_8k_filer_ciks(days_back=4):
    """One-shot 'firehose': the set of CIKs that filed an 8-K in the last `days_back`
    BUSINESS days, from the EDGAR daily index. This lets a full-universe scan flag
    material filers with a set-membership test instead of a submissions call per name
    (SCALING.md Step 2). Resilient to weekend/holiday gaps (missing days just 404 -> skip)."""
    import datetime as dt
    ciks = set()
    # form.idx columns are space-padded; the file-path column always carries the CIK as
    # 'edgar/data/<CIK>/...', which is the robust place to read it (the Date Filed column
    # is YYYYMMDD, no dashes).
    pat = re.compile(r"edgar/data/(\d+)/")
    d = dt.date.today()
    checked, tries = 0, 0
    while checked < days_back and tries < days_back + 6:
        tries += 1
        if d.weekday() < 5:                       # EDGAR posts a daily index on business days
            q = (d.month - 1) // 3 + 1
            url = (f"https://www.sec.gov/Archives/edgar/daily-index/{d.year}/QTR{q}/"
                   f"form.{d.strftime('%Y%m%d')}.idx")
            try:
                raw = _sec_get(url).decode("utf-8", "ignore")
                for line in raw.splitlines():
                    if line.startswith("8-K"):    # 8-K, 8-K/A, 8-K12B, ...
                        m = pat.search(line)
                        if m:
                            ciks.add(int(m.group(1)))
                checked += 1
            except Exception:
                pass                              # day's index not posted yet / holiday -> skip
        d -= dt.timedelta(days=1)
    return ciks


def filing_text(url, max_chars=20000):
    """Plain text of a filing document, whitespace-collapsed and truncated."""
    if not url:
        return ""
    try:
        from bs4 import BeautifulSoup
        html = _sec_get(url).decode("utf-8", "ignore")
        txt = BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
        return re.sub(r"\s+", " ", txt)[:max_chars]
    except Exception:
        return ""


import re  # used by filing_text / recent_filings


def _yfinance_prices(ticker, lookback_days):
    try:
        import yfinance as yf
        period = "2y" if lookback_days > 365 else "1y"
        df = yf.Ticker(ticker).history(period=period, auto_adjust=True)
        if df is None or len(df) == 0:
            return None
        return (list(df.index.strftime("%Y-%m-%d")), list(df["Close"]),
                list(df["High"]), list(df["Low"]), list(df["Volume"]))
    except Exception:
        return None
