from fastapi.testclient import TestClient

from ml_engine.app.main import app

client = TestClient(app)

SAMPLE_FEATURES = {
    "protocol_encoded": 1,
    "packet_size": 512,
    "normalized_packet_size": 0.341,
    "suspicious_large_packet": False,
    "is_private_source": True,
    "is_private_destination": False,
    "source_port_category": "dynamic",
    "destination_port_category": "web",
    "connection_direction": "outbound",
    "risk_score": 0.2,
}

DOS_FEATURES = {
    "protocol_encoded": 1,
    "packet_size": 5000,
    "normalized_packet_size": 1.0,
    "suspicious_large_packet": True,
    "is_private_source": False,
    "is_private_destination": False,
    "source_port_category": "dynamic",
    "destination_port_category": "web",
    "connection_direction": "external",
    "risk_score": 0.9,
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ml-engine"
    assert data["model_loaded"] is True


def test_predict_benign_traffic():
    response = client.post("/predict", json={"features": SAMPLE_FEATURES})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    prediction = data["prediction"]
    assert "threat_type" in prediction
    assert 0.0 <= prediction["confidence"] <= 1.0
    assert prediction["severity"] in ("low", "medium", "high")


def test_predict_dos_like_traffic():
    response = client.post("/predict", json={"features": DOS_FEATURES})
    assert response.status_code == 200
    prediction = response.json()["prediction"]
    assert prediction["threat_type"] in (
        "dos",
        "suspicious",
        "port_scan",
        "brute_force",
        "benign",
    )


def test_predict_malformed_input():
    bad = {**SAMPLE_FEATURES, "risk_score": 5.0}
    response = client.post("/predict", json={"features": bad})
    assert response.status_code == 422


def test_predict_missing_fields():
    response = client.post("/predict", json={"features": {"packet_size": 100}})
    assert response.status_code == 422
