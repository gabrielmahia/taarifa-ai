# AGENTS.md — TaarifaAI

## Purpose
AI-powered civic briefing tool for Kenyan journalists and civil society.
Surfaces budget anomalies, procurement gaps, and parliamentary performance from public records.

## Architecture
- `app.py` — Streamlit single-file app
- Gemini REST API (no SDK) — same pattern as jibu/jumuia
- No local data dependencies — all context built from public datasets at runtime

## AI Behaviour Rules
- NEVER make accusations — surface anomalies and suggest questions only
- Always mark output as "AI-generated — verify with primary sources before publishing"
- Cite specific KES figures, Article numbers, and Act sections
- Suggest FOI requests, committee appearances, IFMIS cross-checks as next steps
- Keep "Sandbox" disclaimer visible when live OCDS/COB API not connected

## Data Sources
- Controller of Budget (cob.go.ke)
- OCDS Kenya (tenders.go.ke/ocds)
- Parliament of Kenya / Mzalendo
- Constitution of Kenya 2010
- Kenya Civic Datasets DOI: 10.34740/kaggle/dsv/15473045

## Key contacts for partnerships
contact@aikungfu.dev — newsrooms, NGOs, county assemblies

<!-- coverage-adaptive-reasoning:v2 -->

## Coverage-Adaptive Reasoning v2

For consequential research, recommendations, investigations, analogy searches, forecasting, opportunity discovery, and canon building:

- A correct ranking inside an incomplete universe is still a failed answer.
- Separate candidate generation from candidate ranking.
- Materiality-gate the search: use the minimum useful set of orthogonal retrieval routes that could change the answer.
- Before closure ask what correct answer the current search method would be structurally incapable of finding.
- Treat aliases, language/geography, era, source class, format, genealogy, taxonomy, legal identity vs operational control/economic benefit, intermediaries, schema categories, null/failure cases, and negative space as potential blind spots when material.
- Maintain leading + competing + null explanations.
- Distinguish answer confidence from coverage confidence.
- “Nothing found” is not evidence of absence when coverage is low.
- Stop when additional independent search routes no longer materially change the candidate universe, hypotheses, decision, or next test.
- When an important miss occurs, repair the retrieval architecture via MISS → SENSOR REDESIGN; do not merely append the missed example.

<!-- v2 section appended 2026-10-28 from https://github.com/gabrielmahia/nairobi-stack/blob/main/docs/COVERAGE_ADAPTIVE_REASONING.md; the rest of this file is unchanged. -->
