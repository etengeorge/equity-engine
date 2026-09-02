"""SEC EDGAR: the only fundamentals source. Free, authoritative, rate-limited.

Two entry points matter:
  fundamentals(ticker) -> the ~15 normalized numbers the valuation needs
  recent_8k_ciks(days) -> set of CIKs that filed an 8-K lately, from the daily index
                          (5 requests for the whole market, not 1,956)
"""
import json, re, time, html as _html, datetime as dt, urllib.request, urllib.error
import config

_last_call = [0.0]
_MIN_INTERVAL = 0.11          # SEC allows 10 req/s; sit just under it


def _get(url, binary=False):
    if not config.SEC_USER_AGENT:
        raise RuntimeError(
            "SEC_USER_AGENT is unset. Export it as 'equity-engine <your-email>' — "
            "SEC returns 403 to anonymous clients.")
    wait = _MIN_INTERVAL - (time.time() - _last_call[0])
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={
        "User-Agent": config.SEC_USER_AGENT,
        "Accept-Encoding": "gzip, deflate",
        "Host": url.split("/")[2],
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    import gzip
                    raw = gzip.decompress(raw)
                _last_call[0] = time.time()
                return raw if binary else raw.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            _last_call[0] = time.time()
            if e.code == 404:
                raise FileNotFoundError(url)
            if e.code in (429, 503) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise
        except Exception:
            _last_call[0] = time.time()
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise


# --- ticker -> CIK -----------------------------------------------------------
_cik_map = None

def cik_for(ticker):
    global _cik_map
    if _cik_map is None:
        p = config.CACHE / "company_tickers.json"
        fresh = p.exists() and (time.time() - p.stat().st_mtime) < 7 * 86400
        if not fresh:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(_get("https://www.sec.gov/files/company_tickers.json"))
        blob = json.loads(p.read_text())
        _cik_map = {v["ticker"].upper(): int(v["cik_str"]) for v in blob.values()}
    # iShares writes class shares as BRK.B / BRK-B; EDGAR uses BRKB style in some rows
    for cand in (ticker, ticker.replace(".", "-"), ticker.replace("-", "."),
                 ticker.replace(".", "").replace("-", "")):
        if cand.upper() in _cik_map:
            return _cik_map[cand.upper()]
    return None


# --- company facts -----------------------------------------------------------
def company_facts(cik, max_age_days=config.FACTS_MAX_AGE_DAYS):
    """Cached XBRL companyfacts. The cache is gitignored and large (0.1-4 MB each);
    only the extracted numbers are ever committed."""
    p = config.CACHE / "facts" / f"{cik:010d}.json"
    if p.exists() and (time.time() - p.stat().st_mtime) < max_age_days * 86400:
        return json.loads(p.read_text())
    p.parent.mkdir(parents=True, exist_ok=True)
    raw = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json")
    p.write_text(raw)
    return json.loads(raw)


_ALIASES = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet",
                "RevenuesNetOfInterestExpense", "SalesRevenueGoodsNet",
                "SalesRevenueServicesNet", "RegulatedAndUnregulatedOperatingRevenue",
                 "Revenue", "RevenueFromSaleOfGoods", "RevenueFromRenderingOfServices"],
    "ebit": ["OperatingIncomeLoss",
             "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
             "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
                 "ProfitLossFromOperatingActivities", "ProfitLossBeforeTax"],
    "income_tax": ["IncomeTaxExpenseBenefit"],
    "net_income": ["NetIncomeLoss", "ProfitLoss",
                 "ProfitLoss"],
    # The numerator ROTCE actually wants. Tangible COMMON equity is the denominator, so
    # earnings have to be after preferred dividends or the return is overstated for any
    # preferred-heavy financial. Not every filer tags it; justified_pb falls back to
    # net_income and says which it used.
    "net_income_common": ["NetIncomeLossAvailableToCommonStockholdersBasic"],
    "cfo": ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
                 "CashFlowsFromUsedInOperatingActivities", "NetCashFlowsFromUsedInOperatingActivities"],
    # capex tagging is the most industry-specific field here: E&P, mining, REITs and
    # utilities all use their own concept, and picking only the manufacturer's tag
    # silently drops the whole cash-flow model for entire sectors
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsForCapitalImprovements",
              "PaymentsToAcquireProductiveAssets",
              "PaymentsToExploreAndDevelopOilAndGasProperties",
              "PaymentsToAcquireOilAndGasProperty",
              "PaymentsToAcquireOilAndGasPropertyAndEquipment",
              "PaymentsToAcquireMiningAssets",
              "PaymentsToAcquirePropertyPlantAndEquipmentAndIntangibleAssets",
              "PaymentsForProceedsFromProductiveAssets",
              "PaymentsToAcquireOtherPropertyPlantAndEquipment",
              "PaymentsForCapitalExpenditures",
                 "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities", "PaymentsToAcquirePropertyPlantAndEquipmentClassifiedAsInvestingActivities", "PurchaseOfPropertyPlantAndEquipment"],
    "interest_expense": ["InterestExpense", "InterestExpenseDebt",
                         "InterestIncomeExpenseNet",
                 "FinanceCosts"],
    "total_debt": ["LongTermDebtNoncurrent", "LongTermDebt",
                   "LongTermDebtAndCapitalLeaseObligations", "DebtLongtermAndShorttermCombinedAmount",
                 "Borrowings", "NoncurrentPortionOfNoncurrentBorrowings"],
    "debt_current": ["DebtCurrent", "LongTermDebtCurrent"],
    # Convertible issuers frequently tag NOTHING in the LongTermDebt* family: the notes
    # sit on the face of the balance sheet under their own concept and the generic debt
    # aliases above return nothing at all. Teladoc reported total_debt of $42.4M against
    # $996.7M of 2027 convertible notes, understating enterprise value 3.4x and turning a
    # fairly-priced name into a +220% "gap". Because missing debt always lowers EV, always
    # lowers the growth the market appears to imply and always widens the gap upward, this
    # class of error manufactures false buys and never false passes -- which is the worst
    # possible direction for it to fail in. Kept as separate buckets rather than appended
    # to the lists above because _series picks ONE alias (the most recent), so appending
    # would let a convertible REPLACE a term loan instead of adding to it.
    "convertible_noncurrent": ["ConvertibleNotesPayableNoncurrent", "ConvertibleDebtNoncurrent",
                               "ConvertibleLongTermNotesPayable", "ConvertibleSubordinatedDebtNoncurrent",
                               "ConvertibleNotesPayable"],
    "convertible_current": ["ConvertibleNotesPayableCurrent", "ConvertibleDebtCurrent"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue",
             "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents",
                 "CashAndCashEquivalents"],
    # kept separate from cash: many small caps park real money here, and leaving it out
    # overstates enterprise value and therefore the growth the market "implies"
    "short_term_investments": ["ShortTermInvestments",
                               "AvailableForSaleSecuritiesDebtSecuritiesCurrent",
                               "MarketableSecuritiesCurrent"],
    "shares": ["CommonStockSharesOutstanding", "EntityCommonStockSharesOutstanding",
               "WeightedAverageNumberOfDilutedSharesOutstanding"],
    "equity": ["StockholdersEquity",
               "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
                 "Equity", "EquityAttributableToOwnersOfParent"],
    "goodwill": ["Goodwill",
                 "Goodwill"],
    "intangibles": ["IntangibleAssetsNetExcludingGoodwill", "FiniteLivedIntangibleAssetsNet"],
    # Stock compensation is added back inside reported CFO, so FCFF built from CFO treats
    # it as free. For software companies it routinely runs 20-40% of operating cash flow,
    # which is the single largest distortion in this universe's valuations.
    "sbc": ["ShareBasedCompensation", "AllocatedShareBasedCompensationExpense",
            "ShareBasedCompensationArrangementByShareBasedPaymentAwardCompensationCost"],
    # Belong in enterprise value by definition: EV = market cap + debt + preferred
    # + minority interest - cash. Zero for most small caps, material for some.
    "preferred": ["PreferredStockValue", "PreferredStockLiquidationPreferenceValue"],
    "minority_interest": ["MinorityInterest",
                          "StockholdersEquityAttributableToNoncontrollingInterest"],
    # Reported for information only. We keep operating leases as an operating expense
    # (their payments already reduce CFO) rather than capitalizing them into debt —
    # doing one without the other double-counts. Flagged when large enough that the
    # alternative treatment would change the conclusion.
    "operating_lease_liability": ["OperatingLeaseLiabilityNoncurrent",
                                  "OperatingLeaseLiability"],
    "dep_amort": ["DepreciationDepletionAndAmortization", "DepreciationAndAmortization",
                  "DepreciationAmortizationAndAccretionNet"],
    # Gross profit is the denominator of last resort for a company with no EBITDA. For a
    # cash-burning business it is far more comparable across a sector than revenue,
    # because it already nets out cost of sales — the line where business models differ
    # most. Many filers report it directly; the rest are derived from revenue minus COGS.
    "gross_profit": ["GrossProfit"],
    "cogs": ["CostOfGoodsAndServicesSold", "CostOfRevenue", "CostOfGoodsSold",
             "CostOfServices"],
}


