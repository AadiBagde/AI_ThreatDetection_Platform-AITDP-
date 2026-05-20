from ml_engine.app.inference.severity_engine import classify_severity
from shared.schemas.prediction_schema import Severity, ThreatType


def test_benign_is_low_severity():
    assert classify_severity(0.95, ThreatType.BENIGN) == Severity.LOW


def test_high_confidence_malicious_is_high():
    assert classify_severity(0.91, ThreatType.DOS) == Severity.HIGH


def test_medium_confidence():
    assert classify_severity(0.5, ThreatType.PORT_SCAN) == Severity.MEDIUM


def test_low_confidence():
    assert classify_severity(0.2, ThreatType.SUSPICIOUS) == Severity.LOW
