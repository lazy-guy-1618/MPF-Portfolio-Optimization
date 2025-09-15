import os, glob
import pandas as pd

SRC_DIR = "data/raw/nifty50"
OUT_CSV = "data/prices_wide.csv"

TICKERS = None  

def find_col(cols, candidates):
    cl = {c.strip().lower(): c for c in cols}
    for cand in candidates:
        if cand in cl:
            return cl[cand]
    return None

def read_one(path):
    sym = os.path.splitext(os.path.basename(path))[0].upper()
    df = pd.read_csv(path)
    date_col = find_col(df.columns, ["date", "timestamp"])
    close_col = find_col(df.columns, ["close", "close price", "adj close", "close*"])
    if date_col is None or close_col is None:
        raise ValueError(f"{sym}: missing date/close columns in {path}")
    out = df[[date_col, close_col]].copy()
    out.columns = ["Date", sym]
    out["Date"] = pd.to_datetime(out["Date"])
    return out

paths = sorted(glob.glob(os.path.join(SRC_DIR, "*.csv")))
frames = []
for p in paths:
    sym = os.path.splitext(os.path.basename(p))[0].upper()
    if TICKERS and sym not in TICKERS:
        continue
    frames.append(read_one(p))

wide = None
for f in frames:
    wide = f if wide is None else wide.merge(f, on="Date", how="outer")

wide = wide.sort_values("Date")
# optional: drop days where *all* assets are NaN (e.g., holidays)
value_cols = [c for c in wide.columns if c != "Date"]
wide = wide.loc[~wide[value_cols].isna().all(axis=1)]

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
wide.to_csv(OUT_CSV, index=False)
print(f"Wrote {OUT_CSV} with shape {wide.shape}")
