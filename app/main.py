from fastapi import FastAPI
from app.api.routes import router as api_router

app = FastAPI()

# The "/api" prefix has been removed to fix the 404 error.
app.include_router(api_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
