"""
journal.py - the compounding memory, as a FOLDER-PER-VERTICAL tree you can mirror to
Google Drive. Each sector is a folder that holds the sector's own news/dossier AND the
docs for the companies in it, so the two update independently and a shift recorded at the
sector level flows into every company's reasoning the next time it's analyzed.

  journal/
    verticals/
      Agriculture/
        _sector.md         <- sector dossier + dated news/event log (human-readable)
        _sector.json       <- the same, STRUCTURED (drivers, entities->tickers, events)
        CALM.md            <- one doc per company IN the sector: news log + thesis history
      Industrials/
        _sector.md
        SHOO.md
        PRDO.md
      ...                  (~11 sector folders)

READ MODEL:
  * a company doc is read ONE AT A TIME for the name being analyzed (scoped),
  * its OWN sector dossier is read with it (sector learnings inform company rationale),
  * ALL sector dossiers are read TOGETHER every run (~11 files, cheap) so a shift in one
    sector is visible when analyzing a name elsewhere with exposure to it.

This module is the file I/O layer; sectors.py is the sector-knowledge layer on top of it.
Git-tracked: commit history is the point-in-time audit trail. push_to_gdoc() is the seam
the Cowork/Code routine fills with your Drive credentials.
"""
import json
import os
import datetime as dt

import config

ROOT = os.path.join(config.STORE_DIR, "journal")
SECTOR_MD = "_sector.md"
SECTOR_JSON = "_sector.json"


def _safe(name):
    return (name or "Unknown").replace("/", "-")


def sector_dir(sector):
    d = os.path.join(ROOT, "verticals", _safe(sector))
    os.makedirs(d, exist_ok=True)
    return d


def sector_md_path(sector):
    return os.path.join(sector_dir(sector), SECTOR_MD)


def sector_json_path(sector):
    return os.path.join(sector_dir(sector), SECTOR_JSON)


def _company_path(sector, ticker):
    return os.path.join(sector_dir(sector), f"{ticker}.md")


