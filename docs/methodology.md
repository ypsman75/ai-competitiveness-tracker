# Methodology (draft, v0.1)

This document defines how observations are selected, recorded and shown. Source-specific
details are in [`data_sources.md`](data_sources.md).

## Geographies

| Code | Meaning | Notes |
|---|---|---|
| `EU27` | The 27 EU member states (post-2020 composition) | Never substituted with "Europe", the EEA, or EU+UK. The UK is always separate. |
| `US` | United States of America | |
| `CHN` | People's Republic of China, as defined by the source | OpenAlex `CN` excludes Hong Kong, Macao and Taiwan. |

When a source covers a different scope, it is kept under its own label or excluded from
the three-way comparison. It is never relabelled.

## Observation status

Every row carries a `status`:

- `observed`: published by the source as a measured value.
- `estimated`: flagged by the source as an estimate (e.g. OECD flag `E`).
- `provisional`: likely to be revised (e.g. the latest OpenAlex year while indexing catches up).
- `manually_transcribed`: copied by hand from a report's text, with the section reference in
  `methodology_note`.

Source flags that are not themselves a status (e.g. OECD `B` break in series, `D` definition
differs) are recorded in `methodology_note`.

## Counting rules

- **Investment:** by destination (where the AI firm receiving funding is located). Investor
  origin is a separate indicator, never mixed with destination.
- **Publications:** a work counts for a geography if at least one author affiliation is
  located there. Works are de-duplicated within EU27 but can count for several
  geographies, so EU27 + US + CHN can exceed the global total.

## Units, currency and price basis

- Each indicator keeps the source's unit (`USD million`, `percent`, `count`).
- No currency conversion or deflation in v0.1. If added later, the method and its source
  must be documented and tested.
- Where a source does not state its price basis, `methodology_note` says so.

## Absolute vs normalised

Absolute values and normalised values (per capita, % of GDP) are separate indicators and
are charted separately. GERD is already normalised (% of GDP) by the source.

## Missing and non-comparable data

- Missing values stay missing. They are never zero-filled or interpolated.
- A geography without a comparable value is shown as **"not available / not comparable"**.
  It is never silently dropped.
- An indicator that cannot support a fair three-way comparison is excluded from the
  headline view, and the reason is shown.

## Interpretation limits

- Publication counts do not measure research quality, model capability or economic value.
- R&D intensity is not AI-specific.
- A single year of VC data is a snapshot in a volatile, mega-deal-driven market, not a trend.
- No composite score before v1.0 (spec §1).
- Policy timelines are context, not causal evidence.
