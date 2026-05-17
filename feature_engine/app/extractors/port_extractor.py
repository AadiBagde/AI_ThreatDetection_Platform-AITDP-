"""Port categorization feature extraction."""

from dataclasses import dataclass

SERVICE_PORT_CATEGORIES: dict[int, str] = {
    80: "web",
    443: "secure_web",
    22: "ssh",
    21: "ftp",
    53: "dns",
    25: "smtp",
}


@dataclass(frozen=True)
class PortFeatures:
    source_port_category: str
    destination_port_category: str


def _categorize_port(port: int) -> str:
    """Classify a port by well-known service or numeric range."""
    if port in SERVICE_PORT_CATEGORIES:
        return SERVICE_PORT_CATEGORIES[port]
    if port <= 1023:
        return "system"
    if port <= 49151:
        return "user"
    return "dynamic"


def extract_port_features(source_port: int, destination_port: int) -> PortFeatures:
    """Extract source and destination port category features."""
    return PortFeatures(
        source_port_category=_categorize_port(source_port),
        destination_port_category=_categorize_port(destination_port),
    )
