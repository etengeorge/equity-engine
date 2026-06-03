"""
synthesis.py - the research brain that produces a DIFFERENTIATED view.

The core idea (your correction): everyone has the 10-K. Access is not edge. Edge
comes from (a) synthesizing across sources a connection others miss, (b) interpreting
the same facts through a sharper prior, or (c) understanding WHY the market believes
what it believes and where that belief is lazy. So this layer is built to force that
thinking, not to summarize filings.

A thesis must:
  1. STEELMAN the consensus — articulate why the market prices the stock as it does,
     including the narrative behind the reverse-DCF implied growth.
  2. Run EVERY thesis lens (catalyst, fundamentals, expectations/sentiment, structural/
     second-order, cyclical, quality/durability) — not pick one a priori.
  3. Name the SPECIFIC mechanism the market is mis-weighting, corroborated by >=2
     independent sources, not a vibe.
  4. Actively seek DISCONFIRMING evidence (the bear case against our own view).
  5. Be allowed to conclude NO EDGE — "market looks right" is valid and should be common.

FREE BY DESIGN: the live reasoning runs through Claude at the orchestration layer
(Cowork/Code), using your subscription, not a metered key. The synthesizing Claude
is expected to AUGMENT the engine-supplied context with its own web_search across the
free sources (sentiment, regulatory feeds, public research) in the moment. A
deterministic stub keeps the whole pipeline testable; it is NOT investment judgment.
"""
import dataclasses as dc
import datetime as dt
import json
import re
from typing import Optional

import data_sources as ds


THESIS_ARCHETYPES = [
    "catalyst_mispricing",      # market under/over-reacting to a specific event
    "fundamentals_divergence",  # implied trajectory != unit economics support
    "expectations_sentiment",   # sentiment disconnected from fundamentals
    "structural_second_order",  # change elsewhere (reg/competitor/supplier/customer) not propagated here
    "cyclical_mean_reversion",  # market extrapolating a cyclical peak/trough as permanent
    "quality_durability",       # moat/durability mispriced (too temporary or too permanent)
    "none_efficiently_priced",  # NO EDGE — the honest null
]


@dc.dataclass
class SynthesisResult:
    adjusted_growth: float
    # the steelman: why the market prices it as it does
    market_narrative: str
    implied_view_interpretation: str
    consensus_interrogation: str        # WHY does the market believe this & what is it MISSING (anti-groupthink)
    perspective_spread: str             # how sell-side/short/retail/filings differ; where they conflict
    # our differentiated view
    thesis_archetype: str
    variant_view: str
    mispriced_mechanism: str            # the SPECIFIC thing the market is mis-weighting
    rationale: str
    deviation_explanation: str
    # scenarios
    bull_case: dict                     # {narrative, growth, what_drives_it}
    base_case: dict
    bear_case: dict
    # catalyst pathway
    catalyst_path: str                  # the SEQUENCE of events that must unfold
    what_must_happen: list              # concrete checkable conditions for the thesis to play out
    # rigor
    evidence: list                      # list[dict] -> Evidence fields, cross-source
    cross_source_corroboration: str     # how independent sources align/conflict
    disconfirming: str                  # the bear case against OUR view
    catalyst: str
    catalyst_date: Optional[str]
    falsification: str
    conviction: int                     # 1-5; low when sources thin or efficiently priced
    horizon_months: int
    edge_source: str                    # synthesis | interpretation | coverage_discipline | none
    company_brief: str = ""             # plain-English: what the company does, segments, customers
    charts: list = dc.field(default_factory=list)  # chart SPECS for non-obvious metrics (margins, swings)
    relationships: list = dc.field(default_factory=list)  # second-order edges (customer/supplier/competitor/regulator/input)
    sector_update: dict = dc.field(default_factory=dict)  # a sector-WIDE learning to record in the dossier
    company_news: str = ""              # one company-specific update to log
    source: str = "stub"                # "stub" | "llm"


