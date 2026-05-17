"""IP-based feature extraction."""

from dataclasses import dataclass

from feature_engine.app.utils.ip_utils import (
    classify_ip,
    determine_connection_direction,
)
from shared.schemas.feature_schema import ConnectionDirection


@dataclass(frozen=True)
class IPFeatures:
    is_private_source: bool
    is_private_destination: bool
    is_public_source: bool
    is_public_destination: bool
    connection_direction: ConnectionDirection


def extract_ip_features(source_ip: str, destination_ip: str) -> IPFeatures:
    """Extract private/public and connection direction features."""
    source = classify_ip(source_ip)
    destination = classify_ip(destination_ip)
    direction = determine_connection_direction(source, destination)
    return IPFeatures(
        is_private_source=source.is_private,
        is_private_destination=destination.is_private,
        is_public_source=source.is_public,
        is_public_destination=destination.is_public,
        connection_direction=direction,
    )