# ------------------------------------------------------------- low-level IO
def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def write_text(path, content):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def write_json(path, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


# ----------------------------------------------------------------------- reads
def read_all_vertical_notes():
    """ALL sector dossiers concatenated — read together every run (cross-sector view)."""
    base = os.path.join(ROOT, "verticals")
    out = []
    if os.path.isdir(base):
        for sec in sorted(os.listdir(base)):
            p = os.path.join(base, sec, SECTOR_MD)
            if os.path.exists(p):
                out.append(f"### {sec}\n{read_text(p)}")
    return "\n\n".join(out) if out else "(no sector dossiers yet)"


def read_sector_dossier(sector):
    """One sector's dossier text — read alongside the company being analyzed so sector-level
    learnings feed the company's rationale (the propagation you asked for)."""
    p = sector_md_path(sector)
    return read_text(p) or f"(no dossier yet for {sector})"


def read_company_history(sector, ticker, max_chars=8000):
    """One company's doc (its news log + prior thesis entries) — scoped read."""
    p = _company_path(sector, ticker)
    if os.path.exists(p):
        return read_text(p)[-max_chars:]
    return "(no prior entries for this company)"


# ---------------------------------------------------------------------- writes
def append_company_news(sector, ticker, items, name=None):
    """Append dated COMPANY-SPECIFIC news/updates to the company doc — separate from the
    thesis entries, so news accrues even on runs where no new thesis is written. `items` is
    a list of dicts (title/date/source/url) and/or plain strings. De-dups against the file."""
    if not items:
        return None
    p = _company_path(sector, ticker)
    existing = read_text(p)
    lines = []
    for it in items:
        if isinstance(it, dict):
            title = (it.get("title") or it.get("event") or "").strip()
            if not title or title in existing:
                continue
            meta = " · ".join(x for x in (it.get("source_label") or it.get("source"),
                                          it.get("date") or it.get("source_date")) if x)
            url = it.get("url")
            lines.append(f"  - {title}" + (f" ({meta})" if meta else "")
                         + (f" — {url}" if url else ""))
        else:
            s = str(it).strip()
            if s and s not in existing:
                lines.append(f"  - {s}")
    if not lines:
        return p
    header = "" if existing else f"# {ticker} — {name or ''} ({sector})\n"
    block = f"\n### News & updates — {dt.date.today().isoformat()}\n" + "\n".join(lines) + "\n"
    with open(p, "a", encoding="utf-8") as f:
        if header:
            f.write(header)
        f.write(block)
    return p


def append_company_entry(sector, ticker, thesis_dict, snapshot):
    """Append a dated thesis entry to the company's doc, takeaways highlighted first."""
    p = _company_path(sector, ticker)
    date = dt.date.today().isoformat()
    gap = thesis_dict.get("gap_vs_price")
    action = snapshot.get("recommendation", {}).get("action", "")
    takeaway = (f"**{action}** · {thesis_dict.get('thesis_archetype','')} · variant growth "
                f"{_pct(thesis_dict.get('variant_growth'))} vs implied "
                f"{_pct(thesis_dict.get('implied_growth'))} · "
                f"gap {_pct(gap)} · conviction {thesis_dict.get('conviction')}/5 · "
                f"horizon {thesis_dict.get('horizon_months')}m")

    ev_lines = "\n".join(
        f"  - _{e.get('direction')}_ — {e.get('claim','')[:200]} "
        f"[{e.get('source_form','')}, {e.get('source_date','')}]"
        for e in thesis_dict.get("evidence", []))

    brief_line = (f"**What this company is:** {thesis_dict['company_brief']}\n\n"
                  if thesis_dict.get("company_brief") else "")
    charts = thesis_dict.get("charts") or []
    charts_line = ("**Charts (rendered in the dashboard):** "
                   + "; ".join(c.get("title", "") for c in charts if isinstance(c, dict))
                   + "\n\n") if charts else ""
    rels = (snapshot.get("synthesis_relationships") or thesis_dict.get("relationships") or [])
    rel_line = ("**Relationships (second-order graph):** "
                + "; ".join(f"{r.get('entity','')} ({r.get('type','')})"
                            for r in rels if isinstance(r, dict)) + "\n\n") if rels else ""

    entry = f"""
---
## {date} — {ticker}
> **Takeaways:** {takeaway}
> **Thesis type:** {thesis_dict.get('thesis_archetype','')} · **edge:** {thesis_dict.get('edge_source','')}

{brief_line}{charts_line}{rel_line}**What the market believes (and why):** {thesis_dict.get('market_narrative','')}
_Implied view:_ {thesis_dict.get('implied_view_interpretation','')}

**Our differentiated view:** {thesis_dict.get('variant_view','')}

**What the market is mis-weighting (the mechanism):** {thesis_dict.get('mispriced_mechanism','')}

**Why we deviate from the market's number:** {thesis_dict.get('deviation_explanation','')}

**Full rationale:** {thesis_dict.get('rationale','')}

**Cross-source corroboration:** {thesis_dict.get('cross_source_corroboration','')}

**Evidence (with receipts):**
{ev_lines or '  - (none captured)'}

**Disconfirming evidence (bear case against our view):** {thesis_dict.get('disconfirming','')}

**Catalyst:** {thesis_dict.get('catalyst','')} (≈ {thesis_dict.get('catalyst_date','')})
**Falsification:** {thesis_dict.get('falsification','')}
**Evaluation window (pinned):** {thesis_dict.get('evaluation_window','')}

**Snapshot:** price ${snapshot.get('price')}, WACC {_pct(snapshot.get('wacc'),1)}, \
fair value {_money(thesis_dict.get('fair_value'))}, beta \
{round(snapshot.get('beta_adjusted'),2) if snapshot.get('beta_adjusted') else '—'}, \
reliability {'OK' if snapshot.get('reliable') else 'FLAGGED: '+','.join(snapshot.get('reliability_flags',[]))}
"""
    header = "" if os.path.exists(p) else f"# {ticker} — {snapshot.get('name','')} ({sector})\n"
    with open(p, "a", encoding="utf-8") as f:
        if header:
            f.write(header)
        f.write(entry)
    return p


def update_vertical_note(sector, note, takeaway):
    """Append a free-text sector-wide observation to the sector dossier markdown."""
    p = sector_md_path(sector)
    date = dt.date.today().isoformat()
    header = "" if os.path.exists(p) else f"# {sector} — sector dossier\n"
    with open(p, "a", encoding="utf-8") as f:
        if header:
            f.write(header)
        f.write(f"\n---\n## {date}\n> **Takeaway:** {takeaway}\n\n{note}\n")
    return p


def append_retro_note(sector, ticker, note, score_dict):
    """Append a retrospective verdict to the company's doc — closing the loop on a matured
    thesis so its outcome is part of the record next time."""
    p = _company_path(sector, ticker)
    date = dt.date.today().isoformat()
    entry = f"""
---
## {date} — RETROSPECTIVE on {ticker}
> **{note}**

Original mechanism bet: {score_dict.get('mispriced_mechanism','')}
Outcome: stock {_pct(score_dict.get('stock_return'))}, sector basket \
{_pct(score_dict.get('sector_basket_return'))} ({score_dict.get('n_peers')} peers), \
idiosyncratic excess {_pct(score_dict.get('idiosyncratic_excess'))}.
Mechanism played out: {score_dict.get('mechanism_played_out')} — {score_dict.get('mechanism_note','')}
"""
    header = "" if os.path.exists(p) else f"# {ticker} ({sector})\n"
    with open(p, "a", encoding="utf-8") as f:
        if header:
            f.write(header)
        f.write(entry)
    return p


# --------------------------------------------------------------- helpers
def _pct(x, dp=1):
    return "—" if x is None else f"{x*100:.{dp}f}%"


def _money(x):
    if x is None:
        return "—"
    if abs(x) >= 1e6:
        return f"${x/1e6:.1f}M"
    return f"${x:,.0f}"


# --------------------------------------------------------------- gdoc seam
def push_to_gdoc(syncer=None, journal_root=None, dry_run=None):
    """Seam, filled at the orchestration layer with your Drive credentials. Walks the
    journal/ tree and, per markdown doc, calls the injected `syncer(relpath, content)` (your
    Drive/Docs connector) or — with no syncer — returns a DRY-RUN manifest. Never raises on
    the default path. Each verticals/<Sector>/ folder maps to a Drive subfolder; see CONNECTING.md."""
    root = journal_root or ROOT
    dry = (syncer is None) if dry_run is None else dry_run
    manifest = []
    if not os.path.isdir(root):
        return manifest
    for dirpath, _dirs, files in os.walk(root):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            relpath = os.path.relpath(full, root)
            manifest.append(relpath)
            if not dry and callable(syncer):
                syncer(relpath, read_text(full))
    return manifest
