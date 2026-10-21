# EU vs US vs China: AI Competitiveness Tracker
## Implementation-ready project brief for Claude Code (V2.1)

**GitHub owner:** `ypsman75`  
**Repository:** `ai-competitiveness-tracker`  
**Repository URL target:** `https://github.com/ypsman75/ai-competitiveness-tracker`  
**Recommended visibility:** Public  
**Language:** Python 3.11+  
**Primary deliverable:** A reproducible, evidence-led comparison of the European Union (EU27), United States, and China across AI investment, research, and adoption using transparent public data.  
**Intended coding agent:** Claude Code, operating in the user's authenticated local development environment with GitHub CLI (`gh`) and Git installed.

> **Success definition for v0.1**  
> A public GitHub repository that a new user can clone, install, validate, regenerate at least three sourced charts from, and open a simple Streamlit dashboard for — all without secrets, invented numbers, or paid services. Every observation is traceable. Coverage limitations are stated clearly.

---

## V2.1 amendments (2026-10-21) — these override the text below where they conflict

1. **Repository already exists.** The repository is `ypsman75/ai-competitiveness-tracker` (created empty by the owner). Do not create another repository; clone it and populate it. All references to the old name have been updated.
2. **Identity and auth.** On the development host, a directory-scoped Git include sets the `ypsman75` identity, SSH key (`core.sshCommand`) and GPG signing key. Pushes go over SSH. The default `gh` account on the host is a different user; `gh` calls for this repository must be made with `GH_TOKEN` set to the ypsman75 token, and that fact must be checked (`gh api user -q .login`) before any `gh repo edit`.
3. **Commits.** Small, GPG-signed commits, one per implementation step. No single squashed "initial commit". Never force-push.
4. **Python.** The development host runs Python 3.14; `requires-python >= 3.11`. CI tests 3.11 and 3.13.
5. **Schema.** `status` and `license_note` are required columns (see §8). Numbers transcribed from a report use `status=manually_transcribed` with page/figure reference in `methodology_note`.
6. **Expected source outcomes (to be verified in Step C, not assumed):**
   - *AI VC (OECD):* OECD.AI VC figures derive from a commercial provider (Preqin); redistribution terms may not allow a public CSV. Fallback: transcribe only headline figures published in the OECD brief.
   - *AI publications:* prefer OpenAlex (CC0, open API) directly, the upstream of OECD.AI's publication series.
   - *Enterprise adoption:* Eurostat `isoc_eb_ai` is EU27-only, US Census BTOS asks a different question, and no comparable official China series is known. Expect "not comparable" for China.
   - *Candidate third three-way indicator:* gross R&D expenditure as % of GDP (World Bank `GB.XPD.RSDV.GD.ZS`, EU aggregate `EUU`, CC BY 4.0). Not AI-specific; caveat accordingly.
7. **Review gate.** Stop after Step C (source review) for owner approval before any observation is written to `data/processed/`.

---

## 0. Instructions to Claude Code: execute this plan

Treat this document as the binding implementation specification. Work directly in the user's local development environment. After checking authentication and permissions, create and populate the new GitHub repository `ypsman75/ai-competitiveness-tracker`.

### Required operating rules

1. **Inspect before changing anything.** Run `pwd`, inspect the current directory, check `git status` if applicable, and verify `python --version`, `git --version`, and `gh --version`. Do not initialize or overwrite an existing unrelated project.
2. **Verify GitHub identity before publishing.** Run `gh auth status` and confirm that the authenticated account is `ypsman75`. If it is not, stop before creating or pushing a repository and tell the user how to authenticate correctly.
3. **Check whether the target repository already exists.** If it exists, do not overwrite it, force-push, or alter its history. Inspect it and ask the user how to proceed if it is not clearly this project. If it does not exist, create it with the name specified above.
4. **Repository visibility:** use public visibility by default because this is intended as an open-source portfolio project. If the creation command requires a visibility choice and the user's preference is unclear, ask before making the repository public.
5. **No secrets or paid-data dependencies.** Never commit API keys, access tokens, `.env` files, credentials, or restricted datasets. Do not use paid data services for the MVP.
6. **No invented data.** Do not create plausible-looking values to fill gaps. If a source cannot be retrieved or verified, document the limitation clearly. Use a clearly labeled, tiny fixture only for unit tests — never as a real observation in `data/processed/`.
7. **Use real, traceable sources.** Every published observation must have a source, observation period, unit, and relevant methodological note. Respect source licensing and terms.
8. **Keep the first version achievable.** Prefer three working indicators with strong documentation over ten unreliable indicators. If fewer than three fully comparable series can be verified, ship with the verified ones and document the coverage gap explicitly in the README and dashboard.
9. **Run the project and tests.** Do not claim success until installation, tests, data validation, and chart generation have been attempted and results reported.
10. **Make changes in small, reviewable commits.** Do not force-push. Do not delete user data. If GitHub permissions, authentication, or an external service blocks a step, explain the exact blocker and leave the project in the best safe local state.
11. **Do not silently enable recurring automation.** A scheduled workflow may be included only if it is safe, low-frequency, and does not require secrets. Document it clearly. Do not create paid cloud resources.
12. **Finish with a concise handover** listing the repository URL, files created, data sources used, commands run, test results, known limitations, and next steps.

