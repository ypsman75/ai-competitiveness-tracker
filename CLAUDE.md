# CLAUDE.md

Agent notes for this repository. The binding spec is `docs/implementation_plan.md`
(V2.1 — read its amendments section first).

- Never invent or fill data. Every row in `data/processed/` needs source URL, period,
  unit, `status` and `license_note`. Test fixtures live only under `tests/`.
- Geo codes: `EU27`, `US`, `CHN`. Never relabel "Europe" as EU27.
- Small GPG-signed commits, one per step. Never force-push.
- `gh` defaults to another account on the dev host: set `GH_TOKEN` to the ypsman75
  token and check `gh api user -q .login` before any `gh` write.
- Before claiming done: `python -m pytest` and `ruff check .` pass, and every README
  command has been run.
