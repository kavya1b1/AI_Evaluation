import streamlit as st
import requests
import time

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="AI Proposal Evaluation System",
    layout="wide",
)

API_URL = "http://localhost:8000"


# ---------------- SIDEBAR NAVBAR ----------------
st.sidebar.title("📌 AI Proposal Evaluator")
st.sidebar.markdown("Navigate through the system:")

page = st.sidebar.radio(
    "Go To",
    [
        "🏠 Home (Evaluate Proposal)",
        "🤖 Reviewer Agent (Q&A Chat)",
        "📜 Evaluation History"
    ]
)


# ======================================================
# 🏠 PAGE 1 — HOME (PROPOSAL EVALUATION)
# ======================================================
if page == "🏠 Home (Evaluate Proposal)":

    st.title("📄 AI Proposal Evaluation System")
    st.caption(
        "Evaluate research proposals using ML Ensembles, Explainable AI, "
        "Novelty Benchmarking, and Generative AI Narratives."
    )

    st.markdown("---")

    # ---------------- INPUT SECTION ----------------
    st.subheader("📌 Submit Proposal")

    file = st.file_uploader("Upload Proposal PDF", type=["pdf"])

    budget = st.number_input(
        "💰 Proposed Budget (₹)",
        min_value=100000.0,
        max_value=5000000.0,
        step=50000.0,
        help="Budget must be between ₹1,00,000 and ₹50,00,000"
    )

    # ---------------- EVALUATE BUTTON ----------------
    if st.button("🚀 Run AI Evaluation"):

        if file is None:
            st.warning("⚠️ Please upload a proposal PDF first.")
        else:
            with st.spinner("🧠 Running AI Evaluation Pipeline..."):
                time.sleep(1)

                response = requests.post(
                    f"{API_URL}/submit/",
                    files={"file": file},
                    data={"budget": budget}
                )

            # ---------------- RESPONSE ----------------
            if response.status_code == 200:
                data = response.json()

                st.success("✅ Proposal Evaluated Successfully!")

                st.markdown("---")

                # ---------------- METRICS ----------------
                c1, c2, c3 = st.columns(3)

                c1.metric("Final Score", f"{data['final_score']:.1f}/100")
                c2.metric("Novelty Score", f"{data['novelty']:.1f}")
                c3.metric("Finance Score", f"{data['finance']:.1f}")

                st.info(f"📌 Decision: **{data['decision']}**")

                # ---------------- SIMILAR PROJECTS ----------------
                if "similar_projects" in data:
                    st.subheader("🔍 Novelty Benchmarking")

                    for proj in data["similar_projects"]:
                        st.write(
                            f"📌 **{proj['project']}** "
                            f"(Similarity: `{proj['similarity']}`)"
                        )

                # ---------------- FINANCE VIOLATIONS ----------------
                if "violations" in data and len(data["violations"]) > 0:
                    st.subheader("⚠️ Financial Violations")

                    for v in data["violations"]:
                        st.error(v)

                # ---------------- AI NARRATIVE ----------------
                st.subheader("🤖 AI Evaluation Narrative")
                st.write(data["ai_report_text"])

                # ---------------- DOWNLOAD REPORT ----------------
                st.subheader("📄 Download Evaluation Report")

                st.markdown(
                    f"""
                    <a href="{data['report_url']}" target="_blank"
                    style="display:inline-block;
                    padding:14px 22px;
                    background:#4F46E5;
                    color:white;
                    border-radius:10px;
                    text-decoration:none;
                    font-weight:600;">
                    ⬇️ Download PDF Report
                    </a>
                    """,
                    unsafe_allow_html=True
                )

            else:
                try:
                    st.error("❌ Evaluation Failed")
                    st.warning(response.json()["detail"])
                except:
                    st.error("Something went wrong. Backend not responding.")


# ======================================================
# 🤖 PAGE 2 — REVIEWER AGENT CHATBOT
# ======================================================
elif page == "🤖 Reviewer Agent (Q&A Chat)":

    st.title("🤖 Reviewer Agent Chat")
    st.caption(
        "Ask questions about the last evaluated proposal. "
        "This agent uses GenAI reasoning over proposal + evaluation summary."
    )

    st.markdown("---")

    question = st.text_input("💬 Ask your question:")

    if st.button("Ask Reviewer"):

        if question.strip() == "":
            st.warning("⚠️ Please type a question first.")
        else:
            with st.spinner("Thinking... 🤖"):
                response = requests.post(
                    f"{API_URL}/ask/",
                    data={"question": question}
                )

            if response.status_code == 200:
                answer = response.json()["answer"]

                st.success("✅ Reviewer Response:")
                st.write(answer)

            else:
                st.error("❌ Reviewer Agent Failed")
                st.warning(response.json()["detail"])


# ======================================================
# 📜 PAGE 3 — EVALUATION HISTORY
# ======================================================
elif page == "📜 Evaluation History":

    st.title("📜 Evaluation History Timeline")
    st.caption("Shows the last 10 evaluated proposals stored in database.")

    st.markdown("---")

    try:
        history = requests.get(f"{API_URL}/history/").json()

        if len(history) == 0:
            st.info("No evaluations found yet.")
        else:
            for item in history:

                color = (
                    "green" if item["final_score"] >= 85
                    else "orange" if item["final_score"] >= 70
                    else "red"
                )

                st.markdown(
                    f"""
                    <div style="
                        padding:15px;
                        margin-bottom:12px;
                        border-radius:12px;
                        border-left:6px solid {color};
                        background:rgba(240,240,240,0.05);
                    ">
                        <b>📄 {item['filename']}</b><br>
                        🕒 {item['created_at']}<br>
                        ⭐ Score: <b>{item['final_score']:.1f}</b><br>
                        📌 Decision: <b>{item['decision']}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    except:
        st.error("❌ Could not load history. Backend might not be running.")
