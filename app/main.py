import logging
from fastapi import FastAPI
from app.api.routes import router as api_router

# --- Logging Configuration ---
# Configure logging to output timestamp, level, and message
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Lovart AI Agent",
    description="Orchestrator for the AI Design Agent, connecting Streamlit UI, Ollama, and A1111.",
    version="1.0.0"
)

# Include the API router
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    """Log application startup"""
    logger.info("Lovart AI application starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """Log application shutdown"""
    logger.info("Lovart AI application shutting down...")

@app.get("/", tags=["Root"])
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"status": "Lovart AI API is running."}
