from conftest import fixture_row, to_frame

from ai_competitiveness.charts import _spread, generate
from ai_competitiveness.load_data import load_indicators
from ai_competitiveness.report import format_value, render


def dataset(tmp_path):
    """TEST FIXTURE: invented values covering every chart's indicator."""
    rows = []
    for geo in ("EU27", "US", "CHN"):
        for year in (2020, 2021):
            rows.append(fixture_row(geo=geo, year=str(year), value=str(year - 1900)))
            rows.append(
                fixture_row(
                    indicator_id="gerd_pct_gdp",
                    unit="percent of GDP",
                    geo=geo,
                    year=str(year),
                    value="2.5",
                    status="estimated",
                )
            )
        for indicator_id in ("ai_vc_deal_value_destination", "ai_vc_deal_value_investor"):
            rows.append(
                fixture_row(
                    indicator_id=indicator_id,
                    unit="USD million",
                    geo=geo,
                    year="2021",
                    value="1000",
                )
            )
    for year, value in (("2021", "7"), ("2023", "9")):
        rows.append(
            fixture_row(
                indicator_id="ai_enterprise_adoption",
                geo="EU27",
                year=year,
                unit="percent of enterprises",
                value=value,
            )
        )
    path = tmp_path / "indicators.csv"
    to_frame(rows).to_csv(path, index=False)
    return load_indicators(path)


def test_generate_writes_every_chart(tmp_path):
    paths = generate(dataset(tmp_path), tmp_path / "charts")
    assert [p.name for p in paths] == [
        "ai_vc_2025.png",
        "ai_publications.png",
        "gerd_pct_gdp.png",
        "ai_enterprise_adoption_eu27.png",
    ]
    assert all(p.stat().st_size > 10_000 for p in paths)


def test_charts_are_reproducible(tmp_path):
    df = dataset(tmp_path)
    first = [p.read_bytes() for p in generate(df, tmp_path / "a")]
    second = [p.read_bytes() for p in generate(df, tmp_path / "b")]
    assert first == second


def test_spread_keeps_labels_apart():
    placed = _spread({"EU27": 10.0, "US": 10.2, "CHN": 30.0}, min_gap=1.0)
    assert placed["US"] - placed["EU27"] >= 1.0
    assert placed["CHN"] == 30.0


def test_report_explains_missing_geographies(tmp_path):
    text = render(dataset(tmp_path))
    assert "Not comparable" in text and "Not available" in text
    assert "## Headline comparison" in text and "## Context" in text


def test_format_value():
    assert format_value(194000, "USD million") == "USD 194.0 bn"
    assert format_value(2.1287, "percent of GDP") == "2.13%"
    assert format_value(36760, "count") == "36,760"
