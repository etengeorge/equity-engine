"""Prices, returns, liquidity and beta for the whole universe in a handful of calls.

yfinance is the free/keyless source. Direct Yahoo REST returns 429 without a cookie+crumb,
so we always go through the library, and we download in bulk (hundreds of tickers per call)
rather than per-name.
"""
import math, datetime as dt
from zoneinfo import ZoneInfo
import pandas as pd
import config

BENCH = "IWM"                   # the universe's own index: the right beta benchmark here
_CHUNK = 200


def download_closes(tickers, period="2y"):
    """Adjusted closes for every ticker, as a DataFrame indexed by date.
    Missing/delisted names simply come back as all-NaN columns."""
    import yfinance as yf
    frames = []
    syms = list(dict.fromkeys(list(tickers) + [BENCH]))
    for i in range(0, len(syms), _CHUNK):
        chunk = syms[i:i + _CHUNK]
        df = yf.download(chunk, period=period, interval="1d", progress=False,
                         auto_adjust=True, threads=True, group_by="column")
        if df is None or df.empty:
            continue
        close = df["Close"] if "Close" in df.columns.get_level_values(0) else df
        if isinstance(close, pd.Series):
            close = close.to_frame(name=chunk[0])
        frames.append(close)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, axis=1).sort_index()


def download_volumes(tickers, period="6mo"):
    import yfinance as yf
    frames = []
    syms = list(dict.fromkeys(tickers))
    for i in range(0, len(syms), _CHUNK):
        chunk = syms[i:i + _CHUNK]
        df = yf.download(chunk, period=period, interval="1d", progress=False,
                         auto_adjust=True, threads=True, group_by="column")
        if df is None or df.empty or "Volume" not in df.columns.get_level_values(0):
            continue
        vol = df["Volume"]
        if isinstance(vol, pd.Series):
            vol = vol.to_frame(name=chunk[0])
        frames.append(vol)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, axis=1).sort_index()


def _ret(series, days):
    s = series.dropna()
    if len(s) < days + 1:
        return None
    prev = s.iloc[-(days + 1)]
    if not prev or not math.isfinite(prev) or prev <= 0:
        return None
    return float(s.iloc[-1] / prev - 1.0)


def beta(stock_closes, bench_closes, weeks=config.BETA_LOOKBACK_WEEKS):
    """Weekly-return beta vs IWM, with an explicit reliability gate.

    Weekly rather than daily: thin small-cap tape makes daily betas collapse toward zero
    through non-synchronous trading. And we do NOT blanket-clamp low betas — a genuinely
    defensive name (CALM) has a real 0.3 beta and clamping it up would inflate its cost of
    equity by ~200bp and understate the growth the market implies. Instead we ask whether
    the regression explains anything at all: R^2 below FLOOR means the estimate is noise,
    and noise gets replaced by 1.0 and flagged, not smuggled into the discount rate.
    """
    a = stock_closes.dropna().resample("W-FRI").last().pct_change().dropna()
    b = bench_closes.dropna().resample("W-FRI").last().pct_change().dropna()
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    j = j.iloc[-weeks:]
    if len(j) < 52:
        return None, None, "insufficient_history"
    var = j.iloc[:, 1].var()
    if not var or not math.isfinite(var) or var <= 0:
        return None, None, "degenerate_benchmark_variance"
    raw = float(j.cov().iloc[0, 1] / var)
    corr = float(j.corr().iloc[0, 1])
    r2 = corr ** 2 if math.isfinite(corr) else 0.0
    if not math.isfinite(raw):
        return None, None, "nonfinite"
    if r2 < config.BETA_MIN_R2:
        return None, round(r2, 3), f"unreliable_r2_{r2:.3f}_raw_{raw:.2f}"
    lo, hi = config.BETA_CLAMP
    if raw < lo or raw > hi:
        return min(max(raw, lo), hi), round(r2, 3), f"clamped_from_{raw:.2f}"
    return raw, round(r2, 3), None


def risk_free_rate():
    """10-year Treasury yield via ^TNX (quoted in percent). Keyless; FRED needs an API key."""
    import yfinance as yf
    try:
        h = yf.Ticker("^TNX").history(period="1mo")
        if not h.empty:
            v = float(h["Close"].dropna().iloc[-1]) / 100.0
            if 0.0 < v < 0.15:
                return v, "^TNX 10y Treasury"
    except Exception:
        pass
    return 0.042, "fallback constant (^TNX unavailable)"


def alternates(ticker, name=""):
    """Other symbols Yahoo might know this security by.

    iShares writes class shares without a separator (MOOG CLASS A -> "MOGA") while Yahoo
    wants "MOG-A". We do NOT apply that as a rule: 263 universe names say "CLASS A" and
    almost all of their tickers are already correct (ZETA is really ZETA, not ZET-A).
    So these are only ever tried as a REPAIR for symbols that came back empty, never as
    a preemptive rewrite.
    """
    out, up = [], name.upper()
    if "." in ticker:
        out.append(ticker.replace(".", "-"))
    if "-" in ticker:
        out.append(ticker.replace("-", "."))
    if len(ticker) >= 3:
        last = ticker[-1]
        if f"CLASS {last}" in up:
            out.append(f"{ticker[:-1]}-{last}")
            out.append(f"{ticker[:-1]}.{last}")
    return [s for s in dict.fromkeys(out) if s != ticker]