### Repository creation guidance

Use GitHub CLI if installed and authenticated. Before creation, check whether the repository exists. For a new repository, initialize the local project, make the first commit, create `ypsman75/ai-competitiveness-tracker`, and push the default branch. Do not initialize the remote with a separate README/license if doing so would conflict with the local initial commit.

If `gh` is unavailable or authentication is missing, continue with the local implementation if safe, but do not pretend the GitHub repository was created. Provide the exact commands or steps the user needs to complete publishing.

Add repository description and topics on creation (or immediately after):  
`AI competitiveness tracker comparing EU27, United States and China using transparent public data.`  
Topics: `ai`, `competitiveness`, `eu`, `china`, `united-states`, `data-visualization`, `python`, `open-data`, `streamlit`.

---

## 1. Product vision

Build an open-source tracker that helps answer:

> **Where is the EU keeping up in AI, where is it falling behind the United States and China, and what do comparable public indicators actually show?**

The project's perspective is pro-innovation, focused on economic dynamism, research, investment, and the ability to turn scientific advances into useful products. Its credibility depends on not pre-deciding the findings.

### Core principles

- **Evidence before rhetoric:** charts must be traceable to source data.
- **Three-way comparison:** EU27, US, and China are first-class geographic series.
- **Comparable measures:** distinguish absolute totals from per-capita, GDP-normalized, or other scaled indicators.
- **Reproducibility:** users can run a documented command to validate data and regenerate charts.
- **Transparent limitations:** mark missing observations, estimates, reporting lags, and differences in definitions.
- **Small MVP:** build a functioning pipeline and a few reliable charts before expanding the scope.
- **No composite score in v0.1–v0.9.** Individual metrics are easier to interpret and less likely to hide differences in definitions or data quality. A composite index is out of scope until at least v1.0 and must include transparent normalization, weighting, missing-data handling, and sensitivity analysis if ever added.

## 2. Geographic definitions

Use these geographic entities consistently:

- **EU27:** the 27 member states of the European Union. Do not silently substitute Europe, the European Economic Area, or EU plus UK.
- **US:** the United States of America.
- **China (CHN):** People's Republic of China, as defined by the source.

When a source uses a different scope (for example, “Europe” or “European countries”), do not relabel it EU27. Either preserve the source's scope explicitly or exclude it from direct three-way comparisons.

Country-level EU breakdowns may be added later, starting with Germany, France, and the Netherlands. The UK must remain a separate geography.

## 3. What to track

Use indicator families, but only ship metrics that pass source and comparability checks.

