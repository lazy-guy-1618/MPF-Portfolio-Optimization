import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_efficient_frontier(frontier: pd.DataFrame, ax: plt.Axes | None = None) -> plt.Axes:
    """
    Plot risk (x) vs return (y) from DataFrame with columns ['risk','return'].
    """
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(frontier["risk"], frontier["return"], marker="o", lw=1)
    ax.set_xlabel("Risk (stdev)")
    ax.set_ylabel("Expected Return")
    ax.set_title("Efficient Frontier")
    return ax

def plot_allocations(weights: np.ndarray, asset_names: list[str]) -> plt.Axes:
    fig, ax = plt.subplots()
    ax.bar(asset_names, weights)
    ax.set_ylabel("Weight")
    ax.set_title("Optimal Allocation")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return ax
