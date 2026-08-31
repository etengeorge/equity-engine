"""Build the static site Vercel serves.

Two tabs, both generated from files already in the repo and nothing else:

  public/index.html                              the screen
  public/research/index.html                     the research index, sector first
  public/research/<sector>/<TICKER>.html         one page per company
  public/research/lessons.html                   the standing priors

The research pages mirror `research/<Sector>/<TICKER>.md` exactly — same folder shape,
same append-only log, newest entry at the bottom. The site is a view of that tree, not a
second copy of it, so anything committed to research/ shows up here on the next build.
No dependencies: the markdown renderer below is deliberately small and only covers the
constructs those files actually contain.
"""
import json, html, re, datetime as dt
import config

CSS = """
:root{
  --bg:#fbfbfa; --panel:#fff; --panel-2:#f7f6f4; --ink:#1a1a19; --dim:#6b6b66;
  --faint:#93938c; --line:#e7e6e2; --line-2:#d8d7d2;
  --pos:#0d7a4d; --pos-bg:#e6f4ec; --neg:#b3261e; --neg-bg:#fbeae9;
  --warn:#8a6100; --warn-bg:#fbf1de; --accent:#2f5fd0; --accent-bg:#eaf0fd;
  --chip:#f1f0ed;
}
@media(prefers-color-scheme:dark){:root{
  --bg:#131312; --panel:#1b1b19; --panel-2:#212120; --ink:#eeeeec; --dim:#a0a099;
  --faint:#77776f; --line:#2c2c29; --line-2:#3a3a36;
  --pos:#54c891; --pos-bg:#12301f; --neg:#f2867c; --neg-bg:#331817;
  --warn:#dcaa4b; --warn-bg:#2f2612; --accent:#84a9f9; --accent-bg:#161f33;
  --chip:#252523;
}}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.6 ui-sans-serif,-apple-system,"Segoe UI",Inter,system-ui,sans-serif;
-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}

/* --- nav ------------------------------------------------------------------ */
.topbar{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);
backdrop-filter:saturate(180%) blur(12px);border-bottom:1px solid var(--line)}
.topbar .inner{max-width:1200px;margin:0 auto;padding:0 20px;display:flex;align-items:center;
gap:22px;height:52px}
.brand{font-weight:680;letter-spacing:-.02em;font-size:15px;white-space:nowrap}
.brand span{color:var(--faint);font-weight:400}
.tabs{display:flex;gap:2px;margin-left:auto}
.tabs a{padding:6px 13px;border-radius:7px;font-size:13.5px;color:var(--dim);font-weight:500}
.tabs a:hover{background:var(--chip);text-decoration:none;color:var(--ink)}
.tabs a.on{background:var(--ink);color:var(--bg)}

.wrap{max-width:1200px;margin:0 auto;padding:26px 20px 90px}
h1{font-size:26px;margin:0 0 5px;letter-spacing:-.025em;font-weight:660}
h2{font-size:15px;margin:42px 0 4px;letter-spacing:.01em;font-weight:640;
text-transform:uppercase;color:var(--dim)}
h2 .n{color:var(--faint);font-weight:400;text-transform:none;letter-spacing:0}
.sub{color:var(--dim);font-size:13px;margin:0 0 12px;max-width:76ch}
.crumb{font-size:12.5px;color:var(--faint);margin:0 0 10px}
.crumb a{color:var(--dim)}

.banner{background:var(--accent-bg);border:1px solid color-mix(in srgb,var(--accent) 25%,transparent);
padding:11px 14px;border-radius:9px;margin:16px 0 6px;font-size:13.5px}

/* --- hero stats ----------------------------------------------------------- */
.hero{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:20px 0 8px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.stat .k{color:var(--dim);font-size:11px;text-transform:uppercase;letter-spacing:.07em;font-weight:600}
.stat .v{font-size:38px;font-weight:660;letter-spacing:-.03em;margin:4px 0 0;
font-variant-numeric:tabular-nums;line-height:1.1}
.stat .s{color:var(--faint);font-size:12.5px;margin-top:4px}

/* --- badges --------------------------------------------------------------- */
.badge{display:inline-block;border-radius:20px;padding:2px 10px;font-size:11.5px;
font-weight:600;letter-spacing:.02em;white-space:nowrap}
.b-cheap{background:var(--pos-bg);color:var(--pos)}
.b-rich{background:var(--neg-bg);color:var(--neg)}
.b-fair,.b-no_edge,.b-no_model{background:var(--chip);color:var(--dim)}
.conv{display:inline-block;font-size:11px;color:var(--dim);border:1px solid var(--line-2);
border-radius:20px;padding:1px 8px;white-space:nowrap}
.chip{display:inline-block;background:var(--chip);border:1px solid var(--line);
border-radius:20px;padding:1px 9px;font-size:11.5px;color:var(--dim);margin:0 3px 3px 0}
.chip.warn{color:var(--warn);background:var(--warn-bg);border-color:transparent}

/* --- opportunity cards ---------------------------------------------------- */
.calls{display:grid;gap:10px;margin-top:12px}
.call{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}
.call>summary{cursor:pointer;list-style:none;padding:14px 16px;display:flex;
align-items:center;gap:12px;flex-wrap:wrap}
.call>summary::-webkit-details-marker{display:none}
.call>summary:hover{background:var(--panel-2)}
.call .tk{font-weight:680;font-size:15.5px;letter-spacing:-.01em}
.call .nm{color:var(--dim);font-size:13px;flex:1 1 180px;min-width:0;
overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.call .gap{font-size:19px;font-weight:660;font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.call .caret{color:var(--faint);font-size:12px;transition:transform .15s}
.call[open] .caret{transform:rotate(90deg)}
.call .body{padding:2px 16px 16px;border-top:1px solid var(--line);margin-top:0}
.call .body h4{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--faint);
margin:14px 0 3px;font-weight:600}
.call .body p{margin:0;font-size:13.5px;color:var(--ink)}
.call .nums{display:flex;gap:18px;flex-wrap:wrap;font-size:12.5px;color:var(--dim);
margin-top:12px;font-variant-numeric:tabular-nums}
.call .nums b{color:var(--ink);font-weight:600;margin-left:6px}
.call .nums>div{white-space:nowrap}
.empty{background:var(--panel);border:1px dashed var(--line-2);border-radius:12px;
padding:22px;color:var(--dim);font-size:13.5px;text-align:center}

/* --- tables --------------------------------------------------------------- */
.scroll{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--panel);
margin-top:12px}
table{border-collapse:collapse;width:100%;font-size:13.5px}
th,td{padding:9px 12px;text-align:left;border-bottom:1px solid var(--line);white-space:nowrap}
th{background:var(--panel-2);font-weight:600;font-size:11px;color:var(--dim);
text-transform:uppercase;letter-spacing:.06em;position:sticky;top:0;cursor:pointer;user-select:none}
th:hover{color:var(--ink)}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover{background:var(--panel-2)}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.pos{color:var(--pos)}.neg{color:var(--neg)}.dim{color:var(--dim)}
.tick{font-weight:650}
.why{color:var(--dim);font-size:12.5px;white-space:normal;max-width:420px}

/* --- research index ------------------------------------------------------- */
.sector{margin-top:26px}
.sector h3{font-size:14.5px;margin:0 0 2px;font-weight:640;letter-spacing:-.01em}
.sector .path{font-size:12px;color:var(--faint);margin:0 0 9px;font-family:ui-monospace,
SFMono-Regular,Menlo,monospace}
.co{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:8px}
.co a{display:block;background:var(--panel);border:1px solid var(--line);border-radius:10px;
padding:11px 13px;color:inherit}
.co a:hover{border-color:var(--line-2);background:var(--panel-2);text-decoration:none}
.co .r1{display:flex;align-items:center;gap:8px}
.co .t{font-weight:660;font-size:14px}
.co .n2{color:var(--faint);font-size:11.5px;margin-top:3px;overflow:hidden;
text-overflow:ellipsis;white-space:nowrap}

/* --- rendered research log ------------------------------------------------ */
.prose{background:var(--panel);border:1px solid var(--line);border-radius:12px;
padding:8px 30px 30px;margin-top:14px;max-width:none}
.prose h1{font-size:17px;margin:18px 0 2px;font-weight:640;color:var(--dim)}
.prose h2{font-size:18px;margin:36px 0 10px;padding-top:20px;border-top:1px solid var(--line);
text-transform:none;letter-spacing:-.02em;color:var(--ink);font-weight:660}
.prose h2:first-of-type{border-top:none;padding-top:0}
.prose h3{font-size:14px;margin:20px 0 4px}
.prose p{margin:9px 0;max-width:82ch}
.prose ul{margin:8px 0;padding-left:20px;max-width:82ch}
.prose li{margin:4px 0}
.prose blockquote{margin:12px 0;padding:9px 14px;border-left:3px solid var(--line-2);
background:var(--panel-2);border-radius:0 8px 8px 0;color:var(--dim);max-width:82ch}
.prose blockquote p{margin:4px 0}
.prose hr{border:none;border-top:1px solid var(--line);margin:22px 0}
.prose code{background:var(--chip);padding:1.5px 5px;border-radius:4px;font-size:12.5px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
.prose a{word-break:break-word}
.factstrip{display:flex;gap:20px;flex-wrap:wrap;background:var(--panel);border:1px solid var(--line);
border-radius:12px;padding:13px 16px;margin-top:12px;font-size:12.5px;color:var(--dim);
font-variant-numeric:tabular-nums}
.factstrip b{display:block;color:var(--ink);font-size:15px;font-weight:640;margin-top:2px}

details.note{background:var(--panel);border:1px solid var(--line);border-radius:10px;
padding:0;margin-top:8px}
details.note>summary{cursor:pointer;padding:11px 14px;font-size:13.5px;font-weight:550;
list-style:none}
details.note>summary::-webkit-details-marker{display:none}
details.note>summary:hover{background:var(--panel-2)}
details.note .inner{padding:0 14px 13px;font-size:13px;color:var(--dim);max-width:82ch}
details.note[open]>summary{border-bottom:1px solid var(--line)}
details.note .inner{padding-top:11px}

footer{margin-top:52px;padding-top:20px;border-top:1px solid var(--line);
color:var(--faint);font-size:12.5px}
code{background:var(--chip);padding:1.5px 5px;border-radius:4px;font-size:12px;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
@media(max-width:640px){
  .wrap{padding:18px 14px 70px}
  .stat .v{font-size:30px}
  .prose{padding:6px 16px 20px}
  /* the brand suffix is the first thing to go: losing it keeps both tabs on screen,
     which matters more than the subtitle at this width */
  .topbar .inner{gap:8px;padding:0 14px}
  .brand{font-size:14px}
  .brand span{display:none}
  .tabs a{padding:6px 11px;font-size:13px}
  h1{font-size:23px}
  .call>summary{padding:12px 13px;gap:8px}
  .call .nm{flex-basis:100%;order:5}
}
"""

