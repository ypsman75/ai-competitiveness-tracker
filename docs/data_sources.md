# Data sources — Step C source review

**Review date:** 2026-10-21 · **Status:** awaiting owner go/no-go (spec V2.1, amendment 7)

This file is the source manifest required by spec §9. It is written **before** any
observation enters `data/processed/`. Values quoted below are evidence gathered during the
review (to show that a source works), not published observations.

## Summary

| # | Indicator (`indicator_id`) | Source | EU27 | US | CHN | Years | Route | Licence | Recommendation |
|---|---|---|---|---|---|---|---|---|---|
| 1 | AI VC deal value by destination (`ai_vc_deal_value`) | OECD Policy Brief No. 50 (data: Preqin via OECD.AI) | ✅ | ✅ | ✅ | **2025 only** | Manual transcription | Brief CC BY 4.0; underlying Preqin data third-party | **GO (single year, manually transcribed)** |
| 2 | AI research publications (`ai_publications`) | OpenAlex | ✅ | ✅ | ✅ | 2015–2025 | Open API, scripted | CC0 | **GO (automated)** |
| 3 | Gross R&D expenditure, % of GDP (`gerd_pct_gdp`) | OECD MSTI | ✅ | ✅ | ✅ | 2010–2024 | SDMX API, scripted | CC BY 4.0 | **GO (automated, not AI-specific)** |
| 4 | Enterprise AI adoption (`ai_enterprise_adoption`) | Eurostat `isoc_eb_ai` | ✅ | ❌ not comparable | ❌ no source | 2021, 2023–2025 | JSON API, scripted | CC BY 4.0 | **EU27 context only — not in headline comparison** |

Result: three indicators support a three-way comparison (1–3). Indicator 4 cannot, and
is shown only as EU27 context with an explicit "not comparable" label.

---

## 1. AI venture-capital investment by destination of AI firm

- **Publication:** OECD (2026), "Venture capital investments in artificial intelligence
  through 2025", *OECD Policy Briefs*, No. 50, OECD Publishing, Paris,
  <https://doi.org/10.1787/a13752f5-en>
- **Underlying data:** "This brief leverages data hosted on the OECD.AI Policy Observatory
  from Preqin". Figure sources read "OECD.AI (2026), data from Preqin, last updated
  2026-01-01, accessed on 2026-01-09".
