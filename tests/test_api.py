from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Tests the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Agentic API"}
