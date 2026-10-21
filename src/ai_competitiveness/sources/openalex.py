"""AI research publications from OpenAlex (CC0)."""

import os
from datetime import date

from ai_competitiveness.sources import get

API_URL = "https://api.openalex.org/works"
AI_SUBFIELD = "1702"  # Computer Science › Artificial Intelligence

# OpenAlex institution country codes (ISO 3166-1 alpha-2).
EU27_CODES = (
    "AT", "BE", "BG", "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "DE", "GR", "HU", "IE",
    "IT", "LV", "LT", "LU", "MT", "NL", "PL", "PT", "RO", "SK", "SI", "ES", "SE",
)  # fmt: skip
GEO_FILTERS = {"EU27": "|".join(EU27_CODES), "US": "US", "CHN": "CN"}

DEFINITION = (
    "Works whose OpenAlex primary topic is in subfield 1702 'Artificial Intelligence', "
    "with at least one author affiliated with an institution in the geography"
)
NOTE = (
    "Topic assigned by OpenAlex's classifier. Full counting across geographies (a work "
    "co-authored in EU27 and US counts for both); counted once within EU27. CHN = CN "
    "(excludes HK, MO, TW). Volume measure, not quality or capability."
)


def params(geo: str, start: int, end: int) -> dict[str, str]:
    return {
        "filter": (
            f"primary_topic.subfield.id:{AI_SUBFIELD},"
            f"publication_year:{start}-{end},"
            f"institutions.country_code:{GEO_FILTERS[geo]}"
        ),
        "group_by": "publication_year",
    }


def parse_group_by(payload: dict, start: int, end: int) -> dict[int, int]:
    """Map year → count; years absent from the response are omitted, not zeroed."""
    counts = {int(g["key"]): int(g["count"]) for g in payload["group_by"]}
    return {y: c for y, c in sorted(counts.items()) if start <= y <= end}


def to_rows(geo: str, counts: dict[int, int], url: str, retrieved: str) -> list[dict]:
    latest = max(counts) if counts else None
    return [
        {
            "indicator_id": "ai_publications",
            "indicator_name": "AI research publications",
            "geo": geo,
            "year": str(year),
            "value": str(count),
            "unit": "count",
            "source_name": "OpenAlex",
            "source_url": url,
            "retrieved_at": retrieved,
            "definition": DEFINITION,
            "methodology_note": NOTE
            + (
                " Latest year: indexing still catching up, expect upward revision."
                if year == latest
                else ""
            ),
            "status": "provisional" if year == latest else "observed",
            "license_note": "CC0 1.0 (OpenAlex)",
        }
        for year, count in counts.items()
    ]


def fetch(start: int = 2015, end: int = 2025) -> list[dict]:
    retrieved = date.today().isoformat()
    api_key = os.environ.get("OPENALEX_API_KEY")
    rows = []
    for geo in GEO_FILTERS:
        query = params(geo, start, end)
        response = get(API_URL, params={**query, **({"api_key": api_key} if api_key else {})})
        public_url = get_public_url(query)
        rows += to_rows(geo, parse_group_by(response.json(), start, end), public_url, retrieved)
    return rows


def get_public_url(query: dict[str, str]) -> str:
    """Query URL without the API key, safe to publish."""
    return f"{API_URL}?filter={query['filter']}&group_by={query['group_by']}"
