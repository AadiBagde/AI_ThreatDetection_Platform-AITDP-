from feature_engine.app.extractors.ip_extractor import extract_ip_features
from feature_engine.app.utils.ip_utils import classify_ip
from shared.schemas.feature_schema import ConnectionDirection


def test_classify_private_ip():
    result = classify_ip("192.168.1.10")
    assert result.is_private is True
    assert result.is_public is False


def test_classify_public_ip():
    result = classify_ip("8.8.8.8")
    assert result.is_private is False
    assert result.is_public is True


def test_outbound_connection():
    features = extract_ip_features("192.168.1.10", "8.8.8.8")
    assert features.is_private_source is True
    assert features.is_private_destination is False
    assert features.connection_direction == ConnectionDirection.OUTBOUND


def test_internal_connection():
    features = extract_ip_features("10.0.0.1", "10.0.0.2")
    assert features.connection_direction == ConnectionDirection.INTERNAL


def test_external_connection():
    features = extract_ip_features("8.8.8.8", "1.1.1.1")
    assert features.connection_direction == ConnectionDirection.EXTERNAL
