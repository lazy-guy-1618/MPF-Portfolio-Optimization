from __future__ import annotations
import numpy as np
import cvxpy as cp
import pandas as pd
from typing import Tuple, Optional, Iterable

def _solve(prob: cp.Problem, candidate_solvers: Iterable[str] = ("SCS", "OSQP", "ECOS")) -> None:
    last_err = None
    for s in candidate_solvers:
        try:
            prob.solve(solver=getattr(cp, s), verbose=False)
            if prob.status in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
                return
        except Exception as e:
            last_err = e
    if last_err:
        raise last_err
    raise RuntimeError(f"Problem not solved; status={prob.status}")

def solve_min_variance(mu: np.ndarray, Sigma: np.ndarray, r_min: float) -> np.ndarray:
    """
    Minimize w' Σ w  s.t. 1'w=1, w>=0, mu'w >= r_min
    """
    n = len(mu)
    w = cp.Variable(n, nonneg=True)
    objective = cp.Minimize(cp.quad_form(w, Sigma))
    constraints = [cp.sum(w) == 1, mu @ w >= r_min]
    prob = cp.Problem(objective, constraints)
    _solve(prob)
    return np.array(w.value).ravel()

def solve_max_return(mu: np.ndarray, Sigma: np.ndarray, sigma2_max: float) -> np.ndarray:
    """
    Maximize mu'w  s.t. 1'w=1, w>=0, w'Σw <= sigma2_max
    """
    n = len(mu)
    w = cp.Variable(n, nonneg=True)
    objective = cp.Maximize(mu @ w)
    constraints = [cp.sum(w) == 1, cp.quad_form(w, Sigma) <= sigma2_max]
    prob = cp.Problem(objective, constraints)
    _solve(prob)
    return np.array(w.value).ravel()

def efficient_frontier(mu: np.ndarray, Sigma: np.ndarray, n_pts: int = 25) -> pd.DataFrame:
    """
    Sweep r_min from low to high, solve min-variance, and return (risk, return).
    """
    r_grid = np.linspace(float(mu.min()), float(mu.max()), n_pts)
    data = []
    for r_min in r_grid:
        w = solve_min_variance(mu, Sigma, r_min=r_min)
        risk_var = float(w @ Sigma @ w)
        data.append({"r_min": r_min, "risk": risk_var**0.5, "return": float(mu @ w)})
    return pd.DataFrame(data)
