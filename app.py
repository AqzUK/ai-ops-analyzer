import json
import os

from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Peak Operations Efficiency Analyzer",
    page_icon="📊",
    layout="wide"
)

CONTACT_EMAIL = "your@email.com"

st.markdown(
    """
    <style>
    .stApp { background-color: #f4f7fb; }
    .block-container { padding-top: 1.5rem; max-width: 1280px; }
    h1, h2, h3 { color: #16325c; font-family: Arial, sans-serif; }

    .hero-card {
        background: linear-gradient(135deg, #16325c 0%, #214a86 100%);
        padding: 2rem 2.2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 24px rgba(22, 50, 92, 0.18);
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
    }

    .section-card, .output-card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 4px 18px rgba(16, 24, 40, 0.06);
        border: 1px solid #e7edf5;
        margin-bottom: 1rem;
    }

    .mini-label {
        color: #16325c;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.4rem;
    }

    div[data-testid="stTextArea"] textarea {
        border-radius: 12px;
        border: 1px solid #d7dfeb;
        background-color: #f9fbfe;
    }

    div.stButton > button {
        background-color: #16325c;
        color: white;
        border-radius: 12px;
        padding: 0.7rem 1.3rem;
        font-weight: 600;
        border: none;
    }

    div.stButton > button:hover {
        background-color: #214a86;
        color: white;
    }

    img { filter: brightness(0.72); }

    [data-testid="stSidebar"] {
        background-color: #eef3f9;
        border-right: 1px solid #dde6f1;
    }

    .email-box {
        background: linear-gradient(135deg, #16325c 0%, #214a86 100%);
        color: white;
        border-radius: 18px;
        padding: 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 8px 24px rgba(22, 50, 92, 0.18);
    }
    </style>
    """,
    unsafe_allow_html=True
)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("API key not found.")
    st.stop()

client = OpenAI(api_key=api_key)

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

with st.sidebar:
    st.markdown("## Analysis Settings")
    industry = st.selectbox(
        "Industry",
        [
            "General",
            "Customer Support",
            "SaaS",
            "Recruitment",
            "Professional Services",
            "Education",
            "Operations"
        ]
    )
    analysis_depth = st.selectbox("Analysis depth", ["Standard", "Detailed"])
    include_cost_view = st.selectbox("Include cost view", ["Yes", "No"])
    st.markdown("---")
    st.caption("This tool provides a high-level diagnostic. For a fuller review, speak to us.")

logo_col1, logo_col2, logo_col3 = st.columns([2, 1, 2])
with logo_col2:
    st.image("logo.png", width=190)

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Peak Operations Efficiency Analyzer</div>
        <div class="hero-subtitle">
            Structured operational diagnostics across process, people, technology, demand, governance and commercial impact.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.info("Provide structured inputs below. The stronger the inputs, the sharper and more useful the analysis will be.")

left, right = st.columns(2)

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">🧩 Problem Overview</div>', unsafe_allow_html=True)
    problem = st.text_area(
        "Problem Overview",
        label_visibility="collapsed",
        height=140,
        placeholder="e.g. Our support team is missing SLAs and response times have increased over the past 3 months."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">⚙️ Process</div>', unsafe_allow_html=True)
    process = st.text_area(
        "Process",
        label_visibility="collapsed",
        height=140,
        placeholder="e.g. Work is manually assigned, there are multiple handoffs and ownership is unclear."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">💻 Technology</div>', unsafe_allow_html=True)
    tech = st.text_area(
        "Technology",
        label_visibility="collapsed",
        height=140,
        placeholder="e.g. Using Zendesk with limited automation, no routing rules and no prioritisation logic."
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">👥 Team & Capacity</div>', unsafe_allow_html=True)
    fte = st.text_area(
        "Team & Capacity",
        label_visibility="collapsed",
        height=140,
        placeholder="e.g. 12 agents, 2 team leads, mixed experience levels, no clear tier structure."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">📊 Demand & Metrics</div>', unsafe_allow_html=True)
    metrics = st.text_area(
        "Demand & Metrics",
        label_visibility="collapsed",
        height=140,
        placeholder="e.g. 1,200 tickets per week, SLA 48 hours, current average 72 hours, backlog increasing."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">💷 Commercial / Financial Context</div>', unsafe_allow_html=True)
    commercial = st.text_area(
        "Commercial / Financial Context",
        label_visibility="collapsed",
        height=140,
        placeholder="e.g. Rising headcount cost, margin pressure, customer churn risk, revenue leakage or sales handoff issues."
    )
    st.markdown('</div>', unsafe_allow_html=True)

context = st.text_area(
    "Additional Context",
    height=100,
    placeholder="e.g. Team morale is dropping, urgent and low-priority work is mixed together, reporting is manual."
)

analyse_clicked = st.button("Run Analysis")

if analyse_clicked:
    if not problem.strip():
        st.warning("Please complete the Problem Overview section.")
    else:
        prompt = f"""
You are a senior operations consultant.

Analyse the operational problem using structured consulting thinking.

Internally determine the most appropriate problem-solving model. Choose from:
- Process Optimisation
- Target Operating Model
- Value Driver / Cost Model
- Demand vs Capacity
- Technology / Automation Transformation

Do not explicitly state which model you are using.
Do not mention consulting firm names or framework names.

Write entirely in British English. Use UK spelling and terminology.
Use a calm, clear, practical and professional tone.

Industry:
{industry}

Analysis depth:
{analysis_depth}

Include cost view:
{include_cost_view}

Problem Overview:
{problem}

Team & Capacity:
{fte}

Process:
{process}

Demand & Metrics:
{metrics}

Technology:
{tech}

Commercial / Financial Context:
{commercial}

Additional Context:
{context}

Return valid JSON only in this exact format:

{{
  "executive_summary": "Short summary of the main issue and primary recommendation.",
  "assessment_approach": "Brief explanation of how the problem has been assessed in plain English without naming frameworks.",
  "key_issues": "Main inefficiencies and bottlenecks.",
  "initial_recommendations": "Initial high-level recommendations only.",
  "commercial_considerations": "Brief note on possible cost, revenue, margin or customer impact where relevant."
}}

Rules:
- Return JSON only
- No markdown
- No code fences
- No extra text
- Be specific to the user inputs
- Do not provide a full implementation plan
- Do not provide detailed root cause analysis
- Do not provide a full target operating model
- Keep enough value to be useful, but leave deeper analysis for a follow-up conversation
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a senior operations consultant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            result = response.choices[0].message.content
            st.session_state.analysis_data = json.loads(result)

        except Exception as e:
            st.error(f"Error: {e}")

data = st.session_state.analysis_data

if data:
    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("Executive Summary")
        st.write(data.get("executive_summary", ""))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("Key Issues")
        st.write(data.get("key_issues", ""))
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("How the problem has been assessed")
        st.write(data.get("assessment_approach", ""))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("Initial Recommendations")
        st.write(data.get("initial_recommendations", ""))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="output-card">', unsafe_allow_html=True)
    st.subheader("Commercial Considerations")
    st.write(data.get("commercial_considerations", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="email-box">
            <h3 style="color:white; margin-top:0;">Speak to us about a deeper review</h3>
            <p>
                This diagnostic provides an initial view only. If the themes reflect what you are seeing,
                we can help turn this into a fuller operational review with clearer priorities, financial impact,
                implementation considerations and next steps.
            </p>
            <p>
                Email us with a short summary of your situation:
            </p>
            <p style="font-size:1.1rem;"><strong>{CONTACT_EMAIL}</strong></p>
        </div>
        """,
        unsafe_allow_html=True
    )