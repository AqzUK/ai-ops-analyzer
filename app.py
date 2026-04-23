import json
import os
import csv
from datetime import datetime

import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Peak Operations Efficiency Analyzer",
    page_icon="📊",
    layout="wide"
)

DETAILED_REPORT_URL = "https://your-payment-link-for-report"
REPORT_AND_CALL_URL = "https://your-payment-link-for-report-and-call"
CONTACT_EMAIL = "your@email.com"
LEADS_FILE = "leads.csv"

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1280px;
    }

    h1, h2, h3 {
        color: #16325c;
        font-family: Arial, sans-serif;
    }

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
        line-height: 1.15;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        opacity: 0.92;
    }

    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1rem 1rem 0.7rem 1rem;
        box-shadow: 0 4px 18px rgba(16, 24, 40, 0.06);
        border: 1px solid #e7edf5;
        margin-bottom: 1rem;
    }

    .output-card {
        background: white;
        border-radius: 16px;
        padding: 1.2rem 1.2rem 0.8rem 1.2rem;
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
        font-size: 0.98rem;
    }

    div[data-testid="stTextInput"] input {
        border-radius: 10px;
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

    img {
        filter: brightness(0.72);
    }

    [data-testid="stSidebar"] {
        background-color: #eef3f9;
        border-right: 1px solid #dde6f1;
    }

    .cta-box {
        background: linear-gradient(135deg, #16325c 0%, #214a86 100%);
        color: white;
        border-radius: 18px;
        padding: 1.4rem 1.5rem;
        margin-top: 1rem;
        box-shadow: 0 8px 24px rgba(22, 50, 92, 0.18);
    }

    .locked-box {
        background: #fff8e8;
        border: 1px solid #f1d38a;
        border-radius: 16px;
        padding: 1.2rem 1.2rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def save_lead_locally(payload: dict) -> None:
    file_exists = os.path.exists(LEADS_FILE)
    with open(LEADS_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "timestamp",
                "name",
                "email",
                "company",
                "selected_option",
                "industry",
                "analysis_depth",
                "include_cost_view",
                "problem_overview"
            ]
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(payload)


def valid_email(email: str) -> bool:
    return "@" in email and "." in email


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

if "lead_saved" not in st.session_state:
    st.session_state.lead_saved = False

if "selected_option" not in st.session_state:
    st.session_state.selected_option = ""


with st.sidebar:
    st.markdown("## Analysis Settings")
    industry = st.selectbox(
        "Industry",
        ["General", "Customer Support", "SaaS", "Recruitment", "Professional Services", "Education", "Operations"]
    )
    analysis_depth = st.selectbox(
        "Analysis depth",
        ["Standard", "Detailed"]
    )
    include_cost_view = st.selectbox(
        "Include cost view",
        ["Yes", "No"]
    )
    st.markdown("---")
    st.caption("The free version gives a high-level diagnostic. Paid options unlock a more tailored review.")

logo_col1, logo_col2, logo_col3 = st.columns([2, 1, 2])
with logo_col2:
    st.image("logo.png", width=190)

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">Peak Operations Efficiency Analyzer</div>
        <div class="hero-subtitle">
            Structured operational diagnostics using consulting logic across process, people, technology, demand and governance.
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
        height=150,
        placeholder="e.g. Our customer support team is missing SLAs and response times have increased over the past 3 months."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">⚙️ Process</div>', unsafe_allow_html=True)
    process = st.text_area(
        "Process",
        label_visibility="collapsed",
        height=150,
        placeholder="e.g. Tickets come in via email and are manually assigned. Multiple handoffs between teams and unclear ownership."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">💻 Technology</div>', unsafe_allow_html=True)
    tech = st.text_area(
        "Technology",
        label_visibility="collapsed",
        height=150,
        placeholder="e.g. Using Zendesk with limited automation. No routing rules or prioritisation logic in place."
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">👥 Team & Capacity</div>', unsafe_allow_html=True)
    fte = st.text_area(
        "Team & Capacity",
        label_visibility="collapsed",
        height=150,
        placeholder="e.g. 12 support agents, 2 team leads. Mix of junior and experienced staff. No clear tier structure."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">📊 Demand & Metrics</div>', unsafe_allow_html=True)
    metrics = st.text_area(
        "Demand & Metrics",
        label_visibility="collapsed",
        height=150,
        placeholder="e.g. 1,200 tickets per week. SLA is 48 hours but currently averaging 72 hours. Backlog increasing."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="mini-label">🧠 Additional Context</div>', unsafe_allow_html=True)
    context = st.text_area(
        "Additional Context",
        label_visibility="collapsed",
        height=150,
        placeholder="e.g. Team morale is dropping, urgent and low-priority issues are mixed together, and reporting is still manual."
    )
    st.markdown('</div>', unsafe_allow_html=True)

analyse_clicked = st.button("Analyse")

if analyse_clicked:
    if not problem.strip():
        st.warning("Please complete the Problem Overview section.")
    else:
        prompt = f"""
You are a senior operations consultant.

Your task is to analyse the problem using structured consulting methodologies.

Internally determine the most appropriate problem-solving model. Choose from:
- Process Optimisation
- Target Operating Model
- Value Driver / Cost Model
- Demand vs Capacity
- Technology / Automation Transformation

Do not explicitly state which model you are using.

Instead, let it shape how you:
- structure the analysis
- prioritise insights
- define recommendations

Write in British English and use a calm, clear, practical tone.
Keep the output easy for a business user to understand, while preserving strong consulting logic and prioritisation.

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

Additional Context:
{context}

Return valid JSON only in this exact format:

{{
  "executive_summary": "Short summary of the main issue and primary recommendation.",
  "assessment_approach": "Brief explanation of how the problem has been assessed in plain English without naming consulting frameworks.",
  "current_operating_model": "Describe the likely current state across process, people, technology, governance and data.",
  "key_issues": "Main inefficiencies and bottlenecks.",
  "root_causes": "What is most likely driving the problem.",
  "target_operating_model": "Describe a stronger future-state design.",
  "recommended_actions": "Top priority actions with rationale.",
  "roadmap": "Short term, medium term and long term actions.",
  "cost_benefit": "Likely cost-saving opportunities and possible investment needs.",
  "impact_effort": [
    {{"initiative": "Automation", "impact": 8, "effort": 4}},
    {{"initiative": "Process Redesign", "impact": 7, "effort": 6}},
    {{"initiative": "Team Changes", "impact": 6, "effort": 5}}
  ],
  "current_vs_target": [
    {{"metric": "Resolution Time", "current": 4, "target": 2}},
    {{"metric": "SLA Compliance", "current": 60, "target": 90}},
    {{"metric": "Manual Work", "current": 80, "target": 40}}
  ]
}}

Rules:
- Return JSON only
- No markdown
- No code fences
- No extra text
- Make the analysis specific to the inputs
- Keep chart values realistic and illustrative
- Do not mention MECE
- Do not name consulting firms or framework names in the output
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
            data = json.loads(result)
            st.session_state.analysis_data = data
            st.session_state.lead_saved = False
            st.session_state.selected_option = ""

        except Exception as e:
            st.error(f"Error: {e}")

data = st.session_state.analysis_data

if data:
    st.markdown("---")

    free_left, free_right = st.columns(2)

    with free_left:
        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("Executive Summary")
        st.write(data.get("executive_summary", ""))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("Key Issues")
        st.write(data.get("key_issues", ""))
        st.markdown('</div>', unsafe_allow_html=True)

    with free_right:
        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("How the problem has been assessed")
        st.write(data.get("assessment_approach", ""))
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="output-card">', unsafe_allow_html=True)
        st.subheader("Initial Recommendations")
        st.write(data.get("recommended_actions", ""))
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="locked-box">
            <h3 style="margin-top:0; color:#16325c;">🔒 Full report locked</h3>
            <p style="margin-bottom:0.4rem;">
                The free version gives you the headline view. The deeper report includes:
            </p>
            <p style="margin-bottom:0.2rem;">• Full root cause analysis</p>
            <p style="margin-bottom:0.2rem;">• Target operating model</p>
            <p style="margin-bottom:0.2rem;">• Prioritised roadmap</p>
            <p style="margin-bottom:0.2rem;">• Cost and benefit view</p>
            <p style="margin-bottom:0;">• Charts and structured report output</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("## Unlock Full Analysis")
    st.write("Enter your details to request the detailed report or the report plus walkthrough.")
    st.caption("By submitting your details, you agree to be contacted about your report request.")

    lead_col1, lead_col2, lead_col3 = st.columns(3)
    with lead_col1:
        name = st.text_input("Your name")
    with lead_col2:
        email = st.text_input("Work email")
    with lead_col3:
        company = st.text_input("Company")

    option_col1, option_col2 = st.columns(2)

    with option_col1:
        detailed_clicked = st.button("Request Detailed Report (£75)")

    with option_col2:
        call_clicked = st.button("Request Report + 30 min Walkthrough (£150)")

    if detailed_clicked or call_clicked:
        selected_option = "Detailed Report (£75)" if detailed_clicked else "Report + Walkthrough (£150)"

        if not name.strip() or not email.strip() or not company.strip():
            st.warning("Please complete your name, work email, and company.")
        elif not valid_email(email.strip()):
            st.warning("Please enter a valid work email.")
        else:
            payload = {
                "timestamp": datetime.utcnow().isoformat(),
                "name": name.strip(),
                "email": email.strip(),
                "company": company.strip(),
                "selected_option": selected_option,
                "industry": industry,
                "analysis_depth": analysis_depth,
                "include_cost_view": include_cost_view,
                "problem_overview": problem[:300].strip()
            }

            try:
                save_lead_locally(payload)
                st.session_state.lead_saved = True
                st.session_state.selected_option = selected_option
                st.success("Your details have been captured. You can now continue to payment.")
            except Exception as e:
                st.error(f"Could not save your details: {e}")

    if st.session_state.lead_saved:
        st.markdown("---")
        st.markdown("### Continue to payment")

        if st.session_state.selected_option == "Detailed Report (£75)":
            st.link_button("Pay for Detailed Report", DETAILED_REPORT_URL)
        elif st.session_state.selected_option == "Report + Walkthrough (£150)":
            st.link_button("Pay for Report + Walkthrough", REPORT_AND_CALL_URL)

        st.caption(f"If you have any questions, contact {CONTACT_EMAIL}.")
