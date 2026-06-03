"""
retrospective.py - the learning loop. This is what makes the system compound.

It does NOT make the model intrinsically smarter (no fine-tuning, no weight update).
It makes the JOURNAL wiser: it scores matured theses, writes down where the reasoning
was right or wrong, finds patterns across many theses, and those written lessons get
fed back into future synthesis context. The model reasons over a richer, self-critical
record each run. That is real, and it is how good discretionary investors improve.

STRICT scoring (your choice): a thesis is "right" only if BOTH hold —
  (1) the named MECHANISM played out within the pinned evaluation window, AND
  (2) the IDIOSYNCRATIC return was positive in the thesis direction — i.e. the stock
      beat a same-sector basket, not just the market. This separates "right about the
      company" from "the whole sector moved" (luck).

(1) is a judgment call: in a live retro run, Claude reads the thesis + what actually
happened (new filings, price action) and judges whether the SPECIFIC mechanism played
out. Without a live judge, mechanism_played_out is recorded as 'unknown' and the verdict
falls back to the idiosyncratic-return component only (flagged as such).
"""
import datetime as dt
import os
import statistics as stats

import config
import store
import data_sources as ds
import journal


# ----------------------------------------------------------- price-at-date helper
def _price_on_or_before(ticker, iso_date):
    """Closest adjusted close on or before iso_date (and the latest close)."""
    px = ds.get_prices(ticker, lookback_days=600)
    if not px:
        return None, None
    dates, closes = px[0], px[1]
    latest = closes[-1]
    target = None
    for d, c in zip(dates, closes):
        if d <= iso_date:
            target = c
        else:
            break
    return target, latest


def _return_since(ticker, iso_date, fallback_start_price=None):
    start, latest = _price_on_or_before(ticker, iso_date)
    if start is None:
        start = fallback_start_price
    if not start or not latest:
        return None, start, latest
    return (latest / start - 1.0), start, latest


# ----------------------------------------------------------- sector basket
def _sector_peers(sector, exclude_ticker):
    """Tickers in the same sector that we have records for (synthetic basket members)."""
    d = os.path.join(config.STORE_DIR, "journal", "companies", sector.replace("/", "-"))
    if not os.path.isdir(d):
        return []
    peers = []
    for fn in os.listdir(d):
        if fn.endswith(".md"):
            tk = fn[:-3]
            if tk != exclude_ticker:
                peers.append(tk)
    return peers


def _sector_basket_return(sector, exclude_ticker, iso_date):
    """Equal-weight, trimmed-mean return of sector peers over the window. Excludes the
    name itself; trims extremes so one peer's corporate action can't impersonate the
    sector (the QA-flagged thin-basket problem)."""
    peers = _sector_peers(sector, exclude_ticker)
    rets = []
    for p in peers:
        r, _, _ = _return_since(p, iso_date)
        if r is not None:
            rets.append(r)
    if len(rets) < 2:
        return None, len(rets)
    rets.sort()
    if len(rets) >= 5:                       # trim top & bottom
        rets = rets[1:-1]
    return stats.mean(rets), len(peers)


