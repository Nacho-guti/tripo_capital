from pathlib import Path
from typing import List, Dict, Optional

import numpy as np
import pandas as pd
from scipy.optimize import minimize


class PortfolioOptimiser:
    """
    Encapsulates portfolio data and optimization logic.
    """
    def __init__(self, price_df: pd.DataFrame, risk_free_rate: float = 0.039):
        # Preprocess and cache
        self.price_df = price_df.copy()
        self.price_df.columns = self.price_df.columns.str.strip()
        self.risk_free_rate = risk_free_rate

        # Compute log returns once
        self.returns = np.log(self.price_df / self.price_df.shift(1)).dropna()
        self.mean_returns = self.returns.mean() * 252
        self.cov_matrix = self.returns.cov() * 252
        self.n = len(self.price_df.columns)

    def _portfolio_performance(self, weights: np.ndarray) -> Dict[str, float]:
        # Vectorized performance calc
        port_return = weights.dot(self.mean_returns)
        port_vol = np.sqrt(weights @ self.cov_matrix.values @ weights)
        sharpe = (port_return - self.risk_free_rate) / port_vol
        return {"return": port_return, "volatility": port_vol, "sharpe": sharpe}

    def optimise(
        self,
        asset_limits: Dict[str, float],
        asset_indices: Dict[str, List[int]],
        per_asset_cap: float = 0.20,
        bounds: Optional[List[tuple]] = None,
    ) -> np.ndarray:
        """
        Finds weights maximizing Sharpe ratio under group and per-asset caps.
        """
        if bounds is None:
            bounds = [(0.0, per_asset_cap)] * self.n

        # Constraint: weights sum to 1
        constraints = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
        # Group constraints
        for cls, limit in asset_limits.items():
            idx = asset_indices.get(cls, [])
            constraints.append({
                "type": "ineq",
                "fun": lambda w, idx=idx, lim=limit: lim - w[idx].sum()
            })

        # Initial equal allocation
        x0 = np.ones(self.n) / self.n

        # Single minimize call with vectorized objective
        result = minimize(
            fun=lambda w: -self._portfolio_performance(w)["sharpe"],
            x0=x0,
            bounds=bounds,
            constraints=constraints,
            method="SLSQP",
            options={"disp": False}
        )

        if not result.success:
            raise RuntimeError(f"Optimization failed: {result.message}")

        return result.x

    @staticmethod
    def list_excel_paths(root: Path, skip_dirs: List[str]) -> List[Path]:
        skip = set(skip_dirs)
        # Single-pass file discovery
        return [p for p in root.rglob("*.xlsx") if not skip.intersection(p.parts)]

    @staticmethod
    def tickers_by_asset(root: Path, skip_dirs: List[str]) -> Dict[str, List[str]]:
        by_asset: Dict[str, List[str]] = {}
        for p in PortfolioOptimiser.list_excel_paths(root, skip_dirs):
            cls = p.relative_to(root).parts[0]
            try:
                df = pd.read_excel(p, usecols=["Ticker"])
                ticker = df["Ticker"].iat[0]
            except Exception:
                ticker = p.stem
            by_asset.setdefault(cls, []).append(str(ticker).strip())
        return by_asset


if __name__ == "__main__":
    # Load price data
    prices = pd.read_excel('portfolio-optimization/data/processed/etf_combined.xlsx', index_col="Date", parse_dates=True)

    # Initialise optimiser
    opt = PortfolioOptimiser(prices, risk_free_rate=0.039)

    # Discover tickers by asset class
    root = Path("../raw")
    skip = ["cash", "risk_free", "benchmarks", "retired"]
    by_asset = opt.tickers_by_asset(root, skip)
    asset_indices = {
        cls: [prices.columns.get_loc(t) for t in ticks if t in prices.columns]
        for cls, ticks in by_asset.items()
    }

    # Define limits
    asset_limits = {"equities": 0.40, "bonds": 0.35, "alternatives": 0.25}
    per_asset_cap = 0.15

    # Optimize
    weights = opt.optimise(asset_limits, asset_indices, per_asset_cap)

    # Output results
    perf = opt._portfolio_performance(weights)
    for ticker, w in zip(prices.columns, weights):
        print(f"{ticker}: {w:.2%}")
    print(f"Return: {perf['return']:.2%}, Volatility: {perf['volatility']:.2%}, Sharpe: {perf['sharpe']:.2f}")
