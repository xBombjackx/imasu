import os
from fastapi import FastAPI
from app.api.routes import router
from app.core.config import OUTPUT_DIR

app = FastAPI(
    title="Agentic Image Generation API",
    description="An API for generating images using a local agentic system.",
    version="0.1.0",
)

# Include the API router
app.include_router(router)

# Create the output directory on startup
os.makedirs(OUTPUT_DIR, exist_ok=True)
