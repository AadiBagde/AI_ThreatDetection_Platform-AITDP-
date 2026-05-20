"""Map model class labels to threat types."""

from shared.schemas.prediction_schema import ThreatType


def map_label_to_threat_type(label: str) -> ThreatType:
    """Convert sklearn class label to ThreatType enum."""
    normalized = label.strip().lower()
    try:
        return ThreatType(normalized)
    except ValueError:
        return ThreatType.SUSPICIOUS
