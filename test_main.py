from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # A mensagem aqui tem que ser IGUALZINHA a do main.py novo
    assert response.json() == {"status": "online", "message": "IsCoolGPT com Gemini AI Ativado!"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}