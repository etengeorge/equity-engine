"""Assemble one self-contained research brief per selected name.

Context budget is enforced here, deliberately. v1 of this project stuffed the entire
sector journal into the prompt, hit a 90k character truncation, and silently delivered
the analyst a memory layer that had been cut off mid-sentence. Every section below has a
hard cap, and the brief states its own budget so an overrun is visible rather than silent.
"""
import json, textwrap, datetime as dt
import config, edgar

PRIOR_RESEARCH_CHARS = 6000
MAX_BRIEF_CHARS = 30000        # raised with the news sections; every section is still capped
COMPANY_NEWS_ITEMS = 18        # ~90 days of headlines for one name
SECTOR_NEWS_ITEMS = 10
MACRO_NEWS_ITEMS = 6
NEWS_SUMMARY_CHARS = 240       # per article; headlines carry most of the signal


def _pct(x, nd=1):
    return "n/a" if x is None else f"{x*100:+.{nd}f}%"


def _usd(x, nd=2):
    if x is None:
        return "n/a"
    for unit, div in (("B", 1e9), ("M", 1e6), ("K", 1e3)):
        if abs(x) >= div:
            return f"${x/div:,.1f}{unit}"
    return f"${x:,.{nd}f}"


def research_path(sector, ticker):
    safe = "".join(c if c.isalnum() or c in " -&" else "_" for c in sector).strip()
    return config.RESEARCH / safe / f"{ticker}.md"


def prior_research(sector, ticker, cap=PRIOR_RESEARCH_CHARS):
    """The most RECENT entries, not the oldest. Files grow forever; a head-truncation
    would feed the analyst their first-ever note and hide everything learned since."""
    p = research_path(sector, ticker)
    if not p.exists():
        return None, 0
    text = p.read_text()
    if len(text) <= cap:
        return text, 0
    tail = text[-cap:]
    cut = tail.find("\n## ")
    if cut > 0:
        tail = tail[cut + 1:]
    return tail, len(text) - len(tail)


def sector_context(sector, exclude, limit=12):
    """What we already concluded about this sector's other names. This is the compounding
    part: by the second pass through the index, every brief arrives with the sector's
    history attached."""
    safe = "".join(c if c.isalnum() or c in " -&" else "_" for c in sector).strip()
    d = config.RESEARCH / safe
    if not d.exists():
        return []
    out = []
    for f in sorted(d.glob("*.md")):
        if f.stem == exclude:
            continue
        head = f.read_text()[:1200]
        verdict = next((l for l in head.splitlines() if l.startswith("- **Verdict:**")), "")
        if verdict:
            out.append(f"{f.stem}: {verdict.replace('- **Verdict:** ', '')}")
        if len(out) >= limit:
            break
    return out


def _news_lines(articles, limit, with_summary=True):
    """Render articles as dated one-liners. Date first, because the analyst's first
    question about any headline is whether it predates the last 10-K."""
    out = []
    for a in articles[:limit]:
        ts = (a.get("ts") or "")[:10] or "undated"
        pub = a.get("publisher") or a.get("source") or ""
        line = f"- **{ts}** · {a.get('title','').strip()}"
        if pub:
            line += f" — *{pub}*"
        if a.get("url"):
            line += f" — {a['url']}"
        out.append(line)
        s = (a.get("summary") or "").strip()
        if with_summary and s:
            out.append(f"  > {s[:NEWS_SUMMARY_CHARS]}")
    return out


