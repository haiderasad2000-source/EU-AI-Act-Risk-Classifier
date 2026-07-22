import streamlit as st
import requests

API_URL = st.secrets.get("API_URL", "http://localhost:8000")

st.set_page_config(page_title="EU AI Act Risk Classifier", layout="wide")
st.title("EU AI Act Risk Classifier")
st.caption("Classify your AI system under Unacceptable, High, Limited, or Minimal risk tiers")

if "assessment_id" not in st.session_state:
    st.session_state["assessment_id"] = None

@st.cache_data
def load_questions():
    try:
        resp = requests.get(f"{API_URL}/api/classify/questions", timeout=10)
        if resp.status_code == 200:
            return resp.json()
    except:
        pass
    return []

questions = load_questions()

with st.sidebar:
    st.header("Assessment Info")
    system_name = st.text_input("System Name", placeholder="e.g., HARP-AI")
    system_description = st.text_area("System Description", placeholder="Brief description of the AI system", height=80)

    st.divider()
    st.header("History")
    try:
        resp = requests.get(f"{API_URL}/api/classify/history", params={"limit": 10}, timeout=10)
        if resp.status_code == 200:
            history = resp.json()
            if history:
                for item in history:
                    risk_color = {
                        "Unacceptable": ":red_circle:",
                        "High": ":orange_circle:",
                        "Limited": ":yellow_circle:",
                        "Minimal": ":green_circle:"
                    }.get(item["classification"], ":white_circle:")
                    label = f"{risk_color} {item['system_name']} ({item['classification']})"
                    with st.expander(label):
                        st.write(f"**Score:** {item['classification_score']:.1f}/100")
                        st.write(f"**Gaps:** {len(item['compliance_gaps'])}")
                        st.write(f"**Created:** {item['created_at'][:16]}")
                        if st.button("Download Report", key=item['id']):
                            resp_report = requests.get(f"{API_URL}/api/classify/{item['id']}/report", timeout=30)
                            if resp_report.status_code == 200:
                                st.download_button(
                                    "Download PDF",
                                    resp_report.content,
                                    file_name=f"EU_AI_Risk_{item['id'][:8]}.pdf",
                                    mime="application/pdf"
                                )
            else:
                st.info("No history yet")
    except:
        pass

st.subheader("Questionnaire")

if not questions:
    st.warning("Could not load questions. Make sure the backend is running.")
    st.stop()

categories = {}
for q in questions:
    cat = q.get("category", "General")
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(q)

answers = {}

for cat, q_list in categories.items():
    with st.expander(f"{cat}", expanded=True):
        for q in q_list:
            q_id = q["id"]
            options = q.get("options", [])
            option_labels = {opt["value"]: opt["label"] for opt in options}
            option_values = list(option_labels.keys())

            if len(option_values) > 3:
                selected = st.selectbox(
                    q["text"],
                    options=option_values,
                    format_func=lambda x: option_labels.get(x, x),
                    key=q_id,
                    help=q.get("help_text", "")
                )
            else:
                selected = st.radio(
                    q["text"],
                    options=option_values,
                    format_func=lambda x: option_labels.get(x, x),
                    key=q_id,
                    help=q.get("help_text", "")
                )

            answers[q_id] = selected

st.divider()
col1, col2, col3 = st.columns([1, 1, 2])

with col1:
    if st.button("Classify System", type="primary"):
        if not system_name:
            st.error("Please enter a system name")
        else:
            with st.spinner("Classifying..."):
                try:
                    payload = {
                        "system_name": system_name,
                        "system_description": system_description,
                        "answers": answers
                    }
                    resp = requests.post(f"{API_URL}/api/classify", json=payload, timeout=30)
                    if resp.status_code == 200:
                        st.session_state["result"] = resp.json()
                        st.session_state["assessment_id"] = resp.json()["id"]
                        st.success("Classification complete!")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Error: {resp.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")

if "result" in st.session_state:
    data = st.session_state["result"]

    st.divider()
    st.subheader("Classification Results")

    classification = data["classification"]
    risk_colors = {
        "Unacceptable": (":red_circle:", "#d32f2f"),
        "High": (":orange_circle:", "#f57c00"),
        "Limited": (":yellow_circle:", "#f9a825"),
        "Minimal": (":green_circle:", "#388e3c")
    }
    emoji, color = risk_colors.get(classification, (":white_circle:", "#757575"))

    col_a, col_b, col_c = st.columns([1, 1, 1])
    col_a.metric("Risk Tier", f"{emoji} {classification}")
    col_b.metric("Score", f"{data['classification_score']:.1f}/100")
    col_c.metric("Gaps", len(data.get("compliance_gaps", [])))

    st.markdown(f"""
    <div style="background: #e0e0e0; border-radius: 10px; height: 24px; width: 100%;">
        <div style="background: {color}; border-radius: 10px; height: 24px; width: {data['classification_score']}%;">
        </div>
    </div>
    """, unsafe_allow_html=True)

    if data.get("compliance_gaps"):
        st.subheader("Compliance Gaps")
        for gap in data["compliance_gaps"]:
            severity_map = {"critical": ":red_circle:", "high": ":orange_circle:", "medium": ":yellow_circle:", "low": ":green_circle:"}
            severity_emoji = severity_map.get(gap.get("severity", "low"), ":white_circle:")
            with st.expander(f"{severity_emoji} Article {gap['article']} &mdash; {gap['requirement'][:60]}..."):
                st.write(f"**Status:** {gap.get('status', 'Unknown')}")
                st.write(f"**Severity:** {gap.get('severity', 'Unknown')}")
                st.write(f"**Recommendation:** {gap.get('recommendation', 'N/A')}")

    st.subheader("Recommendations")
    for rec in data.get("recommendations", []):
        st.write(f"- {rec}")

    if data.get("report_url"):
        st.divider()
        resp_report = requests.get(f"{API_URL}/api/classify/{data['id']}/report", timeout=30)
        if resp_report.status_code == 200:
            st.download_button(
                "Download Full Report (PDF)",
                resp_report.content,
                file_name=f"EU_AI_Risk_{data['id'][:8]}.pdf",
                mime="application/pdf"
            )
