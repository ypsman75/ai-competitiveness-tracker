"""Shared test helpers.

TEST FIXTURE ONLY: the rows built here are invented to exercise validation logic.
They are never written to data/processed/.
"""

import io

import pandas as pd
import pytest

from ai_competitiveness.load_data import read_raw
from ai_competitiveness.schema import REQUIRED_COLUMNS


def fixture_row(**overrides) -> dict:
    row = {
        "indicator_id": "ai_publications",
        "indicator_name": "AI research publications",
        "geo": "US",
        "year": "2020",
        "value": "100",
        "unit": "count",
        "source_name": "TEST FIXTURE",
        "source_url": "https://example.org/test-fixture",
        "retrieved_at": "2026-01-01",
        "definition": "Test fixture, not real data",
        "methodology_note": "",
        "status": "observed",
        "license_note": "test fixture",
    }
    row.update(overrides)
    return row


def to_frame(rows: list[dict]) -> pd.DataFrame:
    """Round-trip through CSV so tests see exactly what the loader sees."""
    buffer = io.StringIO()
    pd.DataFrame(rows, columns=list(rows[0]) if rows else list(REQUIRED_COLUMNS)).to_csv(
        buffer, index=False
    )
    buffer.seek(0)
    return read_raw(buffer)


@pytest.fixture
def valid_rows() -> list[dict]:
    return [
        fixture_row(geo=geo, year=str(year), value=str(100 + year - 2020))
        for geo in ("EU27", "US", "CHN")
        for year in (2020, 2021)
    ]
