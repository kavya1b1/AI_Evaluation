import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Proposal Evaluator", layout="wide")

# ---------------- PREMIUM UI CSS ----------------
st.markdown("""
<style>
            

.stApp {
    background: linear-gradient(120deg,#0f172a,#020617,#000);
    color: white;
    font-family: "Segoe UI", sans-serif;
}
            
h1, h2, h3 {
    font-size: 28px !important;
}

.stMarkdown, .stTextInput label {
    font-size: 18px !important;
}

.glass-card {
    background: rgba(255,255,255,0.07);
    padding: 35px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0px 8px 25px rgba(0,0,0,0.6);
    margin-bottom: 20px;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    background: linear-gradient(90deg,#38BDF8,#A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.chat-user {
    background: #2563eb;
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
    width: fit-content;
    max-width: 80%;
}

.chat-ai {
    background: rgba(255,255,255,0.12);
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
    width: fit-content;
    max-width: 80%;
}

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.15);
    margin: 25px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR NAV ----------------
st.sidebar.title("📌 AI Proposal Evaluator")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🤖 Reviewer Agent Chat", "📜 Evaluation History"]
)

# ======================================================
# SESSION STATE FIX (No Refresh Issue)
# ======================================================
if "last_eval" not in st.session_state:
    st.session_state.last_eval = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ======================================================
# PAGE 1 — HOME
# ======================================================
if page == "🏠 Home":

    st.markdown("<h1 class='big-title'>🚀 AI Proposal Evaluation Dashboard</h1>",
                unsafe_allow_html=True)

    st.markdown("### Upload your R&D proposal PDF for funding evaluation")

    file = st.file_uploader("📄 Upload Proposal PDF", type=["pdf"])

    budget = st.number_input(
        "💰 Proposed Budget (₹)",
        min_value=100000.0,
        max_value=500000000.0,
        step=50000.0
    )

    if st.button("🚀 Run AI Evaluation"):

        if file is None:
            st.error("❌ Please upload a PDF file first.")
            st.stop()

        with st.spinner("Running AI Cognitive Pipeline..."):

            response = requests.post(
                f"{API_URL}/submit/",
                files={"file": file},
                data={"budget": budget}
            )

        data = response.json()

        if "error" in data:
            st.error(data["error"])
            st.stop()

        # ✅ Store evaluation permanently
        st.session_state.last_eval = data

        st.success("✅ Proposal Evaluated Successfully!")

    # ======================================================
    # DISPLAY RESULTS WITH TABS
    # ======================================================
    if st.session_state.last_eval:

        data = st.session_state.last_eval

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📊 Overview", "🔍 Novelty", "⚠ Finance", "🤖 AI Narrative", "📄 Report"]
        )

        # ---------------- TAB 1 Overview ----------------
        with tab1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

            st.subheader("⭐ Final Evaluation Result")

            col1, col2, col3 = st.columns(3)
            col1.metric("Final Score", f"{data['final_score']:.1f}/100")
            col2.metric("Novelty", f"{data['novelty']:.1f}")
            col3.metric("Finance Score", f"{data['finance']:.1f}")

            st.success(f"Decision: **{data['decision']}**")

            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- TAB 2 Novelty ----------------
        with tab2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

            st.subheader("🔍 Similar Past Research Projects")

            for proj in data["similar_projects"]:

                # ✅ Correct key from backend
                title = proj.get("title", "Unknown Paper")

                similarity = proj.get("similarity", 0)
                url = proj.get("url", "")

                st.markdown(
                    f"""
                    <div style="
                        background:rgba(255,255,255,0.08);
                        padding:22px;
                        margin-bottom:18px;
                        border-radius:18px;
                        border-left:6px solid #38BDF8;
                        font-size:19px;
                    ">
                        📌 <b style="font-size:22px;">{title}</b><br><br>

                        Similarity Score:
                        <span style="color:#22c55e;font-weight:800;">
                            {similarity:.2f}
                        </span>
                        <br><br>

                        {"🔗 <a href='" + url + "' target='_blank' style='color:#A78BFA;font-weight:700;font-size:17px;'>Read Full Paper →</a>" if url else ""}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown("</div>", unsafe_allow_html=True)



        # ---------------- TAB 3 Finance ----------------
        with tab3:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

            st.subheader("⚠ Financial Compliance Check")

            if len(data["violations"]) > 0:
                for v in data["violations"]:
                    st.error(f"❌ {v}")
            else:
                st.success("✅ No financial violations detected!")

            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- TAB 4 AI Narrative ----------------
        with tab4:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

            st.subheader("🤖 AI Evaluation Narrative Report")

            st.markdown(
                f"""
                <div style="line-height:1.8;font-size:16px;">
                    {data["ai_report_text"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

        # ---------------- TAB 5 Report Download ----------------
        with tab5:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)

            st.subheader("📄 Download AI Evaluation Report")

            st.markdown(
                f"""
                <a href="{data['report_url']}" target="_blank"
                style="display:inline-block;padding:16px 28px;
                background:linear-gradient(90deg,#2563EB,#7C3AED);
                color:white;border-radius:14px;font-weight:700;
                text-decoration:none;">
                ⬇️ Download PDF Report
                </a>
                """,
                unsafe_allow_html=True
            )

            st.markdown("</div>", unsafe_allow_html=True)

# ======================================================
# PAGE 2 — REVIEWER AGENT CHAT
# ======================================================
elif page == "🤖 Reviewer Agent Chat":

    st.markdown("<h1 class='big-title'>🤖 Reviewer Agent Chat</h1>",
                unsafe_allow_html=True)

    if st.session_state.last_eval is None:
        st.warning("⚠ Please evaluate a proposal first on Home Page.")
        st.stop()

    st.info("Ask things like: Why low score? How to improve? What are risks?")

    question = st.text_input("💬 Enter your question:")

    if st.button("Ask Reviewer"):

        if question.strip() == "":
            st.warning("Please type a question.")
            st.stop()

        with st.spinner("🤖 Reviewer Agent is thinking..."):
            payload = {
                "question": question,
                "proposal_text": st.session_state.last_eval.get("proposal_text", ""),
                "final_score": st.session_state.last_eval["final_score"],
                "decision": st.session_state.last_eval["decision"]
            }

            response = requests.post(f"{API_URL}/ask/", data=payload)

        if response.status_code == 200:

            answer = response.json()["answer"]

            st.session_state.chat_history.append(("user", question))
            st.session_state.chat_history.append(("ai", answer))

        else:
            st.error("❌ Reviewer Agent Failed.")

    # Display Chat History
    st.markdown("---")

    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"<div class='chat-user'>👤 {msg}</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 {msg}</div>",
                        unsafe_allow_html=True)

# ======================================================
# PAGE 3 — HISTORY
# ======================================================
elif page == "📜 Evaluation History":

    st.markdown("<h1 class='big-title'>📜 Evaluation History</h1>",
                unsafe_allow_html=True)

    history = requests.get(f"{API_URL}/history/").json()

    for item in history:

        score = float(item["final_score"])

        # Color logic
        if score >= 85:
            border = "#22C55E"   # Green
        elif score >= 70:
            border = "#EAB308"   # Yellow
        else:
            border = "#EF4444"   # Red

        st.markdown(
            f"""
            <div style="
                background: rgba(255,255,255,0.07);
                padding: 20px;
                border-radius: 16px;
                border-left: 6px solid {border};
                margin-bottom: 15px;
                box-shadow: 0px 8px 20px rgba(0,0,0,0.5);
            ">
                <b style="font-size:18px;">📌 {item['filename']}</b><br><br>

                ⭐ Score: {score:.1f}<br>
                📝 Decision: {item['decision']}<br>
                📅 Date: {item['created_at']}

            </div>
            """,
            unsafe_allow_html=True
        )