def news_sections(ticker, sector, A):
    """The three news blocks, each degrading to an explicit statement of absence.

    Saying "no news found" is information about confidence. Leaving the section out
    entirely lets the analyst assume the question was never asked.
    """
    try:
        import news
    except Exception:
        return
    lookback = config.NEWS_LOOKBACK_DAYS

    company = news.read("companies", ticker, days=lookback)
    A(f"## News on this company — last {lookback} days")
    if company:
        A(f"*{len(company)} items held; showing the {min(len(company), COMPANY_NEWS_ITEMS)} "
          f"most recent. Headlines and summaries only — open the URL for the full story.*")
        A("")
        for line in _news_lines(company, COMPANY_NEWS_ITEMS):
            A(line)
    else:
        A("*No company-specific news in the store for this window.* That is a fact about "
          "coverage, not about the company: a name only earns a per-company news pull when "
          "it moves, trades abnormal volume, files an 8-K, or is picked. Absence here means "
          "the wire was quiet AND the tape was quiet — treat it as a reason to lower "
          "confidence in 'nothing happened', not as confirmation of it.")
    A("")

    sec = news.read("sectors", sector, days=lookback)
    A(f"## What is happening in {sector}")
    if sec:
        A(f"*From the sector ETF feed ({news.SECTOR_ETF.get(sector, 'n/a')}), which covers "
          f"every name in this sector whether or not it got its own pull.*")
        A("")
        for line in _news_lines(sec, SECTOR_NEWS_ITEMS, with_summary=False):
            A(line)
    else:
        A("*No sector news in the store for this window.*")
    A("")

    macro = news.read("market", "macro", days=30)
    market = news.read("market", "market", days=14)
    if macro or market:
        A("## Market and macro context")
        if market:
            for line in _news_lines(market, 4, with_summary=False):
                A(line)
        if macro:
            A("")
            A("*Rules, releases and agency actions:*")
            for line in _news_lines(macro, MACRO_NEWS_ITEMS, with_summary=False):
                A(line)
        A("")


def exhibit_section(cik, A):
    """Earnings press releases and presentations, as filed.

    This is the investor-relations deck by another route: EX-99.1 is almost always the
    release and EX-99.2 the slides. Sourcing them from EDGAR rather than the company's
    IR site means they are actually there.
    """
    if not cik:
        return
    try:
        ex = edgar.exhibits_for(cik)
    except Exception as e:
        A(f"## Earnings materials\n- (exhibit lookup failed: {type(e).__name__})\n")
        return
    A("## Earnings materials (8-K exhibits)")
    if ex:
        A("*The press release and presentation as filed. EX-99.2 is usually the deck.*")
        A("")
        for e in ex[:10]:
            items = ", ".join(e.get("item_labels") or e.get("items") or [])
            desc = e.get("description") or e["exhibit"]
            A(f"- **{e['filed']}** · {e['exhibit']} · {e['kind']} — {desc}"
              + (f" *(item: {items})*" if items else "") + f" — {e['url']}")
    else:
        A("*No EX-99 exhibits filed under a material 8-K item in the last 120 days.*")
    A("")