| Dimension | Candidate metrics | Key caveat |
|---|---|---|
| AI investment | AI VC deal value, deal count, early-stage share, generative-AI investment | VC data can be volatile; distinguish investment into firms from investor origin |
| Research output | AI publications, citation measures, high-impact research, research organizations | Publication counts are not equivalent to commercial leadership or model capability |
| Research and development | Business R&D, public R&D, AI-specific R&D where credible | Broad R&D may not isolate AI expenditure |
| Compute and infrastructure | Data-centre capacity, AI compute measures, infrastructure investment, power availability | Directly comparable compute capacity data may be limited or proprietary |
| Talent | AI-skilled workforce, researchers, AI-related vacancies, graduates | Job classifications and labor-market coverage differ by jurisdiction |
| Adoption | Enterprise AI adoption, use by sector and company size | Survey questions, reference periods, and sample frames may differ |
| Company formation and scale | AI company counts, funding rounds, scale-up financing, major AI firms | Commercial databases can have coverage and classification biases |
| Models and technical capability | Publicly documented model releases, benchmark results, open-weight releases | Benchmarks change; results depend on evaluation setup and should not be collapsed into a simplistic ranking |
| Commercial outcomes | AI-related exports, productivity evidence, business performance where credible | Attribution to AI is difficult; use cautious interpretation |
| Policy context | Major policy milestones, implementation dates, public support programs | A timeline is context, not proof that a policy caused an outcome |

### MVP indicators (ordered preference + fallbacks)

For the first working release, prioritize these three in order:

1. **AI venture-capital investment by destination of AI firm** (preferred primary series from OECD *Venture capital investments in artificial intelligence through 2025* or equivalent public table showing EU27 / US / China).
2. **AI research publication count or share**, using one consistent definition and source across all three geographies (OECD.AI or a well-documented public series).
3. **Enterprise AI adoption**, only if the source provides comparable or carefully harmonized observations for all three. If China or another geography is not covered comparably, do not fabricate a three-way series.

**Fallback rule:** If a preferred series cannot be obtained under open/redistributable terms, replace it with the next strongest public, citable series that supports at least two of the three geographies and document the substitution in `docs/data_sources.md` and the README. Never leave the processed dataset empty or invent numbers. A sourced manual CSV is acceptable for v0.1 if it includes source URL, observation date, units, and license/terms notes; automate retrieval later.

## 4. Known starting evidence (context, not hardcoded truth)

The OECD's February 2026 brief *Venture capital investments in artificial intelligence through 2025* reports that in 2025 US-based AI firms attracted approximately USD 194 billion (75% of global AI VC deal value), EU27 firms USD 15.8 billion (6%), and Chinese firms USD 13.9 billion (5%). The OECD also cautions that investment markets are cyclical and that mega-deals can strongly influence annual totals.

Use this publication as a discovery point and reference, not as permission to invent a full time series. Before including these numbers in data files, inspect the source methodology, definitions, licensing, and whether downloadable observations are available.

Reference:
- OECD publication: https://www.oecd.org/en/publications/venture-capital-investments-in-artificial-intelligence-through-2025_a13752f5-en.html
- Full report: https://www.oecd.org/en/publications/venture-capital-investments-in-artificial-intelligence-through-2025_a13752f5-en/full-report.html

OECD also publishes contextual indicators on AI publications and investment:
- https://www.oecd.org/en/topics/policy-issues/artificial-intelligence.html
- OECD.AI: https://oecd.ai/

## 5. Required MVP user experience

A user should be able to:

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Validate the included processed dataset.
5. Regenerate at least three charts.
6. Launch a simple local dashboard.
7. See each metric's definition, units, geography, period, source, and caveats.

### Required charts

Aim for three to five clear visuals:

- Time series for AI VC investment by EU27, US, and China (or the verified substitute).
- A normalized view (such as per capita or share of GDP) only when the denominator and currency conversion are defensible and sourced.
- AI research publication comparison using a consistent definition.
- Enterprise AI adoption comparison if the data is genuinely comparable; otherwise omit or clearly mark non-comparability.
- A latest-observation table showing metric, geography, year, value, unit, source, and caveat.

Do not build a composite “AI leadership score” in the MVP.

## 6. Implementation choices

Use a modest Python stack:

- Python 3.11 or newer.
- `pandas` for tabular data.
- `requests` for stable public endpoints, if available.
- `matplotlib` for static charts (preferred for reproducibility); use `plotly` only if interactive charts materially improve the dashboard.
- `streamlit` for a simple dashboard.
- `pytest` for tests.
- `ruff` for linting and formatting.

Avoid adding a database, orchestration framework, cloud deployment, or LLM API dependency to v0.1. The MVP should run locally without paid services or API credentials.

## 7. Target repository structure

Create this structure, simplifying only if a file is not yet needed:

