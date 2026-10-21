import pytest
from conftest import fixture_row, to_frame

from ai_competitiveness.load_data import load_indicators
from ai_competitiveness.schema import PROCESSED_PATH
from ai_competitiveness.validate_data import main, validate


def errors_for(rows):
    return validate(to_frame(rows))


def test_valid_fixture_passes(valid_rows):
    assert errors_for(valid_rows) == []


def test_missing_column_is_reported(valid_rows):
    df = to_frame(valid_rows).drop(columns=["source_url"])
    assert validate(df) == ["missing required column(s): source_url"]


def test_unknown_column_is_reported(valid_rows):
    df = to_frame(valid_rows).assign(extra="x")
    assert any("unknown column(s): extra" in e for e in validate(df))


def test_empty_dataset_is_rejected():
    assert "dataset has no rows" in validate(to_frame([fixture_row()]).iloc[0:0])


@pytest.mark.parametrize("geo", ["EU", "Europe", "UK", "CN", ""])
def test_invalid_geo_is_rejected(geo):
    errors = errors_for([fixture_row(geo=geo)])
    assert errors and all(e.startswith("line 2:") for e in errors)


def test_duplicate_key_is_rejected(valid_rows):
    errors = errors_for(valid_rows + [fixture_row(geo="US", year="2020", value="999")])
    assert any(e.startswith("duplicate key") for e in errors)


def test_missing_value_is_allowed_and_stays_missing(valid_rows, tmp_path):
    rows = valid_rows + [fixture_row(geo="CHN", year="2022", value="")]
    assert errors_for(rows) == []
    path = tmp_path / "indicators.csv"
    to_frame(rows).to_csv(path, index=False)
    df = load_indicators(path)
    missing = df[(df["geo"] == "CHN") & (df["year"] == 2022)]["value"]
    assert missing.isna().all()  # never coerced to zero


@pytest.mark.parametrize(
    ("overrides", "fragment"),
    [
        ({"value": "abc"}, "not numeric"),
        ({"value": "-1"}, "negative"),
        ({"value": "1.5"}, "not a whole number"),
        ({"year": "20x0"}, "not an integer"),
        ({"year": "1900"}, "outside"),
        ({"status": "guessed"}, "status 'guessed'"),
        ({"retrieved_at": "2999-01-01"}, "in the future"),
        ({"retrieved_at": "01/02/2026"}, "not an ISO date"),
        ({"source_url": "http://example.org"}, "https://"),
        ({"source_name": ""}, "empty required field 'source_name'"),
        ({"license_note": ""}, "empty required field 'license_note'"),
        ({"indicator_id": "made_up"}, "unknown indicator_id"),
        ({"unit": "USD million"}, "differs from catalog unit"),
        ({"status": "manually_transcribed"}, "need a methodology_note"),
    ],
)
def test_row_rules(overrides, fragment):
    errors = errors_for([fixture_row(**overrides)])
    assert any(fragment in e for e in errors), errors


def test_percentage_above_100_is_rejected():
    row = fixture_row(indicator_id="gerd_pct_gdp", unit="percent of GDP", value="101")
    assert any("exceeds 100" in e for e in errors_for([row]))


def test_mixed_units_within_indicator_are_rejected():
    rows = [fixture_row(year="2020"), fixture_row(year="2021", unit="thousands")]
    assert any("mixes units" in e for e in errors_for(rows))


def test_cli_exit_codes(valid_rows, tmp_path, capsys):
    good, bad = tmp_path / "good.csv", tmp_path / "bad.csv"
    to_frame(valid_rows).to_csv(good, index=False)
    to_frame([fixture_row(geo="EU")]).to_csv(bad, index=False)
    assert main([str(good)]) == 0
    assert main([str(bad)]) == 1
    assert main([str(tmp_path / "absent.csv")]) == 1
    assert "INVALID" in capsys.readouterr().err


def test_processed_dataset_is_valid():
    if not PROCESSED_PATH.exists():
        pytest.skip("processed dataset not built yet")
    load_indicators(PROCESSED_PATH)  # raises on any validation error
