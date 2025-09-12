# Multi-Objective Portfolio Optimisation (Convex Optimisation Project)

_A practical study based on portfolio management using convex optimisation._

> Course project for **Convex Optimisation (MA60213)**, Department of Mathematics, IIT Kharagpur.  
> Authors: **Mihir Mallick (21CS30031)** & **Aatir Zaki (21CH10092)**.  
> Supervisor: **Prof. Swanand Khare**.  
> Semester: **Autumn 2024-25**.

---

## Overview

This repository explores **portfolio construction as a convex optimisation problem**, balancing two competing objectives:

- **Maximise expected return**
- **Minimise portfolio risk (variance)**

We formulate both goals, solve them with **CVXPY**, and compare the optimal strategy with baseline strategies (equal-weight and aggressive concentration). We also visualise the **Pareto-optimal frontier** / **MPT efficient frontier** to understand the trade-off between risk and return.

For a deeper discussion, see the [📄 full report](./Convex_Optimization.pdf) and [🎞️ slides](./Convex%20Optimisation.pptx).

---

## Key Ideas

- **Statistical measures**: expected return, variance/standard deviation, and **Sharpe ratio**.
- **Convex formulations**:
  - **Maximise return** subject to budget, non-negativity, and a **risk (variance) bound**.
  - **Minimise variance** subject to budget, non-negativity, and a **minimum return**.
- **Why convex?** The covariance matrix is **positive semidefinite**, making the variance a convex function of the weights; linear objectives/constraints preserve convexity.
- **Multi-objective view**: solutions lie on the **Pareto front** / **efficient frontier** (Markowitz).

---

## Data

- Historical daily prices for **15 assets** (2000–2021), adapted from a larger Kaggle dataset.
- **Pre-processing**:
  - Kept **closing prices** (dropped open/high/volume, etc.).
  - **KNN imputation** for occasional missing values (mean of 5 nearest neighbours).
- If you’re reproducing from scratch, place cleaned price data under `data/` as a CSV where columns are tickers and rows are dates.

> _Note:_ The original Kaggle notebook used for prototyping is referenced in the report. You may bring your own dataset with similar structure if preferred.

---

## Optimisation Problems

Let:
- \(w \in \mathbb{R}^n\): portfolio weights (non-negative, sum to 1)
- \(r \in \mathbb{R}^n\): expected returns
- \(\Sigma \in \mathbb{R}^{n \times n}\): return covariance matrix

### (A) Maximise expected return (QCQP)

\[
\begin{aligned}
\max_{w}\quad & w^\top r \\
\text{s.t.}\quad & w \ge 0,\; \mathbf{1}^\top w = 1, \\
& w^\top \Sigma w \le \sigma^2_{\max}
\end{aligned}
\]

### (B) Minimise variance (QP)

\[
\begin{aligned}
\min_{w}\quad & w^\top \Sigma w \\
\text{s.t.}\quad & w \ge 0,\; \mathbf{1}^\top w = 1, \\
& w^\top r \ge r_{\min}
\end{aligned}
\]

---

## Environment & Installation

You can either use the repo’s `requirements.txt` (if present) or install the essentials directly:

```bash
# (optional) create a fresh environment
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

pip install numpy pandas cvxpy matplotlib jupyter
