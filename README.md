<p align="center">
  <img src="assets:demo.gif" width="800"/>
</p>
🤖 AI Proposal Evaluation System
--------------------------------------------------------------------------------------------------------------

An end-to-end AI-powered decision support system for automated R&D proposal evaluation

This system evaluates research and innovation proposals using Machine Learning, Explainable AI (XAI), Uncertainty Estimation, and Generative AI, producing transparent scores, confidence estimates, and professional PDF reports.

🚩 Problem Statement
--------------------------------------------------------------------------------------------------------------

Manual evaluation of R&D and research proposals is often:

⏳ Time-consuming

⚖️ Subjective and inconsistent

❌ Lacking transparency

📄 Poorly documented

As proposal volumes grow, funding agencies and institutions need a scalable, objective, and explainable evaluation system.

💡 Our Solution
--------------------------------------------------------------------------------------------------------------

We built an AI Proposal Evaluation System that:

📄 Automatically parses proposal PDFs

🧠 Scores novelty, feasibility, and financial alignment

📊 Uses ML ensembles with uncertainty estimation

🔍 Explains decisions using XAI & SHAP

🤖 Generates human-readable AI narratives

📑 Produces downloadable professional PDF reports

🏗️ System Architecture
--------------------------------------------------------------------------------------------------------------
```
User (Browser)
   │
   ▼
Streamlit Frontend (dashboard.py)
   │
   ▼
FastAPI Backend (proposal_routes.py)
   │
   ├── PDF Parsing & Text Extraction
   ├── Novelty Analysis
   ├── Budget & Financial Check
   ├── ML Ensemble Evaluation
   ├── Uncertainty & Confidence Estimation
   ├── Explainable AI (Feature Importance + SHAP)
   ├── GenAI Narrative Generation
   └── PDF Report Generation
```
⚙️ Technology Stack
--------------------------------------------------------------------------------------------------------------
🔹 Backend
--------------------------------------------------------------------------------------------------------------

FastAPI

SQLAlchemy + SQLite

ReportLab (PDF generation)

🔹 Machine Learning
--------------------------------------------------------------------------------------------------------------

Scikit-learn

Ensemble scoring logic

Sampling-based uncertainty estimation

🔹 Explainable AI
--------------------------------------------------------------------------------------------------------------

Feature importance

SHAP (local explanations)

🔹 Generative AI
--------------------------------------------------------------------------------------------------------------

LLM-based evaluation narrative generation

🔹 Frontend
--------------------------------------------------------------------------------------------------------------

Streamlit

Plotly (interactive visualizations)

📥 Inputs
--------------------------------------------------------------------------------------------------------------
Input	Purpose
Proposal PDF	Main document for evaluation
Budget (₹)	Used to assess financial feasibility
❓ Why Budget Matters

Budget influences:

Financial feasibility score

Overall ML score weighting

Risk & confidence estimation

If budget is missing, the model still works — but financial realism cannot be evaluated, reducing decision quality.

📤 Outputs
--------------------------------------------------------------------------------------------------------------
✅ Final AI score (0–100)

📊 Confidence interval & uncertainty band

🧠 Explainable feature contributions

🤖 AI-generated evaluation narrative

📄 Downloadable PDF report

🕒 Evaluation history timeline

📂## 📁 Project Structure
---

```text
AI_Evaluation/
├── backend/
│   ├── api/
│   │   └── proposal_routes.py
│   ├── services/
│   │   ├── document_parser.py
│   │   ├── novelty_engine.py
│   │   ├── financial_checker.py
│   │   ├── ml_evaluator.py
│   │   ├── uncertainty.py
│   │   ├── explainability.py
│   │   ├── shap_explainer.py
│   │   ├── genai_narrative.py
│   │   └── report_generator.py
│   ├── database.py
│   ├── models.py
│   └── main.py
│
├── frontend/
│   └── dashboard.py
│
├── ml/
│   ├── train_model.py
│   ├── embedding_model.py
│   ├── vector_store.py
│   └── evaluator_model.pkl
│
├── data/
│   └── past_projects.csv
│
├── reports/        # Generated PDFs (ignored in Git)
├── uploads/        # Uploaded proposal PDFs (ignored in Git)
│
├── requirements.txt
├── .gitignore
└── README.md

```
🚀 How to Run Locally
--------------------------------------------------------------------------------------------------------------
```
1️⃣ Clone Repository
git clone https://github.com/your-username/AI_Evaluation.git
cd AI_Evaluation
```
```
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
```
3️⃣ Install Dependencies
pip install -r requirements.txt
```
```
4️⃣ Start Backend
uvicorn backend.main:app --reload
```
```
5️⃣ Start Frontend
streamlit run frontend/dashboard.py
```
📄 Reports & Storage
--------------------------------------------------------------------------------------------------------------
Uploaded PDFs → uploads/

Generated reports → reports/

Evaluation metadata → SQLite database

These folders are excluded from GitHub using .gitignore.

🔒 What to Ignore in GitHub
--------------------------------------------------------------------------------------------------------------
Add this to .gitignore:
```
__pycache__/
*.pyc
venv/
uploads/
reports/
proposals.db
*.pkl
.env
```
🧠 Key Highlights
--------------------------------------------------------------------------------------------------------------
End-to-end AI pipeline

Explainable & auditable decisions

Confidence-aware ML predictions

Professional reporting

Clean, modular architecture

👩‍💻 Author
--------------------------------------------------------------------------------------------------------------

Kavya Gupta
B.Tech | AI & ML | Full-Stack Development
