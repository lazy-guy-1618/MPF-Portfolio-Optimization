# Data folder

This repo does **not** track raw datasets. Use this folder locally only.


## Source
Primary source: **Kaggle – “NIFTY50 stock market data.”**  
Please *do not* commit raw files; build a processed file instead.

## Build the processed dataset
From the repo root, after placing per-stock CSVs under `data/raw/nifty50/`:

```bash
# keep all tickers
python scripts/build_prices.py --src data/raw/nifty50 --out data/prices_wide.csv.gz

# or: restrict to 15 tickers and date window to keep it small
python scripts/build_prices.py \
  --src data/raw/nifty50 \
  --tickers "HDFCBANK,TCS,INFY,RELIANCE,ICICIBANK,KOTAKBANK,HINDUNILVR,ITC,LT,BAJFINANCE,ASIANPAINT,MARUTI,SBIN,BHARTIARTL,ULTRACEMCO" \
  --start 2010-01-01 --end 2021-12-31 \
  --out data/prices_wide.csv.gz
```

## Expected schema (processed file)
- File: data/prices_wide.csv.gz
- Columns: Date,<TICKER_1>,<TICKER_2>,...,<TICKER_N> (daily close prices)
- Date: YYYY-MM-DD

## Load in Code
```Python
import pandas as pd
prices = (pd.read_csv("data/prices_wide.csv.gz", compression="infer", parse_dates=["Date"])
            .set_index("Date").sort_index())
```