# Annual report forms. Foreign private issuers file 20-F and Canadian issuers 40-F
# instead of a 10-K — omitting them does not merely lose a share count, it drops every
# fundamental for those companies, so they fail the screen entirely. There are ~90 of
# them in the Russell 2000 (Golar LNG, Scorpio Tankers, DHT, Brookfield entities...).
_ANNUAL_FORMS = ("10-K", "10-K/A", "20-F", "20-F/A", "40-F", "40-F/A")


def _annual(facts, concept):
    """Annual values from any annual-report form, newest first: [(fy, value, end_date)]."""
    node = (facts.get("facts", {}).get("us-gaap", {}).get(concept)
            or facts.get("facts", {}).get("ifrs-full", {}).get(concept)
            or facts.get("facts", {}).get("dei", {}).get(concept))
    if node is None:
        return []
    by_fy = {}
    for rows in node.get("units", {}).values():
        for r in rows:
            if r.get("fp") != "FY" or r.get("form") not in _ANNUAL_FORMS or "val" not in r:
                continue
            fy, end = r.get("fy"), r.get("end")
            if fy is None or end is None:
                continue
            # A 10-K carries prior-year comparatives under the same fy tag; keep the
            # latest-ending observation for each fiscal year.
            if fy not in by_fy or end > by_fy[fy][2]:
                by_fy[fy] = (fy, r["val"], end)
    return sorted(by_fy.values(), key=lambda x: x[0], reverse=True)