```text
ai-competitiveness-tracker/
├── README.md
├── CLAUDE.md                 # short agent-oriented notes (optional but recommended)
├── LICENSE                   # MIT
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── data/
│   ├── README.md
│   ├── raw/                  # ignored by Git unless small and redistribution is allowed
│   └── processed/
│       └── indicators.csv    # only real, sourced observations
├── docs/
│   ├── methodology.md
│   ├── data_sources.md
│   └── implementation_plan.md
├── src/
│   └── ai_competitiveness/
│       ├── __init__.py
│       ├── load_data.py
│       ├── validate_data.py
│       ├── transform_data.py
│       ├── charts.py
│       └── report.py
├── app/
│   └── dashboard.py
├── outputs/
│   └── charts/               # generated output; keep only useful, small examples
├── tests/
│   ├── test_validate_data.py
│   └── test_transform_data.py
└── .github/
    └── workflows/
        └── tests.yml
```

Do not commit large downloaded datasets, credentials, or data that cannot legally be redistributed. Use `.gitignore` to exclude `.venv/`, `__pycache__/`, `.env`, raw downloads, and generated temporary files as appropriate.

## 8. Canonical data schema

Use a tidy long-form CSV. One row represents one observation of one indicator for one geography and period.

Required columns:

| Column | Description |
|---|---|
| `indicator_id` | Stable slug, e.g. `ai_vc_deal_value` |
| `indicator_name` | Human-readable metric name |
| `geo` | `EU27`, `US`, or `CHN` |
| `year` | Observation year as integer |
| `value` | Numeric value |
| `unit` | e.g. `USD million`, `percent`, `count` |
| `source_name` | Dataset or publisher |
| `source_url` | Source page or dataset URL |
| `retrieved_at` | ISO date on which data was retrieved |
| `definition` | What the metric measures |
| `methodology_note` | Caveats, transformation, coverage, or comparability notes |

Also required: `status` (`observed` / `estimated` / `projection` / `manually_transcribed`) and `license_note`. Optional columns include `currency_basis` and `price_basis`.

**Example valid row (illustrative only — replace with real sourced data):**

```csv
indicator_id,indicator_name,geo,year,value,unit,source_name,source_url,retrieved_at,definition,methodology_note
ai_vc_deal_value,AI VC deal value by destination,US,2025,194000,USD million,OECD,https://www.oecd.org/...,2026-10-21,AI-related venture capital investment received by firms headquartered in the geography,Figures from OECD 2026 brief; mega-deals can dominate annual totals
```

Validation rules:
- Required columns exist and are non-empty where applicable.
- `year` is an integer and `value` is numeric or explicitly missing.
- `geo` is one of the allowed codes unless the schema is deliberately extended.
- Duplicate `(indicator_id, geo, year)` rows are rejected or explicitly resolved.
- Missing values remain missing; never replace them with zero.
- Each observation has source metadata.
- Units are consistent within a chart, or conversions are documented and tested.
- No invented filler observations.

## 9. Source discovery and licensing checklist + data acquisition protocol

Start with official and documented sources. Claude Code must verify each source rather than assume a URL implies API access.

1. **OECD.AI / OECD**
   - AI investment, AI compute, AI publications, and related indicators.
   - https://oecd.ai/
   - https://www.oecd.org/en/topics/policy-issues/artificial-intelligence.html
2. **Eurostat**
   - Enterprise AI adoption and ICT statistics, particularly EU-wide series.
   - https://ec.europa.eu/eurostat/
3. **OECD Data Explorer**
   - Harmonized economic, R&D, productivity, and innovation indicators.
   - https://data-explorer.oecd.org/
4. **US Census Bureau**
   - Business surveys and technology adoption, subject to cross-country comparability.
   - https://www.census.gov/data.html
5. **World Bank Open Data**
   - Population and macroeconomic denominators.
   - https://data.worldbank.org/
6. **China-specific official or academic sources**
   - Use only when definitions, coverage, and provenance are documented. Where official figures are not directly comparable with OECD/US/EU measures, mark that clearly.
7. **Research/model sources**
   - Use a documented public dataset or source with clear methodology. Record benchmark name, release/version, date, and evaluation conditions if model capability is ever included.

### Data acquisition protocol (mandatory)

