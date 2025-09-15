# Data folder

This repo does **not** track raw datasets. Use this folder locally only.

## Source (Kaggle)
This project uses daily close prices from **“NIFTY50 stock market data”** by **rohanrao**.  
Link: https://www.kaggle.com/datasets/rohanrao/nifty50-stock-market-data

We intentionally **do not** commit raw CSVs to the repo.

## Obtain the data
**Manual**
1. Download the dataset from Kaggle.
2. Place the per-stock CSVs under: `data/raw/nifty50/`

**Kaggle API (optional)**
```bash
pip install kaggle
# Place your API token as kaggle.json at:
#   macOS/Linux: ~/.kaggle/kaggle.json
#   Windows:     %USERPROFILE%\.kaggle\kaggle.json
kaggle datasets download rohanrao/nifty50-stock-market-data -p data/raw/nifty50 --unzip
```
## Build the processed dataset
From the repo root, after placing CSVs under `data/raw/nifty50/`:
```bash
# Build a wide, compressed file with all tickers
python scripts/build_prices.py --src data/raw/nifty50 --out data/prices_wide.csv.gz

# OR: restrict to a 15-asset set and date window (smaller file)
python scripts/build_prices.py \
  --src data/raw/nifty50 \
  --tickers "HDFCBANK,TCS,INFY,RELIANCE,ICICIBANK,KOTAKBANK,HINDUNILVR,ITC,LT,BAJFINANCE,ASIANPAINT,MARUTI,SBIN,BHARTIARTL,ULTRACEMCO" \
  --start 2010-01-01 --end 2021-12-31 \
  --out data/prices_wide.csv.gz

```

The script auto-detects date/close columns, merges on `Date`, sorts chronologically, drops all-NaN rows, and writes a gzip CSV.

## Expected schema (processed file)
- File: `data/prices_wide.csv.gz`
- Columns: `Date,<TICKER_1>,<TICKER_2>,...,<TICKER_N>` (daily close prices)
- Date: `YYYY-MM-DD`

## Load in code
```Python
import pandas as pd
prices = (pd.read_csv("data/prices_wide.csv.gz", compression="infer", parse_dates=["Date"])
            .set_index("Date").sort_index())
```
