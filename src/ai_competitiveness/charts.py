"""Regenerate static charts: ``python -m ai_competitiveness.charts``."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402

from ai_competitiveness import GEOS  # noqa: E402
from ai_competitiveness.catalog import INDICATORS  # noqa: E402
from ai_competitiveness.load_data import load_indicators  # noqa: E402
from ai_competitiveness.schema import REPO_ROOT  # noqa: E402
from ai_competitiveness.transform_data import series  # noqa: E402

CHARTS_DIR = REPO_ROOT / "outputs" / "charts"

# Colour follows the geography in every chart (validated categorical slots 1-3).
GEO_COLORS = {"EU27": "#2a78d6", "US": "#eb6834", "CHN": "#1baf7a"}
GEO_LABELS = {"EU27": "EU27", "US": "United States", "CHN": "China"}
SURFACE, INK, INK_2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, BASELINE = "#e1e0d9", "#c3c2b7"
UNCERTAIN = {"estimated", "provisional"}

plt.rcParams.update({
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "font.size": 10,
    "axes.edgecolor": BASELINE,
    "axes.labelcolor": INK_2,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.spines.top": False,
    "axes.spines.right": False,
})  # fmt: skip


def _figure(title: str, subtitle: str, ncols: int = 1):
    fig, axes = plt.subplots(1, ncols, figsize=(9, 5.2), squeeze=False)
    fig.subplots_adjust(top=0.80, bottom=0.20, left=0.08, right=0.84, wspace=0.35)
    fig.text(0.08, 0.94, title, fontsize=14, fontweight="bold", color=INK)
    fig.text(0.08, 0.885, subtitle, fontsize=10, color=INK_2)
    return fig, list(axes[0])


def _footer(fig, df: pd.DataFrame, note: str) -> None:
    sources = sorted(set(df["source_name"]))
    retrieved = max(df["retrieved_at"])
    text = f"Source: {'; '.join(sources)}. Retrieved {retrieved}.\n{note}"
    fig.text(0.08, 0.03, text, fontsize=8, color=MUTED, va="bottom", wrap=True)


def _grid(ax, axis: str = "y") -> None:
    ax.grid(axis=axis, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def _spread(values: dict[str, float], min_gap: float) -> dict[str, float]:
    """Nudge end-label positions apart so labels never overlap."""
    placed: dict[str, float] = {}
    for geo, y in sorted(values.items(), key=lambda kv: kv[1]):
        floor = max(placed.values(), default=y - min_gap) + min_gap
        placed[geo] = max(y, floor)
    return placed


def line_chart(df, indicator_id, title, subtitle, note, fmt, tick_fmt, out: Path) -> Path:
    data = df[df["indicator_id"] == indicator_id]
    table = series(data, indicator_id)
    status = data.pivot(index="year", columns="geo", values="status")
    fig, (ax,) = _figure(title, subtitle)
    ends = {}
    for geo in GEOS:
        col = table[geo].dropna()
        if col.empty:
            continue
        color = GEO_COLORS[geo]
        ax.plot(col.index, col.values, color=color, linewidth=2, label=GEO_LABELS[geo])
        uncertain = status[geo].reindex(col.index).isin(UNCERTAIN)
        ax.scatter(
            col.index[~uncertain],
            col[~uncertain],
            s=36,
            color=color,
            edgecolor=SURFACE,
            linewidth=2,
            zorder=3,
        )
        ax.scatter(col.index[uncertain], col[uncertain], s=36, facecolor=SURFACE,
                   edgecolor=color, linewidth=2, zorder=3)  # fmt: skip
        ends[geo] = (col.index[-1], col.iloc[-1])
    lo, hi = ax.get_ylim()
    ax.set_ylim(min(0, lo), hi * 1.05)
    span = ax.get_ylim()[1] - ax.get_ylim()[0]
    label_y = _spread({g: v for g, (_, v) in ends.items()}, span * 0.06)
    for geo, (x, v) in ends.items():
        ax.annotate(f"{GEO_LABELS[geo]}  {fmt(v)}", xy=(x, v), xytext=(x + 0.4, label_y[geo]),
                    va="center", fontsize=9, color=INK, annotation_clip=False)  # fmt: skip
    ax.legend(loc="upper left", frameon=False, labelcolor=INK_2, fontsize=9)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: tick_fmt(v)))
    ax.set_xticks(table.index[:: max(1, len(table.index) // 8)])
    _grid(ax)
    _footer(fig, data, note + " Hollow markers: estimated or provisional values.")
    fig.savefig(out, dpi=150, metadata={"Software": None})
    plt.close(fig)
    return out


def vc_chart(df: pd.DataFrame, out: Path) -> Path:
    panels = (
        ("ai_vc_deal_value_destination", "Received by AI firms located in…"),
        ("ai_vc_deal_value_investor", "Invested by VC investors located in…"),
    )
    data = df[df["indicator_id"].isin([p[0] for p in panels])]
    year = int(data["year"].max())
    fig, axes = _figure(
        f"AI venture capital, {year}",
        "USD billion · single year, manually transcribed · same scale in both panels",
        ncols=2,
    )
    fig.subplots_adjust(left=0.15, right=0.95)
    vmax = data["value"].max() / 1000
    order = list(reversed(GEOS))  # EU27 on top
    for ax, (indicator_id, heading) in zip(axes, panels, strict=True):
        rows = data[data["indicator_id"] == indicator_id].set_index("geo")
        values = [rows["value"].get(g, float("nan")) / 1000 for g in order]
        ax.barh([GEO_LABELS[g] for g in order], values, height=0.4,
                color=[GEO_COLORS[g] for g in order], edgecolor=SURFACE, linewidth=2)  # fmt: skip
        for i, v in enumerate(values):
            label = "not available" if pd.isna(v) else f"{v:,.1f}"
            ax.text((0 if pd.isna(v) else v) + vmax * 0.02, i, label, va="center",
                    fontsize=9, color=INK)  # fmt: skip
        ax.set_xlim(0, vmax * 1.2)
        ax.set_title(heading, loc="left", fontsize=10, color=INK_2)
        ax.tick_params(axis="y", labelcolor=INK)
        _grid(ax, "x")
    _footer(
        fig,
        data,
        "Deal data from Preqin via OECD.AI. One year only: totals are volatile and "
        "dominated by mega-deals; not a trend.",
    )
    fig.savefig(out, dpi=150, metadata={"Software": None})
    plt.close(fig)
    return out


def adoption_chart(df: pd.DataFrame, out: Path) -> Path:
    indicator = INDICATORS["ai_enterprise_adoption"]
    data = df[(df["indicator_id"] == indicator.id) & (df["geo"] == "EU27")]
    fig, (ax,) = _figure(
        "EU27 enterprises using AI — context only",
        "% of enterprises with 10+ persons employed · not a three-way comparison",
    )
    ax.bar(data["year"], data["value"], width=0.55, color=GEO_COLORS["EU27"])
    for x, v in zip(data["year"], data["value"], strict=True):
        ax.text(x, v + 0.4, f"{v:.2f}%", ha="center", fontsize=9, color=INK)
    surveyed = set(data["year"])
    for gap in range(int(data["year"].min()), int(data["year"].max())):
        if gap not in surveyed:
            ax.text(gap, 0.6, "no survey", ha="center", fontsize=8, color=MUTED)
    ax.set_xticks(range(int(data["year"].min()), int(data["year"].max()) + 1))
    ax.set_ylim(0, max(data["value"]) * 1.2)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}%"))
    _grid(ax)
    notes = "\n".join(
        ["The list of AI technologies surveyed changed between waves; compare years with caution."]
        + [f"{GEO_LABELS[g]} — {n}" for g, n in indicator.geo_notes.items()]
    )
    _footer(fig, data, notes)
    fig.savefig(out, dpi=150, metadata={"Software": None})
    plt.close(fig)
    return out


def generate(df: pd.DataFrame, out_dir: Path = CHARTS_DIR) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    return [
        vc_chart(df, out_dir / "ai_vc_2025.png"),
        line_chart(
            df,
            "ai_publications",
            "AI research publications",
            "Works per year with at least one author affiliated in the geography",
            "Full counting across geographies; volume, not quality.",
            lambda v: f"{v / 1000:.1f}k",
            lambda v: f"{v / 1000:.0f}k",
            out_dir / "ai_publications.png",
        ),
        line_chart(
            df,
            "gerd_pct_gdp",
            "R&D expenditure",
            "Gross domestic expenditure on R&D, % of GDP · all R&D, not AI-specific",
            "EU27 values are OECD estimates; US series has breaks and definition differences.",
            lambda v: f"{v:.2f}%",
            lambda v: f"{v:.1f}%",
            out_dir / "gerd_pct_gdp.png",
        ),
        adoption_chart(df, out_dir / "ai_enterprise_adoption_eu27.png"),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate charts from the processed data.")
    parser.add_argument("--out", default=str(CHARTS_DIR))
    args = parser.parse_args(argv)
    for path in generate(load_indicators(), Path(args.out)):
        print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
