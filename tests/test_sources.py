"""Parser tests on minimal payloads shaped like each API's response (no network)."""

from conftest import to_frame

from ai_competitiveness.sources import eurostat, oecd_msti, openalex
from ai_competitiveness.validate_data import validate


def test_openalex_eu27_filter_covers_27_member_states():
    assert len(set(openalex.EU27_CODES)) == 27
    assert "GB" not in openalex.EU27_CODES


def test_openalex_parse_and_rows():
    payload = {"group_by": [{"key": "2021", "count": 7}, {"key": "2020", "count": 5},
                            {"key": "2026", "count": 1}]}  # fmt: skip
    counts = openalex.parse_group_by(payload, 2020, 2025)
    assert counts == {2020: 5, 2021: 7}
    rows = openalex.to_rows("US", counts, "https://api.openalex.org/works", "2026-01-01")
    assert [r["status"] for r in rows] == ["observed", "provisional"]
    assert validate(to_frame(rows)) == []


def test_openalex_public_url_never_contains_api_key():
    url = openalex.get_public_url(openalex.params("CHN", 2015, 2025))
    assert "api_key" not in url and "country_code:CN" in url


def test_oecd_msti_parse_maps_geos_and_flags():
    text = (
        "DATAFLOW,REF_AREA,FREQ,MEASURE,UNIT_MEASURE,TIME_PERIOD,OBS_VALUE,OBS_STATUS,OBS_STATUS_2\n"
        "X,EU27_2020,A,G,PT_B1GQ,2020,2.1,E,\n"
        "X,USA,A,G,PT_B1GQ,2020,3.4,B,D\n"
        "X,CHN,A,G,PT_B1GQ,2020,2.4,A,\n"
        "X,OECD,A,G,PT_B1GQ,2020,2.7,A,\n"
    )
    rows = oecd_msti.parse_csv(text, "https://sdmx.oecd.org/x", "2026-01-01")
    by_geo = {r["geo"]: r for r in rows}
    assert set(by_geo) == {"EU27", "US", "CHN"}
    assert by_geo["EU27"]["status"] == "estimated"
    assert "break in series" in by_geo["US"]["methodology_note"]
    assert "definition differs" in by_geo["US"]["methodology_note"]
    assert by_geo["CHN"]["status"] == "observed"
    assert validate(to_frame(rows)) == []


def test_eurostat_parse_single_series():
    payload = {
        "id": ["geo", "time"],
        "size": [1, 2],
        "dimension": {"time": {"category": {"index": {"2023": 0, "2024": 1}}}},
        "value": {"1": 13.5, "0": 8.1},
        "status": {"1": "p"},
    }
    rows = eurostat.parse_jsonstat(payload, "https://ec.europa.eu/x", "2026-01-01")
    assert [(r["year"], r["value"], r["status"]) for r in rows] == [
        ("2023", "8.1", "observed"),
        ("2024", "13.5", "provisional"),
    ]
    assert validate(to_frame(rows)) == []
