"""Rebuild ``data/processed/indicators.csv``: ``python -m ai_competitiveness.build_data``.

Fetches the scripted sources (network required), adds the manually transcribed files in
``data/manual/``, validates the result, and writes it only if validation passes.
"""

import argparse
import sys

import pandas as pd

from ai_competitiveness.load_data import read_raw
from ai_competitiveness.schema import (
    KEY,
    MANUAL_DIR,
    OPTIONAL_COLUMNS,
    PROCESSED_PATH,
    REQUIRED_COLUMNS,
)
from ai_competitiveness.sources import eurostat, oecd_msti, openalex
from ai_competitiveness.validate_data import validate

FETCHERS = {
    "openalex": openalex.fetch,
    "oecd_msti": oecd_msti.fetch,
    "eurostat": eurostat.fetch,
}


def build() -> pd.DataFrame:
    frames = []
    for name, fetch in FETCHERS.items():
        rows = fetch()
        print(f"  {name}: {len(rows)} rows")
        frames.append(pd.DataFrame(rows, dtype=str))
    for path in sorted(MANUAL_DIR.glob("*.csv")):
        manual = read_raw(path)
        print(f"  manual/{path.name}: {len(manual)} rows")
        frames.append(manual)
    df = pd.concat(frames, ignore_index=True).fillna("")
    df = df.reindex(columns=list(REQUIRED_COLUMNS) + list(OPTIONAL_COLUMNS), fill_value="")
    df["_year"] = df["year"].astype(int)
    df = df.sort_values(["indicator_id", "geo", "_year"]).drop(columns="_year")
    return df.reset_index(drop=True)


def diff_summary(old: pd.DataFrame, new: pd.DataFrame) -> str:
    def keyed(df):
        return {tuple(r[k] for k in KEY): r["value"] for _, r in df.iterrows()}

    before, after = keyed(old), keyed(new)
    added = len(after.keys() - before.keys())
    removed = len(before.keys() - after.keys())
    changed = sum(1 for k in after.keys() & before.keys() if after[k] != before[k])
    return f"{added} added, {removed} removed, {changed} values changed"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch sources and rebuild the dataset.")
    parser.add_argument("--dry-run", action="store_true", help="validate and diff, don't write")
    parser.add_argument("--out", default=str(PROCESSED_PATH))
    args = parser.parse_args(argv)

    print("Fetching sources:")
    df = build()
    errors = validate(df)
    if errors:
        print(f"INVALID — not writing ({len(errors)} problem(s)):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    try:
        summary = diff_summary(read_raw(args.out), df)
    except FileNotFoundError:
        summary = "new file"
    print(f"Valid: {len(df)} rows ({summary})")
    if args.dry_run:
        print("Dry run: nothing written.")
        return 0
    df.to_csv(args.out, index=False)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