def _series(facts, key, n):
    """Pick the alias whose data is most RECENT, not the one listed first.

    Companies migrate tags over time and leave the old one populated with ancient values
    (Commercial Metals still carries `Revenues` with FY2011 numbers). First-match-wins
    would hand back 15-year-old revenue as if it were current, and every downstream
    number -- growth, EV, the gap -- would be built on it. Recency is the tiebreaker,
    then series length.
    """
    best = None
    for concept in _ALIASES[key]:
        s = _annual(facts, concept)
        if not s:
            continue
        key_tuple = (s[0][2], len(s))          # (newest end date, how many years)
        if best is None or key_tuple > best[0]:
            best = (key_tuple, concept, s)
    if best is None:
        return [], None, None
    _, concept, s = best
    return [v for _, v, _ in s[:n]], concept, s[0][2]


def _latest(facts, key):
    vals, concept, end = _series(facts, key, 1)
    return (vals[0] if vals else None), concept, end


# Balance-sheet items are INSTANTS, not annual periods. `_annual` filters to fp == "FY"
# on an annual-report form, so reading debt or cash through it takes the fiscal-year-end
# figure and ignores every 10-Q filed since — up to a year of staleness on the two
# numbers that set enterprise value and the debt weight in WACC.
#
# That is not hypothetical. Alkermes drew $1.525B of term loans on 2026-02-12, six weeks
# after its year end; the screen read $290.7M of debt and reported an enterprise value
# BELOW market capitalisation for a company carrying $1.8B of debt. Share count already
# reads from any form for exactly this reason (see _latest_shares); these fields now do
# the same. The annual SERIES are left alone — those exist for ratio history, where
# consistent annual periods are the point.
_INSTANT_KEYS = ("total_debt", "debt_current", "convertible_noncurrent",
                 "convertible_current", "cash", "short_term_investments", "equity",
                 "goodwill", "intangibles", "preferred", "minority_interest",
                 "operating_lease_liability")


