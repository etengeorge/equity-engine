"""
Three COMPLETE end-to-end run-throughs on deliberately hard cases. Isolated in a temp
STORE_DIR so it never touches the curated store/out. Live (real EDGAR + prices).

  RUN 1  cross-industry spillover  — a health-IT (tech-classified) name whose thesis hinges
                                     on a HEALTHCARE regulation; must route into Healthcare.
  RUN 2  adversarial / degenerate  — bogus ticker, no-revenue biotech, distressed name, control;
                                     must refuse/flag, never crash, never manufacture a BUY.
  RUN 3  operational via routine    — index churn (a HELD name leaves), a commodity peak, and a
                                     bad ticker in one run; must flag the departure, handle the
                                     peak, skip the bad name, stay recommend-only.
"""
import os
import tempfile
import json

os.environ["STORE_DIR"] = tempfile.mkdtemp(prefix="ee_hard_")
os.environ.setdefault("SEC_USER_AGENT", "equity-engine test you@example.com")
os.environ.setdefault("PRICE_PROVIDER", "yfinance")

import engine
import sectors
import routine
import config


def hr(t):
    print("\n" + "=" * 80 + f"\n  {t}\n" + "=" * 80)


# ============================================================ RUN 1
hr("RUN 1 — CROSS-INDUSTRY SPILLOVER (health-IT name, thesis hinges on a HEALTHCARE rule)")
HSTM = {
    "company_brief": "HealthStream (HSTM) is a SaaS provider of workforce-development, credentialing and "
                     "competency software to U.S. hospitals and health systems — a tech business model with "
                     "a healthcare end-market (recurring subscriptions billed to provider organizations).",
    "adjusted_growth": 0.07,
    "market_narrative": "Market prices steady mid-single-digit SaaS growth for a healthcare-workforce niche.",
    "implied_view_interpretation": "~7% implied roughly matches its subscription growth.",
    "consensus_interrogation": "Demand is tied to hospital IT budgets and clinical-staffing regulation, not the tech cycle.",
    "perspective_spread": "Covered as a small-cap SaaS name; the real swing factor is healthcare staffing/credentialing rules.",
    "thesis_archetype": "structural_second_order",
    "variant_view": "HSTM demand is driven by HEALTHCARE staffing/credentialing regulation more than the tech cycle.",
    "mispriced_mechanism": "The market prices HSTM as generic SaaS, under-weighting that tightening hospital "
                           "staffing/credentialing regulation (a healthcare-sector driver) structurally raises "
                           "demand for its compliance modules.",
    "rationale": "Recurring revenue; the second-order driver is healthcare workforce regulation. (Illustrative hard-case run.)",
    "deviation_explanation": "Modestly above implied if a staffing rule lands; near implied otherwise.",
    "bull_case": {"narrative": "CMS staffing rule mandates credentialing", "growth": 0.12, "what_drives_it": "regulatory tailwind"},
    "base_case": {"narrative": "steady SaaS", "growth": 0.07, "what_drives_it": "renewals"},
    "bear_case": {"narrative": "hospital IT budget cuts", "growth": 0.02, "what_drives_it": "budget pressure"},
    "catalyst": "A CMS hospital staffing / credentialing rule", "catalyst_date": "2026-07-01",
    "catalyst_path": "CMS proposes staffing ratios -> hospitals must document competency -> credentialing demand rises -> HSTM attaches.",
    "what_must_happen": ["CMS advances a staffing/credentialing rule", "hospital IT budgets hold", "retention stays high"],
    "evidence": [{"claim": "HSTM sells credentialing/competency SaaS to hospitals", "source_form": "10-K",
                  "source_url": None, "source_date": None, "direction": "supports_higher"}],
    "cross_source_corroboration": "Illustrative hard-case run.",
    "disconfirming": "If staffing rules stall and hospital budgets tighten, growth stays at the low end.",
    "falsification": "A CMS rule that REDUCES mandatory credentialing, or sustained hospital IT budget cuts.",
    "conviction": 2, "horizon_months": 24, "edge_source": "synthesis",
    "relationships": [
        {"entity": "CMS hospital staffing / credentialing rules", "type": "regulator", "sector": "Healthcare",
         "note": "the real demand driver — a healthcare regulation, not a tech one"},
        {"entity": "U.S. hospitals & health systems", "type": "customer", "sector": "Healthcare", "note": "end customers"},
        {"entity": "AWS", "type": "supplier", "note": "cloud hosting (home-sector / tech edge)"}],
    "sector_update": {"learning": "Hospital staffing-ratio / credentialing regulation is tightening — a tailwind for "
                                  "healthcare-workforce compliance software and a cost/complexity item for providers.",
                      "drivers": ["CMS staffing regulation", "clinical credentialing"],
                      "entities": ["CMS hospital staffing / credentialing rules"],
                      "affected_tickers": ["HSTM"], "sectors": ["Healthcare"]},
    "company_news": "Illustrative hard-case run; HSTM thesis hinges on a healthcare-sector regulation.",
    "charts": [],
}


