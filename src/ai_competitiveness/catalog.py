"""Indicators the tracker publishes, and how each one may be compared."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Indicator:
    id: str
    name: str
    unit: str
    # "headline": supports the EU27 / US / CHN comparison.
    # "context": shown separately, never ranked against other geographies.
    scope: str
    # Why a geography has no comparable value, shown instead of a number.
    geo_notes: dict[str, str] = field(default_factory=dict)


INDICATORS = {
    i.id: i
    for i in (
        Indicator(
            id="ai_vc_deal_value_destination",
            name="AI VC investment received, by location of AI firm",
            unit="USD million",
            scope="headline",
        ),
        Indicator(
            id="ai_vc_deal_value_investor",
            name="AI VC investment made, by location of investor",
            unit="USD million",
            scope="headline",
        ),
        Indicator(
            id="ai_publications",
            name="AI research publications",
            unit="count",
            scope="headline",
        ),
        Indicator(
            id="gerd_pct_gdp",
            name="Gross domestic expenditure on R&D",
            unit="percent of GDP",
            scope="headline",
        ),
        Indicator(
            id="ai_enterprise_adoption",
            name="Enterprises using AI (10+ persons employed)",
            unit="percent of enterprises",
            scope="context",
            geo_notes={
                "US": "Not comparable: the Census BTOS survey uses a two-week reference "
                "period, a different AI definition and all firm sizes.",
                "CHN": "Not available: no comparable official series identified.",
            },
        ),
    )
}
