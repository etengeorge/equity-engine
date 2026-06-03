"""
sectors.py - the sector-knowledge layer on top of the journal folders.

Each vertical folder carries a structured dossier (`_sector.json`, rendered to `_sector.md`):

  drivers   - the variables that actually move the sector (egg price, HPAI, feed cost; Title IV,
              Gainful Employment, enrollment cyclicality; China-sourcing %, tariff regime ...)
  entities  - regulators / customers / suppliers / input commodities / competitors / partners,
              each mapped to the universe tickers it touches  (the second-order RELATIONSHIP graph)
  narrative - the current sector state, in a line
  events    - a dated log of sector-wide developments/news, each tagged to drivers + affected tickers

WHY: this is the substrate for second-order reasoning. A development recorded at the sector level
(a regulator acts, a commodity moves, a competitor signs a deal) is read into EVERY company in that
sector the next time it's analyzed — so "something changed in the vertical folder" automatically
informs each company's rationale. Relationships let an event on entity X fan out to the names X touches.

The synthesis both CONSUMES the dossier (for the structural_second_order lens) and FEEDS it
(emitting sector_update + relationships), so it compounds. All free, all folder-native.
"""
import datetime as dt
import os

import journal

EVENT_CAP = 60


def _today():
    return dt.date.today().isoformat()


def _skeleton(sector):
    return {"sector": sector, "drivers": [], "entities": {}, "narrative": "",
            "events": [], "members": [], "cross_sector_members": [], "updated": _today()}


def load(sector):
    return journal.read_json(journal.sector_json_path(sector)) or _skeleton(sector)


def save(sector, d):
    d["sector"] = sector
    d["updated"] = _today()
    journal.write_json(journal.sector_json_path(sector), d)
    journal.write_text(journal.sector_md_path(sector), render_md(d))   # human-readable mirror
    return d


def all_sectors():
    base = os.path.join(journal.ROOT, "verticals")
    return sorted(os.listdir(base)) if os.path.isdir(base) else []


# ------------------------------------------------------------- writers (feed)
def add_member(sector, ticker):
    d = load(sector)
    tk = (ticker or "").upper()
    if tk and tk not in d["members"]:
        d["members"].append(tk)
        save(sector, d)


def record_relationships(home_sector, ticker, relationships):
    """Fold a company's emitted relationships into the entity graph. A relationship may name a
    DIFFERENT industry it belongs to (r['sector']) — e.g. a TECH company whose key risk is a
    HEALTHCARE regulator (FDA/CMS) — in which case the edge is recorded in THAT industry's
    dossier too, so the cross-industry exposure reaches that industry's companies (cross-sector
    spillover). The ticker is tracked as a 'cross_sector_member' of any non-home industry."""
    if not relationships:
        return
    tk0 = (ticker or "").upper()
    by_sector = {}
    for r in relationships:
        if isinstance(r, dict) and (r.get("entity") or "").strip():
            by_sector.setdefault(r.get("sector") or home_sector, []).append(r)
    for tgt, rels in by_sector.items():
        d = load(tgt)
        if tk0:
            key = "members" if tgt == home_sector else "cross_sector_members"
            d.setdefault(key, [])
            if tk0 not in d[key]:
                d[key].append(tk0)
        for r in rels:
            ent = r["entity"].strip()
            e = d["entities"].setdefault(ent, {"type": "", "tickers": [], "note": ""})
            if r.get("type") and not e["type"]:
                e["type"] = r["type"]
            if r.get("note") and not e["note"]:
                e["note"] = r["note"][:200]
            for tk in [tk0] + [str(x).upper() for x in (r.get("tickers") or [])]:
                if tk and tk not in e["tickers"]:
                    e["tickers"].append(tk)
        save(tgt, d)


def record_event(sector, event, source="", date=None, drivers=None, entities=None,
                 affected_tickers=None):
    """Append a dated sector-wide development to the event log (newest first, capped), merging
    any new drivers/entities. Read into every company in the sector on its next analysis."""
    event = (event or "").strip()
    if not event:
        return
    d = load(sector)
    aff = [str(t).upper() for t in (affected_tickers or [])]
    ev = {"date": date or _today(), "event": event[:400], "source": source or "",
          "drivers": list(drivers or []), "affected_tickers": aff}
    # de-dup identical event text already at the top of the log
    if not any(x.get("event") == ev["event"] for x in d["events"][:8]):
        d["events"].insert(0, ev)
        d["events"] = d["events"][:EVENT_CAP]
    for dr in (drivers or []):
        if dr and dr not in d["drivers"]:
            d["drivers"].append(dr)
    for ent in (entities or []):
        if isinstance(ent, str) and ent and ent not in d["entities"]:
            d["entities"][ent] = {"type": "", "tickers": aff, "note": ""}
    save(sector, d)


