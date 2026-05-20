"""Map confidence scores to severity levels."""

from shared.schemas.prediction_schema import Severity, ThreatType


def classify_severity(confidence: float, threat_type: ThreatType) -> Severity:
    """
    Map confidence to severity.

    0.0-0.3 -> low, 0.3-0.7 -> medium, 0.7-1.0 -> high.
    Benign traffic is always low severity.
    """
    if threat_type == ThreatType.BENIGN:
        return Severity.LOW

    if confidence < 0.3:
        return Severity.LOW
    if confidence < 0.7:
        return Severity.MEDIUM
    return Severity.HIGH
