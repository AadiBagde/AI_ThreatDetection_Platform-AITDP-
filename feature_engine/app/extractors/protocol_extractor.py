"""Protocol encoding feature extraction."""

from dataclasses import dataclass

from feature_engine.app.utils.protocol_utils import encode_protocol, is_unknown_protocol


@dataclass(frozen=True)
class ProtocolFeatures:
    protocol_encoded: int
    protocol_name: str
    is_unknown: bool


def extract_protocol_features(protocol: str) -> ProtocolFeatures:
    """Extract encoded protocol features from raw protocol string."""
    encoded = encode_protocol(protocol)
    normalized = protocol.strip().upper()
    return ProtocolFeatures(
        protocol_encoded=encoded,
        protocol_name=normalized,
        is_unknown=is_unknown_protocol(encoded),
    )
