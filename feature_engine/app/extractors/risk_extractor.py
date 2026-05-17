"""Heuristic risk scoring for extracted packet features."""

from feature_engine.app.utils.protocol_utils import SENSITIVE_DESTINATION_CATEGORIES
from shared.schemas.feature_schema import ConnectionDirection


def extract_risk_score(
    *,
    connection_direction: ConnectionDirection,
    suspicious_large_packet: bool,
    protocol_encoded: int,
    destination_port_category: str,
) -> float:
    """
    Compute a heuristic risk score between 0.0 and 1.0.

    Scoring:
    - external/outbound connection: +0.2
    - suspicious packet size: +0.3
    - unknown protocol: +0.2
    - sensitive destination port: +0.2
    """
    score = 0.0

    if connection_direction in (
        ConnectionDirection.OUTBOUND,
        ConnectionDirection.EXTERNAL,
    ):
        score += 0.2

    if suspicious_large_packet:
        score += 0.3

    if protocol_encoded == 0:
        score += 0.2

    if destination_port_category in SENSITIVE_DESTINATION_CATEGORIES:
        score += 0.2

    return min(score, 1.0)