- Prefer official downloadable tables / CSVs / APIs over scraping.
- For each metric, create a short source manifest entry in `docs/data_sources.md` **before** writing any numbers into `data/processed/`.
- If only a PDF/report exists, extract only the explicitly stated numbers, record page/table reference, and put them in a clearly labeled “manually transcribed” section of the processed data with full provenance.
- Never scrape behind login walls or paywalls.
- If access terms are unclear, do not commit the data. Commit a source manifest and a script that downloads it when terms permit, or document the manual retrieval process.
- Record for every metric: exact dataset/table name, geographic coverage, definition and unit, earliest/latest year, update cadence and publication lag, API/download route, licensing and redistribution constraints, any break in series, and why it is suitable (or unsuitable) for a three-way comparison.

## 10. Methodology and interpretation rules

- Keep EU27, US, and China labels consistent across all outputs.
- Distinguish **AI firms by destination** from **investor origin** for investment flows.
- Show absolute values and normalized values separately; never imply they answer the same question.
- State currency, price basis, and conversion method. Avoid mixing nominal USD, nominal EUR, and constant-price series without clear transformations.
- Do not average country percentages to derive EU27 rates unless statistically correct.
- Clearly mark estimates and projections.
- Display source year, retrieval date, and any reporting lag.
- Do not interpret research paper counts as direct measures of model quality or economic value.
- Do not treat policy timelines as causal evidence.
- Avoid claims that regulation alone explains a gap without an appropriate research design.
- If a metric cannot support a fair three-way comparison, exclude it from the headline comparison and explain why.
- Missing geographies must be shown as “not available / not comparable” rather than omitted silently.

## 11. Implementation plan for Claude Code

### Step A — Environment and repository checks
- Inspect current working directory and tools.
- Confirm GitHub identity is `ypsman75`.
- Check for an existing target repository.
- Create a new local project directory without touching unrelated files.
- Create the GitHub repository only if it does not already exist and visibility is clear.

### Step B — Bootstrap project
- Add `pyproject.toml`, `requirements.txt`, `.gitignore`, MIT `LICENSE`, `README.md`, and optionally `CLAUDE.md`.
- Set up a standard package layout under `src/ai_competitiveness/`.
- Keep dependencies minimal.
- Make installation commands explicit and OS-neutral where possible.

### Step C — Source review
- Evaluate candidate metrics and sources using the acquisition protocol above.
- Create `docs/data_sources.md` and `docs/methodology.md`.
- Select the strongest three metrics that can be verified (or fewer if necessary, with explicit coverage documentation).
- Do not start by filling CSVs with unverified figures.

### Step D — Data validation and processing
- Implement a loader for the chosen source format(s).
- Implement schema validation and useful error messages.
- Create a small processed dataset only from verified observations.
- Add tests for missing columns, invalid geography codes, duplicate keys, missing values, and unit consistency.

### Step E — Charts and report
- Generate at least three charts or clearly document why fewer are possible with the verified data.
- Include chart titles, axis labels, units, source, period, and caveats.
- Save charts reproducibly to `outputs/charts/`.
- Create a simple summary report from processed data.

### Step F — Dashboard
- Implement a lightweight Streamlit app.
- Provide a metric selector and EU27/US/China comparison.
- Show source and methodological metadata next to every chart and table.
- Handle missing data gracefully (“not available / not comparable”).
- The app must work offline and without secret keys. No external calls at runtime for the MVP.

### Step G — Quality checks
- Run `pytest`.
- Run `ruff check .` and formatting checks if configured.
- Run the data validator.
- Run the chart-generation command.
- Smoke-test the dashboard startup.
- Fix errors instead of merely listing them.
- Confirm that every command listed in the README actually works.

### Step H — GitHub release
- Add a GitHub Actions workflow for tests and linting on push and pull request. The build must fail on validation or test failure.
- Confirm no secrets or restricted data are staged.
- Push small, signed, reviewable commits to `main` (see Amendment 3).
- Verify the remote repository and pushed commit.
- Do not force-push.
- Set repository description and topics.

### Step I — Handover
Report:
- Exact repository URL and visibility.
- Summary of implemented features.
- The three (or fewer) indicators actually shipped + full source URLs.
- Confirmation that `pytest`, data validation, and chart generation all passed.
- Commands to install, test, validate data, generate charts, and run the dashboard (verified).
- Known limitations and the precise next recommended milestone.
- Anything not completed and why.

