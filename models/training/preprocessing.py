"""Feature preprocessing for ML training and inference."""

from __future__ import annotations

from typing import Any

import numpy as np

THREAT_CLASSES = ["benign", "dos", "port_scan", "brute_force", "suspicious"]

CATEGORICAL_FIELDS = (
    "connection_direction",
    "source_port_category",
    "destination_port_category",
)

NUMERIC_FIELDS = (
    "protocol_encoded",
    "packet_size",
    "normalized_packet_size",
    "suspicious_large_packet",
    "is_private_source",
    "is_private_destination",
    "risk_score",
)

FEATURE_NAMES = list(NUMERIC_FIELDS) + [
    "connection_direction_enc",
    "source_port_category_enc",
    "destination_port_category_enc",
]


def build_categorical_encoders(samples: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Build label encoders from training samples."""
    encoders: dict[str, dict[str, int]] = {}
    for field in CATEGORICAL_FIELDS:
        values = sorted({str(sample[field]) for sample in samples})
        encoders[field] = {value: idx for idx, value in enumerate(values)}
    return encoders


def encode_categorical(value: str, encoder: dict[str, int]) -> int:
    """Encode a categorical value; unknown values map to -1."""
    return encoder.get(str(value), -1)


def features_to_array(
    features: dict[str, Any],
    categorical_encoders: dict[str, dict[str, int]],
) -> np.ndarray:
    """Convert a feature dictionary into a model input vector."""
    row: list[float] = [
        float(features["protocol_encoded"]),
        float(features["packet_size"]),
        float(features["normalized_packet_size"]),
        float(int(bool(features["suspicious_large_packet"]))),
        float(int(bool(features["is_private_source"]))),
        float(int(bool(features["is_private_destination"]))),
        float(features["risk_score"]),
        float(
            encode_categorical(
                features["connection_direction"], categorical_encoders["connection_direction"]
            )
        ),
        float(
            encode_categorical(
                features["source_port_category"],
                categorical_encoders["source_port_category"],
            )
        ),
        float(
            encode_categorical(
                features["destination_port_category"],
                categorical_encoders["destination_port_category"],
            )
        ),
    ]
    return np.array(row, dtype=np.float64)