# ---------------------------------------------------------------- context build
def build_context(ticker, cik, fund, implied_growth, hist_cagr,
                  vertical_notes_text, company_history_text, max_filing_chars=8000,
                  news_bundle=None, price_xcheck=None, this_sector_dossier=None,
                  congressional_trades=None):
    subs = ds.get_submissions(cik)
    meta = ds.company_meta(cik, subs)
    filings = ds.recent_filings(cik, subs=subs, limit_per_form=4)

    filing_excerpts = []
    for f in filings:
        if f["form"] in ("8-K", "10-K", "10-Q"):
            txt = ds.filing_text(f["url"], max_chars=max_filing_chars)
            if txt:
                filing_excerpts.append({"form": f["form"], "date": f["date"],
                                        "url": f["url"], "text": txt})

    ebit_margin = (fund["ebit"] / fund["revenue"]) if (fund.get("ebit") and
                                                       fund.get("revenue")) else None
    rev_series = fund.get("revenue_series", [])
    return {
        "ticker": ticker, "name": meta["name"], "sector": meta["sector"],
        "sic_desc": meta.get("sic_desc"),
        "implied_growth": implied_growth, "historical_cagr": hist_cagr,
        "ebit_margin": ebit_margin, "revenue": fund.get("revenue"),
        "revenue_series_newest_first": rev_series,
        "total_debt": fund.get("total_debt"), "cash": fund.get("cash"),
        "filing_excerpts": filing_excerpts,
        "news_cross_referenced": news_bundle,
        "material_events": (news_bundle.get("material_events") if isinstance(news_bundle, dict)
                            else None),
        "price_cross_check": price_xcheck,
        "this_sector_dossier": this_sector_dossier,
        # congressional disclosures that PROMOTED this name (a LOOK trigger — investigate
        # the plausible WHY; never proof to copy the trade). Empty when none.
        "congressional_trades": congressional_trades or None,
        "vertical_notes_ALL_SECTORS": vertical_notes_text,
        "company_history": company_history_text,
        # explicit prompts for the live synthesizer to go gather itself:
        "sources_to_augment_via_search": [
            "recent earnings call transcript tone & guidance vs prior",
            f"sector/regulatory developments for {meta['sector']} (e.g. FDA/CMS/EIA/USPTO as relevant)",
            "investor sentiment / message-board narrative (treat as contra-signal, verify)",
            "public consulting/academic research on this industry's trajectory",
            "competitor and customer/supplier news (second-order linkages)",
        ],
    }