def prov1(prompt):
    return json.dumps(HSTM) if '"ticker": "HSTM"' in prompt else None


r1 = engine.run(["HSTM"], llm_synth_provider=prov1, gather_news=False, persist=True, write_journal=True)
row = next((x for x in r1["rows"] if not x.get("error")), None)
if row:
    print(f"HSTM home sector = {row.get('sector')} | action = {row['recommendation']['action']} "
          f"| archetype = {(row.get('thesis') or {}).get('thesis_archetype')} | src = {row.get('synthesis_source')}")
    hc = sectors.load("Healthcare")
    print(f"Healthcare dossier entities    : {list(hc['entities'].keys())}")
    print(f"Healthcare cross-sector members: {hc.get('cross_sector_members')}")
    print(f"Healthcare event log           : {[e['event'][:60] for e in hc.get('events', [])]}")
    print(f"propagation 'CMS'   -> {dict(sectors.affected_tickers(['CMS']))}")
    print(f"propagation 'hospital' -> {dict(sectors.affected_tickers(['hospital']))}")
    ok = "HSTM" in (hc.get("cross_sector_members") or []) and "HSTM" in sectors.affected_tickers(["CMS"])
    print("VERDICT:", "PASS — healthcare exposure of a tech name routed into Healthcare + propagates"
          if ok else "CHECK OUTPUT")
else:
    print("HSTM did not resolve:", r1["rows"])

# ============================================================ RUN 2
hr("RUN 2 — ADVERSARIAL DATA (bogus ticker · no-revenue biotech · distressed name · clean control)")
r2 = engine.run(["ZZZZZZ", "SAVA", "MULN", "UFPT"], gather_news=False, persist=False, write_journal=False)
buys = 0
for x in r2["rows"]:
    if x.get("error"):
        print(f"  {x['ticker']:8} ERROR: {x['error']}")
        continue
    ov = x.get("our_view") or {}
    gap = ov.get("gap_vs_price")
    act = x["recommendation"]["action"]
    if act.startswith("BUY"):
        buys += 1
    print(f"  {x['ticker']:8} {act:36} reliable={str(x.get('reliable')):5} "
          f"gap={('%+.0f%%' % (gap * 100)) if gap is not None else 'n/a':>6} "
          f"flags={(x.get('reliability_flags') or [])[:3]}")
print(f"VERDICT: ran without crashing; clean BUYs on the junk basket = {buys} (want 0; control may be HOLD/PASS)")

# ============================================================ RUN 3
hr("RUN 3 — OPERATIONAL via routine (index churn: a HELD name leaves · commodity peak · bad ticker)")
HOLD = [{"ticker": "SHOO", "shares": 100, "avg_cost": 35.0}]


def write_universe(names):
    p = os.path.join(config.STORE_DIR, "IWM_holdings.csv")
    with open(p, "w") as f:
        f.write('iShares Russell 2000 ETF\nFund Holdings as of,"Jun 1, 2026"\n\nTicker,Name,Sector,Asset Class\n')
        for n in names:
            f.write(f'{n},"{n} INC",Industrials,Equity\n')


print("\n--- run 3a: baseline universe [SHOO(held), CALM, UFPT] ---")
write_universe(["SHOO", "CALM", "UFPT"])
routine.daily_routine(iwm=True, refresh_universe=True, position_source=lambda: HOLD,
                      gather_news=False, persist=True, write_journal=True, max_deep=5,
                      outdir=os.path.join(config.STORE_DIR, "out"))

print("\n--- run 3b: SHOO LEAVES the index; ZZZZZZ (bad) enters; CALM (commodity peak) stays ---")
write_universe(["CALM", "UFPT", "ZZZZZZ"])
res3 = routine.daily_routine(iwm=True, refresh_universe=True, position_source=lambda: HOLD,
                             gather_news=False, persist=True, write_journal=True, max_deep=5,
                             outdir=os.path.join(config.STORE_DIR, "out"))
ch = res3.get("universe_churn") or {}
calm = next((r for r in res3["rows"] if r.get("ticker") == "CALM"), None)
print("\nchurn:", {k: ch.get(k) for k in ("added", "removed", "held_left")})
print("CALM (commodity peak) action:", (calm or {}).get("recommendation", {}).get("action"),
      "| reliable:", (calm or {}).get("reliable"))
print("VERDICT: held SHOO flagged as left-index =", "SHOO" in (ch.get("held_left") or []),
      "; ran to completion through the bad ticker =", True)

import shutil
shutil.rmtree(os.environ["STORE_DIR"], ignore_errors=True)
print("\n[isolated temp store removed]")
