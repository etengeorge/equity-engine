"""
monitor.py - position monitoring via thesis drift, not price noise.

You're connecting Robinhood and want daily re-analysis to tell you when to add or
trim. The right way to do that — and the way that does NOT make you churn — is to
re-run the synthesis on names you hold a thesis on, compare the FRESH thesis to the
STORED one, and alert ONLY when new information has materially changed or invalidated
the thesis.

THE DISCIPLINE (this is the whole point):
  - New FACTS that break or change the thesis  -> ALERT (guidance cut, mechanism broke,
    falsification tripped, conviction collapse, archetype flip).
  - Price merely moving the valuation gap around -> NO ALERT. On a long-horizon thesis,
    interim price action is noise; reacting to it is overtrading, which costs you taxes,
    spread, and — worst — makes you abandon theses right before they work.

So drift is measured in the THESIS, not the price. A 2-year thesis that's flat at month
3 generates nothing. The same thesis where the new 10-Q shows the mechanism breaking
generates a loud alert.
"""
import datetime as dt

import config


# what counts as a MATERIAL change (fact-driven), vs. ignorable (price-driven)
def detect_drift(stored_thesis, fresh_thesis, held=True):
    """Compare a freshly-generated thesis to the last stored one. Return an alert dict
    if the change is MATERIAL, else None. Conservative by design."""
    if not stored_thesis or not fresh_thesis:
        return None

    alerts = []
    risk_sev = 0          # positive: review/trim/exit pressure
    opp_sev = 0           # positive magnitude of an ADD/strengthen signal

    s_arch = stored_thesis.get("thesis_archetype")
    f_arch = fresh_thesis.get("thesis_archetype")
    s_dir = stored_thesis.get("direction")
    f_dir = fresh_thesis.get("direction")
    s_conv = stored_thesis.get("conviction") or 0
    f_conv = fresh_thesis.get("conviction") or 0

    actionable = {"long", "avoid"}
    if s_dir in actionable and f_dir in actionable and s_dir != f_dir:
        alerts.append(f"DIRECTION REVERSED: {s_dir} → {f_dir}")
        risk_sev = max(risk_sev, 3)

    if s_arch and s_arch != "none_efficiently_priced" and f_arch == "none_efficiently_priced":
        alerts.append("EDGE GONE: thesis no longer differentiated; market caught up")
        risk_sev = max(risk_sev, 2)

    if abs(f_conv - s_conv) >= 2:
        if f_conv < s_conv:
            alerts.append(f"CONVICTION COLLAPSED: {s_conv}/5 → {f_conv}/5")
            risk_sev = max(risk_sev, 2)
        else:
            alerts.append(f"CONVICTION STRENGTHENED: {s_conv}/5 → {f_conv}/5")
            opp_sev = max(opp_sev, 1)

    if s_arch and f_arch and s_arch != f_arch and f_arch != "none_efficiently_priced":
        alerts.append(f"THESIS BASIS CHANGED: {s_arch} → {f_arch}")
        risk_sev = max(risk_sev, 1)

    if not alerts:
        return None

    # risk dominates opportunity (be conservative with real money). A pure strengthen
    # (no risk flag) yields a negative severity = ADD signal.
    severity = risk_sev if risk_sev > 0 else (-opp_sev if opp_sev > 0 else 0)
    action = _severity_to_action(severity, f_dir, held)
    return {
        "ticker": fresh_thesis.get("ticker") or stored_thesis.get("ticker"),
        "severity": severity,
        "changes": alerts,
        "stored": {"archetype": s_arch, "direction": s_dir, "conviction": s_conv},
        "fresh": {"archetype": f_arch, "direction": f_dir, "conviction": f_conv},
        "fresh_mechanism": fresh_thesis.get("mispriced_mechanism"),
        "fresh_view": fresh_thesis.get("variant_view"),
        "recommended_action": action,
        "note": ("Thesis-change alert (fact-driven). This is NOT a reaction to price "
                 "movement — it fires only when new information changed the thesis."),
    }


def _severity_to_action(severity, fresh_direction, held):
    # negative severity = thesis materially STRENGTHENED -> add (subject to your cap)
    if severity < 0:
        if held and fresh_direction == "long":
            return ("CONSIDER ADDING: the long thesis strengthened materially on new "
                    "information. Size up toward target — but respect your single-name "
                    "concentration cap (the portfolio view flags if you're already at it).")
        return "STRENGTHENED: thesis improved; a new long looks more attractive."
    if severity >= 3:                         # direction reversed
        if held:
            return ("REVIEW FOR EXIT: the thesis that justified holding has reversed on "
                    "new information. Re-underwrite or trim/exit.")
        return "AVOID: thesis reversed; do not initiate."
    if severity == 2:                          # edge gone or conviction collapse
        if held:
            return ("REVIEW: the basis for the position has weakened materially. Consider "
                    "trimming; the original edge may no longer be there.")
        return "PASS: the differentiated edge has weakened."
    if severity == 1:                          # basis changed
        if held and fresh_direction == "long":
            return ("MONITOR: thesis basis evolved but still constructive. No action "
                    "required; note the new reasoning.")
        return "MONITOR: note the changed reasoning; no action required."
    return "no action"


def check_falsification_signals(fresh_thesis, news_summary):
    """Secondary, lighter check: does fresh news/filing activity touch the thesis's
    falsification condition? Surfaces a watch flag (not a trade signal) so you can
    verify. Still fact-driven, not price-driven."""
    fals = (fresh_thesis or {}).get("falsification", "")
    if not fals or not news_summary:
        return None
    # heuristic: if any fresh story's stance conflicts with the thesis direction, flag
    # it for human verification against the falsification condition.
    conflicts = [s for s in (news_summary.get("top") or [])
                 if s.get("stance_conflict")]
    if conflicts:
        return {"watch": "Fresh conflicting news may bear on the falsification condition; "
                f"verify: '{fals[:160]}'", "stories": conflicts[:3]}
    return None


def summarize_alerts(drift_alerts):
    """Human summary for the brief: only the names where the thesis materially changed."""
    if not drift_alerts:
        return ("No thesis changes today. Held positions' theses remain intact — interim "
                "price movement is expected and is not a reason to trade.")
    lines = [f"{len(drift_alerts)} position(s) had a MATERIAL thesis change today "
             "(fact-driven, not price noise):"]
    for a in sorted(drift_alerts, key=lambda x: x["severity"], reverse=True):
        lines.append(f"  • {a['ticker']} [sev {a['severity']}]: {'; '.join(a['changes'])} "
                     f"→ {a['recommended_action']}")
    return "\n".join(lines)
