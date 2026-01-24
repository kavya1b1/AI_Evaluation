import streamlit as st
import requests
import time
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Proposal Evaluation System",
    layout="centered",
)

# ---------------- GLOBAL CSS ----------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #020617, #000000);
        color: #E5E7EB;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }

    .glass {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(14px);
        border-radius: 18px;
        padding: 26px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    .gradient-text {
        background: linear-gradient(90deg, #38BDF8, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #2563EB, #7C3AED);
        color: white;
        border-radius: 14px;
        padding: 14px 22px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 14px 36px rgba(124,58,237,0.6);
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #1E293B, transparent);
        margin: 36px 0;
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
            Decision intelligence powered by <b>ML Ensembles</b>,
            <b>Explainable AI</b>, and <b>Generative AI</b>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

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
    with st.status("🧠 AI Cognitive Pipeline", expanded=True):
        steps = [
            "Parsing proposal structure",
            "Embedding semantic content",
            "Benchmarking against past projects",
            "Running ML ensemble models",
            "Checking S&T guideline compliance",
            "Generating AI narrative report",
        ]
        for step in steps:
            st.write(f"• {step}")
            time.sleep(0.5)

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

    # ---------------- SUMMARY ----------------
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)

    st.subheader("📊 AI Evaluation Summary")

    c1, c2, c3 = st.columns(3)
    c1.metric("Final Score", f"{data['final_score']:.1f} / 100")
    c2.metric("Novelty", f"{data['novelty']:.1f}")
    c3.metric("Finance", f"{data['finance']:.1f}")

    st.success(f"📝 Decision: **{data['decision']}**")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- SIMILAR PROJECTS ----------------
    if "similar_projects" in data:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)

        st.subheader("🔍 Novelty Benchmarking (Past Project Similarity)")

        st.caption("Top 5 most similar NaCCER-funded past projects:")

        for proj in data["similar_projects"]:
            st.write(
                f"📌 **{proj['title']}** "
                f"(Similarity: `{proj['similarity']}`)"
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- FINANCE VIOLATIONS ----------------
    if "violations" in data and len(data["violations"]) > 0:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)

        st.subheader("⚠️ Financial Guideline Violations")

        for v in data["violations"]:
            st.error(f"❌ {v}")

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- FEATURE IMPORTANCE ----------------
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

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- AI NARRATIVE ----------------
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)

    st.subheader("🤖 AI Evaluation Narrative")
    st.write(data["ai_report_text"])

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DOWNLOAD ----------------
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)

    st.subheader("📄 Download Final Evaluation Report")

    st.markdown(
        f"""
        <a href="{data['report_url']}" target="_blank"
        style="display:inline-block;padding:16px 26px;
        background:linear-gradient(90deg,#2563EB,#7C3AED);
        color:white;border-radius:14px;font-weight:700;text-decoration:none;">
        ⬇️ Download AI Evaluation PDF
        </a>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HISTORY ----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)

st.subheader("🕒 Evaluation History Timeline")

try:
    history = requests.get("http://localhost:8000/history/").json()

    for item in history:
        color = (
            "#22C55E" if item["final_score"] >= 85
            else "#EAB308" if item["final_score"] >= 70
            else "#EF4444"
        )

        st.markdown(
            f"""
            <div style="margin-bottom:14px;padding:14px;border-radius:12px;
            background:rgba(2,6,23,0.6);border-left:5px solid {color};">
                <b>{item['filename']}</b><br>
                <span style="color:#9CA3AF;">{item['created_at']}</span><br>
                <span style="color:{color};font-weight:600;">
                    Score: {item['final_score']:.1f} — {item['decision']}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

except:
    st.warning("Could not load evaluation history.")

st.markdown("</div>", unsafe_allow_html=True)
