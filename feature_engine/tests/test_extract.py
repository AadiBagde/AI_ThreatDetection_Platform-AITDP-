from fastapi.testclient import TestClient

from feature_engine.app.main import app

client = TestClient(app)

SAMPLE_PACKET = {
    "source_ip": "192.168.1.10",
    "destination_ip": "8.8.8.8",
    "source_port": 44321,
    "destination_port": 80,
    "protocol": "TCP",
    "packet_size": 512,
}


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "feature-engine"


def test_extract_endpoint_success():
    response = client.post("/extract", json=SAMPLE_PACKET)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    features = data["features"]
    assert features["protocol_encoded"] == 1
    assert features["packet_size"] == 512
    assert features["is_private_source"] is True
    assert features["is_private_destination"] is False
    assert features["destination_port_category"] == "web"
    assert features["connection_direction"] == "outbound"
    assert 0.0 <= features["risk_score"] <= 1.0


def test_extract_invalid_ip():
    bad_packet = {**SAMPLE_PACKET, "source_ip": "not-an-ip"}
    response = client.post("/extract", json=bad_packet)
    assert response.status_code == 422


def test_extract_missing_fields():
    response = client.post("/extract", json={"source_ip": "192.168.1.10"})
    assert response.status_code == 422
