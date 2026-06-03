"""
thesis.py - the structured rationale behind every recommendation.

A recommendation without its reasoning is an unauditable black box. The thesis
object carries the whole chain so you can pressure-test it:

  implied view (market)  ->  variant view (ours)  ->  evidence (with receipts)
  ->  catalyst + horizon  ->  falsification  ->  conviction

The evaluation_window is pinned at creation from catalyst_date + horizon. The
retrospective scores against THAT window, so "wrong" and "early" don't get
confused.
"""
import dataclasses as dc
import datetime as dt
from typing import Optional


@dc.dataclass
class Evidence:
    claim: str                 # what this supports
    source_form: str           # "8-K", "10-K Item 1A", "earnings call", ...
    source_url: Optional[str]  # provenance: the actual document
    source_date: Optional[str]
    direction: str             # "supports_higher", "supports_lower", "risk"


@dc.dataclass
class Thesis:
    ticker: str
    created: str
    direction: str                     # long | short | avoid | hold
    # the steelman: why the market prices it as it does
    market_narrative: str
    implied_view_interpretation: str
    consensus_interrogation: str
    perspective_spread: str
    # the two views, as growth assumptions for the reverse DCF
    implied_growth: Optional[float]    # what the market prices
    variant_growth: Optional[float]    # what our research supports (= base case)
    # the differentiated view
    thesis_archetype: str
    variant_view: str
    mispriced_mechanism: str
    rationale: str                     # the reasoning narrative
    deviation_explanation: str         # WHY ours differs from the market's
    # scenarios
    bull_case: dict
    base_case: dict
    bear_case: dict
    # catalyst pathway
    catalyst: str
    catalyst_date: Optional[str]
    catalyst_path: str
    what_must_happen: list
    # rigor
    evidence: list                     # list[Evidence]
    cross_source_corroboration: str
    disconfirming: str                 # counter-evidence actively sought
    falsification: str                 # what would prove this wrong
    conviction: int                    # 1-5
    horizon_months: int
    edge_source: str
    evaluation_window: Optional[str]   # pinned: when the retrospective scores it
    fair_value: Optional[float] = None
    gap_vs_price: Optional[float] = None
    sign_survives_fcff_band: Optional[bool] = None
    company_brief: str = ""            # plain-English business description (what/segments/customers)
    charts: list = dc.field(default_factory=list)  # chart specs rendered inline in the dashboard

    @staticmethod
    def evaluation_window_from(created, catalyst_date, horizon_months):
        # window ends at the later of (catalyst date) and (created + horizon),
        # so a near catalyst still gets a fair minimum runway.
        base = dt.date.fromisoformat(created)
        by_horizon = base + dt.timedelta(days=int(horizon_months * 30.4))
        end = by_horizon
        if catalyst_date:
            try:
                cd = dt.date.fromisoformat(catalyst_date)
                end = max(by_horizon, cd)
            except ValueError:
                pass
        return end.isoformat()

    def to_dict(self):
        d = dc.asdict(self)
        return d


def build_thesis(ticker, synth, implied_growth, our_view):
    """Assemble a Thesis from a SynthesisResult + the reverse-DCF our_view."""
    created = dt.date.today().isoformat()
    # Build Evidence defensively: a live LLM may omit a field, add an extra one, or
    # return a bare string. Tolerate all of it rather than crash the whole run.
    ev = []
    for e in synth.evidence:
        if isinstance(e, Evidence):
            ev.append(e)
        elif isinstance(e, dict):
            ev.append(Evidence(claim=str(e.get("claim", "")),
                               source_form=str(e.get("source_form", "")),
                               source_url=e.get("source_url"),
                               source_date=e.get("source_date"),
                               direction=str(e.get("direction", ""))))
        else:
            ev.append(Evidence(claim=str(e), source_form="", source_url=None,
                               source_date=None, direction=""))
    window = Thesis.evaluation_window_from(created, synth.catalyst_date,
                                           synth.horizon_months)
    direction = "long"
    g = our_view.get("gap_vs_price") if our_view else None
    if g is not None:
        direction = "long" if g > 0 else "avoid"
    if synth.thesis_archetype == "none_efficiently_priced":
        direction = "hold"
    return Thesis(
        ticker=ticker, created=created, direction=direction,
        market_narrative=synth.market_narrative,
        implied_view_interpretation=synth.implied_view_interpretation,
        consensus_interrogation=synth.consensus_interrogation,
        perspective_spread=synth.perspective_spread,
        implied_growth=implied_growth, variant_growth=synth.adjusted_growth,
        thesis_archetype=synth.thesis_archetype, variant_view=synth.variant_view,
        mispriced_mechanism=synth.mispriced_mechanism,
        rationale=synth.rationale, deviation_explanation=synth.deviation_explanation,
        bull_case=synth.bull_case, base_case=synth.base_case, bear_case=synth.bear_case,
        catalyst=synth.catalyst, catalyst_date=synth.catalyst_date,
        catalyst_path=synth.catalyst_path, what_must_happen=synth.what_must_happen,
        evidence=[dc.asdict(e) for e in ev],
        cross_source_corroboration=synth.cross_source_corroboration,
        disconfirming=synth.disconfirming,
        falsification=synth.falsification, conviction=synth.conviction,
        horizon_months=synth.horizon_months, edge_source=synth.edge_source,
        evaluation_window=window,
        fair_value=(our_view or {}).get("fair_value"),
        gap_vs_price=(our_view or {}).get("gap_vs_price"),
        sign_survives_fcff_band=(our_view or {}).get("sign_survives_fcff_band"),
        company_brief=getattr(synth, "company_brief", ""),
        charts=getattr(synth, "charts", []) or [],
    )