# ---------------------------------------------------------------- the live seam
PROMPT_TEMPLATE = """You are a buy-side analyst building a DIFFERENTIATED investment view on a \
small-cap company. Your output will drive a real (paper, for now) capital decision, so \
intellectual honesty matters more than sounding smart.

THE BAR: Everyone has the 10-K. Access to public filings is NOT edge. A view is only \
worth stating if it survives this test — "Why would the market NOT already see this?" \
If you cannot answer that, the correct output is thesis_archetype="none_efficiently_priced" \
with low conviction. Most stocks are roughly efficiently priced; finding edge everywhere \
is the sign of a broken analyst. Be willing to conclude there is no edge.

You are given: the growth the market's price implies (reverse DCF), the company's own \
historical growth, recent SEC filings (8-K/10-K/10-Q text), a CROSS-REFERENCED news \
bundle (multiple sources deduplicated; stories carried by >=2 independent sources are \
flagged "corroborated" and sentiment disagreement across sources is flagged), an \
independent price cross-check, notes on ALL sectors (so you can spot cross-sector \
spillover), and this company's prior analysis history. You also have web_search — USE IT \
to gather what's missing: the latest earnings call tone and guidance, sector/regulatory \
developments, investor sentiment (as a contra-signal), public research, and \
competitor/customer/supplier news. Weight CORROBORATED news higher than single-source \
items; treat a single uncorroborated story as a lead to verify, not a fact. Synthesis \
ACROSS these sources is where edge lives.

Work through this reasoning, then output JSON only.

STEP 1 — STEELMAN THE CONSENSUS (you cannot beat a view you don't understand):
  - The reverse DCF says the market is pricing ~{implied_growth} 5y FCFF growth. What \
    NARRATIVE justifies that number? What is the market collectively believing about this \
    company's future (the bull or bear story embedded in the price)?
  - WHY does the market hold that view — what real facts, fears, or heuristics drive it?

STEP 2 — RUN EVERY LENS (do not pre-pick one). For each, ask "does this reveal a gap \
between the market's implied view and a better-reasoned expectation?":
  - catalyst_mispricing: a specific event (earnings, FDA, contract, spinoff, refi, legal) \
    the market is under- or over-reacting to.
  - fundamentals_divergence: the implied trajectory contradicts the unit economics / \
    margin structure / balance sheet reality.
  - expectations_sentiment: sentiment is disconnected from fundamentals (hype or unfair punishment).
  - structural_second_order: a change ELSEWHERE (regulation, a competitor, a supplier, a \
    customer, an adjacent sector) that the market hasn't propagated to THIS name. Use the \
    all-sectors notes here — e.g. a healthcare change hitting a tech name with healthcare exposure.
  - cyclical_mean_reversion: the market is extrapolating a cyclical peak or trough as permanent.
  - quality_durability: the market misjudges how durable the moat / earnings are.

STEP 3 — SELECT and CONSTRUCT. Pick the single strongest lens (or none_efficiently_priced). Then:
  - State the SPECIFIC mechanism the market is mis-weighting (not "sentiment is negative" — \
    rather "the market is treating the customer-concentration risk disclosed in the 10-K as \
    permanent, but the 8-K shows two new logos that diversify it, and the call guided to it").
  - WEIGH THE PERSPECTIVE SPREAD, do not count agreement. The news bundle maps viewpoints \
    (sell-side, short-seller, retail, filings) and flags where they CONFLICT. Multiple sources \
    agreeing is the CONSENSUS NARRATIVE — interrogate what they are collectively missing, do \
    NOT treat it as confirmation. Where a short-seller and a sell-side analyst disagree, that \
    conflict is the highest-signal input; reason to a view neither holds.

STEP 4 — BUILD THREE SCENARIOS. For bull, base, and bear, give a narrative AND the 5y FCFF \
growth assumption that defines each. Base = your central view (this drives the recommendation). \
Bull/bear bound it. State what specifically DRIVES each.

STEP 5 — MAP THE CATALYST PATHWAY. Not just "next earnings." Lay out the SEQUENCE of events \
that must unfold for the thesis to play out, and list the concrete, checkable conditions \
(what_must_happen) you'd watch to know it's working — each one falsifiable.

STEP 6 — DISCONFIRM (pre-mortem). Argue the bear case against YOUR OWN view. What would \
make you wrong? If you can't find disconfirming evidence, you haven't looked hard enough; \
lower your conviction accordingly.

STEP 7 — SIZE THE VIEW. Set adjusted_growth to your BASE-case 5y FCFF growth. If your work \
doesn't justify deviating from the implied {implied_growth}, set it near that value and label \
none_efficiently_priced. Conviction (1-5) reflects source strength and how genuinely \
non-consensus the insight is — NOT how much you like the story. Set horizon_months REALISTICALLY: \
most fundamental mispricings take MULTIPLE QUARTERS TO YEARS to resolve, not weeks. A thesis that \
needs the market to re-rate a business usually plays out over 12-36 months. Do not set a short \
horizon just to get faster feedback — the evaluation window is when this thesis gets graded, so \
it must match how long the mechanism realistically needs.

REPORTING STANDARDS (apply to every field — the reader acts on this with no outside context):
- COMPANY BRIEF: open with company_brief — 2-4 plain sentences on what the company does, its business \
segments, and who its customers are. Assume the reader does not already know the company.
- ATTRIBUTE EVERY SOURCE BY NAME: never write "an analyst", "some reports", or a bare "the market". \
Name the specific firm, publication, filing, or dataset, with a date where it matters — e.g. \
"Barrington Research Outperform, $42 PT (Apr 2026)" or "Q1 FY2026 10-Q (filed 2026-05-08)", not \
"an analyst upgrade". Every evidence[].source_url must point to the actual document.
- NO REPETITION ACROSS SECTIONS: each field has ONE job; state a fact where it belongs and reference \
it elsewhere by name rather than restating it. market_narrative = the consensus story; \
consensus_interrogation = why the market believes it and what it is missing; perspective_spread = who \
holds which view and where they conflict; mispriced_mechanism = the one specific mis-weighting; \
rationale = the numbers/evidence and how you reach your figure; deviation_explanation = the arithmetic \
of your number vs the market's. Detail that changes the decision is welcome; filler and restatement are not.
- CHARTS: put a spec in charts[] ONLY for a non-obvious metric a picture genuinely clarifies — a margin \
trend, a specific reporting-line swing, a hard-to-assemble ratio. Supply the underlying data inline and \
cite its source. Do NOT chart simple revenue-over-time; state that in the writing. Use [] if nothing warrants one.

SECTOR MEMORY & SECOND-ORDER (read the dossier, and feed it back):
- You are given this_sector_dossier (THIS company's sector: its drivers, the key entities — regulators, \
customers, suppliers, input commodities, competitors, partners — and which peers each touches, plus a dated \
log of recent sector events) and vertical_notes_ALL_SECTORS (every sector's dossier). These are your MEMORY \
for the structural_second_order lens: a development recorded at the sector level — a regulator acting, a \
commodity moving, a competitor or a big customer doing something — is a LEAD for this name even if it was \
never in this name's news. Small items (a partnership, a supplier capacity add, a customer guidance cut) are \
often the parts that build or break a thesis; weigh them explicitly.
- FEED the memory so it compounds: emit `relationships` (the customers / suppliers / competitors / regulators \
/ input commodities this name depends on — from the 10-K and your search, naming the universe peers they also \
touch), and when you learn something SECTOR-WIDE, emit `sector_update` so every other name in the sector \
inherits it next run.
- CROSS-INDUSTRY: edge often crosses sectors — a TECH name whose real risk is an FDA/CMS HEALTHCARE rule, an \
industrial exposed to an ENERGY-price regulation, a consumer name hit by a FINANCIAL-sector credit tightening. \
When a relationship or a learning belongs to ANOTHER industry, tag it (the relationship's `sector`, or \
`sector_update.sectors`) so it is logged in THAT industry's dossier and reaches its companies too — not just this one's.

OUTPUT — JSON only, no prose around it:
{{
  "company_brief": "<2-4 plain sentences: what the company does, its segments, and who its customers are>",
  "adjusted_growth": <float, = base_case growth>,
  "market_narrative": "<the consensus story embedded in the price>",
  "implied_view_interpretation": "<what ~{implied_growth} implied growth means in plain terms>",
  "consensus_interrogation": "<WHY the market holds its view, and specifically what it is collectively MISSING or over-weighting>",
  "perspective_spread": "<how the different source-types view this; where they conflict and what that tells you>",
  "thesis_archetype": "<catalyst_mispricing | fundamentals_divergence | expectations_sentiment | structural_second_order | cyclical_mean_reversion | quality_durability | none_efficiently_priced>",
  "variant_view": "<your differentiated view in 1-2 sentences>",
  "mispriced_mechanism": "<the SPECIFIC thing the market is mis-weighting, mechanistically>",
  "rationale": "<full reasoning, citing filings and the sources you searched>",
  "deviation_explanation": "<precisely why your base number differs from the market's implied {implied_growth}>",
  "bull_case": {{"narrative": "<what goes right>", "growth": <float>, "what_drives_it": "<drivers>"}},
  "base_case": {{"narrative": "<central view>", "growth": <float>, "what_drives_it": "<drivers>"}},
  "bear_case": {{"narrative": "<what goes wrong>", "growth": <float>, "what_drives_it": "<drivers>"}},
  "catalyst": "<the primary re-rating event>",
  "catalyst_date": "<YYYY-MM-DD or null>",
  "catalyst_path": "<the SEQUENCE of events that must unfold, in order>",
  "what_must_happen": ["<checkable condition 1>", "<condition 2>", "<condition 3>"],
  "evidence": [{{"claim": "<specific>", "source_form": "<8-K | 10-K Item 1A | earnings call | FDA | sentiment | research | competitor news>", "source_url": "<url or null>", "source_date": "<date or null>", "direction": "<supports_higher | supports_lower | risk>"}}],
  "cross_source_corroboration": "<how independent sources align OR conflict on the mechanism>",
  "disconfirming": "<the strongest bear case against YOUR view>",
  "falsification": "<what observation would prove this thesis wrong>",
  "conviction": <int 1-5>,
  "horizon_months": <int>,
  "edge_source": "<synthesis | interpretation | coverage_discipline | none>",
  "charts": [{{"title": "<what the chart shows>", "x": ["<label>", "..."], "series": [{{"name": "<e.g. Operating margin (%)>", "data": [<numbers>], "kind": "bar | line", "axis": "left | right"}}], "source": "<where the data came from>"}}],
  "relationships": [{{"entity": "<customer/supplier/competitor/regulator/input/partner name>", "type": "<customer|supplier|competitor|regulator|input|partner>", "note": "<why it matters to this name>", "tickers": ["<universe peer also touched>", "..."], "sector": "<the INDUSTRY this entity belongs to if DIFFERENT from this company's (e.g. Healthcare for an FDA/CMS rule on a tech name); else omit>"}}],
  "sector_update": {{"learning": "<a sector-WIDE development worth recording for the OTHER names in this sector, else empty>", "drivers": ["<driver it touches>"], "entities": ["<entity>"], "affected_tickers": ["<ticker>"], "sectors": ["<OTHER industries this learning also applies to, e.g. Healthcare; else omit>"]}},
  "company_news": "<one short company-specific update to log, else empty>"
}}

Do NOT invent facts not present in the filings or your search results. If sources are thin, \
say so and lower conviction. A small, well-supported edge honestly stated beats a big story.

LEARN FROM YOUR TRACK RECORD: the context includes retrospective_lessons — patterns from \
your OWN past theses that were scored after maturing (e.g. "cyclical_mean_reversion calls are \
frequently early" or "expectations_sentiment theses have a low hit-rate"). Take these seriously: \
if a lesson warns about the archetype or pattern you're about to use, adjust your horizon, \
conviction, or view accordingly. This is how you get better over time.

MATERIAL EVENTS — RE-UNDERWRITE, don't footnote: the context may include material_events \
(partnerships, M&A, regulatory decisions, clinical results, operational failures like a failed \
launch, guidance changes, executive departures, litigation). These are FACTS that change the \
business, not sentiment. If a material event is present, you MUST explicitly assess: does it \
BREAK, WEAKEN, or STRENGTHEN the specific mechanism this thesis rests on? Then re-derive your \
growth/margin assumptions and your target IN LIGHT OF IT — a failed launch or a lost anchor \
customer should move the number, not sit as a note. RELIABILITY: if the event is "confirmed" \
(>=2 independent sources or an 8-K filing), re-rate fully. If "provisional" (single unverified \
report), analyze it but mark your revised target provisional and say you await corroboration — \
early reports are often wrong or exaggerated. If later/updating news is present, price in the \
most recent, best-sourced version.

CONGRESSIONAL TRADES — a LOOK, never an ACT: the context may include congressional_trades \
(a member of Congress disclosed a large purchase/sale in this name). This is why the name was \
promoted. Treat it as a REASON TO INVESTIGATE, not as evidence the stock is mispriced and never \
as a signal to copy. Ask WHAT THE FILER MIGHT SEE that the market doesn't — pending legislation \
or appropriations, a government contract, a committee assignment touching the sector, a broader \
policy tailwind — and go verify that mechanism in filings/news/search. If you find a real, \
checkable mechanism, fold it into the thesis (cite it as evidence, source_form "congressional \
disclosure"); if you find nothing beyond the trade itself, say so and DO NOT let the disclosure \
inflate conviction — "a politician bought it" is not a thesis, and the reverse-DCF gap still governs.

CONTEXT:
{context_json}
"""