def _latest_instant(facts, key):
    """Newest reported value for a balance-sheet item, from ANY form including 10-Q.

    Returns (value, concept, end_date, form). Alias choice follows the same recency rule
    as `_series`: the concept with the newest observation wins, so a company that
    migrated tags does not hand back a stale one.
    """
    best = None
    for concept in _ALIASES.get(key, []):
        node = (facts.get("facts", {}).get("us-gaap", {}).get(concept)
                or facts.get("facts", {}).get("ifrs-full", {}).get(concept)
                or facts.get("facts", {}).get("dei", {}).get(concept))
        if node is None:
            continue
        for rows in node.get("units", {}).values():
            for r in rows:
                end, val = r.get("end"), r.get("val")
                if not end or not isinstance(val, (int, float)):
                    continue
                # An instant fact has no start date. Duration facts (revenue, CFO) do,
                # and must not be picked up here.
                if r.get("start"):
                    continue
                if best is None or end > best[2]:
                    best = (val, concept, end, r.get("form"))
    return best if best else (None, None, None, None)


def _latest_shares(facts):
    """Most recent share count, from any form.

    `dei:EntityCommonStockSharesOutstanding` is a cover-page instant fact filed with every
    10-Q and 10-K, not an annual-period fact — restricting it to FY/10-K rows both misses
    companies that only tag it quarterly AND, for everyone else, prices a current share
    price against a share count up to a year stale. Buybacks and equity raises make that
    a real error in market cap, not a rounding one. Newest `end` date wins.
    """
    best = None
    for ns, concept in (("dei", "EntityCommonStockSharesOutstanding"),
                        ("us-gaap", "CommonStockSharesOutstanding"),
                        ("dei", "EntityCommonStockSharesOutstanding")):
        node = facts.get("facts", {}).get(ns, {}).get(concept)
        if not node:
            continue
        for rows in node.get("units", {}).values():
            for r in rows:
                end, val = r.get("end"), r.get("val")
                if not end or not isinstance(val, (int, float)) or val <= 0:
                    continue
                if best is None or end > best[0]:
                    best = (end, val, f"{ns}:{concept}", r.get("form"))
    return best


