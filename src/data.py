from __future__ import annotations
import pandas as pd
import numpy as np
from typing import Tuple

def load_prices(csv_path: str, date_col: str = "Date") -> pd.DataFrame:
    """
    Load a wide CSV of prices with a date column and one column per asset.
    Keeps only numeric asset columns.
    """
    df = pd.read_csv(csv_path)
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col])
        df = df.set_index(date_col).sort_index()
    # keep numeric columns only
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    return df[numeric_cols]

def _local_mean_impute(series: pd.Series, k: int = 5) -> pd.Series:
    """
    KNN-style local mean fill (k neighbors ~ centered rolling mean).
    This mirrors the report's 'mean of 5 neighboring values' idea.
    """
    filled = series.copy()
    # centered rolling mean; min_periods=1 to use available neighbors
    rolled = series.rolling(window=k, center=True, min_periods=1).mean()
    filled = filled.fillna(rolled)
    # final pass to catch edges
    return filled.interpolate(method="linear", limit_direction="both")

def impute_prices(prices: pd.DataFrame, k: int = 5) -> pd.DataFrame:
    return prices.apply(lambda s: _local_mean_impute(s, k=k))

def to_returns(prices: pd.DataFrame, log: bool = False) -> pd.DataFrame:
    if log:
        rets = np.log(prices).diff().dropna()
    else:
        rets = prices.pct_change().dropna()
    return rets.replace([np.inf, -np.inf], np.nan).dropna(how="any")

def mean_cov(returns: pd.DataFrame, ann_factor: int = 252) -> Tuple[np.ndarray, np.ndarray]:
    mu = returns.mean().values * ann_factor
    Sigma = returns.cov().values * ann_factor
    return mu, Sigma
