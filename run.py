"""
run.py - entry point.

  python run.py --tickers PLAB,SHOO,UFPT,CALM
  python run.py --tickers PLAB,SHOO,UFPT,CALM --positions positions.json

positions.json : [{"ticker":"SHOO","shares":50,"avg_cost":40.0}]

The synthesis runs autonomously (stub by default; live Claude synthesis is wired
at the orchestration layer — see CONNECTING.md). Outputs land in out/.
"""
import argparse
import json
import os

import engine
import outputs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", help="comma-separated symbols")
    ap.add_argument("--positions", help="path to positions JSON")
    ap.add_argument("--outdir", default="out")
    args = ap.parse_args()

    tickers = [t.strip().upper() for t in (args.tickers or "").split(",") if t.strip()]
    positions = json.load(open(args.positions)) if args.positions else None
    if not tickers:
        print("no tickers given (use --tickers or wire in the IWM holdings pull — see SCALING.md)")
        return

    results = engine.run(tickers, positions=positions)
    os.makedirs(args.outdir, exist_ok=True)
    print("wrote", outputs.build_dashboard(results, os.path.join(args.outdir, "dashboard.html")))
    print("wrote", outputs.build_email(results, os.path.join(args.outdir, "email_brief.html")))
    for r in results["rows"]:
        if r.get("error"):
            print(f"  {r['ticker']:6} ERROR {r['error']}")
        else:
            t = r.get("thesis") or {}
            print(f"  {r['ticker']:6} {r['recommendation']['action']:34} "
                  f"gap={t.get('gap_vs_price')} reliable={r['reliable']}")


if __name__ == "__main__":
    main()
