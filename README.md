# 📰 TaarifaAI — Kenya Civic Briefing AI

> *Taarifa* (Kiswahili) — report, news, briefing.

AI-powered civic briefing tool for Kenya. Feed it a county, a time period, or a topic — get a structured investigative brief: budget anomalies, procurement gaps, parliamentary performance, and constitutional rights violations — in plain language, ready to publish.

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)](https://taarifaai.streamlit.app)
[![Powered by Gemini](https://img.shields.io/badge/Gemini-Free%20tier-blue)](https://aistudio.google.com)

## Who this is for

- **Investigative journalists** covering devolution, procurement, and public finance
- **Civil society organisations** doing budget accountability work
- **County assemblies** wanting to scrutinise executive spending
- **Academics and researchers** studying Kenya's devolution
- **Citizens** who want to understand how their county's money is spent

## What it produces

Given a county and FY, TaarifaAI generates a structured brief:

```
COUNTY ACCOUNTABILITY BRIEF — TURKANA, FY 2022/23
Generated: April 22, 2026 | Source: Controller of Budget + OCDS

BUDGET SUMMARY
  Development allocation:  KES 4.2B
  Absorbed:                KES 1.72B (41%)
  Unspent:                 KES 2.48B — flagged for follow-up

PROCUREMENT CROSS-CHECK
  Contracts in OCDS:       8 tenders, 5 awarded
  Total contract value:    KES 890M
  Unexplained gap:         KES 830M — no procurement records

KEY QUESTIONS FOR INVESTIGATION
  1. Where did KES 830M in absorbed spend go without tender records?
  2. 3 road contracts awarded to single vendor — possible single-sourcing?
  3. 0 health facility tenders despite KES 400M health allocation

CONSTITUTIONAL ANGLE
  Article 201: Public finance must promote accountability
  Article 35: Citizens have the right to access this information

RECOMMENDED NEXT STEPS
  → File FOI request under Access to Information Act 2016
  → Contact County Assembly Budget Committee
  → Cross-reference with IFMIS records
```

## Quickstart

```bash
git clone https://github.com/gabrielmahia/taarifa-ai
cd taarifa-ai
pip install -r requirements.txt
streamlit run app.py
```

## Data sources

- **Controller of Budget** — county budget execution reports
- **OCDS Kenya** — procurement contracts (tenders.go.ke/ocds)
- **Parliament of Kenya** — MP and bill records
- **Constitution of Kenya 2010** — rights framework

All data from [Kenya Civic Datasets](https://doi.org/10.34740/kaggle/dsv/15473045) (DOI: `10.34740/kaggle/dsv/15473045`)

## AI engine

Powered by **Google Gemini** (free tier — no credit card needed).
Get a free key at [aistudio.google.com](https://aistudio.google.com).

The AI synthesises cross-dataset findings into investigative briefs. It does not make accusations — it surfaces anomalies and suggests questions for human journalists to pursue.

## Related

- [Hesabu](https://hesabu.streamlit.app) — Budget execution dashboard
- [hesabu-agent](https://github.com/gabrielmahia/hesabu-agent) — CrewAI budget analysis agent
- [kenya-rag](https://github.com/gabrielmahia/kenya-rag) — RAG over Kenya civic data
- [Jibu](https://jibuyangu.streamlit.app) — Constitutional rights assistant

## For media organisations and NGOs

Interested in a white-label version, API access, or training for your newsroom? [contact@aikungfu.dev](mailto:contact@aikungfu.dev)

## IP & Collaboration

© 2026 Gabriel Mahia · [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
License: CC BY-NC-ND 4.0
Not affiliated with any county government, COB, or Parliament of Kenya.
