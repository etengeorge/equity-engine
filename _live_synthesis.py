"""
Live-synthesis driver: feeds the analyst's OWN deep synthesis (done by Claude via
web_search, not the deterministic stub) back through engine.run() as the
llm_synth_provider, then rebuilds the dashboard + email brief.

Each dict below is the JSON the synthesis prompt asks for (synthesis.PROMPT_TEMPLATE
output schema), including the standing reporting standards now baked into that prompt:
  - company_brief at the top (what the company does, segments, customers),
  - every source named (firm / publication / filing / dataset, with dates),
  - each section a DISTINCT job (no restating the same fact across sections),
  - chart specs for non-obvious metrics (margins, reporting swings) with cited data.

All chart data is verified from the yfinance annual income statement (pulled
2026-06-01) and company filings — not invented. Reasoning is recommend-only;
no trade is placed or suggested anywhere. Date of synthesis: 2026-06-01.
"""
import json

import engine
import outputs
import config

# ----------------------------------------------------------------------------- SHOO
SHOO = {
    "company_brief": (
        "Steven Madden (SHOO) designs and wholesales branded footwear, handbags and accessories. "
        "Its brands include Steve Madden, Dolce Vita and — since the 2025 acquisition — UK-based "
        "Kurt Geiger; it also makes low-margin private-label (unbranded) product for other "
        "retailers' house brands. It sells through U.S. department and specialty stores, its own "
        "DTC stores/websites, and international partners, and sources most product from Asia."
    ),
    "adjusted_growth": 0.13,
    "market_narrative": (
        "The reverse DCF implies ~10.2% 5y FCFF growth — below Steven Madden's ~16% six-year "
        "revenue CAGR. The story embedded in that price: revenue keeps growing (Kurt Geiger plus "
        "international), but operating margin stays near today's depressed level because tariffs "
        "are a permanent cost, the Kurt Geiger mix is lower-margin, and discretionary footwear "
        "demand is soft."
    ),
    "implied_view_interpretation": (
        "In plain terms, ~10.2% pays for mid-single-digit-plus revenue growth while assuming "
        "little of the FY2025 operating-margin collapse — to 3.2%, from 13.5%/11.1%/10.4% in "
        "FY2022-24 (see chart) — ever reverses. The market is capitalizing the trough, not a recovery."
    ),
    "consensus_interrogation": (
        "Why the market holds it: the FY2025 margin hit is real, and the Q1 FY2026 EPS beat "
        "($1.00 vs $0.57) was flattered by a one-time ~$90.2M IEEPA tariff refund (IEEPA = the "
        "emergency-powers law the 2025 China tariffs were levied under), so quant screens read "
        "'low-quality earnings.' What it under-weights: the exposure driving the trough is being "
        "structurally removed. Per the Q1 FY2026 call (Motley Fool transcript, 2026-05-06), China "
        "fell from >70% of sourcing in 2024 to the low-40s in 2025, targeted to mid-single-digit % "
        "of U.S. imports (ex-Kurt Geiger) by spring 2026 — a cost treated as permanent that is ~90% gone."
    ),
    "perspective_spread": (
        "The disagreement is about margin TIMING, not direction. Bull framing: ainvest's "
        "'strategic turnaround / undervalued growth' pieces (Jul 2025) lean on the sourcing shift "
        "and Kurt Geiger. Bear input: a Yahoo Finance/RSS 'three reasons to avoid SHOO' item "
        "flags the organic decline plus the tariff overhang. Management sits in between — CEO Ed "
        "Rosenfeld told WWD (2026-05) 'the worst is behind us' on tariffs while guiding 2026 EPS "
        "to only $2.00-2.10. Real sell-side coverage is thin, so the 10-Q (2026-05-08) is the most "
        "reliable input; it confirms both the margin hit and the sourcing progress."
    ),
    "thesis_archetype": "fundamentals_divergence",
    "variant_view": (
        "The market is capitalizing a transitory margin trough as if it were structural. Operating "
        "margin should partially recover from 3.2% as tariff exposure is removed and Kurt Geiger "
        "integrates, so base-case FCFF growth runs modestly above the implied ~10.2%."
    ),
    "mispriced_mechanism": (
        "The FY2025 3.2% operating margin embeds three self-liquidating costs: peak China-tariff "
        "expense, Kurt Geiger integration drag, and the wind-down of low-margin private label. The "
        "market extrapolates that 3.2% forward — but China sourcing is being cut ~90%, Kurt Geiger "
        "EBIT is guided to improve, and exiting private label is gross-margin-accretive. Normalized "
        "FCFF therefore sits above the trough the price capitalizes."
    ),
    "rationale": (
        "Operating margin ran 13.5%/11.1%/10.4% in FY2022-24 before collapsing to 3.2% in FY2025 "
        "(yfinance income statement; see chart). Q1 FY2026 (10-Q, 2026-05-08): revenue +18% to "
        "$653.1M (Kurt Geiger-led; organic down on private-label softness), gross margin 46.3%, EPS "
        "$1.00 including the one-time refund. FY2026 guide (Q1 call): revenue +10-12%, EPS $2.00-2.10, "
        "with Section 122 import tariffs (a temporary U.S. tariff authority capped at 15%) stepping "
        "to 15% after July. I set base-case 5y FCFF growth at 13% — above the implied 10.2% but well "
        "below the 16% historical CAGR — crediting a PARTIAL recovery of the ~7-point margin drop, "
        "not a full snap-back, given the ongoing 15% tariff and soft demand."
    ),
    "deviation_explanation": (
        "My 13% vs the implied 10.2% is ~3 points, and it is entirely a margin call: I accept the "
        "company's 10-12% revenue guide and add only a partial recovery of the operating-margin "
        "drop. Pricing a full margin snap-back would justify a number nearer the 16% history; I "
        "deliberately stop short of that."
    ),
    "bull_case": {
        "narrative": "Tariff mitigation completes, Kurt Geiger EBIT returns to pre-tariff levels, "
                     "private-label drag is gone, and operating margin rebuilds toward double digits.",
        "growth": 0.18,
        "what_drives_it": "China sourcing to mid-single-digits, Kurt Geiger synergies, pricing, mix lift",
    },
    "base_case": {
        "narrative": "Revenue grows ~10-12% as guided; operating margin partially recovers from the "
                     "3.2% trough but stays below the prior peak under a 15% tariff.",
        "growth": 0.13,
        "what_drives_it": "in-line revenue + partial margin recovery as the tariff/integration trough passes",
    },
    "bear_case": {
        "narrative": "15% tariffs stick, discretionary demand weakens, organic decline persists, and "
                     "Kurt Geiger stays margin-dilutive — the trough proves semi-permanent.",
        "growth": 0.05,
        "what_drives_it": "sticky tariffs, soft consumer, organic/private-label erosion, KG mix drag",
    },
    "catalyst": "Sequential operating-margin recovery as China sourcing reaches mid-single-digit % of "
                "U.S. imports (spring 2026) and Kurt Geiger EBIT normalizes; delivery of the $2.00-2.10 "
                "FY2026 EPS guide.",
    "catalyst_date": "2026-08-05",
    "catalyst_path": (
        "1) Spring 2026: China sourcing reaches mid-single-digit % of U.S. imports (ex-KG). 2) Q2/Q3 "
        "FY2026 prints: operating margin steps up sequentially once the one-time refund washes out. "
        "3) Kurt Geiger EBIT climbs toward pre-tariff levels. 4) FY2026 EPS lands in $2.00-2.10. "
        "5) The market stops capitalizing the trough and the multiple re-rates."
    ),
    "what_must_happen": [
        "China sourcing confirmed at mid-single-digit % of U.S. imports (ex-Kurt Geiger) through 2026",
        "Operating margin expands sequentially in Q2/Q3 FY2026 EXCLUDING one-time tariff refunds",
        "Kurt Geiger EBIT margin improves toward pre-tariff levels (management's stated path)",
        "FY2026 EPS tracks the $2.00-2.10 guide with no further guide-down",
    ],
    "evidence": [
        {"claim": "China fell from >70% of sourcing (2024) to the low-40s (2025), targeted to "
                  "mid-single-digit % of U.S. imports ex-Kurt Geiger by spring 2026 — a ~90% cut to "
                  "tariff-exposed sourcing.",
         "source_form": "earnings call", "source_date": "2026-05-06",
         "source_url": "https://www.fool.com/earnings/call-transcripts/2026/05/06/steven-madden-shoo-q1-2026-earnings-transcript/",
         "direction": "supports_higher"},
        {"claim": "Operating margin collapsed to 3.2% in FY2025 ($81M operating income on $2,534M "
                  "revenue) from 13.5%/11.1%/10.4% in FY2022-24 — a margin trough, not a revenue problem.",
         "source_form": "research", "source_date": "2026-06-01",
         "source_url": "https://finance.yahoo.com/quote/SHOO/financials",
         "direction": "supports_higher"},
        {"claim": "Q1 FY2026 revenue +18% to $653.1M, gross margin 46.3%, EPS $1.00 — but it included "
                  "a one-time ~$90.2M IEEPA tariff refund, so underlying margin is still tariff-depressed.",
         "source_form": "10-Q", "source_date": "2026-05-08",
         "source_url": "https://www.sec.gov/Archives/edgar/data/913241/000162828026032774/shoo-20260331.htm",
         "direction": "risk"},
        {"claim": "FY2026 guide of +10-12% revenue and $2.00-2.10 EPS; CEO Ed Rosenfeld (WWD, 2026-05) "
                  "said 'the worst is behind us' on tariffs, but Section 122 tariffs step to 15% after July.",
         "source_form": "earnings call", "source_date": "2026-05-06",
         "source_url": "https://wwd.com/footwear-news/shoe-industry-news/steven-madden-outlook-ed-rosenfeld-1238337790/",
         "direction": "risk"},
    ],
    "cross_source_corroboration": (
        "The sourcing shift is corroborated by the Q1 call transcript (Motley Fool, 2026-05-06), WWD "
        "(2026-05) and supply-chain trade coverage; the margin and refund figures tie to the 10-Q "
        "and the yfinance income statement. Bulls and bears cite the same facts and differ only on "
        "recovery speed — which is why conviction is moderate, not high."
    ),
    "disconfirming": (
        "Strongest bear case against me: the EPS beat was a one-time refund, organic revenue is "
        "genuinely declining, the 15% tariff from July is a permanent cost step-up (not a trough), "
        "Kurt Geiger is structurally lower-margin so mix may permanently cap blended margin, and "
        "footwear is discretionary into a possibly slowing consumer. If the margin cap is structural "
        "rather than cyclical, my 13% is too high and the implied ~10.2% is right."
    ),
    "falsification": (
        "Two consecutive quarters (Q2/Q3 FY2026) in which operating margin EXCLUDING one-time tariff "
        "refunds fails to expand sequentially — or a FY2026 EPS guide-down below $2.00 — invalidates "
        "the margin-recovery premise."
    ),
    "conviction": 3,
    "horizon_months": 24,
    "edge_source": "interpretation",
    "relationships": [
        {"entity": "China (sourcing/tariffs)", "type": "input", "note": "primary sourcing base; the tariff-exposed cost the thesis turns on"},
        {"entity": "Section 122 / IEEPA tariff regime", "type": "regulator", "note": "U.S. import-tariff authority setting the margin headwind"},
        {"entity": "Kurt Geiger", "type": "partner", "note": "2025 acquisition; UK luxury footwear/accessories driving mix"},
        {"entity": "Vietnam / Cambodia / Mexico / Brazil", "type": "supplier", "note": "diversified sourcing replacing China"},
        {"entity": "U.S. department & specialty retailers", "type": "customer", "note": "wholesale channel"}],
    "sector_update": {"learning": "U.S. import tariffs (Section 122 stepping to 15% after July 2026) are the swing variable for China-sourced consumer goods; sourcing diversification out of China is the mitigation to watch.",
                      "drivers": ["tariff regime", "China sourcing %"],
                      "entities": ["Section 122 / IEEPA tariff regime", "China (sourcing/tariffs)"],
                      "affected_tickers": ["SHOO"]},
    "company_news": "Q1 FY2026 (2026-05-06): +18% revenue (Kurt Geiger), gross margin 46.3%, EPS $1.00 incl. a one-time $90.2M IEEPA tariff refund; FY guide +10-12% revenue, $2.00-2.10 EPS.",
    "charts": [
        {"title": "Revenue rose while operating margin collapsed to a 3.2% trough (FY25)",
         "x": ["FY22", "FY23", "FY24", "FY25"],
         "series": [
             {"name": "Revenue ($M)", "data": [2122, 1982, 2283, 2534], "kind": "bar", "axis": "left"},
             {"name": "Operating margin (%)", "data": [13.5, 11.1, 10.4, 3.2], "kind": "line", "axis": "right"},
         ],
         "source": "yfinance annual income statement, FY2022-FY2025 (pulled 2026-06-01)"},
    ],
}

