"""Prediction helper utilities."""

from shared.schemas.prediction_schema import ThreatType


def is_threat_detected(threat_type: str) -> bool:
    return threat_type != ThreatType.BENIGN.value
