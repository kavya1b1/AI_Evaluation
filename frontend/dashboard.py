import streamlit as st
import requests
import time
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Proposal Evaluation System",
    layout="centered",
)

# ---------------- GLOBAL CSS ----------------
st.markdown(
    """
    <style>
    /* Background */
    .stApp {
        background: radial-gradient(circle at top, #020617, #000000);
        color: #E5E7EB;
    }

    /* Fade-in animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }

    /* Glass card */
    .glass {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(14px);
        border-radius: 16px;
        padding: 22px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    /* Gradient title */
    .gradient-text {
        background: linear-gradient(90deg, #38BDF8, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }

    /* Button */
    div.stButton > button {
        background: linear-gradient(90deg, #2563EB, #7C3AED);
        color: white;
        border-radius: 12px;
        padding: 12px 20px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 10px 30px rgba(124,58,237,0.6);
    }

    /* Section divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #1E293B, transparent);
        margin: 32px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- HERO ----------------
st.markdown(
    """
    <div class="glass fade-in">
        <h1 class="gradient-text">🤖 AI Proposal Evaluation System</h1>
        <p style="color:#9CA3AF;font-size:16px;">
            An intelligent decision-support platform powered by
            <b>Machine Learning</b>, <b>Explainable AI</b>, and <b>Generative AI</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------------- INPUT ----------------
st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)
st.subheader("📄 Submit Proposal")

file = st.file_uploader("Upload Proposal PDF", type=["pdf"])
budget = st.number_input("💰 Proposed Budget (₹)", min_value=0.0, step=10000.0)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "result" not in st.session_state:
    st.session_state.result = None

# ---------------- EVALUATE ----------------
if st.button("🚀 Run AI Evaluation", disabled=(file is None)):
    with st.status("🧠 AI Cognitive Pipeline", expanded=True) as status:
        steps = [
            "Parsing proposal structure",
            "Generating semantic embeddings",
            "Running ML evaluation model",
            "Estimating uncertainty & confidence",
            "Generating LLM evaluation narrative",
        ]
        for step in steps:
            st.write(f"• {step}")
            time.sleep(0.6)

        status.update(label="✅ AI Evaluation Complete", state="complete")

    response = requests.post(
        "http://localhost:8000/submit/",
        files={"file": file},
        data={"budget": budget}
    )

    if response.status_code == 200:
        st.session_state.result = response.json()
    else:
        st.error("❌ Evaluation failed")

# ---------------- RESULTS ----------------
if st.session_state.result:
    data = st.session_state.result

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)
    st.subheader("📊 AI Evaluation Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Final Score", f"{data['final_score']:.1f} / 100")
    c2.metric("Novelty", f"{data['novelty']:.1f}")
    c3.metric("Finance", f"{data['finance']:.1f}")

    st.progress(min(data["final_score"] / 100, 1.0))
    st.success(f"📝 Decision: **{data['decision']}**")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- XAI ----------------
    if "feature_importance" in data:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)
        st.subheader("📊 Explainable AI – Feature Importance")

        fi = data["feature_importance"]
        fig = px.bar(
            x=list(fi.values()),
            y=list(fi.keys()),
            orientation="h",
            color=list(fi.values()),
            color_continuous_scale="blues"
        )
        fig.update_layout(
            height=360,
            showlegend=False,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)
        st.caption("ML model contribution of each feature.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- AI NARRATIVE ----------------
    if "ai_report_text" in data:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)
        st.subheader("🤖 AI Evaluation Narrative")
        st.write(data["ai_report_text"])
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DOWNLOAD ----------------
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)
    st.subheader("📄 Evaluation Report")

    st.markdown(
        f"""
        <a href="{data['report_url']}" target="_blank"
        style="display:inline-block;padding:14px 22px;
        background:linear-gradient(90deg,#2563EB,#7C3AED);
        color:white;border-radius:12px;font-weight:600;text-decoration:none;">
        ⬇️ Download AI Evaluation PDF
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)
