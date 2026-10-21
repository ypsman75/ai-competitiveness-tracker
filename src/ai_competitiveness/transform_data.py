"""Reshape loaded observations for charts and tables."""

import pandas as pd

from ai_competitiveness import GEOS


def series(df: pd.DataFrame, indicator_id: str) -> pd.DataFrame:
    """Year × geography table for one indicator; every geography is a column, gaps are NaN."""
    subset = df[df["indicator_id"] == indicator_id]
    table = subset.pivot(index="year", columns="geo", values="value")
    return table.reindex(columns=list(GEOS)).sort_index()


def latest_observations(df: pd.DataFrame) -> pd.DataFrame:
    """Latest non-missing observation per indicator and geography.

    Every indicator gets one row per geography; a geography without data gets a row
    with NaN ``value`` and ``year`` rather than disappearing.
    """
    present = df.dropna(subset=["value"]).sort_values("year")
    latest = present.groupby(["indicator_id", "geo"]).tail(1)
    grid = pd.MultiIndex.from_product(
        [sorted(df["indicator_id"].unique()), list(GEOS)], names=["indicator_id", "geo"]
    ).to_frame(index=False)
    return grid.merge(latest, on=["indicator_id", "geo"], how="left")
