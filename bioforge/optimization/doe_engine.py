"""
BioForge DOE Engine
-------------------
Generates Box-Behnken Design (BBD) matrices for bioprocess optimization.
Validated against published citric acid study (Okedi et al., Industrial Crops
and Products, Impact Factor 6.2).
"""

import numpy as np
import pandas as pd
from itertools import combinations


class DOEEngine:
    """
    Design of Experiments matrix generator for bioprocess optimization.
    Supports Box-Behnken Design (BBD) for 3-factor systems.
    """

    def __init__(self, factors: dict):
        """
        Parameters
        ----------
        factors : dict
            Keys are factor names, values are (low, center, high) tuples.
            Example:
                {
                    'EDTA (g/l)':           (0.00, 0.15, 0.30),
                    'Coconut oil (%w/w)':   (0.00, 2.50, 5.00),
                    'Sodium fluoride (g/l)':(0.00, 0.05, 0.10),
                }
        """
        self.factors = factors
        self.factor_names = list(factors.keys())
        self.n_factors = len(factors)
        self.levels = {k: v for k, v in factors.items()}

    def generate_bbd(self, center_points: int = 5) -> pd.DataFrame:
        """
        Generate a Box-Behnken Design matrix.

        Parameters
        ----------
        center_points : int
            Number of center point replications (default 5, matching published study).

        Returns
        -------
        pd.DataFrame
            Full BBD matrix with actual (decoded) factor values.
        """
        n = self.n_factors
        # BBD edge midpoints: all pairs of factors varied, third at center
        pairs = list(combinations(range(n), 2))
        coded_rows = []

        for i, j in pairs:
            for xi in [-1, 1]:
                for xj in [-1, 1]:
                    row = [0] * n
                    row[i] = xi
                    row[j] = xj
                    coded_rows.append(row)

        # Add center points
        for _ in range(center_points):
            coded_rows.append([0] * n)

        coded = np.array(coded_rows)

        # Decode to actual values
        decoded = np.zeros_like(coded, dtype=float)
        for col_idx, fname in enumerate(self.factor_names):
            lo, mid, hi = self.levels[fname]
            decoded[:, col_idx] = np.where(
                coded[:, col_idx] == -1, lo,
                np.where(coded[:, col_idx] == 1, hi, mid)
            )

        df = pd.DataFrame(decoded, columns=self.factor_names)
        df.insert(0, 'Run', range(1, len(df) + 1))
        df['Coded_' + self.factor_names[0]] = coded[:, 0]
        df['Coded_' + self.factor_names[1]] = coded[:, 1]
        df['Coded_' + self.factor_names[2]] = coded[:, 2]
        return df

    def decode(self, coded_value: float, factor_name: str) -> float:
        """Convert a coded level (-1, 0, +1) to actual value."""
        lo, mid, hi = self.levels[factor_name]
        if coded_value == -1:
            return lo
        elif coded_value == 1:
            return hi
        return mid
