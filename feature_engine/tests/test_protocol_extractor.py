from feature_engine.app.extractors.protocol_extractor import extract_protocol_features
from feature_engine.app.utils.protocol_utils import encode_protocol


def test_encode_protocol_tcp():
    assert encode_protocol("TCP") == 1
    assert encode_protocol("tcp") == 1


def test_encode_protocol_udp():
    assert encode_protocol("UDP") == 2


def test_encode_protocol_icmp():
    assert encode_protocol("ICMP") == 3


def test_encode_protocol_unknown():
    assert encode_protocol("HTTP") == 0
    assert encode_protocol("unknown") == 0


def test_extract_protocol_features():
    features = extract_protocol_features("tcp")
    assert features.protocol_encoded == 1
    assert features.protocol_name == "TCP"
    assert features.is_unknown is False


def test_extract_unknown_protocol():
    features = extract_protocol_features("SCTP")
    assert features.protocol_encoded == 0
    assert features.is_unknown is True
