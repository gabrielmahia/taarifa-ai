"""
TaarifaAI — East African Investigative Journalism Assistant
Fact-checking, Hansard analysis, procurement anomalies, bilingual reporting.
"""
import json, urllib.request, ssl
import streamlit as st

st.set_page_config(
    page_title="TaarifaAI — East African Journalism",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_key():
    try:
        return st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

def gemini(prompt: str, key: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1500}}
    req = urllib.request.Request(f"{url}?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        d = json.loads(r.read())
    return d["candidates"][0]["content"]["parts"][0]["text"]

with st.sidebar:
    st.image("https://flagcdn.com/w40/ke.png", width=40)
    st.title("TaarifaAI 📰")
    st.caption("East African Journalism AI")
    st.divider()
    mode = st.radio("Tool", [
        "✅ Fact Checker",
        "🔍 Procurement Analyser",
        "📜 Hansard Analyst",
        "🌍 Bilingual Reporter",
        "📊 Data Story Generator",
        "💬 Investigative Chat"
    ])
    st.divider()
    st.caption("⚠️ Verify all AI outputs against primary sources before publishing.")
    st.caption("📍 Designed for East African journalism context.")

key = get_key()
if not key:
    st.warning("Add GOOGLE_API_KEY to Streamlit secrets.")

# ── TOOL 1: FACT CHECKER ─────────────────────────────────────
if mode == "✅ Fact Checker":
    st.title("✅ East African Fact Checker")
    st.markdown("*Verify claims against Kenya public data sources*")

    claim = st.text_area("Claim to fact-check",
        placeholder="e.g. Kenya's debt-to-GDP ratio is sustainable at 68%...", height=100)
    source = st.text_input("Claimed source (optional)", placeholder="CS Treasury, press statement...")

    if claim and key and st.button("🔍 Fact check", type="primary"):
        with st.spinner("Analysing claim..."):
            prompt = f"""You are TaarifaAI, an East African fact-checking assistant.

Claim: "{claim}"
Claimed source: {source or "Not provided"}

Fact-check this claim systematically:

**1. Verdict** (one of: TRUE / MOSTLY TRUE / MISLEADING / MOSTLY FALSE / FALSE / UNVERIFIABLE)

**2. Evidence**
- What official data/documents support or contradict this?
- Reference: IMF Article IV, Kenya National Treasury, CBK, KNBS, World Bank, court records
- If economic data: cite latest available figures

**3. Context missing**
- What information is omitted that changes the meaning?
- What comparisons would a reader need?

**4. Recommended verification**
- FOIA/ATI request to which institution?
- Which public database to check?
- Which official to interview?

**5. Similar verified claims**
- Are there related claims that have been verified or debunked?

Be precise. Distinguish between confirmed data and inference.
Flag if this is outside your knowledge window."""
            resp = gemini(prompt, key)
            st.markdown(resp)
            st.info("📌 This fact-check is a starting point. Always verify against primary sources before publishing.")

# ── TOOL 2: PROCUREMENT ANALYSER ─────────────────────────────
elif mode == "🔍 Procurement Analyser":
    st.title("🔍 Procurement & CDF Analyser")
    st.markdown("*Identify anomalies in Kenya public procurement records*")

    col1, col2 = st.columns(2)
    with col1:
        entity = st.text_input("Government entity", placeholder="Nairobi County, Ministry of Health...")
        amount = st.number_input("Contract amount (KES)", min_value=0, value=50000000, step=1000000)
        proc_type = st.selectbox("Procurement method", [
            "Open tender", "Restricted tender", "Direct procurement",
            "Request for quotation", "Framework agreement", "Not stated"
        ])
    with col2:
        project = st.text_area("Project description", placeholder="Borehole drilling, road construction...", height=80)
        awarded_to = st.text_input("Awarded to (if known)", placeholder="Company name...")
        red_flags = st.multiselect("Observed red flags", [
            "No public tender notice found",
            "Single bidder",
            "Award above threshold for method",
            "Work completed before contract signed",
            "Same company wins repeatedly",
            "Contract split to avoid threshold",
            "Unusually fast award process",
            "No performance bond"
        ])

    if entity and project and key and st.button("🔍 Analyse procurement", type="primary"):
        with st.spinner("Analysing..."):
            prompt = f"""You are TaarifaAI, helping an East African investigative journalist analyse a public procurement record.

Entity: {entity}
Project: {project}
Amount: KES {amount:,}
Method: {proc_type}
Awarded to: {awarded_to or "Unknown"}
Observed flags: {", ".join(red_flags) if red_flags else "None identified yet"}

Provide:

**1. Risk Assessment** (LOW / MEDIUM / HIGH / CRITICAL)
With specific reasoning for Kenya's Public Procurement and Asset Disposal Act 2015 (PPADA) thresholds.

**2. PPADA Compliance Check**
- Is this procurement method appropriate for this amount?
- What should have been done vs what was apparently done?
- Which PPADA sections are potentially violated?

**3. Documents to Request (FOIA/ATI)**
List specific documents, the institution to request from, and the legal basis.

**4. Story Angles**
Two or three investigative angles this data point could support.

**5. Verification Steps**
What a journalist should do next before publication.

Note DEMO clearly — do not imply real data unless explicitly provided."""
            resp = gemini(prompt, key)
            st.markdown(resp)
            st.caption("⚠️ DEMO: This analysis is based on the information you provided. Verify all findings independently.")

# ── TOOL 3: HANSARD ANALYST ──────────────────────────────────
elif mode == "📜 Hansard Analyst":
    st.title("📜 Hansard & Parliamentary Record Analyst")
    st.markdown("*Analyse Kenya National Assembly and Senate debates*")

    hansard_text = st.text_area("Paste Hansard excerpt or parliamentary statement",
        placeholder="Paste text from Kenya National Assembly Hansard or Senate debates...",
        height=200)
    mp_name = st.text_input("MP/Senator name (optional)", placeholder="Hon. [Name], MP for [Constituency]")
    analysis_type = st.multiselect("What to analyse", [
        "Key policy positions stated",
        "Contradictions with voting record",
        "Promises made (track against delivery)",
        "Named persons/entities",
        "Budget/financial claims",
        "Allegations and charges made",
        "Procedure and Standing Orders compliance"
    ], default=["Key policy positions stated", "Named persons/entities"])

    if hansard_text and key and st.button("📜 Analyse Hansard", type="primary"):
        with st.spinner("Analysing parliamentary record..."):
            prompt = f"""You are TaarifaAI, an East African parliamentary records analyst.

Speaker: {mp_name or "Unknown"}
Analysis requested: {", ".join(analysis_type)}

Parliamentary text:
---
{hansard_text[:3000]}
---

Analyse this text systematically:

**1. Summary** (2-3 sentences of what was said)

**2. Key Claims** (numbered list — each claim that could be verified)

**3. Named Entities** (people, organisations, places, amounts mentioned)

**4. Verifiable Statements**
For each factual claim: what data source would confirm or deny it?

**5. Notable Language**
Hedging phrases, absolute claims, or statements that warrant scrutiny.

**6. Story Value**
Is there a public interest story here? If yes, what is it?

Context: Kenya National Assembly/Senate procedures, Standing Orders, public interest journalism standards."""
            resp = gemini(prompt, key)
            st.markdown(resp)

# ── TOOL 4: BILINGUAL REPORTER ───────────────────────────────
elif mode == "🌍 Bilingual Reporter":
    st.title("🌍 Bilingual East African Reporter")
    st.markdown("*Translate and adapt journalism for Swahili and English audiences*")

    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.radio("Source language", ["English", "Swahili"])
        source_text = st.text_area(f"Enter {source_lang} text",
            placeholder="Paste your article, press release, or statement...", height=200)
    with col2:
        output_type = st.selectbox("Output format", [
            "Full translation",
            "Summary (200 words)",
            "Community radio script",
            "Social media post (Twitter/X)",
            "SMS alert (160 chars)",
            "WhatsApp bulletin"
        ])
        target_audience = st.selectbox("Target audience", [
            "Urban Nairobi readers",
            "Rural community (simplified Swahili)",
            "Diaspora (English + context)",
            "Government officials (formal)",
            "Youth/social media",
            "ASAL communities (simple, practical)"
        ])

    if source_text and key and st.button("🌍 Generate output", type="primary"):
        target_lang = "Swahili" if source_lang == "English" else "English"
        with st.spinner("Generating..."):
            prompt = f"""You are TaarifaAI, a bilingual East African journalism assistant.

Source ({source_lang}):
{source_text[:2000]}

Create a {output_type} in {target_lang} for: {target_audience}

Rules:
- Preserve all facts accurately — no additions or omissions of key information
- Adapt language complexity for the target audience
- Use Kenya-specific references (counties, ministries, programmes) where relevant
- For Swahili: use standard Kiswahili sanifu unless audience requires otherwise
- For community radio: use short sentences, repetition of key points, local examples
- For SMS: maximum 160 characters, most critical information only
- Mark [TRANSLATION STARTS] and [TRANSLATION ENDS]"""
            resp = gemini(prompt, key)
            st.markdown(resp)

# ── TOOL 5: DATA STORY GENERATOR ─────────────────────────────
elif mode == "📊 Data Story Generator":
    st.title("📊 Data Story Generator")
    st.markdown("*Turn Kenya public data into compelling journalism*")

    data_input = st.text_area("Paste data (CSV, numbers, statistics, or describe the dataset)",
        placeholder="e.g. County budget allocations: Nairobi 450B, Mombasa 89B, Turkana 32B...",
        height=150)
    story_angle = st.selectbox("Story angle", [
        "Inequality / Disparity",
        "Government accountability",
        "Progress / Regression over time",
        "East Africa comparison",
        "Impact on ordinary citizens",
        "Policy effectiveness",
        "Budget vs delivery"
    ])
    audience = st.selectbox("Publication", [
        "Nation Media Group (Daily Nation)",
        "Standard Media Group",
        "The Star Kenya",
        "NTV/Citizen TV (broadcast)",
        "International media (Reuters, BBC Africa)",
        "Community newspaper / radio"
    ])

    if data_input and key and st.button("📊 Generate story", type="primary"):
        with st.spinner("Generating data story..."):
            prompt = f"""You are TaarifaAI, a Kenya data journalism specialist.

Data: {data_input}
Angle: {story_angle}
Publication: {audience}

Generate:

**1. HEADLINE** (for {audience} — attention-grabbing, accurate)

**2. STANDFIRST / DECK** (2 sentences explaining the significance)

**3. LEAD PARAGRAPH** (news inverted pyramid — most important first, 50 words max)

**4. KEY DATA POINTS** (3-5 bullets, each with the specific number and what it means)

**5. HUMAN IMPACT** (how this affects ordinary Kenyans — one specific example)

**6. VOICES NEEDED** (who to interview: government, civil society, affected people)

**7. DATA LIMITATIONS** (what caveats a responsible journalist should include)

**8. RELATED STORIES** (2 follow-up angles this data suggests)

Follow Kenya journalism standards. Be specific — cite exact numbers, not approximations."""
            resp = gemini(prompt, key)
            st.markdown(resp)

# ── TOOL 6: INVESTIGATIVE CHAT ───────────────────────────────
else:
    st.title("💬 Investigative Chat")
    st.markdown("*Open-ended investigative journalism assistance*")

    if "taarifa_chat" not in st.session_state:
        st.session_state.taarifa_chat = []

    for msg in st.session_state.taarifa_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_q = st.chat_input("Ask an investigative journalism question...")
    if user_q and key:
        st.session_state.taarifa_chat.append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.markdown(user_q)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.taarifa_chat[-6:])
                prompt = f"""You are TaarifaAI, an East African investigative journalism assistant.
You specialise in: Kenya public procurement, Hansard analysis, data journalism, fact-checking, FOIA requests, source verification, Swahili media.

Conversation:
{history}

Respond helpfully and specifically. Reference Kenya institutions (EACC, OAG, PPRA, DCI) and legal frameworks (PPADA, Access to Information Act, Media Act) where relevant.
Always note when professional verification or legal advice is needed."""
                try:
                    resp = gemini(prompt, key)
                    st.markdown(resp)
                    st.session_state.taarifa_chat.append({"role":"assistant","content":resp})
                except Exception as e:
                    st.error(f"AI error: {e}")

st.divider()
st.caption("TaarifaAI © 2026 | [East African Decision Infrastructure](https://gabrielmahia.github.io) | contact@aikungfu.dev")
st.caption("⚠️ Verify all AI outputs against primary sources. AI can be wrong. You are the journalist.")
