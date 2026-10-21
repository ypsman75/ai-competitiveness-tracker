import math

from conftest import fixture_row, to_frame

from ai_competitiveness.load_data import load_indicators
from ai_competitiveness.transform_data import latest_observations, series


def loaded(rows, tmp_path):
    path = tmp_path / "indicators.csv"
    to_frame(rows).to_csv(path, index=False)
    return load_indicators(path)


def test_series_has_every_geo_column_even_when_one_is_absent(tmp_path):
    rows = [fixture_row(geo="US", year="2020"), fixture_row(geo="EU27", year="2021")]
    table = series(loaded(rows, tmp_path), "ai_publications")
    assert list(table.columns) == ["EU27", "US", "CHN"]
    assert table["CHN"].isna().all()
    assert list(table.index) == [2020, 2021]


def test_latest_observation_skips_missing_latest_year(tmp_path):
    rows = [
        fixture_row(geo="US", year="2020", value="10"),
        fixture_row(geo="US", year="2021", value=""),
    ]
    latest = latest_observations(loaded(rows, tmp_path)).set_index("geo")
    assert latest.loc["US", "year"] == 2020
    assert latest.loc["US", "value"] == 10


def test_latest_observations_keeps_a_row_for_geos_without_data(tmp_path):
    rows = [fixture_row(geo="US", year="2020")]
    latest = latest_observations(loaded(rows, tmp_path))
    assert sorted(latest["geo"]) == ["CHN", "EU27", "US"]
    chn = latest[latest["geo"] == "CHN"].iloc[0]
    assert math.isnan(chn["value"])
