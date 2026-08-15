from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from therados.main import app
from therados.db.session import get_db

mock_db = AsyncMock()

async def override_get_db():
    yield mock_db

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_models_endpoint():
    mock_res = MagicMock()
    mock_res.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_res

    response = client.get("/api/v1/models")
    assert response.status_code == 200
    providers = response.json()
    assert len(providers) >= 4

def test_integrations_endpoint():
    response = client.get("/api/v1/integrations")
    assert response.status_code == 200
    integrations = response.json()
    assert len(integrations) >= 5

def test_evaluate_smiles_endpoint():
    response = client.post("/api/v1/pharmacology/evaluate-smiles", json={"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O"})
    assert response.status_code == 200
    data = response.json()
    assert data["valid_smiles"] is True

def test_safety_gate_endpoint():
    response = client.post("/api/v1/pharmacology/safety-gate", params={"herg": "HIGH"})
    assert response.status_code == 200
    data = response.json()
    assert data["passed"] is False

def test_copilot_endpoint():
    mock_res = MagicMock()
    mock_res.scalar_one_or_none.return_value = None
    mock_res.scalars.return_value.all.return_value = []
    mock_db.execute.return_value = mock_res

    response = client.post("/api/v1/copilot/query", json={"program_id": "prog-test", "query": "Why did H1 rank higher?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