JS = """
document.querySelectorAll('table').forEach(function(t){
  t.querySelectorAll('th').forEach(function(th,i){
    th.addEventListener('click',function(){
      var tb=t.tBodies[0],rows=[].slice.call(tb.rows),asc=th.dataset.asc!=='1';
      t.querySelectorAll('th').forEach(function(x){x.dataset.asc=''});
      th.dataset.asc=asc?'1':'0';
      rows.sort(function(a,b){
        var x=a.cells[i].dataset.v,y=b.cells[i].dataset.v;
        var nx=parseFloat(x),ny=parseFloat(y);
        if(!isNaN(nx)&&!isNaN(ny))return asc?nx-ny:ny-nx;
        x=(x||a.cells[i].textContent).trim();y=(y||b.cells[i].textContent).trim();
        return asc?x.localeCompare(y):y.localeCompare(x);
      });
      rows.forEach(function(r){tb.appendChild(r)});
    });
  });
});
"""

GITHUB = "https://github.com/etengeorge/equity-engine/blob/main"


# --- cell formatters ---------------------------------------------------------
def _pct(x, cls=True):
    if x is None:
        return '<td class="num dim" data-v="">—</td>'
    c = "pos" if x > 0 else ("neg" if x < 0 else "dim")
    return f'<td class="num {c if cls else ""}" data-v="{x}">{x*100:+.1f}%</td>'


