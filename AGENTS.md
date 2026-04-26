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