def drop_incomplete_session(closes, vols=None, now_et=None):
    """Remove today's bar while the US market is still open.

    yfinance hands back a partial bar for the session in progress, and it is
    indistinguishable from a close in the frame. The engine relied on the 07:23 ET cron
    to stay ahead of the open instead of checking, which made correctness a property of
    the SCHEDULE rather than of the data: a scheduled run has already been delayed 7h10m
    once, and the DST guard's response to a late run was to skip the day silently. With
    the partial bar dropped here, a late run is merely late — it still prices off the
    last completed session and reports the right `price_asof`.

    Only drops a bar dated today before 16:00 ET. A bar for any earlier date is a real
    close and is always kept, so this is a no-op for the normal pre-market run.
    """
    if closes is None or closes.empty:
        return closes, vols, None
    now_et = now_et or dt.datetime.now(ZoneInfo("America/New_York"))
    if now_et.hour >= 16:                    # regular session has closed
        return closes, vols, None
    last = closes.index[-1].date()
    if last != now_et.date():
        return closes, vols, None
    dropped = str(last)
    closes = closes.iloc[:-1]
    if vols is not None and not vols.empty and vols.index[-1].date() == now_et.date():
        vols = vols.iloc[:-1]
    return closes, vols, dropped


def build_quotes(tickers, names=None):
    """One row per ticker: price, trailing returns, liquidity, beta.
    This is the file the screen and the selector both read."""
    names = names or {}
    closes = download_closes(tickers)
    vols = download_volumes(tickers)

    # repair pass: anything with no usable history gets retried under its alternates
    missing = [t for t in tickers
               if t not in closes or closes[t].dropna().empty]
    remap = {}
    if missing:
        cand = {}
        for t in missing:
            for a in alternates(t, names.get(t, "")):
                cand[a] = t
        if cand:
            print(f"[prices] repairing {len(missing)} empty symbols via "
                  f"{len(cand)} alternates", flush=True)
            fixed = download_closes(list(cand), period="2y")
            fixed_v = download_volumes(list(cand), period="6mo")
            for alt, orig in cand.items():
                if alt in fixed and not fixed[alt].dropna().empty:
                    closes[orig] = fixed[alt]
                    if alt in fixed_v:
                        vols[orig] = fixed_v[alt]
                    remap[orig] = alt
    if remap:
        print(f"[prices] resolved: {remap}", flush=True)
    if closes.empty:
        raise RuntimeError("price download returned nothing — check network/yfinance")
    closes, vols, dropped = drop_incomplete_session(closes, vols)
    if dropped:
        print(f"[prices] dropped {dropped}: the session is still open, so that bar is "
              f"a partial print, not a close", flush=True)
    if closes.empty:
        raise RuntimeError("no completed session left after dropping the partial bar")
    bench = closes[BENCH] if BENCH in closes else None
    asof = str(closes.index[-1].date())
    rows = []
    for t in tickers:
        if t not in closes:
            rows.append({"ticker": t, "asof": asof, "status": "no_data"})
            continue
        s = closes[t].dropna()
        if s.empty:
            rows.append({"ticker": t, "asof": asof, "status": "no_data"})
            continue
        stale_days = (closes.index[-1] - s.index[-1]).days
        b, br2, bnote = (beta(closes[t], bench) if bench is not None
                         else (None, None, "no_benchmark"))
        # Dollar volume over two windows. The 60-day figure is the liquidity gate; the
        # ratio of the last week to it is a NEWS detector -- a small cap trading several
        # times its normal volume has something going on, and that shows up here before
        # any wire story does.
        dv = dv5 = vratio = None
        if t in vols:
            v = vols[t].dropna()
            if len(v):
                p = s.reindex(v.index).ffill()
                dollars = (v * p).dropna()
                if len(dollars) >= 5:
                    dv = float(dollars.iloc[-60:].mean())
                    dv5 = float(dollars.iloc[-5:].mean())
                    if dv and dv > 0:
                        vratio = round(dv5 / dv, 2)
        rows.append({
            "ticker": t, "asof": asof,
            "status": "ok" if stale_days <= 5 else "stale",
            "price": float(s.iloc[-1]),
            "stale_days": stale_days,
            "ret_1d": _ret(s, 1), "ret_5d": _ret(s, 5), "ret_21d": _ret(s, 21),
            "ret_63d": _ret(s, 63), "ret_252d": _ret(s, 252),
            "high_252d": float(s.iloc[-252:].max()) if len(s) >= 20 else None,
            "low_252d": float(s.iloc[-252:].min()) if len(s) >= 20 else None,
            "dollar_volume_60d": dv,
            "dollar_volume_5d": dv5,
            "volume_ratio": vratio,
            "beta": b, "beta_r2": br2, "beta_note": bnote,
            "yahoo_symbol": remap.get(t, t),
        })
    return pd.DataFrame(rows), closes
