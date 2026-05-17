"""Traffic volume feature extraction."""

from dataclasses import dataclass

from feature_engine.app.utils.protocol_utils import MTU_BYTES


@dataclass(frozen=True)
class TrafficFeatures:
    packet_size: int
    normalized_packet_size: float
    suspicious_large_packet: bool


def extract_traffic_features(packet_size: int) -> TrafficFeatures:
    """Extract packet size and anomaly indicators."""
    normalized = min(packet_size / MTU_BYTES, 1.0)
    suspicious = packet_size > MTU_BYTES
    return TrafficFeatures(
        packet_size=packet_size,
        normalized_packet_size=round(normalized, 4),
        suspicious_large_packet=suspicious,
    )
