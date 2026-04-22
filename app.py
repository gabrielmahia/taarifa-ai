"""TaarifaAI — Kenya civic briefing tool. AI-powered public records analysis."""
import sys, os, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

st.set_page_config(page_title="TaarifaAI", page_icon="📰", layout="centered")
st.markdown("""<style>
  .main > div { padding: 0.5rem 1rem 2rem; }
  h1 { font-size: 1.6rem !important; }
</style>""", unsafe_allow_html=True)

def _get_key():
    try:
        k = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if k: return k
    except: pass
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", "")

def _call_gemini(system, user, api_key):
    _BASE = "https://generativelanguage.googleapis.com"
    models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": 1200, "temperature": 0.2},
    }
    for model in models:
        url = f"{_BASE}/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
              headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code in (400, 404): continue
            raise
        except Exception: continue
    raise RuntimeError("Gemini unavailable")

COUNTIES = [
    "Nairobi", "Mombasa", "Kiambu", "Nakuru", "Machakos", "Kisumu", "Meru", "Kakamega",
    "Turkana", "Garissa", "Wajir", "Mandera", "Marsabit", "Isiolo", "Baringo", "Laikipia",
    "Narok", "Kajiado", "Bomet", "Kericho", "Bungoma", "Kitui", "Makueni", "Embu",
]

SYSTEM_BRIEF = """You are a civic accountability analyst for Kenya. Generate structured investigative briefs based on public data.

Your briefs are factual, specific, and action-oriented. They:
- Flag statistical anomalies (low absorption, procurement gaps, single-sourcing)
- Cite specific KES figures and percentages
- Suggest concrete questions for journalists to investigate
- Reference the relevant law (PFM Act, Employment Act, Constitution)
- Recommend next steps (FOI requests, committee appearances, IFMIS cross-checks)
- NEVER make accusations — surface anomalies and questions only
- Mark all AI analysis as "AI-generated — verify with primary sources before publishing"

Format output with clear section headers. Be concise and specific."""

st.title("📰 TaarifaAI")
st.caption("Civic accountability briefs for Kenya · For journalists, civil society, and researchers")

api_key = _get_key()

col1, col2 = st.columns(2)
with col1:
    county = st.selectbox("County:", COUNTIES)
with col2:
    brief_type = st.selectbox("Brief type:", [
        "County accountability brief",
        "Budget anomaly report",
        "Procurement gap analysis",
        "Parliamentary performance",
        "Constitutional rights audit",
    ])

focus = st.text_input("Specific focus (optional):", placeholder="e.g. health sector, road construction, CDF utilisation")

if not api_key:
    with st.expander("🔑 Add your free Google AI key to generate briefs"):
        api_key = st.text_input("Google AI key:", type="password",
                                 placeholder="AIza...",
                                 help="Free at aistudio.google.com — no credit card needed.")

if st.button("Generate brief", type="primary", use_container_width=True):
    if not api_key:
        st.info("Add a free Google AI key above. Get one at [aistudio.google.com](https://aistudio.google.com)")
    else:
        with st.spinner(f"Analysing {county} data..."):
            # Build context from available data
            context_parts = [
                f"County: {county}",
                f"Brief type: {brief_type}",
                f"Focus area: {focus or 'general accountability'}",
                f"Data period: FY 2022/23",
                "",
                "Available data context:",
                "- Controller of Budget: county development fund absorption rates",
                "- OCDS Kenya: procurement contracts (tenders.go.ke/ocds)",
                "- Parliament of Kenya: MP records, bills, CDF",
                "- Constitution of Kenya 2010",
                "",
                "Note: This is a sandbox demo using illustrative data patterns.",
                "In production, live COB/OCDS/Parliament APIs would be queried.",
            ]
            prompt = "\n".join(context_parts)
            prompt += f"\n\nGenerate a {brief_type} for {county} county."
            if focus:
                prompt += f" Focus specifically on {focus}."

            try:
                brief = _call_gemini(SYSTEM_BRIEF, prompt, api_key)
                st.markdown("---")
                st.markdown("### Accountability Brief")
                st.markdown(brief)
                st.markdown("---")
                col_a, col_b = st.columns(2)
                col_a.download_button("📥 Download brief (.txt)", brief,
                                      file_name=f"taarifa_{county.lower()}_{brief_type[:20].replace(' ','_')}.txt")
                col_b.caption("⚠️ AI-generated — verify with primary sources before publishing.")
            except urllib.error.HTTPError as e:
                st.error("API key not recognised." if e.code == 403 else "Too many requests — please wait a moment.")
            except Exception:
                st.error("Could not generate brief. Please try again.")

with st.expander("📚 About TaarifaAI"):
    st.markdown("""
**TaarifaAI** surfaces anomalies in Kenya's public data for journalists and civil society.

**Data sources:**
- Controller of Budget (COB) — county development fund absorption
- OCDS Kenya — procurement contracts (tenders.go.ke/ocds)
- Parliament of Kenya — MP records, bills, CDF
- Constitution of Kenya 2010

**Part of the Kenya civic portfolio:**
[Hesabu (budgets)](https://hesabu.streamlit.app) · [Jibu (rights)](https://jibuyangu.streamlit.app) · [Macho ya Wananchi (MPs)](https://macho-ya-wananchi.streamlit.app)

**For newsrooms and NGOs:** [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
""")

st.divider()
st.caption("© 2026 Gabriel Mahia · CC BY-NC-ND 4.0 · Powered by Google Gemini · contact@aikungfu.dev")
