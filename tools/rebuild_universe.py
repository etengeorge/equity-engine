"""Re-baseline the fixed universe from an iShares Russell 2000 holdings export.

Run this ONLY when you deliberately want to change the universe — e.g. after the June
reconstitution. Between runs the universe is frozen on purpose: a rotation that keeps
changing underneath itself never finishes a pass, and past research stops being comparable.

    python tools/rebuild_universe.py ~/Downloads/iShares-Russell-2000-ETF_fund.xls universe.csv

Get the file from iShares' IWM page ("Detailed Holdings and Analytics"). It downloads as
.xls but is actually SpreadsheetML XML, which is why this parses it as text.
"""
import csv, re, sys
from collections import Counter

# GICS sector -> how we can honestly value it.
#   fcff  = two-stage free-cash-flow-to-firm reverse DCF
#   book  = justified price/tangible book from residual income (debt is raw material here)
#   none  = no defensible free model; qualitative research only
METHOD_BY_SECTOR = {
    "Financials": "book",
    "Real Estate": "none",   # depreciated historical-cost book makes P/B meaningless, and
                             # FFO needs adjustments XBRL won't give us reliably
}


def main(src, dst):
    raw = open(src, encoding="utf-8", errors="replace").read()
    rows = re.findall(r"<ss:Row>(.*?)</ss:Row>", raw, re.S)

    def cells(r):
        return [re.sub(r"<[^>]+>", "", c).strip()
                for c in re.findall(r"<ss:Cell.*?>(.*?)</ss:Cell>", r, re.S)]

    asof, recs = "", []
    for c in map(cells, rows):
        if len(c) >= 2 and c[0] == "Fund Holdings as of":
            asof = c[1]
        if len(c) >= 6 and c[3] == "Equity" and c[0] and c[0] != "Ticker":
            t = c[0].strip().upper()
            if not re.fullmatch(r"[A-Z][A-Z.\-]{0,6}", t):
                continue                      # cash lines, futures, malformed rows
            recs.append({"ticker": t, "name": c[1], "sector": c[2],
                         "weight_pct": round(float(c[5]), 5) if c[5] else 0.0,
                         "method": METHOD_BY_SECTOR.get(c[2], "fcff")})

    recs.sort(key=lambda r: -r["weight_pct"])   # rotation starts with the largest names
    seen, out = set(), []
    for r in recs:
        if r["ticker"] not in seen:
            seen.add(r["ticker"])
            out.append(r)

    with open(dst, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["ticker", "name", "sector", "weight_pct", "method"])
        w.writeheader()
        w.writerows(out)
    print(f"holdings as of {asof}: wrote {len(out)} tickers -> {dst}")
    for m, n in Counter(r["method"] for r in out).most_common():
        print(f"  method={m:5s} {n:5d}")
    print("\nNOTE: names dropped from the index keep their research/ files. Nothing is "
          "deleted — the history stays readable even after a constituent leaves.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