def build(pick, screen_meta, today=None):
    r = pick["row"]
    t, sector = r["ticker"], r["sector"]
    today = today or dt.date.today()
    L = []
    A = L.append

    A(f"# {t} — {r.get('name')}")
    A(f"*{sector} · brief generated {today} · selected as **{pick['slot']}***")
    A("")
    A("## Why this name is on today's list")
    for w in pick["why"]:
        A(f"- {w}")
    if pick.get("score") is not None:
        A(f"- urgency score {pick['score']}")
    A("")

    A("## Market")
    A("| | |")
    A("|---|---|")
    A(f"| price | {_usd(r.get('price'))} |")
    A(f"| market cap | {_usd(r.get('market_cap'))} |")
    A(f"| 5d / 21d / 63d / 252d | {_pct(r.get('ret_5d'))} / {_pct(r.get('ret_21d'))} / "
      f"{_pct(r.get('ret_63d'))} / {_pct(r.get('ret_252d'))} |")
    A(f"| 60d avg daily $ volume | {_usd(r.get('dollar_volume_60d'))} |")
    A(f"| beta (vs IWM) | {r.get('beta') and round(r['beta'],2)} "
      f"(R²={r.get('beta_r2')})"
      + (f" · **{r['beta_source']}**" if r.get("beta_source") not in (None, "regression") else "")
      + " |")
    if r.get("volume_ratio"):
        A(f"| 5d volume vs 60d average | {r['volume_ratio']:.1f}x |")
    if r.get("balance_sheet_asof"):
        A(f"| balance sheet as of | {r['balance_sheet_asof']} "
          f"({r.get('balance_sheet_form') or 'n/a'}) |")
    if r.get("weight_debt") is not None:
        A(f"| WACC weights | equity {r['weight_equity']:.0%} / debt {r['weight_debt']:.0%} |")
    A("")

    A("## What the market's price already assumes")
    method = r.get("method")
    if method == "fcff":
        A(f"Normalized FCFF base **{_usd(r.get('fcff_base'))}** "
          f"(mean of CFO−capex over {len(r.get('fcff_series') or [])}y, plus after-tax interest)")
        if r.get("fcff_series"):
            A(f"  annual FCF, newest first: {[_usd(x) for x in r['fcff_series']]}")
        A(f"Enterprise value **{_usd(r.get('enterprise_value'))}** · "
          f"FCFF yield **{_pct(r.get('fcff_yield'))}**")
        A("")
        A("**Reverse DCF — the 5y FCFF growth the current price requires:**")
        A("")
        A("| WACC | implied 5y FCFF growth |")
        A("|---|---|")
        A(f"| {_pct(r.get('wacc'))[1:]} − 1pt | {_pct(r.get('implied_growth_low_wacc'))} |")
        A(f"| **{_pct(r.get('wacc'))[1:]} (point)** | **{_pct(r.get('implied_growth'))}** |")
        A(f"| {_pct(r.get('wacc'))[1:]} + 1pt | {_pct(r.get('implied_growth_high_wacc'))} |")
        A("")
        if r.get("sbc_share_of_fcff") is not None and r["sbc_share_of_fcff"] > 0.10:
            A("")
            A(f"> **Stock compensation is {r['sbc_share_of_fcff']:.0%} of this FCFF base.** "
              f"Reported operating cash flow adds it back, so the number above treats it as "
              f"free. Expensing it gives FCFF of **{_usd(r.get('fcff_ex_sbc'))}**"
              + (f" and an implied growth of **{_pct(r.get('implied_growth_ex_sbc'))}** "
                 f"instead of {_pct(r.get('implied_growth'))}."
                 if r.get("implied_growth_ex_sbc") is not None else
                 ", which is not positive — no growth rate can be solved for on that basis.")
              + " Decide which treatment you are underwriting and say so explicitly.")
        A("")
        A(f"Naive baseline for comparison: **{_pct(r.get('baseline_growth'))}** "
          f"({r.get('baseline_growth_note')}).")
        A(f"Gap under that baseline: **{_pct(r.get('gap'))}** "
          f"(fair value {_usd(r.get('fair_value'))} vs price {_usd(r.get('price'))}).")
        A("")
        A("> The baseline is the company's own revenue history mechanically applied to FCFF. "
          "It is NOT a thesis and carries no judgment — it exists only to rank candidates. "
          "Your job below is to replace it.")
    elif method == "book":
        A("This is a financial. FCFF is meaningless here (debt is raw material, not "
          "financing), so the model is justified price/tangible book from sustainable ROTCE.")
        A("")
        A("| | |")
        A("|---|---|")
        A(f"| sustainable ROTCE | {_pct(r.get('rotce'))} |")
        A(f"| cost of equity | {_pct(r.get('cost_of_equity'))} |")
        A(f"| justified P/TBV | {r.get('justified_p_tbv') and round(r['justified_p_tbv'],2)} |")
        A(f"| actual P/TBV | {r.get('actual_p_tbv') and round(r['actual_p_tbv'],2)} |")
        A(f"| tangible book / share | {_usd(r.get('tangible_book_per_share'))} |")
        A(f"| implied gap | {_pct(r.get('gap'))} |")
    else:
        A(f"**No defensible free numeric model for this name** (status: {r.get('status')}).")
        if r.get("model_note"):
            A(f"> {r['model_note']}")
        A("")
        A("Research it qualitatively. Do NOT invent a fair value to fill the gap — "
          "'no model' is a legitimate and expected outcome, and saying so is the correct "
          "answer when the cash flows won't support a valuation.")
    A("")

    mv = r.get("multiple_valuation")
    if mv and mv.get("rows"):
        A("## What the sector cohort pays for this")
        A("*A discounted cash flow cannot value negative cash flow, but 'unmodellable' "
          "and 'worthless' are different claims. Below is what this name is worth at the "
          "multiples its own sector actually trades at. Read the RANGE — a comparables "
          "valuation is a statement about the cohort, not about this company.*")
        A("")
        A("| multiple | its own | cohort p25 / median / p75 | value at p25 / median / p75 |")
        A("|---|---|---|---|")
        for m in mv["rows"]:
            own = f"{m['own_multiple']:.1f}x" if m.get("own_multiple") else "n/a"
            A(f"| {m['metric']} (n={m['cohort_n']}) | {own} | "
              f"{m['cohort_p25']:.1f}x / {m['cohort_median']:.1f}x / {m['cohort_p75']:.1f}x | "
              f"{_usd(m['value_low'])} / {_usd(m['value_mid'])} / {_usd(m['value_high'])} |")
        A("")
        A(f"Blended midpoint **{_usd(mv.get('blended_value'))}** vs price "
          f"{_usd(r.get('price'))} — gap **{_pct(mv.get('gap'))}**.")
        A("")
        A("> This number is NOT in the cohort rank or the selection score, on purpose: "
          "those are built from DCF gaps and mixing the two would compare different "
          "things. It is here for you to judge, not to defer to.")
        A("")

    if r.get("cohort_pct") is not None:
        A(f"Cohort: **{r['cohort_pct']:.0f}th percentile** of {r.get('cohort_n')} "
          f"{sector} names priced the same way — a HIGH percentile means cheap relative "
          f"to peers (gap vs cohort median: {_pct(r.get('gap_vs_cohort'))}).")
    else:
        A(f"Cohort: **not ranked** — too few comparable {sector} names to define a "
          f"distribution honestly, so judge the absolute gap with extra caution.")
    A(f"Cohort rank is the honest comparator — absolute gaps shift with the ERP "
      f"({screen_meta['assumptions']['equity_risk_premium']:.1%}) and terminal growth "
      f"({screen_meta['assumptions']['terminal_growth']:.1%}) constants, which are choices, not facts.")
    A("")

    flags = r.get("flags") or []
    A("## Data-quality flags")
    if flags:
        A("Attack these before you trust any number above.")
        for f in flags:
            A(f"- `{f}`")
    else:
        A("- none raised")
    A("")

    if r.get("cik"):
        A("## Recent filings")
        try:
            for f in edgar.recent_filings(r["cik"], limit=10):
                items = f" — items {f['items']}" if f["items"] else ""
                A(f"- {f['filed']} **{f['form']}**{items} — {f['url']}")
        except Exception as e:
            A(f"- (filing lookup failed: {type(e).__name__})")
        A("")

    exhibit_section(r.get("cik"), A)
    news_sections(t, sector, A)

    prior, dropped = prior_research(sector, t)
    A("## What we concluded before")
    if prior:
        A(f"*(most recent {len(prior)} chars of the file"
          + (f"; {dropped} older chars not shown)*" if dropped else ")*"))
        A("")
        A(prior.strip())
    else:
        A("*No prior research — this is the first pass on this name.*")
    A("")

    peers = sector_context(sector, t)
    if peers:
        A(f"## Prior verdicts elsewhere in {sector}")
        for p in peers:
            A(f"- {p}")
        A("")

    A(TASK)
    text = "\n".join(L)
    if len(text) > MAX_BRIEF_CHARS:
        text = (text[:MAX_BRIEF_CHARS]
                + f"\n\n> **BRIEF TRUNCATED** at {MAX_BRIEF_CHARS} chars. "
                  "Sections above are complete; the task block was cut — re-read it "
                  "from ROUTINE.md before answering.\n")
    return text