# ----------------------------------------------------------- scoring
def score_thesis(rec, mechanism_judge=None):
    """Score one matured thesis. mechanism_judge: optional callable(thesis_dict, context)
    -> ('played_out'|'did_not'|'partial', explanation). Without it, mechanism='unknown'."""
    snap = rec.get("latest", {})
    th = snap.get("thesis")
    if not th or not th.get("evaluation_window"):
        return None
    today = dt.date.today().isoformat()
    if th["evaluation_window"] > today:
        return None  # not matured yet

    ticker = snap["ticker"]
    sector = snap.get("sector", "")
    direction = th.get("direction")          # long | avoid | hold
    created = th.get("created")
    start_price = snap.get("price")

    stock_ret, start, latest = _return_since(ticker, created, start_price)
    basket_ret, n_peers = _sector_basket_return(sector, ticker, created)
    if stock_ret is None:
        return {"ticker": ticker, "verdict": "inconclusive",
                "reason": "no price data to score", "thesis_archetype": th.get("thesis_archetype")}

    idiosyncratic = (stock_ret - basket_ret) if basket_ret is not None else None

    # mechanism judgment (component 1 of the strict definition)
    mech = "unknown"
    mech_expl = "no live judge supplied; scored on idiosyncratic return only"
    if mechanism_judge:
        try:
            result = mechanism_judge(th, {"stock_return": stock_ret,
                                          "idiosyncratic": idiosyncratic,
                                          "ticker": ticker,
                                          "cik_for_judge": rec.get("cik")})
            # contract: judge returns (mech_str, explanation_str)
            if isinstance(result, tuple) and len(result) == 2:
                mech, mech_expl = result
            else:
                # a judge that returns the wrong shape is a real failure — surface it,
                # don't silently degrade to "unknown" (that would hide a broken judge).
                mech = "judge_error"
                mech_expl = (f"mechanism judge returned unexpected shape "
                             f"{type(result).__name__}; expected (verdict, explanation) tuple")
        except Exception as e:
            mech = "judge_error"
            mech_expl = f"mechanism judge raised {type(e).__name__}: {e}"

    # direction-correct on idiosyncratic basis (component 2)
    if idiosyncratic is None:
        idio_correct = None
    elif direction == "long":
        idio_correct = idiosyncratic > 0
    elif direction == "avoid":
        idio_correct = idiosyncratic < 0       # avoid = expected underperformance
    else:
        idio_correct = None

    # STRICT verdict
    if direction == "hold" or th.get("thesis_archetype") == "none_efficiently_priced":
        verdict = "no_call"  # we explicitly took no view; nothing to grade
    elif idio_correct is None:
        verdict = "inconclusive"
    elif mech == "played_out" and idio_correct:
        verdict = "correct_idiosyncratic"        # the real win: right mechanism, beat sector
    elif mech == "played_out" and not idio_correct:
        verdict = "right_mechanism_wrong_outcome" # mechanism happened but didn't pay (timing/priced-in)
    elif mech in ("did_not", "partial") and idio_correct:
        verdict = "correct_but_wrong_reason"      # made money for a reason other than the thesis = luck
    elif mech == "unknown" and idio_correct:
        verdict = "idio_correct_mechanism_unverified"
    elif mech == "unknown" and not idio_correct:
        verdict = "idio_wrong_mechanism_unverified"
    else:
        verdict = "wrong"

    # earliness flag: only meaningful LATE in the window. On a long-horizon thesis,
    # being flat early is EXPECTED, not a failure. We flag "early" only when the
    # catalyst date has passed AND we're past ~70% of the way to the evaluation
    # window, with the mechanism still not in and the move still flat.
    early = False
    cd = th.get("catalyst_date")
    try:
        created_d = dt.date.fromisoformat(created)
        window_d = dt.date.fromisoformat(th["evaluation_window"])
        today_d = dt.date.today()
        frac_elapsed = ((today_d - created_d).days /
                        max(1, (window_d - created_d).days))
    except Exception:
        frac_elapsed = 1.0
    if (cd and cd <= today and frac_elapsed >= 0.70
            and mech in ("did_not", "partial", "unknown")
            and idiosyncratic is not None and abs(idiosyncratic) < 0.05):
        early = True

    return {
        "ticker": ticker, "sector": sector, "direction": direction,
        "thesis_archetype": th.get("thesis_archetype"),
        "conviction": th.get("conviction"), "edge_source": th.get("edge_source"),
        "created": created, "evaluation_window": th["evaluation_window"],
        "stock_return": round(stock_ret, 4),
        "sector_basket_return": round(basket_ret, 4) if basket_ret is not None else None,
        "n_peers": n_peers,
        "idiosyncratic_excess": round(idiosyncratic, 4) if idiosyncratic is not None else None,
        "mechanism_played_out": mech, "mechanism_note": mech_expl,
        "idio_direction_correct": idio_correct,
        "verdict": verdict, "likely_early": early,
        "mispriced_mechanism": th.get("mispriced_mechanism"),
    }


