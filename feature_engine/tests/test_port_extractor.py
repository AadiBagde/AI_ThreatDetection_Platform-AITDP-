from feature_engine.app.extractors.port_extractor import extract_port_features


def test_web_port_category():
    features = extract_port_features(44321, 80)
    assert features.destination_port_category == "web"


def test_secure_web_port():
    features = extract_port_features(1024, 443)
    assert features.destination_port_category == "secure_web"


def test_dynamic_source_port():
    features = extract_port_features(50000, 80)
    assert features.source_port_category == "dynamic"


def test_system_port():
    features = extract_port_features(22, 80)
    assert features.source_port_category == "ssh"