TASK = """---

## Your task

Work in this order. Do not skip to the answer.

1. **Steelman the price.** The implied-growth number above is what a large number of
   informed people are collectively willing to pay for. Argue their case first, in
   specifics. If you cannot construct a credible reason for the current price, you have
   not understood the name yet — go back and read.
2. **Research.** Start with what is already in this brief: the 90 days of company news,
   the sector feed, and the 8-K exhibits — the press release is EX-99.1 and the
   presentation is usually EX-99.2. Then search for anything after the last item shown.
   Guidance, management change, litigation, regulation, end-market demand, capital
   allocation. Note what you could NOT find; absence of news is information about your
   confidence, not permission to assume nothing happened.

   **If you need a document this runtime cannot open, fetch it.** SEC and most hosts are
   blocked from the analyst session, but the `adhoc-fetch` GitHub workflow runs on a
   machine with full internet. Dispatch it with the ticker and what you need, wait for it
   to finish, `git pull`, and read `data/adhoc/<TICKER>/`. It takes about ninety seconds
   and it is the difference between reading a filing and guessing at one. Use it whenever
   an input actually turns on a number you cannot see.
3. **Attack the model's inputs before its conclusion.** Every flag above is a live
   objection. Is the FCFF base a peak or a trough? Is the share count current? Is there
   an acquisition inside the window that makes the history incomparable? Is the growth
   history a real trend or one lumpy year? Check the 8-K list above for items 1.01, 2.01
   and 3.02 in the last two quarters — a completed acquisition, a new financing or an
   equity issuance AFTER the last 10-K invalidates the enterprise value and the share
   count this model is built on, and nothing flags that for you.
4. **Form your own base case.** State a 5-year FCFF growth rate (or, for a financial, a
   sustainable ROTCE) and defend it in one paragraph tied to the business, not to the
   stock. Say explicitly where you differ from the naive baseline and why.
5. **Devil's advocate — a genuinely adversarial pass.** Argue the OPPOSITE of your base
   case as well as you argued the base case. The strongest version, not a strawman: what
   would have to be true for you to be wrong, what evidence would show it, and is any of
   that evidence already visible? Then reconcile: state your final assumption and say
   plainly which of the devil's-advocate points you could not answer.
6. **Size the conclusion honestly.** `no_edge` is the correct and expected answer most of
   the time. A gap that exists only because of a data artifact is not a gap. A gap you
   cannot explain with a mechanism is not a thesis — say so and move on.

Return ONLY a JSON object, no prose around it:

```json
{
  "ticker": "XXXX",
  "consensus_case": "the strongest argument for today's price, in specifics",
  "what_changed": "news/filings since the last 10-K, or 'nothing material found'",
  "base_case_growth": 0.05,
  "base_case_rationale": "one paragraph, tied to the business",
  "fcff_base_override": null,
  "bear_growth": 0.00,
  "bull_growth": 0.09,
  "scenario_drivers": {
    "bear": "the specific thing that has to go wrong, not just a lower number",
    "bull": "the specific thing that has to go right"
  },
  "rotce_override": null,
  "devils_advocate": {
    "strongest_counter": "the best case that the base case is wrong",
    "what_would_prove_it": "the observable that would settle it",
    "already_visible": "any of that evidence present today, or 'none'",
    "unresolved": "what you could not answer"
  },
  "final_growth": 0.04,
  "conviction": "low | medium | high",
  "verdict": "cheap | fair | rich | no_model | no_edge",
  "horizon_months": 24,
  "key_risks": ["...", "..."],
  "watch_for": ["the specific event that would change this view"],
  "data_quality_note": "which flags above you resolved and which remain open",
  "sources": ["urls actually read"]
}
```

Rules that override everything above:
- `final_growth` is the single number that moves the valuation. Everything else is the
  audit trail for why. Set it from your reasoning, not from the gap you want.
- **For a financial (`book` method), put your sustainable ROTCE in `rotce_override`**,
  as a decimal — 0.14 for 14%. That is the number the model prices, and it is a RETURN,
  not a growth rate. Leave `final_growth` null on those names.
- **Always give `bear_growth` and `bull_growth`,** and name the driver of each in
  `scenario_drivers`. Not "a bit worse" and "a bit better" — the specific thing that has
  to happen. The output is a grid of fair values across those cases and across the
  discount rate, and that spread is the honest precision of this model. A single point
  estimate claims a precision it does not have.
- If the FCFF base is negative and the brief shows a multiples valuation, you may reason
  from that instead. Say plainly that you are valuing on comparables, quote the cohort
  size, and treat the range as a range — a comparables number is a statement about the
  cohort, not about this company.
- If the devil's advocate wins, say so and set `verdict` accordingly. A red-team pass
  that never changes an answer is theatre.
- Never manufacture a fair value for a `no_model` name.
- An extreme gap is a suspected data error until you have personally verified the inputs.
"""


def write_all(picks, screen_meta, outdir=None):
    outdir = outdir or config.ROOT / "briefs"
    outdir.mkdir(parents=True, exist_ok=True)
    for f in outdir.glob("*.md"):
        f.unlink()
    written = []
    for p in picks:
        text = build(p, screen_meta)
        path = outdir / f"{p['ticker']}.md"
        path.write_text(text)
        written.append((p["ticker"], len(text)))
    return written
