"""Canonical schema for ``data/processed/indicators.csv`` (spec §8)."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_PATH = REPO_ROOT / "data" / "processed" / "indicators.csv"
MANUAL_DIR = REPO_ROOT / "data" / "manual"

REQUIRED_COLUMNS = (
    "indicator_id",
    "indicator_name",
    "geo",
    "year",
    "value",
    "unit",
    "source_name",
    "source_url",
    "retrieved_at",
    "definition",
    "methodology_note",
    "status",
    "license_note",
)
OPTIONAL_COLUMNS = ("currency_basis", "price_basis")

# Columns that may be empty in a row. An empty ``value`` means missing, never zero.
NULLABLE_COLUMNS = frozenset({"value", "methodology_note", "currency_basis", "price_basis"})

STATUSES = ("observed", "estimated", "provisional", "manually_transcribed")

KEY = ("indicator_id", "geo", "year")