## 12. Acceptance criteria for v0.1

The implementation is complete only when the following are true, or any unmet item is explicitly explained:

- [ ] New repository `ypsman75/ai-competitiveness-tracker` exists and contains the project, or an explicit authentication/permission blocker is documented.
- [ ] README explains the purpose, scope, setup, commands, data sources, and limitations.
- [ ] EU27, US, and China are consistently represented.
- [ ] At least three real, traceable indicators are included if three comparable public series can be verified; otherwise the coverage limitation and substitution are documented.
- [ ] Data validation runs from the command line.
- [ ] At least three charts can be regenerated from the processed data (or fewer with explicit documentation).
- [ ] A local dashboard launches successfully.
- [ ] Tests cover schema validation and key transformation logic.
- [ ] GitHub Actions runs tests and linting and fails on error.
- [ ] No credentials, secrets, or restricted datasets are committed.
- [ ] The project does not claim that incomplete or non-comparable data proves a simple ranking.
- [ ] Installation and run instructions work from a clean environment.
- [ ] Every README command has been tested and works.

## 13. Commands the finished project should support

Choose stable command names and document them in the README. Preferred interface:

```bash
# Create and activate a virtual environment (activation varies by shell)
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Install project dependencies
python -m pip install -r requirements.txt
# or: python -m pip install -e .

# Validate processed data
python -m ai_competitiveness.validate_data

# Generate charts and summary outputs
python -m ai_competitiveness.charts

# Optional summary report
python -m ai_competitiveness.report

# Run tests
python -m pytest

# Launch the dashboard
streamlit run app/dashboard.py
```

Claude Code must adjust these commands to the final package structure and ensure they actually work. Do not leave README commands that have not been tested. `python -m ai_competitiveness --help` (or equivalent) should also work if a CLI entry point is defined.

## 14. Suggested README copy

### Title
**EU vs US vs China: AI Competitiveness Tracker**

### One-line description
A Python-powered, open-source tracker comparing EU27, US, and Chinese AI ecosystems through transparent, reproducible data.

### Opening paragraph
Which AI ecosystem is best positioned to lead the next decade? This project compares the EU27, United States, and China across investment, research, and adoption. It uses traceable sources, documents data limitations, and generates reproducible charts so readers can inspect the evidence rather than rely on slogans.

### Tagline
**Three AI ecosystems. One transparent comparison. Follow the data.**

## 15. Roadmap after v0.1

- **v0.1 — Evidence baseline:** verified metrics, data schema, charts, tests, documentation.
- **v0.2 — Interactive dashboard:** filtering, metric metadata, latest-value comparisons, clearer missing-data handling.
- **v0.3 — Data refresh:** robust source-specific downloaders and change detection.
- **v0.4 — Broader AI stack:** additional compute, talent, adoption, and commercial indicators.
- **v0.5 — Policy context:** carefully sourced policy timeline annotations.
- **v1.0 — Reproducible tracker:** stable data pipeline, documented methodology, CI, contribution guide, and (only if rigorously designed) optional composite index with sensitivity analysis.

---

## Reference links

- OECD, *Venture capital investments in artificial intelligence through 2025*: https://www.oecd.org/en/publications/venture-capital-investments-in-artificial-intelligence-through-2025_a13752f5-en.html
- OECD full report: https://www.oecd.org/en/publications/venture-capital-investments-in-artificial-intelligence-through-2025_a13752f5-en/full-report.html
- OECD AI topic page: https://www.oecd.org/en/topics/policy-issues/artificial-intelligence.html
- OECD.AI: https://oecd.ai/
- Eurostat: https://ec.europa.eu/eurostat/
- OECD Data Explorer: https://data-explorer.oecd.org/
- US Census Bureau data: https://www.census.gov/data.html
- World Bank Open Data: https://data.worldbank.org/
- GitHub CLI documentation: https://cli.github.com/manual/gh_repo_create

**Planning status:** This is an implementation specification (V2.1). It does not claim that every suggested dataset has a stable API or is directly comparable across all three geographies. Claude Code must verify data availability, definitions, licensing, and reproducibility during implementation. Prefer shipping fewer fully sourced indicators over many weakly sourced ones.