def set_narrative(sector, narrative):
    if not narrative:
        return
    d = load(sector)
    d["narrative"] = narrative.strip()[:600]
    save(sector, d)


def record_sector_update(home_sector, update, ticker=""):
    """Apply a synthesis-emitted sector_update: a sector-wide LEARNING + the drivers/entities/
    tickers it touches. Recorded as an event (and the home sector's narrative). CROSS-INDUSTRY:
    if the learning also applies to OTHER industries (update['sectors']) — e.g. a healthcare
    regulatory shift surfaced while analyzing a tech name — it is recorded in those industries'
    dossiers too, so their companies inherit it."""
    if not isinstance(update, dict):
        return
    learning = (update.get("learning") or "").strip()
    if not learning:
        return
    src = f"synthesis:{ticker}" if ticker else "synthesis"
    targets = list(dict.fromkeys([home_sector] + [s for s in (update.get("sectors") or []) if s]))
    for tgt in targets:
        record_event(tgt, learning, source=src, drivers=update.get("drivers"),
                     entities=update.get("entities"), affected_tickers=update.get("affected_tickers"))
    set_narrative(home_sector, learning)


# ------------------------------------------------------------- readers (propagate)
def affected_tickers(entities, sectors=None):
    """Reverse lookup for news->company propagation: given event entities (regulator/commodity/
    company names), return {ticker: (sector, entity)} for every universe name those entities touch."""
    hits = {}
    ents = [e.lower() for e in (entities or []) if e]
    if not ents:
        return hits
    for sec in (sectors or all_sectors()):
        d = load(sec)
        for name, info in (d.get("entities") or {}).items():
            nl = name.lower()
            if any(e == nl or e in nl or nl in e for e in ents):
                for tk in info.get("tickers", []):
                    hits.setdefault(tk, (sec, name))
    return hits


def recent_event_tickers(days=3, since_date=None, sectors=None):
    """For wiring the sector arm INTO the daily scan: the universe tickers touched by a sector
    event recorded within the window — i.e. the names to RE-EXAMINE because something changed in
    their (or a linked) vertical. This is what turns 'a development logged in the vertical folder'
    into 'the affected companies get re-underwritten next run'. Returns {ticker: (sector, event, date)}."""
    cutoff = since_date or (dt.date.today() - dt.timedelta(days=int(days))).isoformat()
    hits = {}
    for sec in (sectors or all_sectors()):
        d = load(sec)
        for ev in d.get("events", []):
            if str(ev.get("date", "")) >= cutoff:
                for tk in ev.get("affected_tickers", []):
                    hits.setdefault(str(tk).upper(), (sec, ev.get("event", ""), ev.get("date", "")))
    return hits


# ------------------------------------------------------------- render
def render_md(d):
    L = [f"# {d.get('sector','')} — sector dossier", f"_updated {d.get('updated','')}_", ""]
    if d.get("narrative"):
        L += [f"**Current sector narrative:** {d['narrative']}", ""]
    if d.get("drivers"):
        L += [f"**Drivers:** {', '.join(d['drivers'])}", ""]
    if d.get("entities"):
        L.append("**Key entities & exposure (entity → universe names it touches):**")
        for name, info in sorted(d["entities"].items()):
            tks = ", ".join(info.get("tickers", [])) or "—"
            note = f" — {info['note']}" if info.get("note") else ""
            L.append(f"  - {name} ({info.get('type','')}) → {tks}{note}")
        L.append("")
    if d.get("members"):
        L += [f"**Members analyzed:** {', '.join(sorted(d['members']))}", ""]
    if d.get("cross_sector_members"):
        L += ["**Cross-sector exposure (names from OTHER industries that touch this sector):** "
              + ", ".join(sorted(d["cross_sector_members"])), ""]
    if d.get("events"):
        L.append("**Recent sector events / news (newest first):**")
        for ev in d["events"][:25]:
            aff = (" [affects: " + ", ".join(ev["affected_tickers"]) + "]") if ev.get("affected_tickers") else ""
            src = f" ({ev['source']})" if ev.get("source") else ""
            L.append(f"  - {ev.get('date','')}: {ev.get('event','')}{aff}{src}")
        L.append("")
    return "\n".join(L) + "\n"
