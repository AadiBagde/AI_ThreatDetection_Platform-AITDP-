"""Feature vector preprocessing for ML inference."""

from __future__ import annotations

from typing import Any

import numpy as np

from models.training.preprocessing import FEATURE_NAMES, features_to_array
from shared.schemas.feature_schema import FeatureVector


def validate_feature_vector(features: FeatureVector) -> dict[str, Any]:
    """Convert and validate a feature vector for inference."""
    payload = features.model_dump(mode="json")
    payload["connection_direction"] = features.connection_direction.value
    return payload


def vectorize_features(
    features: dict[str, Any],
    categorical_encoders: dict[str, dict[str, int]],
) -> np.ndarray:
    """Transform features into a scaled-ready numpy row."""
    return features_to_array(features, categorical_encoders).reshape(1, -1)


REQUIRED_FEATURE_KEYS = (
    "protocol_encoded",
    "packet_size",
    "normalized_packet_size",
    "suspicious_large_packet",
    "is_private_source",
    "is_private_destination",
    "source_port_category",
    "destination_port_category",
    "connection_direction",
    "risk_score",
)


def validate_feature_compatibility(features: dict[str, Any]) -> None:
    """Ensure all required features are present before inference."""
    missing = [key for key in REQUIRED_FEATURE_KEYS if key not in features]
    if missing:
        raise ValueError(f"Missing required features: {missing}")