- **Geography:** reported by location of the AI firm receiving investment ("Firms in the
  United States attract…"), separately from investor origin ("outgoing" investment).
  The brief uses **EU27** explicitly. China = "People's Republic of China".
- **Explicitly stated figures (2025, key-findings section):**

  | Measure | US | EU27 | CHN |
  |---|---|---|---|
  | AI VC received by firms in geography (destination) | USD 194 bn (≈75%) | USD 15.8 bn (6%) | USD 13.9 bn (5%) |
  | AI VC invested by investors in geography (origin) | USD 124 bn (≈56%) | USD 14.5 bn (7%) | USD 17.2 bn (8%) |

  Global AI VC in 2025: USD 258.7 bn. Origin shares use fractional attribution across
  co-investing countries and only deals with at least one identified investor country.
- **Time series:** 2012–2025 by geography exists only in the brief's charts and the OECD.AI
  interactive. No downloadable table or StatLink was found in the brief.
- **Price basis:** not stated in the brief. Recorded as "USD, price basis not stated
  (assumed current USD)" in `methodology_note`.
- **Licence:** OECD written content published from 1 July 2024 is CC BY 4.0, but OECD terms
  state "Data may be subject to restrictions … because third parties may have ownership
  interests". Preqin is a commercial provider. **Conservative route:** transcribe only the
  figures stated in the brief's text, with attribution. Do not copy chart series or
  OECD.AI downloads.
- **Access note:** oecd.org is behind a Cloudflare bot check. The text was read from the
  Internet Archive copy of 2026-02-28. Retrieval has to be manual; it cannot be scripted.
- **Suitability:** good for a 2025 snapshot (destination). Volatile: mega-deals were 73% of
  2025 value, and the top five deals were about a quarter of the total.
- **Not available:** a reproducible multi-year EU27/US/CHN series under open terms.
- **Rejected alternative:** OECD SDMX `DSD_VC@DF_VC_INV` (venture capital investments,
  market statistics) covers VC in general, by stage, with no AI breakdown.

## 2. AI research publications

- **Source:** OpenAlex, <https://openalex.org>, API `https://api.openalex.org/works`
- **Licence:** CC0 ("released under a CC0 public-domain license"). Redistribution allowed.
- **Definition:** works whose **primary topic** falls in OpenAlex subfield 1702
  "Artificial Intelligence" (Computer Science), counted by `publication_year`.
- **Geography:** a work counts for a geography if at least one author lists an institution
  there (`authorships.institutions.country_code`).
  - US = `US`; China = `CN` (excludes `HK`, `MO`, `TW`, which OpenAlex codes separately).
  - EU27 = one query OR-ing the 27 member-state codes, so a work with authors in two member
    states counts **once** for EU27.
  - Full counting *across* geographies: an EU–US co-authored work counts for both.
- **Query (one call per geography):**
  `filter=primary_topic.subfield.id:1702,publication_year:2015-2025,institutions.country_code:<geo>&group_by=publication_year`
- **Cost:** OpenAlex meters usage. Each grouped query cost USD 0.0001. The anonymous budget
  is USD 0.10/day shared per IP; a free key gives USD 1/day. The pipeline needs 3 queries,
  so **no key is required**. An optional `OPENALEX_API_KEY` environment variable may be
  supported; it is never committed.
- **Probe results (2026-10-21, for evidence only):** 2015 → 2025: US 11,224 → 32,688;
  EU27 18,286 → 36,752; CHN 10,419 → 55,202.
- **Caveats:** topics are assigned by a machine-learning classifier. Coverage favours
  indexed, DOI-bearing literature. Recent years keep growing as indexing catches up, so the
  latest year is marked provisional. Counts measure volume, not quality, citations, or
  model capability.
- **Suitability:** strong. Open, scripted, the same definition for all three geographies.

## 3. Gross domestic expenditure on R&D (GERD), % of GDP

- **Source:** OECD Main Science and Technology Indicators (MSTI), SDMX dataflow
  `OECD.STI.STP,DSD_MSTI@DF_MSTI`, key `USA+CHN+EU27_2020.A.G.PT_B1GQ..`, via
  `https://sdmx.oecd.org/public/rest/data/` (CSV)
- **Licence:** OECD data, CC BY 4.0 (OECD terms; no third-party restriction identified for MSTI).
- **Coverage:** EU27_2020, USA, CHN, 2010–2024 (15 observations each).
- **Probe (2024, evidence only):** US 3.44, CHN 2.69, EU27 2.13.
- **Observation flags to carry into `status` and `methodology_note`:**
  - EU27: every observation flagged `E` (estimated).
  - US: flags `D` (definition differs) and `B` (break in series) in several years.
  - CHN: no flags.
- **Caveat:** total R&D, **not AI-specific**. It is context for the innovation base, not a
  measure of AI capacity.
- **Cross-check source:** World Bank WDI `GB.XPD.RSDV.GD.ZS` (UNESCO UIS data, CC BY 4.0;
  EU aggregate `EUU`, to 2023 only). The World Bank v2 API returned HTTP 502 on every call
  on 2026-10-21; the Data360 API works. Its EUU level differs from OECD EU27 (e.g. 2.26 vs
  about 2.1) because the EU is aggregated differently. **Do not mix the two sources in one
  series.**

## 4. Enterprise AI adoption

- **EU27 — Eurostat `isoc_eb_ai`** "Artificial intelligence by size class of enterprise",
  indicator `E_AI_TANY` (enterprises using at least one AI technology), `size_emp=GE10`,
  `unit=PC_ENT`. Licence CC BY 4.0. Last updated 2026-06-15.
  Probe: 2021 7.65%, 2023 8.06%, 2024 13.48%, 2025 19.95%. Note the 2021→2023 definition
  change in the list of AI technologies.
- **US — Census Bureau BTOS** (`https://www.census.gov/hfp/btos/downloads/National.xlsx`,
  public domain). Question: "In the last two weeks, did this business use Artificial
  Intelligence (AI) in any of its business functions?" It is asked every two weeks, covers
  employer businesses of every size, and uses a different reference period and AI
  definition. **Not comparable** with Eurostat.
- **China:** no official, documented series found that is comparable with either.
- **Recommendation:** no three-way or two-way headline comparison. Optionally show the EU27
  series as context with "US: not comparable · China: not available".

## Not pursued for v0.1

- Stanford AI Index, Dealroom, Crunchbase, Preqin direct: restrictive or unverified
  redistribution terms, or a paid service.
- Compute and talent indicators: no open, three-way comparable series identified at this
  stage (roadmap v0.4).
