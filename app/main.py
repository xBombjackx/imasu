import os
from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import OUTPUT_DIR

app = FastAPI(
    title="Agentic Image Generation API",
    description="An API for generating images using a local agentic system.",
    version="0.1.0",
)

# Ensure the output directory exists on startup
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Include the API router from app/api/routes.py
app.include_router(api_router)


# The root endpoint from your old routes file is now here
@app.get("/")
def read_root():
    return {"message": "Welcome to the Agentic API"}