def render_prompt(context):
    return PROMPT_TEMPLATE.format(
        implied_growth=(f"{context.get('implied_growth'):.1%}"
                        if context.get("implied_growth") is not None else "n/a"),
        context_json=json.dumps(context, default=str)[:90000],
    )


def _extract_json(raw):
    """Pull a JSON object out of a model response. Handles: clean JSON, ```json fences,
    and prose preamble/postamble around a JSON object (a common real LLM output shape).
    Raises ValueError if no parseable object is found."""
    txt = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        pass
    # fall back to the first balanced {...} span
    start = txt.find("{")
    if start == -1:
        raise ValueError("no JSON object found in model response")
    depth, in_str, esc = 0, False, False
    for i in range(start, len(txt)):
        ch = txt[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(txt[start:i + 1])
    raise ValueError("unbalanced JSON object in model response")


def _clamp_int(value, default, lo, hi):
    """Coerce to int and clamp to [lo, hi]. Raises if value is non-numeric (so a truly
    malformed response falls through to the stub rather than silently miscoding)."""
    iv = int(value) if value is not None else default
    return max(lo, min(hi, iv))


def from_llm_json(raw):
    d = _extract_json(raw)
    arch = d.get("thesis_archetype", "none_efficiently_priced")
    if arch not in THESIS_ARCHETYPES:
        arch = "none_efficiently_priced"
    return SynthesisResult(
        adjusted_growth=float(d["adjusted_growth"]),
        market_narrative=d.get("market_narrative", ""),
        implied_view_interpretation=d.get("implied_view_interpretation", ""),
        consensus_interrogation=d.get("consensus_interrogation", ""),
        perspective_spread=d.get("perspective_spread", ""),
        thesis_archetype=arch,
        variant_view=d.get("variant_view", ""),
        mispriced_mechanism=d.get("mispriced_mechanism", ""),
        rationale=d.get("rationale", ""),
        deviation_explanation=d.get("deviation_explanation", ""),
        bull_case=d.get("bull_case", {}),
        base_case=d.get("base_case", {}),
        bear_case=d.get("bear_case", {}),
        catalyst_path=d.get("catalyst_path", ""),
        what_must_happen=d.get("what_must_happen", []),
        evidence=d.get("evidence", []),
        cross_source_corroboration=d.get("cross_source_corroboration", ""),
        disconfirming=d.get("disconfirming", ""),
        catalyst=d.get("catalyst", ""),
        catalyst_date=d.get("catalyst_date"),
        falsification=d.get("falsification", ""),
        # conviction is 1-5 (drives sizing) — clamp hard; horizon kept to a sane window.
        conviction=_clamp_int(d.get("conviction", 2), 2, 1, 5),
        horizon_months=_clamp_int(d.get("horizon_months", 12), 12, 1, 120),
        edge_source=d.get("edge_source", "none"),
        company_brief=d.get("company_brief", ""),
        charts=d.get("charts", []) if isinstance(d.get("charts"), list) else [],
        relationships=d.get("relationships", []) if isinstance(d.get("relationships"), list) else [],
        sector_update=d.get("sector_update", {}) if isinstance(d.get("sector_update"), dict) else {},
        company_news=d.get("company_news", "") if isinstance(d.get("company_news"), str) else "",
        source="llm",
    )


# ---------------------------------------------------------------- the stub
def stub_synthesize(context):
    """Deterministic placeholder that exercises every field. NOT investment judgment."""
    implied = context.get("implied_growth")
    hist = context.get("historical_cagr")
    excerpts = context.get("filing_excerpts", [])

    if implied is not None and hist is not None:
        # A market pricing an FCFF DECLINE (negative implied) against a positive history is the
        # classic cyclical-PEAK signature — e.g. a commodity at the top of its cycle. Blending
        # toward positive history would apply growth to PEAK cash flow and manufacture a "buy"
        # the math doesn't support (CLAUDE.md rule 3). The deterministic stub cannot judge the
        # cycle, so it defers to the market's decline rather than fight it.
        if implied < 0:
            adj, arch = implied, "none_efficiently_priced"
            mech = ("market prices an FCFF decline; the deterministic stub cannot tell a "
                    "cyclical peak from a structural fall, so it forms no differentiated view")
        else:
            adj = 0.4 * implied + 0.6 * hist
            gap = implied - hist
            if gap < -0.05:
                arch = "cyclical_mean_reversion"
                mech = ("market appears to extrapolate recent weakness/strength as permanent; "
                        "historical compounding suggests reversion")
            elif gap > 0.05:
                arch = "expectations_sentiment"
                mech = "market prices growth above the demonstrated track record"
            else:
                arch = "none_efficiently_priced"
                mech = "implied growth is close to historical; no obvious gap"
    elif implied is not None:
        adj, arch = implied * 0.9, "none_efficiently_priced"
        mech = "insufficient history to form a differentiated view"
    else:
        adj, arch = hist if hist is not None else 0.03, "none_efficiently_priced"
        mech = "valuation inputs incomplete"

    evidence = []
    for e in excerpts[:3]:
        evidence.append({"claim": f"{e['form']} {e['date']}: {e['text'][:140]}...",
                         "source_form": e["form"], "source_url": e["url"],
                         "source_date": e["date"],
                         "direction": "risk" if e["form"] == "8-K" else "supports_lower"})

    return SynthesisResult(
        adjusted_growth=round(adj, 4),
        market_narrative=("[STUB] Market-implied growth of "
                          f"{_p(implied)} reflects the consensus trajectory; the live "
                          "synthesis articulates the actual narrative behind it."),
        implied_view_interpretation=f"[STUB] Price implies ~{_p(implied)} 5y FCFF growth.",
        consensus_interrogation=("[STUB] Live synthesis explains WHY the market holds its "
                                 "view and what it is collectively missing; this placeholder "
                                 "does not interrogate consensus."),
        perspective_spread=("[STUB] Live synthesis weighs sell-side vs short vs retail vs "
                            "filings and surfaces conflicts; not assessed in stub."),
        thesis_archetype=arch,
        variant_view="[STUB] Placeholder view anchored on mean-reversion toward history.",
        mispriced_mechanism=f"[STUB] {mech}.",
        rationale=("[STUB REASONING — NOT REAL ANALYSIS] This deterministic placeholder "
                   "blends implied and historical growth and labels a lens mechanically. "
                   "Run via Claude Code (ROUTINE.md) for genuine cross-source synthesis."),
        deviation_explanation=(f"[STUB] Implied {_p(implied)} vs historical {_p(hist)}; "
                               "anchors toward the track record absent evidence otherwise."),
        bull_case={"narrative": "[STUB] upside scenario", "growth": round(adj + 0.05, 4),
                   "what_drives_it": "[STUB] live synthesis specifies drivers"},
        base_case={"narrative": "[STUB] central view", "growth": round(adj, 4),
                   "what_drives_it": "[STUB] mean-reversion toward history"},
        bear_case={"narrative": "[STUB] downside scenario", "growth": round(adj - 0.05, 4),
                   "what_drives_it": "[STUB] live synthesis specifies drivers"},
        catalyst_path=("[STUB] Live synthesis lays out the event sequence; here: next "
                       "earnings -> guidance -> multiple re-rating."),
        what_must_happen=["[STUB] earnings confirm trajectory",
                          "[STUB] guidance holds or rises",
                          "[STUB] no balance-sheet deterioration"],
        evidence=evidence,
        cross_source_corroboration="[STUB] Live synthesis weighs how sources align or conflict.",
        disconfirming=("[STUB] Live synthesis argues the bear case against its own view; "
                       "here, acceleration evidence in filings would break the reversion premise."),
        catalyst="Next earnings report and guidance update",
        catalyst_date=(dt.date.today() + dt.timedelta(days=180)).isoformat(),
        falsification=("Two consecutive quarters materially above the historical trend "
                       "would invalidate the mean-reversion premise."),
        conviction=2, horizon_months=18,
        edge_source="none",
        company_brief=("[STUB] Live synthesis writes a plain-English company brief (what it does, "
                       "its segments, and its customers); not generated in the deterministic stub."),
        charts=[],
        relationships=[], sector_update={}, company_news="",
        source="stub",
    )


def synthesize(context, llm_json=None):
    if llm_json:
        try:
            return from_llm_json(llm_json)
        except Exception as e:
            # A genuinely unparseable response correctly falls back to the stub, but record
            # WHY on the stub so a systematically-broken provider is visible (not silent).
            res = stub_synthesize(context)
            res.source = "stub_after_parse_error"
            res.rationale = (f"[STUB — LLM RESPONSE FAILED TO PARSE: {type(e).__name__}: "
                             f"{str(e)[:120]}] " + res.rationale)
            return res
    return stub_synthesize(context)


def _p(x):
    return "n/a" if x is None else f"{x*100:.1f}%"
