"""Confidence scoring from model probabilities."""

from __future__ import annotations

import numpy as np


def calculate_confidence(probabilities: np.ndarray) -> float:
    """
    Return the highest class probability as confidence.

    Clamped to [0.0, 1.0].
    """
    confidence = float(np.max(probabilities))
    return max(0.0, min(confidence, 1.0))
