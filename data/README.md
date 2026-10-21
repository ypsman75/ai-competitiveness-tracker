# Data

- `processed/indicators.csv`: tidy long-form observations (schema: `docs/implementation_plan.md`
  §8 and `src/ai_competitiveness/schema.py`). Rebuilt by `python -m ai_competitiveness.build_data`;
  only real, sourced observations.
- `manual/`: rows transcribed by hand from publications, already in the canonical schema,
  with `status=manually_transcribed` and the reference in `methodology_note`.
- `raw/`: local downloads; ignored by Git unless small and redistributable.