# ----------------------------------------------------------------------------- PRDO
PRDO = {
    "company_brief": (
        "Perdoceo Education (PRDO) operates online, career-focused universities funded largely by "
        "federal student aid (Title IV). Its schools are Colorado Technical University (CTU; "
        "tech/business), the American InterContinental University System (AIUS), and — since "
        "Dec 2024 — the University of St. Augustine for Health Sciences (USAHS), a campus-based "
        "physical-therapy / occupational-therapy / nursing graduate school. Customers are "
        "working-adult and graduate students; the business runs ~23-31% operating margins with zero "
        "debt and net cash."
    ),
    "adjusted_growth": 0.03,
    "market_narrative": (
        "The reverse DCF implies ~ -7.7% 5y FCFF growth — the market prices Perdoceo to SHRINK. The "
        "embedded story: for-profit colleges carry a permanent regulatory/Title-IV tail risk and a "
        "secularly challenged, counter-cyclically weak enrollment base, so the sector earns a "
        "distressed ~10x P/E regardless of current cash generation."
    ),
    "implied_view_interpretation": (
        "Concretely, -7.7% assumes free cash flow falls ~8%/yr for five years — a melting-ice-cube "
        "path. That decline is what the ~10x earnings multiple encodes."
    ),
    "consensus_interrogation": (
        "Why the market believes it: the sector has a real history of regulatory blow-ups, and "
        "Perdoceo carries specific scar tissue — a 2019 $30M FTC settlement over lead-generation "
        "marketing and a 2020 deferral of ~$39M of Title IV funds to stay inside the 90/10 rule "
        "(which bars a for-profit from drawing >90% of revenue from federal aid). 2026 is also a "
        "live regulatory year (the specifics, and who is on each side, are under Perspective spread). "
        "What the consensus under-weights: Perdoceo has structurally de-risked since the 2010s — the "
        "mechanism is below — yet it is still priced as the 2015-era sector."
    ),
    "perspective_spread": (
        "Coverage is thin and split, and the split is the signal. SELL-SIDE BULLS: Barrington "
        "Research reiterated Outperform with a $42 price target, and Weiss Ratings has a Buy; "
        "consensus is a 'Moderate Buy' with an average target around $42-44 (MarketBeat) — i.e. "
        "~30%+ above the ~$32 price, so even the Street sees upside. QUANT/CAUTIOUS: Zacks "
        "Investment Research went the other way, DOWNGRADING PRDO from Strong-Buy to Hold on "
        "2026-04-21, so the older Zacks-style 'upgraded to Buy' headlines are stale. THE BEAR CASE "
        "IS REGULATORY, sourced to government rather than the Street: 2026 is the first year a "
        "program can lose Title IV eligibility under Gainful Employment — the federal rule cutting "
        "aid to programs whose graduates' debt is high relative to earnings — with student warnings "
        "beginning July 1, 2026 (Higher Ed Dive; U.S. Dept. of Education). On top of it, the One Big "
        "Beautiful Bill Act (OBBB, signed July 2025) added an earnings-accountability test tying "
        "federal-loan eligibility to graduate-earnings benchmarks (Federal Register, 2026-04-20). "
        "The conflict: the Street prices ~30% upside while the reverse DCF prices a decline — that "
        "gap IS the regulatory discount, a tail risk rather than a base-rate cash-flow path."
    ),
    "thesis_archetype": "expectations_sentiment",
    "variant_view": (
        "A blanket regulatory-distress discount is disconnected from Perdoceo's de-risked, "
        "cash-generative fundamentals. A net-cash business growing low-single-digits should not be "
        "priced to shrink ~8%/yr; my base case is modest positive growth."
    ),
    "mispriced_mechanism": (
        "The market applies a sector-wide regulatory discount but ignores the one move that most "
        "mitigates it: the USAHS acquisition shifts mix toward graduate health-sciences programs "
        "(physical/occupational therapy, nursing) whose graduates earn well and therefore CLEAR the "
        "Gainful-Employment debt-to-earnings tests the discount is premised on. The de-risking is "
        "priced as if it never happened."
    ),
    "rationale": (
        "Operating income rose every year — $174M (FY22) -> $198M -> $212M -> $225M (FY25) — at "
        "25-31% operating margins (yfinance; see chart); the FY25 dip to 26.7% reflects lower-margin "
        "USAHS revenue entering the mix, not weakness. Q1 FY2026 (8-K press release, 2026-05-07): "
        "revenue +4.1% to $221.7M, operating income +22% to $63.1M, adjusted EPS $0.90; total "
        "enrollment +1.1% (CTU +1.9%, USAHS +3.1%, AIUS -2.2%), retention near multi-year highs. "
        "FY2026 guide: adjusted operating income $254-263M, EPS $3.05-3.16 (~10x at ~$32), zero debt. "
        "USAHS was acquired Dec 2024 for ~$138M (Businesswire), immediately accretive. Against a "
        "business whose operating income has compounded ~9%/yr, I set base-case 5y FCFF growth at "
        "+3% — a haircut below the +4% historical revenue CAGR for live 2026 regulatory risk, but "
        "far above the implied -7.7%."
    ),
    "deviation_explanation": (
        "The ~11-point gap between my +3% and the implied -7.7% is large, but the implied number is "
        "the outlier: it prices an ~8%/yr decline onto a company whose operating income grew ~9%/yr "
        "over FY22-25 and that guides higher. I am not forecasting acceleration — only that FCFF "
        "roughly holds its demonstrated low-single-digit growth instead of melting."
    ),
    "bull_case": {
        "narrative": "The 2026 regulatory framework lands benignly for Perdoceo's program mix, "
                     "health-sciences scales, enrollment/retention keep rising, and the ~10x multiple "
                     "re-rates toward the low-teens.",
        "growth": 0.06,
        "what_drives_it": "benign Gainful-Employment/OBBB outcome, USAHS growth, capital returns, re-rating",
    },
    "base_case": {
        "narrative": "FCFF grows low-single-digits in line with the demonstrated track record; USAHS "
                     "accretion is in the base; buybacks/dividend continue; the distress discount narrows modestly.",
        "growth": 0.03,
        "what_drives_it": "low-single-digit organic growth + USAHS mix, net cash, ongoing capital returns",
    },
    "bear_case": {
        "narrative": "A Gainful-Employment / OBBB finding hits a material program, AIUS decline "
                     "accelerates, a strong labor market pressures enrollment, and the multiple stays distressed.",
        "growth": -0.10,
        "what_drives_it": "adverse regulatory finding, counter-cyclical enrollment loss, AIUS erosion",
    },
    "catalyst": "2026 Gainful-Employment / OBBB outcomes landing benignly for Perdoceo's program mix, "
                "alongside continued enrollment growth and capital returns re-rating the ~10x multiple.",
    "catalyst_date": "2026-07-01",
    "catalyst_path": (
        "1) July 1, 2026: Gainful-Employment warnings/disclosures begin; Perdoceo's health-sciences "
        "and tech/business mix avoids material ineligibility. 2) The OBBB earnings-accountability "
        "rule (proposed April 2026) finalizes without a program-killing outcome. 3) Q2-Q4 FY2026 "
        "prints keep enrollment rising and confirm the $3.05-3.16 EPS guide. 4) Buybacks/dividend "
        "continue on net cash. 5) With the tail not materializing, the distressed multiple re-rates."
    ),
    "what_must_happen": [
        "No material Perdoceo program is flagged ineligible under Gainful Employment in 2026 (July 1 warnings)",
        "OBBB earnings-accountability rule finalizes without a program-killing outcome for PRDO",
        "Enrollment/retention keep rising (CTU + USAHS offsetting AIUS); FY2026 EPS tracks $3.05-3.16",
        "Net cash maintained; buybacks/dividend continue, supporting per-share FCFF",
    ],
    "evidence": [
        {"claim": "Q1 FY2026 revenue +4.1% to $221.7M, operating income +22% to $63.1M, adjusted EPS "
                  "$0.90; total enrollment +1.1% with retention near multi-year highs.",
         "source_form": "8-K", "source_date": "2026-05-07",
         "source_url": "https://www.sec.gov/Archives/edgar/data/0001046568/000119312526211824/prdo-ex99_1.htm",
         "direction": "supports_higher"},
        {"claim": "Operating income rose every year FY22-25 ($174M -> $198M -> $212M -> $225M) at "
                  "25-31% operating margins — a business compounding, not shrinking as the price implies.",
         "source_form": "research", "source_date": "2026-06-01",
         "source_url": "https://finance.yahoo.com/quote/PRDO/financials",
         "direction": "supports_higher"},
        {"claim": "USAHS (health sciences: PT/OT/nursing) acquired Dec 2024 for ~$138M, immediately "
                  "accretive, shifting mix toward high-graduate-earnings programs that clear "
                  "Gainful-Employment debt-to-earnings tests — structurally mitigating the regulatory tail.",
         "source_form": "research", "source_date": "2024-12-02",
         "source_url": "https://www.businesswire.com/news/home/20241202135619/en/Perdoceo-Education-Corporation-completes-its-previously-announced-acquisition-of-University-of-St.-Augustine-for-Health-Sciences-LLC",
         "direction": "supports_higher"},
        {"claim": "Street is constructive: Barrington Research Outperform $42 PT and Weiss Ratings Buy; "
                  "consensus 'Moderate Buy', avg target ~$42-44 (~30%+ above ~$32). Zacks downgraded to "
                  "Hold on 2026-04-21, so coverage is mixed, not uniformly bullish.",
         "source_form": "analyst ratings", "source_date": "2026-04-21",
         "source_url": "https://www.marketbeat.com/stocks/NASDAQ/PRDO/forecast/",
         "direction": "supports_higher"},
        {"claim": "2026 is the first year a program can lose Title IV eligibility under Gainful "
                  "Employment (warnings begin July 1, 2026); the OBBB Act (July 2025) added an "
                  "earnings-accountability framework — a genuine, active regulatory overhang.",
         "source_form": "research", "source_date": "2026-04-20",
         "source_url": "https://www.federalregister.gov/documents/2026/04/20/2026-07666/accountability-in-higher-education-and-access-through-demand-driven-workforce-pell-student-tuition",
         "direction": "risk"},
        {"claim": "Perdoceo's history includes a 2019 $30M FTC settlement and a 2020 90/10-rule Title "
                  "IV deferral — the market's distrust of the sector is not baseless.",
         "source_form": "research", "source_date": None,
         "source_url": "https://en.wikipedia.org/wiki/Perdoceo",
         "direction": "risk"},
    ],
    "cross_source_corroboration": (
        "Growth/guidance are corroborated by the 8-K and the yfinance income statement; the "
        "regulatory risk by the Federal Register and Higher Ed Dive; the valuation gap by MarketBeat's "
        "consensus target. Street and government sources do not contradict on facts — they weight the "
        "regulatory tail differently, which is the whole debate."
    ),
    "disconfirming": (
        "Strongest bear case against me: regulation in 2026 is not hypothetical — Gainful Employment "
        "goes live and OBBB adds earnings tests, and a single adverse program finding can impair "
        "enrollment and cash flow fast. For-profit enrollment is counter-cyclical, so a resilient "
        "labor market is a structural headwind, and AIUS is already shrinking (-2.2%). If the market "
        "is pricing a real, imminent regulatory impairment I am underweighting, then -7.7% is "
        "foresight, not fear, and my +3% is wrong."
    ),
    "falsification": (
        "A Gainful-Employment or OBBB finding that flags a material Perdoceo program as "
        "ineligible/at-risk, OR two consecutive quarters of falling total enrollment with a FY "
        "guide-down, would falsify the 'de-risked grower' thesis."
    ),
    "conviction": 3,
    "horizon_months": 24,
    "edge_source": "interpretation",
    "relationships": [
        {"entity": "U.S. Department of Education", "type": "regulator", "note": "administers Title IV; sets Gainful Employment / OBBB earnings accountability"},
        {"entity": "Title IV federal student aid", "type": "input", "note": "funds most revenue; the regulated lifeblood"},
        {"entity": "Gainful Employment rule", "type": "regulator", "note": "2026 first live year; cuts aid to programs whose grads' debt is too high vs earnings"},
        {"entity": "OBBB earnings-accountability framework", "type": "regulator", "note": "July-2025 law tying federal-loan eligibility to graduate earnings"},
        {"entity": "USAHS (health sciences)", "type": "partner", "note": "Dec-2024 acquisition de-risking the regulatory tail"}],
    "sector_update": {"learning": "2026 is the first live Gainful-Employment year (student warnings begin July 1) plus the OBBB earnings-accountability rulemaking — a sector-wide regulatory overhang on for-profit / Title-IV-funded education.",
                      "drivers": ["Title IV regulation", "Gainful Employment", "enrollment cyclicality"],
                      "entities": ["U.S. Department of Education", "Gainful Employment rule", "OBBB earnings-accountability framework"],
                      "affected_tickers": ["PRDO"]},
    "company_news": "Q1 FY2026 (2026-05-07): +4.1% revenue to $221.7M, operating income +22%, adj EPS $0.90; enrollment +1.1%, retention near multi-year highs; FY EPS guide $3.05-3.16.",
    "charts": [
        {"title": "Operating income rose every year ($174M->$225M) — priced to shrink",
         "x": ["FY22", "FY23", "FY24", "FY25"],
         "series": [
             {"name": "Operating income ($M)", "data": [174, 198, 212, 225], "kind": "bar", "axis": "left"},
             {"name": "Operating margin (%)", "data": [25.1, 27.9, 31.2, 26.7], "kind": "line", "axis": "right"},
         ],
         "source": "yfinance annual income statement, FY2022-FY2025; FY25 margin dip = lower-margin USAHS in the mix"},
    ],
}