def fundamentals(cik):
    """Normalize messy XBRL into the numbers both valuation methods need.
    Every field can be None — the caller gates on that rather than guessing."""
    f = company_facts(cik)
    cfo, cfo_c, _ = _series(f, "cfo", config.FCFF_YEARS)
    capex, capex_c, _ = _series(f, "capex", config.FCFF_YEARS)
    rev, _, _ = _series(f, "revenue", 6)
    sbc, _, _ = _series(f, "sbc", config.FCFF_YEARS)
    ni, ni_c, _ = _series(f, "net_income", 3)
    ni_common, ni_common_c, _ = _series(f, "net_income_common", 3)
    eq, eq_c, _ = _series(f, "equity", 3)
    # Balance sheet from the newest filing of ANY form -- see _latest_instant.
    debt_lt, debt_lt_c, debt_end, debt_form = _latest_instant(f, "total_debt")
    debt_cur, debt_cur_c, dc_end, _ = _latest_instant(f, "debt_current")
    # Convertibles get the same freshness treatment as the rest of the balance sheet.
    conv_lt, conv_lt_c, conv_lt_end, _ = _latest_instant(f, "convertible_noncurrent")
    conv_cur, conv_cur_c, conv_cur_end, _ = _latest_instant(f, "convertible_current")
    # max, deliberately, not sum. A filer that tags LongTermDebtNoncurrent is reporting
    # TOTAL long-term debt there, convertibles included, so adding the separately-tagged
    # convertible on top would double-count it. A filer that tags only the convertible
    # concepts has nothing in the LongTermDebt* family, and max lifts the figure from
    # (usually) zero to the real one. The residual weakness is a company carrying both a
    # term loan and separately-tagged convertibles with no combined total, where max
    # returns the larger rather than the sum -- still understated, but far less so, and
    # never overstated. Erring downward keeps EV low and gaps wide, which is the same
    # direction as the old bug; erring upward would invent expensiveness that isn't there.
    debt_noncurrent = max(debt_lt or 0.0, conv_lt or 0.0)
    debt_current_all = max(debt_cur or 0.0, conv_cur or 0.0)
    debt_concepts = [c for c in (debt_lt_c, debt_cur_c, conv_lt_c, conv_cur_c) if c]
    # the balance-sheet date reported alongside is the newest of the pieces actually used
    debt_end = max([d for d in (debt_end, dc_end, conv_lt_end, conv_cur_end) if d],
                   default=None)
    ebit, ebit_c, _ = _latest(f, "ebit")
    ebit_derived = False
    if not isinstance(ebit, (int, float)):
        # EBIT ~= pretax income + interest expense. Missing tag must not be read as a loss:
        # that used to blackball profitable companies (CMC, SLAB) out of the model entirely.
        pretax, _, _ = _latest(f, "ebit")
        ni_l, _, _ = _latest(f, "net_income")
        tax_l, _, _ = _latest(f, "income_tax")
        i_l, _, _ = _latest(f, "interest_expense")
        if all(isinstance(x, (int, float)) for x in (ni_l, tax_l)):
            ebit = ni_l + tax_l + (i_l if isinstance(i_l, (int, float)) else 0.0)
            ebit_derived = True
    intex, _, _ = _latest(f, "interest_expense")
    cash, _, cash_end, cash_form = _latest_instant(f, "cash")
    sti, _, _, _ = _latest_instant(f, "short_term_investments")
    shares, _, _ = _latest(f, "shares")
    cover = _latest_shares(f)
    shares_asof = shares_src = None
    if cover:
        shares, shares_asof, shares_src = cover[1], cover[0], f"{cover[2]} ({cover[3]})"
    pref, _, _, _ = _latest_instant(f, "preferred")
    minint, _, _, _ = _latest_instant(f, "minority_interest")
    olease, _, _, _ = _latest_instant(f, "operating_lease_liability")
    da_s, _, _ = _series(f, "dep_amort", 3)
    gp_s, _, _ = _series(f, "gross_profit", 3)
    if not gp_s:
        # Derived only when both legs are present for the same number of years, so a
        # short COGS series cannot silently pair with a long revenue series.
        cogs_s, _, _ = _series(f, "cogs", 3)
        n = min(len(rev), len(cogs_s))
        gp_s = [rev[i] - cogs_s[i] for i in range(n)] if n else []
    gw_s, _, _ = _series(f, "goodwill", 3)
    intang_s, _, _ = _series(f, "intangibles", 3)
    gw, _, _, _ = _latest_instant(f, "goodwill")
    intang, _, _, _ = _latest_instant(f, "intangibles")
    eq_now, _, eq_end, _ = _latest_instant(f, "equity")
    _, _, latest_end = _latest(f, "revenue")
    # The newest date across the balance-sheet reads, so downstream can say how current
    # the enterprise value actually is instead of assuming it matches the fiscal year end.
    bs_asof = max([d for d in (debt_end, dc_end, cash_end, eq_end) if d], default=None)
    return {
        "cik": cik,
        "entity": f.get("entityName"),
        "fy_end": latest_end,
        "revenue_series": rev,
        "net_income_series": ni,
        "net_income_common_series": ni_common,
        "net_income_concept": ni_c,
        "equity_series": eq,
        "ebit": ebit,
        "ebit_derived": ebit_derived,
        "interest_expense": intex,
        "total_debt": debt_noncurrent + debt_current_all,
        "cash": cash or 0.0,
        "short_term_investments": sti or 0.0,
        "preferred": pref or 0.0,
        "minority_interest": minint or 0.0,
        "operating_lease_liability": olease or 0.0,
        "shares": shares,
        "shares_asof": shares_asof,
        "shares_source": shares_src,
        # How current the enterprise value and the WACC weights actually are. Before
        # this, both silently used the fiscal year end no matter how much had happened.
        "balance_sheet_asof": bs_asof,
        "balance_sheet_form": debt_form or cash_form,
        "equity_now": eq_now,
        "goodwill": gw or 0.0,
        "intangibles": intang or 0.0,
        # series so returns can be averaged as RATIOS per year: averaging equity LEVELS
        # across an acquisition (UMBF/Heartland: book 3.5B -> 7.7B) corrupts P/TBV badly
        "goodwill_series": gw_s,
        "intangibles_series": intang_s,
        # Denominators for the multiples model, which is the only valuation available
        # for a name whose normalized FCFF is negative.
        "dep_amort_series": da_s,
        "gross_profit_series": gp_s,
        "cfo_series": cfo,
        "sbc_series": sbc,
        "capex_series": capex,
        # which equity concept was picked decides whether NCI is already inside the
        # number: StockholdersEquity is parent-only, the IncludingPortion... variant and
        # IFRS Equity are not. justified_pb cannot deduct minority interest correctly
        # without knowing which one it got.
        "equity_concept": eq_c,
        "source": {"cfo": cfo_c, "capex": capex_c, "debt": debt_concepts,
                   "equity": eq_c,
                   "url": f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"},
    }


# --- recent 8-K filers, cheaply ----------------------------------------------
def recent_8k_ciks(days_back=4):
    """Set of CIKs that filed an 8-K in the last `days_back` business days.
    Uses the daily full index: ~5 requests for the entire market."""
    out, day, checked = set(), dt.date.today(), 0
    while checked < days_back:
        day -= dt.timedelta(days=1)
        if day.weekday() >= 5:
            continue
        checked += 1
        q = (day.month - 1) // 3 + 1
        url = (f"https://www.sec.gov/Archives/edgar/daily-index/{day.year}/QTR{q}/"
               f"form.{day:%Y%m%d}.idx")
        try:
            body = _get(url)
        except (FileNotFoundError, urllib.error.HTTPError):
            continue          # holiday / not yet published
        for line in body.splitlines():
            if line.startswith("8-K "):
                parts = line.split()
                for p in parts:
                    if p.isdigit() and len(p) <= 10:
                        out.add(int(p))
                        break
    return out


def recent_filings(cik, forms=("8-K", "10-K", "10-Q", "DEF 14A"), limit=12):
    """Recent filings for ONE company, from the submissions endpoint.
    Only called for the ten names selected each day, so the cost is 10 requests."""
    try:
        blob = json.loads(_get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json"))
    except Exception:
        return []
    r = blob.get("filings", {}).get("recent", {})
    out = []
    for i in range(len(r.get("form", []))):
        if r["form"][i] not in forms:
            continue
        acc = r["accessionNumber"][i].replace("-", "")
        out.append({
            "form": r["form"][i],
            "filed": r["filingDate"][i],
            "items": (r.get("items") or [""] * (i + 1))[i],
            "doc": r["primaryDocument"][i],
            "url": (f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/"
                    f"{r['primaryDocument'][i]}"),
        })
        if len(out) >= limit:
            break
    return out


# --- 8-K exhibits: the earnings deck, from a source that will not break -------
# There is no free index mapping a ticker to its investor-relations site, and IR pages
# are per-company, JavaScript-rendered and frequently bot-blocked -- scraping them
# across 1,956 names produces silent nothing for most of them. The material that deck
# contains is filed anyway: under Item 2.02 (results) or 7.01 (Reg FD), EX-99.1 is
# almost always the press release and EX-99.2 the presentation itself. Those live on
# EDGAR, are already covered by SEC_USER_AGENT, and do not move.

# Item codes worth pulling exhibits for, and what each one means in a brief.
MATERIAL_8K_ITEMS = {
    "1.01": "entry into a material agreement",
    "1.02": "termination of a material agreement",
    "2.01": "completion of an acquisition or disposition",
    "2.02": "results of operations",
    "2.03": "new debt obligation",
    "2.06": "material impairment",
    "3.02": "unregistered sale of equity",
    "4.01": "change of accountant",
    "5.02": "officer or director change",
    "7.01": "Reg FD disclosure",
    "8.01": "other material event",
}


_DOC_BLOCK = re.compile(r"<DOCUMENT>(.*?)</DOCUMENT>", re.S | re.I)


def _sgml_field(block, name):
    """One line-delimited SGML header field, e.g. `<TYPE>EX-99.1`."""
    m = re.search(rf"<{name}>(.*)", block, re.I)
    return m.group(1).strip() if m else ""


def filing_documents(cik, accession):
    """Every document inside one filing, with the exhibit type EDGAR assigned it.

    Read from the submission's SGML header (`<accession>-index-headers.html`), NOT from
    the directory `index.json`. That endpoint looks like it carries the answer and does
    not: its `type` field is the icon filename — literally "text.gif" and
    "compressed.gif" — and it has no description at all. Keying off it meant
    `type.startswith("EX-99")` was false for every document of every filing ever, so
    `exhibits_for` returned an empty list universally and every brief printed "No EX-99
    exhibits filed under a material 8-K item" as though that were a fact about the
    company. All ten names on 2026-09-01 printed it while filing 8-Ks under items 2.02
    and 9.01; ANF's Q2 press release was sitting in that same directory the whole time as
    q22026pressrelease.htm, and it held the $100M one-time tariff refund that decided the
    name.

    The header file is small, is served for every submission, and gives TYPE, FILENAME
    and DESCRIPTION per document. Its SGML tags arrive HTML-escaped inside a <pre>, so
    unescape before parsing.
    """
    acc = str(accession).replace("-", "")
    if len(acc) != 18:
        return []
    dashed = f"{acc[:10]}-{acc[10:12]}-{acc[12:]}"
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc}"
    try:
        txt = _html.unescape(_get(f"{base}/{dashed}-index-headers.html"))
    except Exception:
        return []
    out = []
    for block in _DOC_BLOCK.findall(txt):
        name = _sgml_field(block, "FILENAME")
        if not name or not name.lower().endswith((".htm", ".html", ".txt", ".pdf")):
            continue
        out.append({
            "name": name,
            "type": _sgml_field(block, "TYPE").upper(),
            "description": _sgml_field(block, "DESCRIPTION"),
            "size": None,
            "url": f"{base}/{name}",
        })
    return out


def filings_with_items(cik, days_back=120, forms=("8-K",), limit=40):
    """Recent filings for one company WITH their item codes, newest first.

    `recent_filings` already reads the submissions endpoint; this keeps the item string
    parsed into a list and filters to a date window, because an 8-K's item codes are the
    single most informative free field about what actually happened.
    """
    cutoff = (dt.date.today() - dt.timedelta(days=days_back)).isoformat()
    try:
        blob = json.loads(_get(f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json"))
    except Exception:
        return []
    r = blob.get("filings", {}).get("recent", {})
    out = []
    for i in range(len(r.get("form", []))):
        if forms and r["form"][i] not in forms:
            continue
        filed = r["filingDate"][i]
        if filed < cutoff:
            break                     # submissions come newest-first
        items = [x.strip() for x in (r.get("items") or [""] * (i + 1))[i].split(",") if x.strip()]
        out.append({
            "form": r["form"][i],
            "filed": filed,
            "accession": r["accessionNumber"][i],
            "items": items,
            "item_labels": [MATERIAL_8K_ITEMS.get(x, x) for x in items],
            "url": (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
                    f"{r['accessionNumber'][i].replace('-', '')}/{r['primaryDocument'][i]}"),
        })
        if len(out) >= limit:
            break
    return out


def exhibits_for(cik, days_back=120, max_filings=6):
    """The earnings-presentation set for one company: every EX-99.x attached to an 8-K
    filed under a material item in the window.

    Called only for the ten names picked each day, so the cost is bounded at roughly
    `10 x (1 + max_filings)` requests. Returns the URLs, not the documents -- fetching
    a PDF deck is a separate, opt-in step because some run to tens of megabytes.
    """
    out = []
    for f in filings_with_items(cik, days_back=days_back)[:max_filings]:
        if not any(i in MATERIAL_8K_ITEMS for i in f["items"]):
            continue
        for d in filing_documents(cik, f["accession"]):
            if not d["type"].startswith("EX-99"):
                continue
            out.append({
                "filed": f["filed"], "items": f["items"],
                "item_labels": f["item_labels"],
                "exhibit": d["type"], "description": d["description"],
                "kind": ("presentation" if d["name"].lower().endswith(".pdf")
                         or "present" in d["description"].lower()
                         or d["type"] == "EX-99.2" else "press release"),
                "url": d["url"],
            })
    return out


# --- the durable fundamentals store ------------------------------------------
# Raw companyfacts payloads are 0.1-4 MB each; 1,956 of them is gigabytes and cannot be
# committed. The ~20 extracted numbers per company CAN be, so the repo carries those and
# treats the raw payloads as disposable. A CI run with a cold cache re-fetches only the
# companies whose extract has aged out, not the whole index.
_STORE = None

# Bump whenever `fundamentals()` starts extracting a field the model depends on.
# Without this, a cached entry stays valid for FACTS_MAX_AGE_DAYS and a newly added
# field silently reads as missing for a month — the multiples model would have had no
# EBITDA or gross profit for any company until the store aged out on its own.
# 3: convertible debt folded into total_debt, and equity_concept recorded so
#    justified_pb can tell whether minority interest is already inside the equity
#    figure. Both change numbers the valuation depends on, so the old shape must not
#    be served — otherwise the convertible fix would not reach a single name for a
#    month and the bug would outlive its own fix.
EXTRACT_VERSION = 3


def _store_path():
    return config.DATA / "fundamentals.json"


def load_store():
    global _STORE
    if _STORE is None:
        p = _store_path()
        try:
            _STORE = json.loads(p.read_text()) if p.exists() else {}
        except json.JSONDecodeError:
            _STORE = {}
    return _STORE


def save_store():
    if _STORE is None:
        return
    config.DATA.mkdir(parents=True, exist_ok=True)
    _store_path().write_text(json.dumps(_STORE, sort_keys=True, default=float))


def fundamentals_cached(cik, max_age_days=config.FACTS_MAX_AGE_DAYS, discard_raw=True):
    """Extracted fundamentals, refreshed at most every `max_age_days`.

    Returns (data, source) where source is 'store' or 'edgar'. On a network failure we
    fall back to a STALE store entry and say so, rather than dropping the name from the
    screen entirely — a month-old 10-K extract is still the same 10-K.
    """
    store = load_store()
    key = str(cik)
    hit = store.get(key)
    if hit and hit.get("fetched_utc") and hit.get("v", 1) >= EXTRACT_VERSION:
        try:
            age = (dt.datetime.now(dt.timezone.utc)
                   - dt.datetime.fromisoformat(hit["fetched_utc"])).days
            if age < max_age_days:
                return hit["data"], "store"
        except ValueError:
            pass
    try:
        data = fundamentals(cik)
    except Exception:
        if hit:
            return hit["data"], "store_stale"
        raise
    store[key] = {"fetched_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                  "v": EXTRACT_VERSION, "data": data}
    if discard_raw:
        p = config.CACHE / "facts" / f"{cik:010d}.json"
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass
    return data, "edgar"
