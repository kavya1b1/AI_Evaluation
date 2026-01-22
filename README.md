🤖 AI Proposal Evaluation System

An end-to-end AI-powered decision support system that automatically evaluates R&D / research proposals using Machine Learning, Explainable AI (XAI), Uncertainty Estimation, and Generative AI, and generates a professional evaluation report.

🚩 Problem Statement

Manual evaluation of research and R&D proposals is often:

⏳ Time-consuming

⚖️ Subjective and inconsistent

❌ Lacking transparency

📄 Poorly documented

As a result, funding agencies, academic institutions, and innovation boards struggle to scale proposal evaluation while maintaining fairness and explainability.

💡 Our Solution

We designed and built an AI Proposal Evaluation System that:

📄 Analyzes proposal PDFs automatically

📊 Scores novelty, feasibility, and financial alignment

📈 Estimates prediction confidence and risk

🧠 Explains decisions using Explainable AI (XAI & SHAP)

🤖 Generates human-readable AI evaluation narratives

📑 Produces professional, downloadable PDF reports

🧠 System Architecture
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
     ├── Budget & Financial Feasibility Check
     ├── ML Ensemble Evaluation
     ├── Uncertainty & Confidence Estimation
     ├── Explainable AI (Feature Importance + SHAP)
     ├── Generative AI Narrative
     ├── PDF Report Generation
     │
     ▼
SQLite Database (Evaluation History)

✨ Key Features
📄 Proposal Upload & Parsing

Accepts PDF proposals

Extracts and processes text automatically

📊 ML-Based Evaluation

Ensemble-based scoring model

Produces a final score (0–100)

💰 Budget Analysis (Why Budget Matters)

Budget is not optional input.

It is used to:

Check feasibility against expected funding norms

Penalize unrealistic or risky budgets

Balance innovation with financial practicality

📌 A strong idea with an unrealistic budget increases project risk — the model captures this trade-off.

📈 Confidence & Uncertainty Estimation

Outputs confidence bands (lower, mean, upper)

Indicates reliability of predictions

Helps decision-makers understand risk

🧠 Explainable AI (XAI)

Feature importance visualization

SHAP-based local explanations

Answers: “Why did the model give this score?”

🤖 Generative AI Narrative

Automatically generates a human-readable evaluation

Summarizes strengths, weaknesses, and recommendations

Makes reports reviewer-ready

📄 Automated PDF Report

Each evaluation produces a professional PDF containing:

Evaluation scores

Funding recommendation

Explainable AI insights

Confidence & risk analysis

AI-generated narrative

🕒 Evaluation History

Stores past evaluations

Displays a timeline with scores and decisions

🛠️ Tech Stack
Frontend

Streamlit

Plotly

Custom CSS (glassmorphism UI)

Backend

FastAPI

SQLAlchemy

SQLite

Machine Learning

Scikit-learn

Ensemble scoring logic

Sampling-based uncertainty estimation

Explainable AI

Feature Importance

SHAP

Generative AI

LLM-based evaluation narrative generation

Reporting

ReportLab (PDF generation)

📂 Project Structure
AI_Proposal_Evaluator/
│
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
│   ├── schemas.py
│   └── main.py
│
├── frontend/
│   └── dashboard.py
│
├── ml/
│   ├── train_model.py
│   ├── embedding_model.py
│   └── vector_store.py
│
├── data/
│   └── past_projects.csv
│
├── requirements.txt
├── .gitignore
└── README.md

🚀 How to Run Locally
1️⃣ Clone the Repository
git clone https://github.com/your-username/AI_Proposal_Evaluator.git
cd AI_Proposal_Evaluator

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Start Backend
uvicorn backend.main:app --reload

5️⃣ Start Frontend
streamlit run frontend/dashboard.py