# ----------------------------------------------------------- pattern aggregation
def aggregate_patterns(scores):
    """Find recurring patterns across scored theses — the self-knowledge that compounds."""
    graded = [s for s in scores if s and s["verdict"] not in ("no_call", "inconclusive")]
    n = len(graded)
    if n == 0:
        return {"n_graded": 0, "lessons": ["No matured, gradeable theses yet."]}

    def hit_rate(subset):
        wins = [s for s in subset if s["verdict"] == "correct_idiosyncratic"]
        return (len(wins) / len(subset)) if subset else None

    by_arch, by_sector, by_dir = {}, {}, {}
    for s in graded:
        by_arch.setdefault(s["thesis_archetype"], []).append(s)
        by_sector.setdefault(s["sector"], []).append(s)
        by_dir.setdefault(s["direction"], []).append(s)

    lessons = []
    # archetype patterns
    for arch, subset in sorted(by_arch.items(), key=lambda kv: -len(kv[1])):
        hr = hit_rate(subset)
        early = sum(1 for s in subset if s.get("likely_early"))
        wrong_reason = sum(1 for s in subset if s["verdict"] == "correct_but_wrong_reason")
        msg = f"{arch}: {len(subset)} graded, idiosyncratic hit-rate {hr:.0%}."
        if early >= max(2, len(subset) // 2):
            msg += f" FREQUENTLY EARLY ({early}/{len(subset)}) — catalysts take longer than assumed; widen horizons."
        if wrong_reason >= max(2, len(subset) // 3):
            msg += f" {wrong_reason} 'right for the wrong reason' — gains may be luck, not edge."
        lessons.append(msg)
    # direction patterns
    for d, subset in by_dir.items():
        hr = hit_rate(subset)
        if hr is not None:
            lessons.append(f"{d} theses: {len(subset)} graded, hit-rate {hr:.0%}.")
    # overall idiosyncratic
    idios = [s["idiosyncratic_excess"] for s in graded if s["idiosyncratic_excess"] is not None]
    if idios:
        avg = stats.mean(idios)
        lessons.append(f"Overall mean idiosyncratic excess across {len(idios)} graded "
                       f"theses: {avg:+.1%}. " +
                       ("Net positive — some edge net of sector beta." if avg > 0 else
                        "Net negative/flat — NO demonstrated edge yet; do not fund."))
    return {"n_graded": n, "by_archetype_hit_rate": {a: hit_rate(s) for a, s in by_arch.items()},
            "lessons": lessons}


# ----------------------------------------------------------- run + persist lessons
LESSONS_PATH = os.path.join(config.STORE_DIR, "journal", "LESSONS.md")


def run_retrospective(mechanism_judge=None, llm_provider=None):
    """Score all matured theses, write verdicts to company journals, and write the
    aggregated lessons file that future synthesis runs read back.

    Supply EITHER a ready mechanism_judge callable, OR an llm_provider (orchestration
    layer) which is wrapped into a live judge. With neither, mechanism stays 'unknown'
    and verdicts rest on the idiosyncratic component only."""
    if mechanism_judge is None and llm_provider is not None:
        mechanism_judge = make_live_judge(llm_provider)
    cdir = os.path.join(config.STORE_DIR, "companies")
    scores = []
    if os.path.isdir(cdir):
        for fn in os.listdir(cdir):
            if fn.endswith(".json"):
                rec = store.load(int(fn[:-5]))
                if rec:
                    s = score_thesis(rec, mechanism_judge=mechanism_judge)
                    if s:
                        scores.append(s)
    patterns = aggregate_patterns(scores)

    # write per-thesis verdicts into each company's journal
    for s in scores:
        if s["verdict"] in ("no_call",):
            continue
        sector = s.get("sector", "")
        note = (f"verdict **{s['verdict']}** · idiosyncratic {(_pct(s.get('idiosyncratic_excess')))} "
                f"(stock {_pct(s.get('stock_return'))} vs sector {_pct(s.get('sector_basket_return'))}) · "
                f"mechanism {s.get('mechanism_played_out')}"
                + (" · LIKELY EARLY" if s.get("likely_early") else ""))
        journal.append_retro_note(sector, s["ticker"], note, s)

    # write the compounding lessons file
    _write_lessons(patterns, scores)
    return {"scores": scores, "patterns": patterns}


def _write_lessons(patterns, scores):
    os.makedirs(os.path.dirname(LESSONS_PATH), exist_ok=True)
    date = dt.date.today().isoformat()
    lines = [f"# LESSONS — self-critique that compounds (updated {date})", "",
             "_Read by every synthesis run. Patterns from scored, matured theses. "
             "The system does not retrain; it reasons against this record._", "",
             f"**Graded theses:** {patterns.get('n_graded', 0)}", ""]
    for L in patterns.get("lessons", []):
        lines.append(f"- {L}")
    lines += ["", "## Recent thesis verdicts", ""]
    for s in sorted([x for x in scores if x["verdict"] != "no_call"],
                    key=lambda x: x.get("created", ""), reverse=True)[:30]:
        lines.append(f"- **{s['ticker']}** [{s['thesis_archetype']}/{s['direction']}] "
                     f"→ {s['verdict']} (idio {_pct(s.get('idiosyncratic_excess'))}, "
                     f"mech {s.get('mechanism_played_out')})")
    with open(LESSONS_PATH, "w") as f:
        f.write("\n".join(lines))
    return LESSONS_PATH


def read_lessons(max_chars=6000):
    """Surfaced into synthesis context so future views are informed by past errors."""
    if os.path.exists(LESSONS_PATH):
        with open(LESSONS_PATH) as f:
            return f.read()[:max_chars]
    return "(no retrospective lessons yet — accumulate by running the retrospective on matured theses)"


def _pct(x, dp=1):
    return "—" if x is None else f"{x*100:.{dp}f}%"


# ============================================================================
# MECHANISM JUDGE — resolves "did the thesis's mechanism actually play out?"
# ============================================================================
# This is the judgment half of the strict definition. It is deliberately separate
# from the price math: the whole point is to distinguish "the mechanism happened"
# from "the price moved." So the judge reads the ORIGINAL thesis (the specific
# mechanism, the what-must-happen checklist) against FRESH evidence filed AFTER the
# thesis was created — new 8-Ks, 10-Qs, earnings — and judges whether the mechanism
# materialized. Price action is provided as context but is NOT the basis for the
# mechanism call (that would collapse the skill-vs-luck distinction we're protecting).
#
# FREE BY DESIGN: runs through Claude at the orchestration layer (subscription), same
# as synthesis. Without a live provider, the verdict is honestly 'unknown'.

import data_sources as ds  # noqa (used by judge context)


def build_judge_context(thesis_dict, cik, outcome):
    """Assemble what the judge needs: the original thesis, the outcome metrics, and
    the evidence filed AFTER the thesis was created (so it can see what actually
    happened, not just what the price did)."""
    created = thesis_dict.get("created", "")
    new_filings = []
    try:
        for f in ds.recent_filings(cik, limit_per_form=6):
            if f.get("date", "") > created:
                txt = ds.filing_text(f["url"], max_chars=6000)
                if txt:
                    new_filings.append({"form": f["form"], "date": f["date"],
                                        "url": f["url"], "text": txt})
    except Exception:
        pass
    return {
        "original_thesis": {
            "mispriced_mechanism": thesis_dict.get("mispriced_mechanism"),
            "variant_view": thesis_dict.get("variant_view"),
            "thesis_archetype": thesis_dict.get("thesis_archetype"),
            "direction": thesis_dict.get("direction"),
            "catalyst": thesis_dict.get("catalyst"),
            "catalyst_path": thesis_dict.get("catalyst_path"),
            "what_must_happen": thesis_dict.get("what_must_happen", []),
            "falsification": thesis_dict.get("falsification"),
            "created": created,
            "evaluation_window": thesis_dict.get("evaluation_window"),
        },
        "outcome": outcome,
        "evidence_filed_since_thesis": new_filings,
    }


JUDGE_PROMPT_TEMPLATE = """You are scoring one of your OWN past investment theses now that its \
evaluation window has closed. Be ruthlessly honest — the point is to learn where the REASONING \
was right or wrong, not to claim credit. The price outcome is given, but your job is NOT to grade \
the price; it is to judge whether the SPECIFIC MECHANISM the thesis bet on actually played out, \
based on what was filed and reported AFTER the thesis was created.

Critical distinction: a stock can rise for reasons unrelated to the thesis. If the mechanism did \
NOT play out but the stock rose anyway, that is LUCK, not edge — say so plainly (did_not).

ORIGINAL THESIS:
  Mechanism the market was said to be mis-weighting: {mechanism}
  Differentiated view: {variant_view}
  Direction: {direction} · Archetype: {archetype}
  Catalyst expected: {catalyst}
  What had to happen (the checklist): {what_must_happen}

WHAT ACTUALLY HAPPENED:
  Stock return over the window: {stock_return}
  Idiosyncratic excess (vs same-sector basket): {idiosyncratic}
  Evidence filed since the thesis (8-Ks/10-Qs/etc.): in the context below.

Assess each item in the checklist (met / not_met / unclear) from the evidence, then judge the \
mechanism overall. Output JSON only:
{{
  "mechanism_verdict": "<played_out | did_not | partial>",
  "explanation": "<2-4 sentences: did the mechanism materialize in the filings/reports? cite specifics>",
  "checklist_assessment": [{{"condition": "<from what_must_happen>", "status": "<met|not_met|unclear>", "note": "<why>"}}],
  "was_outcome_luck": <true|false, true if stock moved favorably but mechanism did NOT play out>,
  "lesson": "<one sentence: what this teaches about this archetype or your reasoning>"
}}

CONTEXT:
{context_json}
"""


def render_judge_prompt(ctx):
    import json as _json
    ot = ctx["original_thesis"]
    oc = ctx["outcome"]
    return JUDGE_PROMPT_TEMPLATE.format(
        mechanism=ot.get("mispriced_mechanism"), variant_view=ot.get("variant_view"),
        direction=ot.get("direction"), archetype=ot.get("thesis_archetype"),
        catalyst=ot.get("catalyst"), what_must_happen=ot.get("what_must_happen"),
        stock_return=_pct(oc.get("stock_return")), idiosyncratic=_pct(oc.get("idiosyncratic")),
        context_json=_json.dumps(ctx, default=str)[:60000],
    )


def from_judge_json(raw):
    import json as _json
    import re as _re
    txt = _re.sub(r"^```(json)?|```$", "", raw.strip(), flags=_re.MULTILINE).strip()
    d = _json.loads(txt)
    verdict = d.get("mechanism_verdict", "unknown")
    if verdict not in ("played_out", "did_not", "partial"):
        verdict = "unknown"
    expl = d.get("explanation", "")
    if d.get("was_outcome_luck"):
        expl = "[FLAGGED LUCK] " + expl
    return verdict, expl


def make_live_judge(llm_provider):
    """Wrap an orchestration-layer LLM provider into a mechanism_judge callable that
    run_retrospective can use. The provider is callable(prompt:str)->json_str."""
    def judge(thesis_dict, outcome_ctx):
        cik = outcome_ctx.get("cik_for_judge")
        ctx = build_judge_context(thesis_dict, cik, outcome_ctx)
        try:
            raw = llm_provider(render_judge_prompt(ctx))
            return from_judge_json(raw)
        except Exception as e:
            return "unknown", f"judge error: {e}"
    return judge
