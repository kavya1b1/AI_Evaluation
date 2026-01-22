from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.api.proposal_routes import router
from backend.database import Base, engine
from ml.vector_store import load_past_projects

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app FIRST
app = FastAPI(title="AI Proposal Evaluation System")

# Mount static folders AFTER app is created
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Include API routes
app.include_router(router)

# Load vector DB on startup
@app.on_event("startup")
def startup_event():
    load_past_projects()