# ----------------------------------------------------------------------------- CRAI
CRAI = {
    "company_brief": (
        "CRA International (CRAI), operating as Charles River Associates, is a Boston-based economic "
        "and management consulting firm. It sells expert testimony, litigation support and "
        "economic/strategy analysis through two segments — Legal & Regulatory Consulting (~80% of "
        "revenue: antitrust, finance, IP, energy, life sciences) and Management Consulting (~20%, "
        "incl. the Marakon brand). Customers are law firms, large corporations and government "
        "agencies (it cites 85% of the Fortune 100 and 98% of the Am Law 100); ~40% of senior staff hold PhDs."
    ),
    "adjusted_growth": 0.085,
    "market_narrative": (
        "The reverse DCF implies ~9.4% 5y FCFF growth — slightly ABOVE CRA's ~8.1% six-year revenue "
        "CAGR. The market already credits CRA as a durable, high-quality compounder printing record "
        "revenue, and pays a small premium for it."
    ),
    "implied_view_interpretation": (
        "~9.4% is not a neglected-stock number — it is a modest premium to the long-run growth rate, "
        "i.e. the quality is recognized and already in the price."
    ),
    "consensus_interrogation": (
        "Why the market holds it: CRA keeps compounding — revenue $591M -> $624M -> $687M -> $752M "
        "across FY22-25 with operating margin actually stable-to-rising at 9.9%/9.2%/10.3%/11.1% "
        "(yfinance; see chart) — and Q1 FY2026 set a record at +10.5% to $201M. The 'margin "
        "compression' in May-2026 coverage (StockStory/TradingView) is a QUARTERLY EPS effect from "
        "paying up for senior talent, not a full-year decline; FY2026 guidance is a healthy 12-13% "
        "non-GAAP EBITDA margin. There is no fact the market is collectively missing here."
    ),
    "perspective_spread": (
        "Coverage agrees more than it conflicts. Investing.com and StockStory report the Q1 record "
        "revenue and the 'beat'; the same outlets flag near-term margin/EPS pressure from the "
        "compensation ramp ('record revenue, lower profit'). Management reaffirmed FY2026 guidance "
        "($785-805M revenue, 12-13% non-GAAP EBITDA margin; 8-K 2026-05-07) and pays a $0.57 "
        "quarterly dividend. There is no short-seller or contrarian thesis of note. Aligned coverage "
        "on a fully-priced quality name is not an edge."
    ),
    "thesis_archetype": "none_efficiently_priced",
    "variant_view": (
        "No differentiated edge. CRA is a high-quality compounder already priced as one (implied "
        "9.4% > 8.1% historical CAGR). I will not manufacture a thesis the cash-flow math doesn't support."
    ),
    "mispriced_mechanism": (
        "There is no specific mis-weighting to exploit. The market correctly prices both the durable "
        "demand and the rising senior-staff cost base; the implied ~9.4% fairly captures a "
        "high-single-digit revenue grower whose FCFF growth roughly tracks revenue."
    ),
    "rationale": (
        "Revenue compounded ~8-9%/yr FY22-25 ($591M -> $752M) with operating margin 9.9%/9.2%/10.3%/"
        "11.1% — stable-to-rising, NOT compressing on a full-year basis (yfinance; see chart). Q1 "
        "FY2026 (8-K, 2026-05-07): record revenue +10.5% to $201M, utilization 77% (vs 76%), 971 "
        "consultants, with near-term EPS pressure from senior-hire compensation. FY2026 guidance "
        "reaffirmed ($785-805M; 12-13% non-GAAP EBITDA margin). With implied growth (9.4%) already a "
        "touch above the 8.1% historical CAGR, I set base-case 5y FCFF growth at 8.5% — essentially "
        "the market's number — and label none_efficiently_priced. 'Market looks right' is the "
        "correct, and common, output."
    ),
    "deviation_explanation": (
        "My 8.5% is within rounding of the implied 9.4%, a hair lower only because FCFF growth tends "
        "to lag revenue growth as compensation rises. I have no evidence for a material deviation, "
        "so I do not invent one."
    ),
    "bull_case": {
        "narrative": "Demand stays broad-based, utilization pushes above the upper-70s, and CRA gets "
                     "operating leverage on the senior-talent investment.",
        "growth": 0.11,
        "what_drives_it": "utilization break-out + leverage on the compensation investment",
    },
    "base_case": {
        "narrative": "High-single-digit revenue growth in line with guidance and history; margins "
                     "hold ~10-11%; FCFF growth slightly trails revenue.",
        "growth": 0.085,
        "what_drives_it": "steady consulting demand, utilization ~upper-70s, rising compensation",
    },
    "bear_case": {
        "narrative": "A macro / litigation-cycle slowdown cuts utilization and pipeline while "
                     "compensation stays sticky, compressing margins.",
        "growth": 0.05,
        "what_drives_it": "demand slowdown + sticky senior-staff compensation",
    },
    "catalyst": "None specific — efficiently priced. Would revisit on utilization sustainably above "
                "the upper-70s WITH margin expansion, or a clear margin inflection.",
    "catalyst_date": None,
    "catalyst_path": (
        "No re-rating catalyst identified. The watch-items that could create one: utilization "
        "sustained above the upper-70s, or evidence the senior-talent investment is producing "
        "operating leverage rather than just absorbing it. Absent that, price and value track each other."
    ),
    "what_must_happen": [
        "Utilization sustains above the upper-70s rather than holding flat",
        "Senior-talent compensation investment converts into operating leverage (margin inflection)",
        "FY2026 results land within the reaffirmed $785-805M / 12-13% EBITDA-margin guide",
    ],
    "evidence": [
        {"claim": "Revenue compounded ~8-9%/yr FY22-25 ($591M -> $752M) with operating margin "
                  "stable-to-rising at 9.9%/9.2%/10.3%/11.1% — a durable quality franchise.",
         "source_form": "research", "source_date": "2026-06-01",
         "source_url": "https://finance.yahoo.com/quote/CRAI/financials",
         "direction": "supports_higher"},
        {"claim": "Q1 FY2026 record revenue +10.5% to $201M and utilization 77% (vs 76%), but with "
                  "near-term margin/EPS pressure from senior-talent compensation ('record revenue, lower profit').",
         "source_form": "earnings call", "source_date": "2026-05-07",
         "source_url": "https://www.investing.com/news/transcripts/earnings-call-transcript-cra-international-q1-2026-revenue-hits-record-high-93CH-4669590",
         "direction": "risk"},
        {"claim": "Reaffirmed FY2026 guidance: revenue $785-805M and non-GAAP EBITDA margin 12-13%; "
                  "quarterly dividend $0.57 — solid but on-trend, not an acceleration.",
         "source_form": "8-K", "source_date": "2026-05-07",
         "source_url": "https://www.sec.gov/Archives/edgar/data/1053706/000105370626000013/crai-20260507.htm",
         "direction": "supports_lower"},
        {"claim": "Market-implied ~9.4% 5y FCFF growth already exceeds the ~8.1% six-year historical "
                  "revenue CAGR — the quality is in the price, leaving little daylight to exploit.",
         "source_form": "research", "source_date": None,
         "source_url": None,
         "direction": "supports_lower"},
    ],
    "cross_source_corroboration": (
        "Investing.com, StockStory and the 8-K all describe the same thing — record revenue, "
        "comp-driven near-term EPS pressure, guidance on trend. Alignment here is consensus, and the "
        "consensus looks right."
    ),
    "disconfirming": (
        "Against 'efficiently priced': if the senior-talent hiring is a step-change that drives "
        "durable share gains and operating leverage, CRA could compound above 9% and I am too "
        "conservative. Conversely, consulting is cyclical — a litigation/M&A slowdown would expose "
        "the now-higher fixed compensation base. Both tails exist, which is why conviction is 2, not zero."
    ),
    "falsification": (
        "Two-plus quarters of utilization sustainably above the upper-70s WITH margin expansion would "
        "prove this mispriced to the upside; a utilization/pipeline drop with sticky compensation "
        "would prove it mispriced to the downside. Either falsifies 'efficiently priced.'"
    ),
    "conviction": 2,
    "horizon_months": 18,
    "edge_source": "none",
    "relationships": [
        {"entity": "Am Law 100 / large law firms", "type": "customer", "note": "litigation & antitrust engagements (98% of Am Law 100)"},
        {"entity": "Fortune 100 corporations", "type": "customer", "note": "management & economic consulting (85% of Fortune 100)"},
        {"entity": "antitrust / M&A enforcement (DOJ/FTC)", "type": "regulator", "note": "drives demand for competition-economics work"},
        {"entity": "senior consultant talent market", "type": "input", "note": "the comp cost base; utilization is the margin swing"}],
    "sector_update": {"learning": "Litigation/economic-consulting demand is broad-based and utilization firm (upper-70s), but senior-talent compensation is the margin swing — record revenue can come with quarterly EPS pressure.",
                      "drivers": ["litigation/M&A cycle", "utilization", "senior-comp cost"],
                      "entities": ["antitrust / M&A enforcement (DOJ/FTC)"],
                      "affected_tickers": ["CRAI"]},
    "company_news": "Q1 FY2026 (2026-05-07): record revenue +10.5% to $201M, utilization 77%; near-term EPS pressure from senior-hire comp; FY guide reaffirmed $785-805M, 12-13% EBITDA margin.",
    "charts": [
        {"title": "Revenue compounding with stable-to-rising ~10-11% operating margin (quality, but priced)",
         "x": ["FY22", "FY23", "FY24", "FY25"],
         "series": [
             {"name": "Revenue ($M)", "data": [591, 624, 687, 752], "kind": "bar", "axis": "left"},
             {"name": "Operating margin (%)", "data": [9.9, 9.2, 10.3, 11.1], "kind": "line", "axis": "right"},
         ],
         "source": "yfinance annual income statement, FY2022-FY2025 (pulled 2026-06-01)"},
    ],
}

