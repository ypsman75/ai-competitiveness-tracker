"""Write the latest-observations summary: ``python -m ai_competitiveness.report``."""

import argparse
from pathlib import Path

import pandas as pd

from ai_competitiveness.catalog import INDICATORS
from ai_competitiveness.charts import GEO_LABELS
from ai_competitiveness.load_data import load_indicators
from ai_competitiveness.schema import REPO_ROOT
from ai_competitiveness.transform_data import latest_observations

REPORT_PATH = REPO_ROOT / "outputs" / "summary.md"


def format_value(value: float, unit: str) -> str:
    if pd.isna(value):
        return ""
    if unit == "count":
        return f"{value:,.0f}"
    if unit == "USD million":
        return f"USD {value / 1000:,.1f} bn"
    return f"{value:.2f}%" if unit.startswith("percent") else f"{value:,}"


def latest_table(df: pd.DataFrame) -> pd.DataFrame:
    """Metric × geography table; missing geographies say why instead of being blank."""
    rows = []
    for _, r in latest_observations(df).iterrows():
        indicator = INDICATORS[r["indicator_id"]]
        missing = pd.isna(r["value"])
        rows.append({
            "Metric": indicator.name,
            "Scope": indicator.scope,
            "Geography": GEO_LABELS[r["geo"]],
            "Year": "" if missing else str(int(r["year"])),
            "Value": indicator.geo_notes.get(r["geo"], "not available") if missing
            else format_value(r["value"], indicator.unit),
            "Status": "" if missing else r["status"],
            "Source": "" if missing else r["source_name"],
        })  # fmt: skip
    return pd.DataFrame(rows)


def to_markdown(table: pd.DataFrame) -> str:
    cols = list(table.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    lines += ["| " + " | ".join(str(v) for v in row) + " |" for row in table.itertuples(False)]
    return "\n".join(lines)


def render(df: pd.DataFrame) -> str:
    table = latest_table(df)
    headline = table[table["Scope"] == "headline"].drop(columns="Scope")
    context = table[table["Scope"] == "context"].drop(columns="Scope")
    retrieved = max(df["retrieved_at"])
    return f"""# Latest observations

Generated from `data/processed/indicators.csv` (latest retrieval {retrieved}).
Each value is the most recent non-missing year per geography; years differ by source.
See `docs/data_sources.md` for definitions and caveats. No composite score is computed.

## Headline comparison (EU27 · United States · China)

{to_markdown(headline)}

## Context (not comparable across all three)

{to_markdown(context)}
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write the latest-observations summary.")
    parser.add_argument("--out", default=str(REPORT_PATH))
    args = parser.parse_args(argv)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(load_indicators()))
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
