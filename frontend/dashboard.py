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
            "Running ML ensemble models",
            "Estimating uncertainty & confidence",
            "Generating LLM evaluation narrative",
        ]
        for step in steps:
            st.write(f"• {step}")
            time.sleep(0.6)

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

    st.success(f"📝 Decision: **{data['decision']}**")
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CONFIDENCE & UNCERTAINTY ----------------
    cb = data["confidence_band"]

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)
    st.subheader("📈 ML Confidence & Uncertainty")

    fig = go.Figure()

    # Confidence band
    fig.add_trace(go.Bar(
        x=[cb["upper"] - cb["lower"]],
        y=["Confidence Interval"],
        base=[cb["lower"]],
        orientation="h",
        marker=dict(color="rgba(99,102,241,0.35)"),
        hoverinfo="skip"
    ))

    # Mean marker
    fig.add_trace(go.Scatter(
        x=[cb["mean"]],
        y=["Confidence Interval"],
        mode="markers",
        marker=dict(size=16, color="#38BDF8"),
        name="Predicted Score"
    ))

    fig.update_layout(
        xaxis=dict(range=[0, 100], title="Score"),
        yaxis=dict(visible=False),
        height=220,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.metric(
        "Model Confidence",
        f"{cb['confidence']:.1f}%",
        help="Higher confidence means lower prediction uncertainty"
    )

    st.caption(
        "Shaded region shows the 95% confidence interval. Narrower intervals indicate higher model certainty."
    )

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
        st.caption("Relative contribution of each feature to the ML decision.")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SHAP WATERFALL ----------------
    if "shap_values" in data:
        shap = data["shap_values"]
        baseline = shap["baseline"]
        contributions = shap["contributions"]

        features = list(contributions.keys())
        values = list(contributions.values())

        cumulative = [baseline]
        for v in values:
            cumulative.append(cumulative[-1] + v)

        fig = go.Figure()

        # Contribution bars
        for i, feature in enumerate(features):
            fig.add_trace(go.Bar(
                x=[values[i]],
                y=[feature],
                orientation="h",
                base=cumulative[i],
                marker=dict(
                    color="#22C55E" if values[i] > 0 else "#EF4444"
                ),
                hovertemplate=f"{feature}: {values[i]:+.2f}<extra></extra>",
                showlegend=False
            ))

        # Final score marker
        fig.add_trace(go.Scatter(
            x=[data["final_score"]],
            y=["Final Score"],
            mode="markers",
            marker=dict(size=18, color="#38BDF8"),
            hovertemplate="Final Score: %{x:.2f}<extra></extra>",
            showlegend=False
        ))

        fig.update_layout(
            title="🧠 SHAP Waterfall – Feature Impact on Final Score",
            xaxis=dict(title="Score Contribution"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=400
        )

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='glass fade-in'>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "SHAP-style explanation showing how each feature pushes the score higher or lower from the baseline."
        )
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
    st.subheader("📄 Evaluation Report")

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
        color = "#22C55E" if item["final_score"] >= 85 else "#EAB308" if item["final_score"] >= 70 else "#EF4444"

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