# ----------------------------------------------------------------------------- CALM
CALM = {
    "company_brief": (
        "Cal-Maine Foods (CALM) is the largest U.S. producer and marketer of shell eggs (conventional "
        "and specialty/cage-free), selling to grocery retailers, club stores and foodservice. Egg "
        "prices are a volatile commodity, so revenue and margins swing hard with the cycle. It is "
        "diversifying into prepared/ready-to-eat foods via the Echo Lake Foods (acquired Jun 2025) "
        "and Van's Foods (May 2026) acquisitions; the balance sheet is nearly debt-free with ~$500M cash."
    ),
    "adjusted_growth": -0.30,
    "market_narrative": (
        "The reverse DCF implies ~ -29.8% 5y FCFF growth. Far from a mispricing, this is the market "
        "correctly DECLINING to capitalize peak egg-cycle cash flow: it prices a steep normalization "
        "back toward mid-cycle egg economics."
    ),
    "implied_view_interpretation": (
        "-29.8% is the market saying 'today's cash flow is a cyclical peak that reverts hard' — the "
        "right read of a commodity producer at the top of a price spike, not a sign the stock is cheap."
    ),
    "consensus_interrogation": (
        "Why the market holds it (and is right): the FY2025 operating margin of 36% (and a +33% "
        "trailing revenue CAGR) sits at an avian-flu-driven peak that is already unwinding — Q3 "
        "FY2026 net income fell 90% YoY and sales 53% as conventional egg prices dropped ~70% "
        "(10-Q, 2026-04-01). Operating margin has swung 7.8% -> 30.6% -> 13.3% -> 36.1% across "
        "FY22-25 (yfinance; see chart): there is no stable earnings base to capitalize. The only "
        "thing the consensus could be 'missing' is upside if avian flu recurs — not investable on a "
        "forward basis."
    ),
    "perspective_spread": (
        "Coverage agrees prices are normalizing and debates only the landing. Food Business News and "
        "Feedstuffs document the egg-price decline and the 90% earnings drop; a Seeking Alpha piece "
        "frames it as a 'brutal downcycle but well-prepared'; WATTAgNet covers the prepared-foods "
        "diversification (Echo Lake, Van's). Late-2025 trade coverage also notes federal pricing "
        "scrutiny. No credible source argues today's cash flow is sustainable — unanimity that this "
        "is a peak means no long-side edge."
    ),
    "thesis_archetype": "none_efficiently_priced",
    "variant_view": (
        "No long-side edge. This is a commodity at peak margins, and the market's deeply negative "
        "implied growth correctly prices normalization. I will not turn a mechanical valuation gap "
        "into a BUY when the cash-flow math behind it is peak-cycle and unreliable."
    ),
    "mispriced_mechanism": (
        "The apparent 'cheapness' in a naive DCF is an ARTIFACT: normalized FCFF (a 3-year average "
        "spanning the avian-flu spike) is inflated by record egg prices, so any growth applied to it "
        "overstates value. The market's -29.8% implied growth is precisely the correction for that. "
        "Egg-price mean reversion is the dominant variable, and the market is already pricing it."
    ),
    "rationale": (
        "Operating margin swung 7.8% (FY22) -> 30.6% (FY23) -> 13.3% (FY24) -> 36.1% (FY25) on "
        "revenue $1.78B -> $3.15B -> $2.33B -> $4.26B — extreme commodity cyclicality (yfinance; see "
        "chart). Q3 FY2026 (10-Q, 2026-04-01): net income -90% to $50.5M ($1.06) from $508.5M "
        "($10.38), sales -53% to ~$667M, conventional egg prices -70%; USDA depopulations -70.6% and "
        "the layer flock +2.2% YoY (Food Business News). The engine's trailing inputs (~$4.26B "
        "revenue, ~36% EBIT margin, +33% CAGR) are all peak, which is why a 5y-growth-to-perpetuity "
        "reverse DCF is the wrong lens and the name flags reliable=False. I set base-case growth at "
        "-30% (essentially the market's normalization), label none_efficiently_priced, and decline a "
        "BUY. Echo Lake (Jun 2025) and Van's Foods (May 2026; Globe Newswire) add a small non-egg "
        "floor, not a thesis."
    ),
    "deviation_explanation": (
        "My -30% base is just below the market's -29.8% implied — I essentially AGREE and, if "
        "anything, lean slightly more cautious because reversion can overshoot into oversupply and "
        "the company faces federal pricing scrutiny. The near-zero deviation is deliberate: it "
        "neutralizes the misleading positive gap a naive DCF throws off peak-cycle cash flow."
    ),
    "bull_case": {
        "narrative": "Avian flu recurs or persists, keeping egg supply tight and prices elevated "
                     "longer than expected; diversification adds a non-commodity earnings layer.",
        "growth": 0.05,
        "what_drives_it": "renewed avian-flu supply shock, sticky elevated egg prices, prepared-foods mix",
    },
    "base_case": {
        "narrative": "Egg prices normalize toward mid-cycle as the flock rebuilds; FCFF reverts hard "
                     "from the peak; prepared-foods diversification provides only a small floor.",
        "growth": -0.30,
        "what_drives_it": "supply normalization, egg-price mean reversion off records",
    },
    "bear_case": {
        "narrative": "The flock rebuild overshoots into oversupply, egg prices fall below mid-cycle, "
                     "and federal pricing scrutiny pressures the model — a deeper-than-average trough.",
        "growth": -0.45,
        "what_drives_it": "oversupply, sub-mid-cycle egg prices, regulatory/pricing scrutiny",
    },
    "catalyst": "None on the long side. The dominant variable is the egg-price cycle, which the "
                "market is already pricing; normalization is the base case, not a re-rating catalyst.",
    "catalyst_date": None,
    "catalyst_path": (
        "No long-side re-rating path. The cycle path: flock rebuild continues -> egg prices normalize "
        "toward mid-cycle -> CALM FCFF reverts from peak. Diversification (Echo Lake, Van's) slowly "
        "grows a non-egg layer but is too small over this horizon to offset the commodity swing. A "
        "long case would require a new supply shock, which is not investable on a forward basis."
    ),
    "what_must_happen": [
        "Egg supply (layer flock) continues to normalize, pulling prices toward mid-cycle (base case)",
        "Prepared-foods (Echo Lake + Van's) grows but remains small vs the egg-segment swing",
        "No assumption that peak egg-cycle FCFF is sustainable — the naive DCF gap is treated as an artifact",
    ],
    "evidence": [
        {"claim": "Operating margin swung 7.8% -> 30.6% -> 13.3% -> 36.1% across FY22-25 — extreme "
                  "commodity cyclicality with no stable earnings base to capitalize.",
         "source_form": "research", "source_date": "2026-06-01",
         "source_url": "https://finance.yahoo.com/quote/CALM/financials",
         "direction": "risk"},
        {"claim": "Q3 FY2026 net income collapsed ~90% to $50.5M ($1.06) from $508.5M ($10.38) and "
                  "sales fell 53% to ~$667M as conventional egg prices dropped ~70% — current cash flow "
                  "is an avian-flu-driven peak.",
         "source_form": "10-Q", "source_date": "2026-04-01",
         "source_url": "https://www.sec.gov/Archives/edgar/data/16160/000156276226000046/calm-20260228.htm",
         "direction": "risk"},
        {"claim": "USDA depopulations down ~70.6% and the national layer flock up ~2.2% YoY — supply "
                  "is normalizing, structurally pulling egg prices and margins down from records.",
         "source_form": "research", "source_date": None,
         "source_url": "https://www.foodbusinessnews.net/articles/29600-cal-maine-foods-loses-momentum-as-egg-prices-weaken",
         "direction": "risk"},
        {"claim": "Diversification via Echo Lake (Jun 2025) and Van's Foods (May 2026) adds "
                  "prepared-foods revenue but is small relative to the egg-segment swing — a modest "
                  "non-commodity floor, not a thesis.",
         "source_form": "8-K", "source_date": "2026-05-12",
         "source_url": "https://www.globenewswire.com/news-release/2026/05/12/3292652/0/en/cal-maine-foods-and-sara-lee-frozen-bakery-announce-cal-maine-foods-acquisition-of-van-s-foods-brand.html",
         "direction": "supports_higher"},
    ],
    "cross_source_corroboration": (
        "Filings (10-Q) and trade press (Food Business News, Feedstuffs, WATTAgNet) corroborate the "
        "same fact: egg prices and earnings are normalizing hard from an avian-flu peak. No credible "
        "source argues peak cash flow is durable — the corroboration all points one way, against a long thesis."
    ),
    "disconfirming": (
        "The case against my 'no edge / fairly priced for reversion' call is a bull one: if avian flu "
        "recurs (CEO Sherman Miller notes the epidemiological curve resembles prior years including "
        "2022), egg prices could stay elevated and the stock would look cheap on near-term cash flow. "
        "But betting on a renewed animal-disease outbreak is not an investable forward thesis, and "
        "buying a commodity producer at peak margins is the classic value trap — so I decline the long."
    ),
    "falsification": (
        "Sustained egg prices well above mid-cycle for multiple quarters (e.g. a renewed avian-flu "
        "shock) with CALM FCFF holding near peak would falsify the 'peak reverts' base case. Absent "
        "that, normalization confirms it."
    ),
    "conviction": 2,
    "horizon_months": 24,
    "edge_source": "none",
    "relationships": [
        {"entity": "USDA", "type": "regulator", "note": "publishes flock size, depopulations, HPAI status — the supply data that sets egg prices"},
        {"entity": "HPAI / avian influenza", "type": "input", "note": "outbreaks cull layers and spike egg prices; the dominant cycle driver"},
        {"entity": "corn & soybean feed", "type": "input", "note": "primary cost input"},
        {"entity": "egg commodity price", "type": "input", "note": "revenue is largely price x volume of a volatile commodity"},
        {"entity": "Echo Lake Foods / Van's Foods", "type": "partner", "note": "prepared-foods acquisitions diversifying off the egg cycle"},
        {"entity": "grocery retailers & club stores", "type": "customer", "note": "primary sales channel"}],
    "sector_update": {"learning": "Egg prices are normalizing ~70% off the HPAI-driven peak; USDA depopulations down ~70% and the layer flock rebuilding — bearish for shell-egg producers' near-term margins (a peak that reverts, not a base to capitalize).",
                      "drivers": ["egg price cycle", "HPAI", "layer flock size", "feed cost"],
                      "entities": ["USDA", "HPAI / avian influenza", "egg commodity price"],
                      "affected_tickers": ["CALM"]},
    "company_news": "Q3 FY2026 (10-Q 2026-04-01): net income -90% to $50.5M, sales -53% as conventional egg prices fell ~70%; Van's Foods acquisition (May 2026) extends prepared-foods diversification.",
    "charts": [
        {"title": "Operating margin swung 8%->31%->13%->36%: a commodity at a cyclical peak",
         "x": ["FY22", "FY23", "FY24", "FY25"],
         "series": [
             {"name": "Revenue ($M)", "data": [1777, 3146, 2326, 4262], "kind": "bar", "axis": "left"},
             {"name": "Operating margin (%)", "data": [7.8, 30.6, 13.3, 36.1], "kind": "line", "axis": "right"},
         ],
         "source": "yfinance annual income statement, fiscal years ending May 2022-May 2025"},
    ],
}

