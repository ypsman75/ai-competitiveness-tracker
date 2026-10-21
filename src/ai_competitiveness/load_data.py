"""Read the processed indicator dataset."""

from pathlib import Path

import pandas as pd

from ai_competitiveness.schema import PROCESSED_PATH


def read_raw(path: Path | str = PROCESSED_PATH) -> pd.DataFrame:
    """Read the CSV with every cell as text, so nothing is coerced or filled."""
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def load_indicators(path: Path | str = PROCESSED_PATH, validate: bool = True) -> pd.DataFrame:
    """Load observations with typed ``year`` and ``value``; empty values stay NaN."""
    df = read_raw(path)
    if validate:
        from ai_competitiveness.validate_data import validate as run_validation

        errors = run_validation(df)
        if errors:
            raise ValueError(f"{path} failed validation:\n  " + "\n  ".join(errors))
    df["year"] = df["year"].astype(int)
    df["value"] = pd.to_numeric(df["value"].where(df["value"] != ""))
    return df
