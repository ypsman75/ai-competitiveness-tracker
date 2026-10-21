# EU vs US vs China: AI Competitiveness Tracker

**Three AI ecosystems. One transparent comparison. Follow the data.**

A Python-powered, open-source tracker comparing EU27, US, and Chinese AI ecosystems
through transparent, reproducible data.

> **Status: v0.0.1 — project skeleton.** No indicators are published yet. Data sources
> are under review (see [`docs/implementation_plan.md`](docs/implementation_plan.md)).
> Nothing in this repository should be read as a finding until sourced data is added.

## Scope

- **Geographies:** EU27, United States, China — used consistently; "Europe" is never
  relabelled as EU27.
- **Dimensions (planned for v0.1):** AI investment, AI research output, and one further
  comparable indicator, each with source, unit, period and caveats.
- **No composite score.** Individual metrics only.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Commands

```bash
python -m ai_competitiveness --help   # package entry point
python -m pytest                      # run tests
ruff check .                          # lint
```

Data validation, chart generation and the dashboard will be added in later steps.

## License

Code: MIT (see `LICENSE`). Data files carry their own source licences, recorded per
observation in `license_note`.