SYNTH = {"SHOO": SHOO, "PRDO": PRDO, "CRAI": CRAI, "CALM": CALM}


def provider(prompt):
    """Match the rendered synthesis prompt to its ticker and return our JSON."""
    for tk, obj in SYNTH.items():
        if f'"ticker": "{tk}"' in prompt:
            return json.dumps(obj)
    return None  # unknown ticker -> engine falls back to stub (never crashes the run)


def main():
    positions = json.load(open("positions.json"))
    results = engine.run(["SHOO", "PRDO", "CRAI", "CALM"],
                         llm_synth_provider=provider, positions=positions,
                         persist=True, write_journal=True, gather_news=True)

    print(f"\nPAPER_MODE={config.PAPER_MODE}  (recommend-only; no trades placed or suggested)\n")
    print(f"{'TK':5} {'ACTION':38} {'ARCH':26} {'conv':4} {'gap':>8} {'fairval':>9} "
          f"{'reliable':8} {'src':6} {'charts':6}")
    for r in results["rows"]:
        if r.get("error"):
            print(f"{r['ticker']:5} ERROR {r['error']}")
            continue
        th = r.get("thesis") or {}
        ov = r.get("our_view") or {}
        gap = ov.get("gap_vs_price")
        fv = ov.get("fair_value")
        print(f"{r['ticker']:5} {r['recommendation']['action']:38} "
              f"{str(th.get('thesis_archetype'))[:26]:26} {str(th.get('conviction')):4} "
              f"{('%+.1f%%' % (gap*100)) if gap is not None else 'n/a':>8} "
              f"{('%.2f' % fv) if fv is not None else 'n/a':>9} "
              f"{str(r.get('reliable')):8} {str(r.get('synthesis_source')):6} "
              f"{len(th.get('charts') or []):6}")

    import os
    os.makedirs("out", exist_ok=True)
    print("\nwrote", outputs.build_dashboard(results, os.path.join("out", "dashboard.html")))
    print("wrote", outputs.build_email(results, os.path.join("out", "email_brief.html")))


if __name__ == "__main__":
    main()