def _pct_of_high(price, high):
    """Current price as a percentage of the highest close in the trailing 252 sessions.

    Deliberately uncoloured: unlike a return, "far below the high" is not good or bad on
    its own — it is the reason a name is worth looking at, which is the opposite of a
    conclusion. Renders "—" when the screen predates the high_252d field.
    """
    if price is None or high is None or high <= 0:
        return '<td class="num dim" data-v="">—</td>'
    v = price / high
    return f'<td class="num" data-v="{v}">{v*100:.0f}%</td>'


def _usd(x, nd=2):
    if x is None:
        return '<td class="num dim" data-v="">—</td>'
    return f'<td class="num" data-v="{x}">${x:,.{nd}f}</td>'


def _cap(x):
    if x is None:
        return '<td class="num dim" data-v="">—</td>'
    for u, d in (("B", 1e9), ("M", 1e6)):
        if abs(x) >= d:
            return f'<td class="num" data-v="{x}">${x/d:,.1f}{u}</td>'
    return f'<td class="num" data-v="{x}">${x:,.0f}</td>'


def _e(s):
    return html.escape(str(s if s is not None else ""))


def _table(rows, cols):
    h = "".join(f"<th>{c}</th>" for c in cols)
    return (f'<div class="scroll"><table><thead><tr>{h}</tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


# --- research tree -----------------------------------------------------------
def sector_slug(sector):
    """Folder name on disk -> URL segment. Stable, lowercase, no spaces."""
    s = re.sub(r"[^a-z0-9]+", "-", str(sector).lower()).strip("-")
    return s or "other"


def research_tree(root=None):
    """Walk research/ and return {sector_dir_name: [ticker, ...]}, sorted.

    The filesystem is the source of truth, not data/verdicts — imported names carry a
    written log with no verdict json, and they must still appear.
    """
    root = root or config.RESEARCH
    tree = {}
    if not root.exists():
        return tree
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        tickers = sorted(f.stem for f in d.glob("*.md"))
        if tickers:
            tree[d.name] = tickers
    return tree


# --- markdown ----------------------------------------------------------------
_URL = re.compile(r"https?://[^\s<>()\[\]]+")
_MDLINK = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
_CODE = re.compile(r"`([^`\n]+)`")
_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
_ITAL_STAR = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
# Underscore italics ONLY at word boundaries with no inner underscore. Research text is
# full of snake_case (no_edge, stock_comp_is_67%_of_fcff) and a naive rule mangles it.
_ITAL_US = re.compile(r"(?<![\w`])_([^_`\n]{1,90})_(?![\w])")


def _inline(text):
    """Escape first, then format. Links and code are parked as tokens so the emphasis
    passes cannot chew through a URL containing an underscore or asterisk."""
    out = _e(text)
    parked = []

    def park(html_fragment):
        parked.append(html_fragment)
        return f"\x00{len(parked)-1}\x00"

    out = _CODE.sub(lambda m: park(f"<code>{m.group(1)}</code>"), out)
    out = _MDLINK.sub(
        lambda m: park(f'<a href="{m.group(2)}" rel="noopener">{m.group(1)}</a>'), out)
    out = _URL.sub(
        lambda m: park(f'<a href="{m.group(0)}" rel="noopener">{m.group(0)}</a>'), out)
    out = _BOLD.sub(r"<strong>\1</strong>", out)
    out = _ITAL_STAR.sub(r"<em>\1</em>", out)
    out = _ITAL_US.sub(r"<em>\1</em>", out)
    for i, frag in enumerate(parked):
        out = out.replace(f"\x00{i}\x00", frag)
    return out


def md_to_html(text):
    """A deliberately small renderer for the constructs research logs actually use:
    ATX headings, bullet lists, blockquotes, horizontal rules, paragraphs, and inline
    bold/italic/code/links. Anything else degrades to a paragraph rather than breaking."""
    lines = (text or "").replace("\r\n", "\n").split("\n")
    out, para, bullets, quote = [], [], [], []

    def flush_para():
        if para:
            out.append(f"<p>{_inline(' '.join(para))}</p>")
            para.clear()

    def flush_bullets():
        if bullets:
            out.append("<ul>" + "".join(f"<li>{_inline(b)}</li>" for b in bullets) + "</ul>")
            bullets.clear()

    def flush_quote():
        if quote:
            inner = "".join(f"<p>{_inline(q)}</p>" for q in quote if q.strip())
            out.append(f"<blockquote>{inner}</blockquote>")
            quote.clear()

    def flush_all():
        flush_para(); flush_bullets(); flush_quote()

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_all()
            continue
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", stripped):
            flush_all()
            out.append("<hr>")
            continue
        m = re.match(r"(#{1,6})\s+(.*)", stripped)
        if m:
            flush_all()
            lvl = min(len(m.group(1)), 4)
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>")
            continue
        if stripped.startswith(">"):
            flush_para(); flush_bullets()
            quote.append(stripped.lstrip("> ").strip())
            continue
        m = re.match(r"[-*+]\s+(.*)", stripped)
        if m:
            flush_para(); flush_quote()
            bullets.append(m.group(1))
            continue
        flush_bullets(); flush_quote()
        para.append(stripped)
    flush_all()
    return "".join(out)


def latest_section(md, label):
    """Pull one '**Label.** ...' block out of the NEWEST entry of an append-only log.

    Newest is last, so we search from the end. Returns None rather than guessing when the
    label is absent — imported entries use a different vocabulary and must not be forced
    into this shape.
    """
    if not md:
        return None
    entries = re.split(r"\n(?=## )", md)
    for chunk in reversed(entries):
        m = re.search(rf"\*\*{re.escape(label)}\.?\*\*[ \t]*(.+?)(?=\n\s*\n|\Z)",
                      chunk, re.S)
        if m and m.group(1).strip():
            return re.sub(r"\s+", " ", m.group(1)).strip()
    return None


def _clip(s, n):
    if not s:
        return ""
    s = s.strip()
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


# --- page shell --------------------------------------------------------------
def _shell(title, body, active="dashboard", subtitle=""):
    tabs = "".join(
        f"<a class='{'on' if active == key else ''}' href='{href}'>{label}</a>"
        for key, href, label in (("dashboard", "/index.html", "Dashboard"),
                                 ("research", "/research/index.html", "Research")))
    return (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{_e(title)}</title><style>{CSS}</style></head><body>"
        f"<div class='topbar'><div class='inner'><div class='brand'>Equity Engine "
        f"<span>· Russell 2000</span></div><div class='tabs'>{tabs}</div></div></div>"
        f"<div class='wrap'>{body}"
        "<footer>Built from free sources only: SEC EDGAR XBRL company facts and "
        "end-of-day prices. No paid data, no paywalled sources, and no order-placement "
        "path anywhere in this system.<br>Universe frozen from the iShares Russell 2000 "
        "holdings file; index membership drifts between reconstitutions.</footer>"
        f"</div><script>{JS}</script></body></html>")


# --- the screen page ---------------------------------------------------------
def _calls_section(verdicts, logs):
    """Names where the engine actually reached a directional conclusion.

    `cheap` and `rich` only. Everything else — fair, no_edge, no_model — is a deliberate
    refusal and belongs in the table below, not here. Conviction rides on the face of the
    card because most calls are low by design and hiding that would oversell them.
    """
    calls = [v for v in verdicts if v.get("verdict") in ("cheap", "rich")]
    rank = {"high": 0, "medium": 1, "low": 2}
    calls.sort(key=lambda v: (rank.get(v.get("conviction"), 3),
                              -abs((v.get("priced") or {}).get("gap") or 0)))
    P = [f"<h2>Where the engine has a view <span class='n'>· {len(calls)} of "
         f"{len(verdicts)} researched names</span></h2>",
         "<p class='sub'>Only <code>cheap</code> and <code>rich</code> appear here. "
         "<code>fair</code>, <code>no_edge</code> and <code>no_model</code> are refusals, "
         "and refusing is the expected answer most days. These are research conclusions to "
         "check, not instructions — nothing in this system can place an order.</p>"]
    if not calls:
        P.append("<div class='empty'>No directional call today. Every researched name came "
                 "back <code>fair</code>, <code>no_edge</code> or <code>no_model</code>.<br>"
                 "That is the system working, not the system failing.</div>")
        return "".join(P)

    P.append("<div class='calls'>")
    for v in calls:
        t = v["ticker"]
        pr = v.get("priced") or {}
        gap = pr.get("gap") if pr.get("ok") else None
        gcls = "pos" if v["verdict"] == "cheap" else "neg"
        gtxt = f"{gap*100:+.0f}%" if gap is not None else "—"
        href = f"/research/{sector_slug(v['sector'])}/{t}.html"
        md = logs.get(t, "")
        why = v.get("base_case_rationale") or latest_section(md, "Base case")
        counter = ((v.get("devils_advocate") or {}).get("strongest_counter")
                   or latest_section(md, "Devil's advocate"))
        changed = v.get("what_changed") or latest_section(md, "What changed")
        watch = v.get("watch_for") or []

        P.append(f"<details class='call'><summary>"
                 f"<span class='caret'>▶</span>"
                 f"<span class='tk'>{_e(t)}</span>"
                 f"<span class='badge b-{v['verdict']}'>{_e(v['verdict'])}</span>"
                 f"<span class='conv'>{_e(v.get('conviction'))} conviction</span>"
                 f"<span class='nm'>{_e(v.get('name'))}</span>"
                 f"<span class='gap {gcls}'>{gtxt}</span></summary><div class='body'>")
        # Short on purpose. This card is a summary that has to be readable at a glance;
        # the full argument, the sources and the data-quality note are one click away and
        # truncating here is what keeps the reader going there.
        if why:
            P.append(f"<h4>Why</h4><p>{_e(_clip(why, 360))}</p>")
        if counter:
            P.append(f"<h4>Strongest case against</h4><p>{_e(_clip(counter, 300))}</p>")
        if changed:
            P.append(f"<h4>What changed</h4><p>{_e(_clip(changed, 240))}</p>")
        if watch:
            P.append(f"<h4>Watch for</h4><p>{_e(_clip('; '.join(str(w) for w in watch), 200))}</p>")
        P.append("<div class='nums'>")
        for label, val in (("Price", f"${v['price_at_verdict']:,.2f}"
                            if v.get("price_at_verdict") else "—"),
                           ("Market implies", f"{v['market_implied_growth']*100:+.1f}%"
                            if v.get("market_implied_growth") is not None else "n/a"),
                           ("We assume", f"{v['final_growth']*100:+.1f}%"
                            if v.get("final_growth") is not None else "no number"),
                           ("Horizon", f"{v.get('horizon_months')}m"
                            if v.get("horizon_months") else "—"),
                           ("Dated", v.get("date", "—"))):
            P.append(f"<div>{_e(label)}<b>{_e(val)}</b></div>")
        P.append(f"</div><p style='margin-top:14px'><a href='{href}'>"
                 f"Full reasoning, sources and data-quality note →</a></p>")
        P.append("</div></details>")
    P.append("</div>")
    return "".join(P)


def build_dashboard(screen, picks, verdicts, logs, tree):
    gen = screen.get("generated_utc", "")
    a = screen["assumptions"]
    rows = screen["rows"]
    n = len(rows)
    all_modelled = sum(1 for r in rows if r.get("gap") is not None)
    modelled = [r for r in rows
                if r.get("gap") is not None
                and abs(r["gap"]) <= config.MAX_ABS_GAP
                and "illiquid_below_min_dollar_volume" not in (r.get("flags") or [])
                and "below_min_market_cap" not in (r.get("flags") or [])]
    cheap = sorted([r for r in modelled if r["gap"] > 0], key=lambda r: -r["gap"])
    rich = sorted([r for r in modelled if r["gap"] < 0], key=lambda r: r["gap"])
    have_page = {t for ts in tree.values() for t in ts}

    def tick(ticker, sector):
        if ticker in have_page:
            return (f"<td class='tick' data-v='{_e(ticker)}'><a href='/research/"
                    f"{sector_slug(sector)}/{_e(ticker)}.html'>{_e(ticker)}</a></td>")
        return f"<td class='tick' data-v='{_e(ticker)}'>{_e(ticker)}</td>"

    P = []
    A = P.append
    A(f"<h1>The screen</h1><p class='sub'>Generated {_e(gen)} UTC · risk-free "
      f"{screen.get('risk_free_rate',0)*100:.2f}% ({_e(screen.get('risk_free_source'))})</p>")
    A("<div class='banner'><strong>This engine screens and recommends. You decide and "
      "you execute.</strong> Nothing here is a trade instruction, and no part of this "
      "system can place one.</div>")

    A("<div class='hero'>")
    A(f"<div class='stat'><div class='k'>Total universe</div><div class='v'>{n:,}</div>"
      f"<div class='s'>Russell 2000 constituents, frozen</div></div>")
    A(f"<div class='stat'><div class='k'>Total screened</div><div class='v'>{all_modelled:,}</div>"
      f"<div class='s'>got a defensible number; {n-all_modelled:,} refused one</div></div>")
    A("</div>")

    A(_calls_section(verdicts, logs))

    shocks = (picks[0] or {}).get("_shocks") if picks else None
    if shocks:
        A("<h2>Sector moves driving today's priorities</h2>")
        A("<p class='sub'>Read off the tape, not a news feed: a sector whose median 5-day "
          "return has moved hard pulls its worst-hit names forward in the queue.</p>")
        for sec, s in sorted(shocks.items(), key=lambda kv: kv[1]["median"]):
            cls = "neg" if s["median"] < 0 else "pos"
            A(f"<span class='chip'>{_e(sec)} <b class='{cls}'>{s['median']*100:+.1f}%</b> "
              f"median 5d ({s['n']} names)</span>")

    if picks:
        A(f"<h2>Today's ten <span class='n'>· selected for deep research</span></h2>")
        vmap = {v["ticker"]: v for v in verdicts}
        tr = []
        for p in picks:
            r = p["row"]
            v = vmap.get(p["ticker"], {})
            pr = v.get("priced") or {}
            verdict = v.get("verdict")
            vc = (f"<td data-v='{verdict}'><span class='badge b-{verdict}'>{_e(verdict)}"
                  f"</span></td>" if verdict else "<td class='dim' data-v=''>pending</td>")
            tr.append(
                "<tr>" + tick(p["ticker"], r["sector"])
                + f"<td data-v='{_e(r.get('name'))}'>{_e(r.get('name'))}</td>"
                f"<td data-v='{_e(r['sector'])}'>{_e(r['sector'])}</td>"
                f"<td data-v='{_e(p['slot'])}'><span class='chip'>{_e(p['slot'])}</span></td>"
                + _usd(r.get("price"))
                + _pct_of_high(r.get("price"), r.get("high_252d"))
                + _pct(r.get("implied_growth")) + _pct(r.get("gap"))
                + (_pct(pr.get("gap")) if pr.get("ok") else "<td class='num dim' data-v=''>—</td>")
                + vc
                + f"<td class='why' data-v=''>{_e('; '.join(p['why'][:3]))}</td></tr>")
        A(_table(tr, ["Ticker", "Name", "Sector", "Slot", "Price", "% of 52w high",
                      "Mkt implied g", "Baseline gap", "Analyst gap", "Verdict",
                      "Why selected"]))

    if verdicts:
        A(f"<h2>Researched names <span class='n'>· {len(verdicts)} with a written thesis"
          f"</span></h2>")
        A("<p class='sub'>Through the full loop: news, own assumptions, adversarial pass. "
          "Sorted by the analyst's gap, not the screen's. Click a ticker for the reasoning.</p>")
        vs = sorted(verdicts, key=lambda v: -((v.get("priced") or {}).get("gap") or -9))
        tr = []
        for v in vs[:120]:
            pr = v.get("priced") or {}
            tr.append(
                "<tr>" + tick(v["ticker"], v["sector"])
                + f"<td data-v='{_e(v.get('name'))}'>{_e(v.get('name'))}</td>"
                f"<td data-v='{_e(v['sector'])}'>{_e(v['sector'])}</td>"
                f"<td data-v='{v['verdict']}'><span class='badge b-{v['verdict']}'>"
                f"{_e(v['verdict'])}</span></td>"
                f"<td data-v='{_e(v.get('conviction'))}'>{_e(v.get('conviction'))}</td>"
                + _usd(v.get("price_at_verdict"))
                + _pct(v.get("market_implied_growth")) + _pct(v.get("final_growth"))
                + (_pct(pr.get("gap")) if pr.get("ok") else "<td class='num dim' data-v=''>—</td>")
                + f"<td class='dim' data-v='{_e(v['date'])}'>{_e(v['date'])}</td></tr>")
        A(_table(tr, ["Ticker", "Name", "Sector", "Verdict", "Conviction", "Price",
                      "Mkt implied g", "Analyst g", "Analyst gap", "Dated"]))

    A("<h2>Screen — widest baseline gaps <span class='n'>· mechanical, no judgment"
      "</span></h2>")
    A("<p class='sub'>Every name priced off its own history, nothing more. This ranks "
      "candidates for research; it is not a view. Illiquid and sub-scale names are "
      "excluded, and gaps beyond ±300% are treated as data errors and dropped.</p>")
    tr = []
    for r in (cheap[:60] + rich[:25]):
        fl = "".join(f"<span class='chip warn'>{_e(f.split('(')[0][:26])}</span>"
                     for f in (r.get("flags") or [])[:2])
        tr.append(
            "<tr>" + tick(r["ticker"], r["sector"])
            + f"<td data-v='{_e(r.get('name'))}'>{_e(r.get('name'))}</td>"
            f"<td data-v='{_e(r['sector'])}'>{_e(r['sector'])}</td>"
            f"<td data-v='{_e(r.get('method'))}'>{_e(r.get('method'))}</td>"
            + _usd(r.get("price")) + _cap(r.get("market_cap"))
            + _pct(r.get("implied_growth")) + _pct(r.get("baseline_growth"))
            + _pct(r.get("gap"))
            + f"<td class='num' data-v='{r.get('cohort_pct') if r.get('cohort_pct') is not None else ''}'>"
              f"{r.get('cohort_pct') if r.get('cohort_pct') is not None else '—'}</td>"
            + f"<td data-v=''>{fl}</td></tr>")
    A(_table(tr, ["Ticker", "Name", "Sector", "Method", "Price", "Mkt cap",
                  "Mkt implied g", "Baseline g", "Gap", "Cohort %ile", "Flags"]))

    counts = screen.get("counts", {})
    A("<h2>How to read this, and where it is weak</h2>")
    A("<details class='note' open><summary>Method</summary><div class='inner'>"
      "Each name is priced twice with the same two-stage model. <b>Reverse DCF:</b> solve "
      "for the 5-year free-cash-flow growth that makes the model reproduce today's "
      "enterprise value — that is what the market is assuming. <b>Forward DCF:</b> price an "
      "assumption of our own and compare. On this page the forward number is a mechanical "
      "baseline (the company's own revenue history), which is why it carries no judgment. "
      "The ten researched names each day replace that baseline with a real one.<br><br>"
      "Financials get justified price-to-tangible-book from sustainable return on tangible "
      "equity instead — free cash flow to the firm is meaningless when debt is raw "
      "material. REITs and companies with negative normalized cash flow get no number at "
      "all.<br><br><b>% of 52w high</b> is the current price divided by the highest close "
      "in the trailing 252 sessions.</div></details>")
    A("<details class='note'><summary>Assumptions that move every number on this page"
      "</summary><div class='inner'>"
      f"Equity risk premium <code>{a['equity_risk_premium']:.1%}</code> · terminal growth "
      f"<code>{a['terminal_growth']:.1%}</code> · explicit forecast "
      f"<code>{a['explicit_years']}y</code> · tax <code>{a['marginal_tax_rate']:.0%}</code>. "
      "These are choices, not facts, and they shift every absolute gap in the same "
      "direction. That is exactly why the cohort percentile column exists: it compares a "
      "name to its own sector under identical assumptions, so a whole sector cannot look "
      "cheap because of a constant chosen here. Implied growth is also reported at ±1pt of "
      "WACC on each brief, because it is far more sensitive to the discount rate than to "
      "anything else.</div></details>")
    A("<details class='note'><summary>What this screen cannot do</summary><div class='inner'>"
      "It cannot value pre-revenue biotech, bitcoin miners, or anything with negative "
      "normalized free cash flow — those are refused rather than guessed at. It cannot see "
      "off-balance-sheet obligations, segment detail, or anything not tagged in XBRL. A "
      "single lumpy year still distorts a three-year cash-flow base, which is why briefs "
      "carry dispersion flags. Prices are end-of-day. Fundamentals are as of the last "
      "annual filing and can be up to a year stale.</div></details>")
    A("<details class='note'><summary>Coverage detail</summary><div class='inner'>"
      + " · ".join(f"<code>{_e(k)}</code> {v}" for k, v in counts.items())
      + "</div></details>")
    return _shell("Equity Engine — Russell 2000 screen", "".join(P), "dashboard")


# --- the research tab --------------------------------------------------------
def build_research_index(tree, verdicts, logs, covered_pct):
    vmap = {v["ticker"]: v for v in verdicts}
    total = sum(len(v) for v in tree.values())
    P = [f"<h1>Research</h1><p class='sub'>Every company this engine has written about, "
         f"organised the way it is stored: sector folder first, one append-only log per "
         f"company inside it. Newest entry at the bottom of each page. This mirrors "
         f"<code>research/&lt;Sector&gt;/&lt;TICKER&gt;.md</code> in the repository — the "
         f"site is a view of that tree, not a second copy.</p>"]
    written = sum(1 for t in (x for ts in tree.values() for x in ts) if t in vmap)
    P.append("<div class='hero'>")
    P.append(f"<div class='stat'><div class='k'>Companies covered</div>"
             f"<div class='v'>{total:,}</div>"
             f"<div class='s'>{covered_pct:.1f}% of the index, across {len(tree)} sectors</div></div>")
    P.append(f"<div class='stat'><div class='k'>Written this engine</div>"
             f"<div class='v'>{written:,}</div>"
             f"<div class='s'>the rest carry logs imported from the previous one</div></div>")
    P.append("</div>")
    P.append("<p class='sub' style='margin-top:12px'><a href='/research/lessons.html'>"
             "Standing lessons →</a> the priors the analyst is held to before every "
             "session.</p>")

    if not tree:
        P.append("<div class='empty'>Nothing written yet.</div>")
        return _shell("Equity Engine — Research", "".join(P), "research")

    for sector, tickers in tree.items():
        slug = sector_slug(sector)
        P.append(f"<div class='sector'><h3>{_e(sector)} <span class='n' "
                 f"style='color:var(--faint);font-weight:400'>· {len(tickers)}</span></h3>"
                 f"<p class='path'>research/{_e(sector)}/</p><div class='co'>")
        for t in tickers:
            v = vmap.get(t, {})
            verdict = v.get("verdict")
            badge = (f"<span class='badge b-{verdict}'>{_e(verdict)}</span>" if verdict
                     else "<span class='badge b-fair'>imported</span>")
            name = v.get("name") or _first_heading_name(logs.get(t, "")) or ""
            P.append(f"<a href='/research/{slug}/{_e(t)}.html'><div class='r1'>"
                     f"<span class='t'>{_e(t)}</span>{badge}</div>"
                     f"<div class='n2'>{_e(name)}</div></a>")
        P.append("</div></div>")
    return _shell("Equity Engine — Research", "".join(P), "research")


def _first_heading_name(md):
    m = re.match(r"#\s+\S+\s+—\s+(.+)", (md or "").lstrip())
    return m.group(1).strip() if m else None


def build_company_page(sector, ticker, md, verdict):
    slug = sector_slug(sector)
    name = (verdict or {}).get("name") or _first_heading_name(md) or ticker
    P = [f"<p class='crumb'><a href='/research/index.html'>Research</a> / "
         f"{_e(sector)} / {_e(ticker)}</p>",
         f"<h1>{_e(ticker)} <span style='color:var(--faint);font-weight:400'>"
         f"{_e(name)}</span></h1>"]
    if verdict:
        pr = verdict.get("priced") or {}
        cells = [("Verdict", f"<span class='badge b-{verdict['verdict']}'>"
                  f"{_e(verdict['verdict'])}</span>"),
                 ("Conviction", _e(verdict.get("conviction"))),
                 ("Price at verdict", f"${verdict['price_at_verdict']:,.2f}"
                  if verdict.get("price_at_verdict") else "—"),
                 ("Analyst gap", f"{pr['gap']*100:+.0f}%" if pr.get("ok") else "not repriced"),
                 ("Dated", _e(verdict.get("date")))]
        P.append("<div class='factstrip'>"
                 + "".join(f"<div>{k}<b>{v}</b></div>" for k, v in cells)
                 + "</div>")
    P.append(f"<div class='prose'>{md_to_html(md)}</div>")
    P.append(f"<p class='sub' style='margin-top:14px'>Source of truth: "
             f"<a href='{GITHUB}/research/{sector.replace(' ', '%20')}/{ticker}.md'>"
             f"research/{_e(sector)}/{_e(ticker)}.md</a> — append-only, newest at the "
             f"bottom. This page is generated from it.</p>")
    return _shell(f"{ticker} — Equity Engine research", "".join(P), "research")


# --- entry point -------------------------------------------------------------
def build(screen, picks=None, verdicts=None, out=None):
    picks = picks or []
    verdicts = verdicts or []
    out = out or (config.PUBLIC / "index.html")
    root = out.parent
    root.mkdir(parents=True, exist_ok=True)

    tree = research_tree()
    logs, sector_of = {}, {}
    for sector, tickers in tree.items():
        for t in tickers:
            logs[t] = (config.RESEARCH / sector / f"{t}.md").read_text()
            sector_of[t] = sector
    vmap = {v["ticker"]: v for v in verdicts}

    written = [out]
    out.write_text(build_dashboard(screen, picks, verdicts, logs, tree))

    rdir = root / "research"
    rdir.mkdir(parents=True, exist_ok=True)
    n = len(screen.get("rows") or []) or 1
    covered = len({v["ticker"] for v in verdicts} | set(logs))
    idx = rdir / "index.html"
    idx.write_text(build_research_index(tree, verdicts, logs, covered / n * 100))
    written.append(idx)

    lessons_md = config.RESEARCH / "LESSONS.md"
    if lessons_md.exists():
        body = (f"<p class='crumb'><a href='/research/index.html'>Research</a> / Lessons</p>"
                f"<h1>Standing lessons</h1><p class='sub'>Priors about how this kind of "
                f"thesis goes wrong. The analyst reads these before every session and is "
                f"held to them. Not scored results — no thesis has matured yet.</p>"
                f"<div class='prose'>{md_to_html(lessons_md.read_text())}</div>")
        p = rdir / "lessons.html"
        p.write_text(_shell("Standing lessons — Equity Engine", body, "research"))
        written.append(p)

    for t, md in logs.items():
        sector = sector_of[t]
        d = rdir / sector_slug(sector)
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"{t}.html"
        p.write_text(build_company_page(sector, t, md, vmap.get(t)))
        written.append(p)

    return out, written
