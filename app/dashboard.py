"""EU27 · US · China AI competitiveness dashboard: ``streamlit run app/dashboard.py``.

Reads only the local processed dataset; makes no network calls at runtime.
"""

import os

import altair as alt
import pandas as pd
import streamlit as st

from ai_competitiveness import GEOS
from ai_competitiveness.catalog import INDICATORS
from ai_competitiveness.charts import GEO_COLORS, GEO_LABELS, SURFACE, UNCERTAIN
from ai_competitiveness.load_data import load_indicators
from ai_competitiveness.report import format_value, latest_table
from ai_competitiveness.schema import PROCESSED_PATH

st.set_page_config(page_title="AI Competitiveness Tracker", layout="wide")


@st.cache_data
def data() -> pd.DataFrame:
    return load_indicators(PROCESSED_PATH)


def geo_scale() -> alt.Scale:
    return alt.Scale(domain=[GEO_LABELS[g] for g in GEOS], range=[GEO_COLORS[g] for g in GEOS])


def chart(rows: pd.DataFrame, unit: str) -> alt.Chart:
    rows = rows.assign(
        Geography=rows["geo"].map(GEO_LABELS),
        uncertain=rows["status"].isin(UNCERTAIN),
        Value=rows["value"].map(lambda v: format_value(v, unit)),
    )
    color = alt.Color("Geography:N", scale=geo_scale(), legend=alt.Legend(orient="top"))
    tooltip = ["Geography:N", "year:O", "Value:N", "status:N"]
    if rows["year"].nunique() == 1:
        return (
            alt.Chart(rows)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("value:Q", title=unit),
                y=alt.Y("Geography:N", sort=[GEO_LABELS[g] for g in GEOS], title=None),
                color=color,
                tooltip=tooltip,
            )
            .properties(height=alt.Step(56))
        )
    base = alt.Chart(rows).encode(
        x=alt.X("year:Q", title=None, axis=alt.Axis(format="d", tickMinStep=1)),
        y=alt.Y("value:Q", title=unit, scale=alt.Scale(zero=True)),
    )
    lines = base.mark_line(strokeWidth=2).encode(color=color)
    points = base.mark_point(size=60, strokeWidth=2, filled=True, opacity=1).encode(
        stroke=alt.Stroke("Geography:N", scale=geo_scale(), legend=None),
        fill=alt.condition(
            "datum.uncertain",
            alt.value(SURFACE),
            alt.Fill("Geography:N", scale=geo_scale(), legend=None),
        ),
        tooltip=tooltip,
    )
    return (lines + points).properties(height=380)


def latest_cards(df: pd.DataFrame, indicator) -> None:
    rows = df[df["indicator_id"] == indicator.id].dropna(subset=["value"])
    for col, geo in zip(st.columns(len(GEOS)), GEOS, strict=True):
        geo_rows = rows[rows["geo"] == geo].sort_values("year")
        with col:
            if geo_rows.empty:
                st.metric(GEO_LABELS[geo], "—")
                st.caption(indicator.geo_notes.get(geo, "Not available."))
                continue
            last = geo_rows.iloc[-1]
            st.metric(
                GEO_LABELS[geo],
                format_value(last["value"], indicator.unit),
                help=f"{last['year']} · {last['status']}",
            )
            st.caption(f"{last['year']} · {last['status'].replace('_', ' ')}")


def metadata(rows: pd.DataFrame) -> None:
    first = rows.iloc[0]
    st.markdown(f"**Definition.** {first['definition']}")
    st.markdown(f"**Unit.** {first['unit']}")
    for (name, url), group in rows.groupby(["source_name", "source_url"]):
        st.markdown(f"**Source.** [{name}]({url}) · retrieved {group['retrieved_at'].max()}")
    st.markdown(f"**Licence.** {first['license_note']}")
    st.markdown("**Methodology notes.**")
    common, per_geo = split_notes(rows)
    if common:
        st.markdown(common)
    for geo, rest in per_geo.items():
        st.markdown(f"- *{GEO_LABELS[geo]}:* {rest}")


def split_notes(rows: pd.DataFrame) -> tuple[str, dict[str, str]]:
    """Show the text shared by every note once, then only what differs per geography."""
    notes = [n for n in rows["methodology_note"] if n]
    if not notes:
        return "", {}
    prefix = os.path.commonprefix(notes)
    prefix = prefix[: prefix.rfind(". ") + 1] if len(set(notes)) > 1 else prefix
    per_geo = {}
    for geo, group in rows.groupby("geo", sort=False):
        rests = sorted({n[len(prefix) :].strip() for n in group["methodology_note"] if n} - {""})
        if rests:
            per_geo[geo] = " ".join(rests)
    return prefix.strip(), {g: per_geo[g] for g in GEOS if g in per_geo}


df = data()

st.title("EU vs US vs China: AI Competitiveness Tracker")
st.caption(
    "Three AI ecosystems. One transparent comparison. Every value is sourced; missing "
    "or non-comparable data is labelled, never filled. No composite score."
)

headline = [i for i in INDICATORS.values() if i.scope == "headline"]
context = [i for i in INDICATORS.values() if i.scope == "context"]
choice_id = st.sidebar.radio(
    "Metric",
    [i.id for i in headline + context],
    format_func=lambda i: (
        INDICATORS[i].name + ("" if INDICATORS[i].scope == "headline" else " (context)")
    ),
)
choice = INDICATORS[choice_id]
st.sidebar.caption(
    "Headline metrics support an EU27 / US / China comparison. Context metrics do not."
)
st.sidebar.caption(f"Data: `{PROCESSED_PATH.relative_to(PROCESSED_PATH.parents[2])}`")

rows = df[df["indicator_id"] == choice.id].sort_values(["geo", "year"])
st.header(choice.name)
if choice.scope == "context":
    st.warning("Context only — not comparable across all three geographies.")
if rows["year"].nunique() == 1:
    st.info(
        f"Single year ({rows['year'].iloc[0]}): a snapshot, not a trend. Annual totals "
        "can be dominated by a few very large deals."
    )

latest_cards(df, choice)
st.altair_chart(chart(rows, choice.unit), use_container_width=True)
if rows["year"].nunique() > 1:
    st.caption("Hollow points: estimated or provisional values. Hover for details.")

with st.expander("Definition, source and caveats", expanded=True):
    metadata(rows)

with st.expander("Data table"):
    st.dataframe(
        rows[["geo", "year", "value", "unit", "status", "methodology_note"]],
        hide_index=True,
        use_container_width=True,
    )

st.divider()
st.subheader("Latest observations, all metrics")
order = {i.name: n for n, i in enumerate(headline + context)}
st.dataframe(
    latest_table(df).sort_values("Metric", key=lambda s: s.map(order), kind="stable"),
    hide_index=True,
    use_container_width=True,
)
st.download_button(
    "Download processed dataset (CSV)",
    PROCESSED_PATH.read_bytes(),
    file_name="indicators.csv",
    mime="text/csv",
)
