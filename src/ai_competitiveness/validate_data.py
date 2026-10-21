"""Validate the processed dataset: ``python -m ai_competitiveness.validate_data``."""

import argparse
import math
import sys
from datetime import date

import pandas as pd

from ai_competitiveness import GEOS
from ai_competitiveness.catalog import INDICATORS
from ai_competitiveness.load_data import read_raw
from ai_competitiveness.schema import (
    KEY,
    NULLABLE_COLUMNS,
    OPTIONAL_COLUMNS,
    PROCESSED_PATH,
    REQUIRED_COLUMNS,
    STATUSES,
)

MIN_YEAR = 1990


def _check_row(row: pd.Series) -> list[str]:
    problems = []
    for col in REQUIRED_COLUMNS:
        if col not in NULLABLE_COLUMNS and not str(row[col]).strip():
            problems.append(f"empty required field '{col}'")

    if row["geo"] and row["geo"] not in GEOS:
        problems.append(f"geo '{row['geo']}' not in {GEOS}")
    if row["status"] and row["status"] not in STATUSES:
        problems.append(f"status '{row['status']}' not in {STATUSES}")

    try:
        year = int(row["year"])
        if not MIN_YEAR <= year <= date.today().year:
            problems.append(f"year {year} outside {MIN_YEAR}..{date.today().year}")
    except ValueError:
        problems.append(f"year '{row['year']}' is not an integer")

    if row["retrieved_at"]:
        try:
            if date.fromisoformat(row["retrieved_at"]) > date.today():
                problems.append(f"retrieved_at {row['retrieved_at']} is in the future")
        except ValueError:
            problems.append(f"retrieved_at '{row['retrieved_at']}' is not an ISO date")

    if row["source_url"] and not row["source_url"].startswith("https://"):
        problems.append("source_url must start with https://")

    if row["status"] == "manually_transcribed" and not row["methodology_note"].strip():
        problems.append("manually_transcribed rows need a methodology_note with the reference")

    indicator = INDICATORS.get(row["indicator_id"])
    if row["indicator_id"] and indicator is None:
        problems.append(f"unknown indicator_id '{row['indicator_id']}' (see catalog.py)")
    elif indicator and row["unit"] and row["unit"] != indicator.unit:
        problems.append(f"unit '{row['unit']}' differs from catalog unit '{indicator.unit}'")

    if row["value"] != "":
        try:
            value = float(row["value"])
        except ValueError:
            problems.append(f"value '{row['value']}' is not numeric")
        else:
            if not math.isfinite(value):
                problems.append(f"value '{row['value']}' is not finite")
            elif value < 0:
                problems.append(f"value {value} is negative")
            elif row["unit"].startswith("percent") and value > 100:
                problems.append(f"percentage {value} exceeds 100")
            elif row["unit"] == "count" and not value.is_integer():
                problems.append(f"count {value} is not a whole number")
    return problems


def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of human-readable problems; an empty list means valid."""
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        return [f"missing required column(s): {', '.join(missing)}"]

    errors = []
    unknown = sorted(set(df.columns) - set(REQUIRED_COLUMNS) - set(OPTIONAL_COLUMNS))
    if unknown:
        errors.append(f"unknown column(s): {', '.join(unknown)}")
    if df.empty:
        return errors + ["dataset has no rows"]

    df = df.fillna("").astype(str)
    for pos, (_, row) in enumerate(df.iterrows()):
        # +2: one for the header line, one because CSV lines count from 1
        errors += [f"line {pos + 2}: {p}" for p in _check_row(row)]

    dupes = df[df.duplicated(list(KEY), keep=False)]
    for key, group in dupes.groupby(list(KEY)):
        lines = ", ".join(str(df.index.get_loc(i) + 2) for i in group.index)
        errors.append(f"duplicate key {dict(zip(KEY, key, strict=True))} on lines {lines}")

    for indicator_id, units in df.groupby("indicator_id")["unit"].unique().items():
        if len(units) > 1:
            errors.append(f"indicator '{indicator_id}' mixes units: {sorted(units)}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the processed indicator dataset.")
    parser.add_argument("path", nargs="?", default=str(PROCESSED_PATH))
    args = parser.parse_args(argv)
    try:
        df = read_raw(args.path)
    except FileNotFoundError:
        print(f"ERROR: {args.path} not found", file=sys.stderr)
        return 1
    errors = validate(df)
    if errors:
        print(f"INVALID: {args.path} — {len(errors)} problem(s)", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print(f"OK: {args.path} — {len(df)} rows, {df['indicator_id'].nunique()} indicators")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
