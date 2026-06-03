"""
charts.py - render a compact chart SPEC (carried in a thesis) to a base64 PNG
data-URI, so the dashboard can embed it inline and stay a single self-contained file.

A chart spec is plain JSON the synthesizer produces ALONGSIDE its reasoning, e.g.:

    {
      "title": "Operating margin collapsed to a tariff/integration trough",
      "x": ["FY22", "FY23", "FY24", "FY25"],
      "series": [
        {"name": "Revenue ($M)",        "data": [2122, 1982, 2283, 2534], "kind": "bar",  "axis": "left"},
        {"name": "Operating margin (%)", "data": [13.5, 11.1, 10.4, 3.2],  "kind": "line", "axis": "right"}
      ],
      "source": "yfinance annual income statement, FY2022-FY2025"
    }

Charts are for NON-obvious metrics (margin trends, specific reporting swings) — not
simple revenue-over-time, which belongs in the writing. Rendering is best-effort:
any malformed spec returns None and the dashboard simply omits the image.
"""
import base64
import io

try:
    import matplotlib
    matplotlib.use("Agg")            # headless: no display needed
    import matplotlib.pyplot as plt
    # Don't treat '$' as LaTeX math delimiters — "$174M" is a dollar figure, not math.
    matplotlib.rcParams["text.parse_math"] = False
    _OK = True
except Exception:                    # matplotlib absent -> charts silently skipped
    _OK = False

_LEFT = ["#4E79A7", "#A0C4E2"]       # bars / left-axis lines (blues)
_RIGHT = ["#C0573B", "#E0A03B"]      # right-axis lines (warm)


def render_chart_to_datauri(spec):
    """Return 'data:image/png;base64,...' for a chart spec, or None on any problem."""
    if not _OK or not isinstance(spec, dict):
        return None
    x = spec.get("x") or []
    series = spec.get("series") or []
    if not x or not series:
        return None
    try:
        idx = list(range(len(x)))
        fig, ax_left = plt.subplots(figsize=(6.6, 3.3), dpi=110)
        ax_right = None
        bars = [s for s in series if s.get("kind") == "bar"]
        n_bars = max(1, len(bars))
        width = 0.8 / n_bars
        bi = li = ri = 0
        handles, labels = [], []

        for s in series:
            data = s.get("data") or []
            if len(data) != len(x):
                continue
            name = s.get("name", "")
            on_right = s.get("axis") == "right"
            if on_right and ax_right is None:
                ax_right = ax_left.twinx()
            ax = ax_right if on_right else ax_left
            if s.get("kind") == "bar":
                off = (bi - (n_bars - 1) / 2) * width
                h = ax.bar([i + off for i in idx], data, width=width,
                           label=name, color=_LEFT[bi % len(_LEFT)], zorder=2)
                bi += 1
            else:
                color = (_RIGHT if on_right else _LEFT)[(ri if on_right else li) % 2]
                (h,) = ax.plot(idx, data, marker="o", linewidth=2.2, label=name,
                               color=color, zorder=3)
                ri, li = (ri + 1, li) if on_right else (ri, li + 1)
            handles.append(h)
            labels.append(name)

        ax_left.set_xticks(idx)
        ax_left.set_xticklabels(x, fontsize=9)
        ax_left.tick_params(axis="y", labelsize=8)
        if ax_right is not None:
            ax_right.tick_params(axis="y", labelsize=8)
        ax_left.set_title(spec.get("title", ""), fontsize=10.5, fontweight="bold", pad=8)
        ax_left.grid(axis="y", alpha=0.25, zorder=0)
        ax_left.legend(handles, labels, loc="best", fontsize=8, framealpha=0.85)

        src = spec.get("source")
        if src:
            fig.text(0.01, 0.005, f"source: {src}", fontsize=6.5,
                     color="#6b6b6b", ha="left", va="bottom")
        fig.tight_layout(rect=(0, 0.05 if src else 0, 1, 1))

        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        plt.close(fig)
        b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        return f"data:image/png;base64,{b64}"
    except Exception:
        try:
            plt.close("all")
        except Exception:
            pass
        return None
