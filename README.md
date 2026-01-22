🤖 AI Proposal Evaluation System

An end-to-end AI-powered decision support system that automatically evaluates R&D / research proposals using Machine Learning, Explainable AI (XAI), Uncertainty Estimation, and Generative AI, and generates a professional evaluation report.

📌 Problem Statement

Manual evaluation of research and R&D proposals is:

⏳ Time-consuming

⚖️ Subjective and inconsistent

❌ Lacking transparency

📄 Poorly documented

Funding agencies, academic institutions, and innovation boards need a scalable, explainable, and objective system that can:

Assess proposal quality

Justify decisions transparently

Estimate confidence and risk

Generate professional evaluation reports

💡 Our Solution

We built an AI Proposal Evaluation System that:

✔️ Analyzes proposal PDFs
✔️ Scores novelty, feasibility, and financial alignment
✔️ Uses ML ensembles with uncertainty estimation
✔️ Explains decisions using Explainable AI & SHAP
✔️ Generates AI-written evaluation narratives
✔️ Produces downloadable PDF reports
✔️ Provides an interactive, modern dashboard

🧠 System Architecture
User (Browser)
     │
     ▼
Streamlit Frontend (dashboard.py)
     │
     ▼
FastAPI Backend (proposal_routes.py)
     │
     ├── Document Parsing (PDF → Text)
     ├── Novelty Analysis
     ├── Financial Feasibility Check (Budget)
     ├── ML Evaluation + Uncertainty
     ├── Explainable AI (Feature Importance + SHAP)
     ├── Generative AI Narrative
     ├── PDF Report Generation
     │
     ▼
SQLite Database (Evaluation History)

🧩 Key Features
📄 Proposal Upload & Parsing

Accepts proposal PDFs

Extracts and processes text automatically

📊 ML-Based Evaluation

Ensemble-based scoring model

Outputs final score (0–100)

💰 Budget Analysis (Why Budget Matters)

Budget is not optional noise — it directly impacts feasibility.

It is used to:

Check alignment with funding norms

Penalize unrealistic budgets

Balance innovation vs practicality

📌 A great idea with an unrealistic budget is risky — the model captures this trade-off.

📈 Confidence & Uncertainty Estimation

Produces a confidence band (lower, mean, upper)

Shows how reliable the prediction is

Helps decision-makers understand risk

🧠 Explainable AI (XAI)

Feature importance for transparency

SHAP explanations for local predictions

Answers: “Why did the model give this score?”

🤖 Generative AI Narrative

Automatically generates a human-readable evaluation

Explains strengths, weaknesses, and recommendations

Makes reports reviewer-ready

📄 Automated PDF Report

Each evaluation produces a professional PDF containing:

Scores

Decision

Explainable AI insights

Confidence & risk

AI-generated narrative

🕒 Evaluation History

Stores past evaluations

Displays timeline with scores & decisions

🛠️ Tech Stack
Frontend

Streamlit

Plotly (interactive charts)

Custom CSS (glassmorphism UI)

Backend

FastAPI

SQLAlchemy

SQLite

Machine Learning

Scikit-learn

Ensemble scoring logic

Confidence estimation via sampling

Explainable AI

Feature Importance

SHAP

Generative AI

LLM-based narrative generation (via API)

Reporting

ReportLab (PDF generation)
