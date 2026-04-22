import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Peak Operations Efficiency Analyzer",
    page_icon="📊",
    layout="centered"
)

st.markdown(
    """
    <style>
    img {
        filter: brightness(0.7);
    }
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.image("logo.png", width=200)
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
    except:
        api_key = None

if not api_key:
    st.error("API key not found.")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("Peak Operations Efficiency Analyzer")

st.write("Analyse operational problems using structured consulting logic.")

problem = st.text_area("Describe the operational problem")

metrics = st.text_area("Optional metrics or context (volume, SLA, team size, etc.)")

if st.button("Analyse"):

    if not problem:
        st.warning("Please describe the problem.")
    else:
        prompt = f"""
You are a senior operations consultant.

Write in British English, with a calm, clear and supportive tone. 
Your role is not just to analyse, but to guide and teach the user how to think about the problem.

The user has described an operational challenge.

Problem:
{problem}

Context:
{metrics}

Structure your response as follows:

1. Framing the Problem
Briefly restate the situation in simple terms to show understanding.

2. What MECE Means (Brief Explanation)
Explain that MECE stands for Mutually Exclusive, Collectively Exhaustive.
Clarify that it is a way of breaking a problem into distinct areas with no overlap, ensuring nothing important is missed.
Keep this explanation simple and practical.

3. Problem Breakdown (MECE)
Break the problem into clear categories such as:
- Process
- People
- Technology
- Demand / Volume

4. Likely Root Causes
Explain what is likely driving the inefficiencies, linking back to the breakdown.

5. Key Bottlenecks
Highlight where delays, friction, or wasted effort are most likely occurring.

6. Improvement Opportunities
Suggest realistic improvements such as:
- automation
- process redesign
- clearer ownership
- better prioritisation

7. Impact vs Effort
For each improvement, briefly describe:
- expected impact (High, Medium, Low)
- level of effort (High, Medium, Low)

8. Practical Action Plan
Lay this out in simple phases:

Short term (quick wins)
Medium term (process improvements)
Long term (structural or system changes)

9. Optional Cost Consideration
Where relevant, give a rough indication of:
- where cost savings might come from
- or where investment may be required (tools, people, systems)

Guidelines:
- Keep the tone human and natural, not robotic
- Avoid bullet symbols or hyphens
- Keep it clear and easy to follow
- Focus on practical, real-world improvements
- Do not overcomplicate language
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a senior operations consultant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        result = response.choices[0].message.content

        st.text_area("Analysis", result, height=400)