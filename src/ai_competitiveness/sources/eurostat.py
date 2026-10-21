"""EU27 enterprise AI use from Eurostat ``isoc_eb_ai`` (CC BY 4.0). Context only."""

from datetime import date

from ai_competitiveness.sources import get

DATA_URL = (
    "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai"
    "?geo=EU27_2020&indic_is=E_AI_TANY&size_emp=GE10&unit=PC_ENT&lang=EN"
)
DEFINITION = (
    "Share of enterprises with 10 or more persons employed using at least one AI "
    "technology (Eurostat indicator E_AI_TANY)"
)
NOTE = (
    "EU27 only; no comparable US or China series. Survey years are not consecutive, and "
    "the list of AI technologies asked about has changed between waves (see Eurostat "
    "metadata isoc_e_esms): compare years with caution."
)


def parse_jsonstat(payload: dict, url: str, retrieved: str) -> list[dict]:
    """Parse a single-series JSON-stat response (all dimensions size 1 except time)."""
    sizes = dict(zip(payload["id"], payload["size"], strict=True))
    if any(n != 1 for dim, n in sizes.items() if dim != "time"):
        raise ValueError(f"expected one series, got dimension sizes {sizes}")
    years = {i: y for y, i in payload["dimension"]["time"]["category"]["index"].items()}
    flags = payload.get("status") or {}
    rows = []
    for idx, value in sorted(payload["value"].items(), key=lambda kv: int(kv[0])):
        flag = flags.get(idx, "")
        rows.append(
            {
                "indicator_id": "ai_enterprise_adoption",
                "indicator_name": "Enterprises using AI (10+ persons employed)",
                "geo": "EU27",
                "year": years[int(idx)],
                "value": str(value),
                "unit": "percent of enterprises",
                "source_name": "Eurostat (isoc_eb_ai)",
                "source_url": url,
                "retrieved_at": retrieved,
                "definition": DEFINITION,
                "methodology_note": NOTE + (f" Eurostat flag: {flag}." if flag else ""),
                "status": "provisional"
                if "p" in flag
                else "estimated"
                if "e" in flag
                else "observed",
                "license_note": "CC BY 4.0 (Eurostat)",
            }
        )
    return rows


def fetch() -> list[dict]:
    return parse_jsonstat(get(DATA_URL).json(), DATA_URL, date.today().isoformat())
