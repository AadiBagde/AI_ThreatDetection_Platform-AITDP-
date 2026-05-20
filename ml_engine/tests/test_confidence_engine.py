import numpy as np

from ml_engine.app.inference.confidence_engine import calculate_confidence


def test_confidence_is_max_probability():
    probs = np.array([0.1, 0.7, 0.2])
    assert calculate_confidence(probs) == 0.7


def test_confidence_clamped():
    probs = np.array([1.5, 0.0])
    assert calculate_confidence(probs) == 1.0
