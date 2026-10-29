"""Basic API tests; these tests do not call an LLM."""
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200

def test_unknown_document_is_404():
    response = client.get("/api/resume/not-a-real-id")
    assert response.status_code == 404

def test_rejects_txt_file():
    response = client.post("/api/upload", files={"file": ("resume.txt", b"hello", "text/plain")})
    assert response.status_code == 400
