"""Gross domestic expenditure on R&D (% of GDP) from OECD MSTI (CC BY 4.0)."""

import csv
import io
from datetime import date

from ai_competitiveness.sources import get

DATA_URL = (
    "https://sdmx.oecd.org/public/rest/data/OECD.STI.STP,DSD_MSTI@DF_MSTI,"
    "/USA+CHN+EU27_2020.A.G.PT_B1GQ..?startPeriod={start}"
)
GEO_MAP = {"EU27_2020": "EU27", "USA": "US", "CHN": "CHN"}
FLAG_NOTES = {
    "B": "break in series",
    "D": "definition differs",
    "E": "estimated",
    "P": "provisional",
}
DEFINITION = "Gross domestic expenditure on R&D (GERD) as a percentage of GDP"
NOTE = "Total R&D, not AI-specific."


def _flags(record: dict) -> list[str]:
    cols = ("OBS_STATUS", "OBS_STATUS_2", "OBS_STATUS_3")
    return [record[c] for c in cols if record.get(c) and record[c] != "A"]


def parse_csv(text: str, url: str, retrieved: str) -> list[dict]:
    rows = []
    for record in csv.DictReader(io.StringIO(text)):
        geo = GEO_MAP.get(record["REF_AREA"])
        if geo is None or record["OBS_VALUE"] == "":
            continue
        flags = _flags(record)
        status = "provisional" if "P" in flags else "estimated" if "E" in flags else "observed"
        flag_text = "; ".join(
            f"OECD flag {f}: {FLAG_NOTES.get(f, 'see OECD codelist')}" for f in flags
        )
        rows.append(
            {
                "indicator_id": "gerd_pct_gdp",
                "indicator_name": "Gross domestic expenditure on R&D",
                "geo": geo,
                "year": record["TIME_PERIOD"],
                "value": record["OBS_VALUE"],
                "unit": "percent of GDP",
                "source_name": "OECD Main Science and Technology Indicators (MSTI)",
                "source_url": url,
                "retrieved_at": retrieved,
                "definition": DEFINITION,
                "methodology_note": f"{NOTE} {flag_text}".strip(),
                "status": status,
                "license_note": "CC BY 4.0 (OECD)",
            }
        )
    return sorted(rows, key=lambda r: (r["geo"], int(r["year"])))


def fetch(start: int = 2010) -> list[dict]:
    url = DATA_URL.format(start=start)
    response = get(url, headers={"Accept": "application/vnd.sdmx.data+csv; charset=utf-8"})
    return parse_csv(response.text, url, date.today().isoformat())
