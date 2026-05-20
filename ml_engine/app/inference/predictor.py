"""End-to-end ML inference pipeline."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ml_engine.app.inference.confidence_engine import calculate_confidence
from ml_engine.app.inference.severity_engine import classify_severity
from ml_engine.app.inference.threat_classifier import map_label_to_threat_type
from ml_engine.app.loaders.model_loader import ModelLoadError, get_artifacts
from ml_engine.app.utils.feature_preprocessing import (
    validate_feature_compatibility,
    validate_feature_vector,
    vectorize_features,
)
from ml_engine.app.utils.prediction_utils import is_threat_detected
from shared.schemas.feature_schema import FeatureVector
from shared.schemas.prediction_schema import PredictionResult, ThreatType


class InferenceError(Exception):
    """Raised when inference cannot be completed."""


@dataclass(frozen=True)
class InferenceResult:
    prediction: PredictionResult
    predicted_label: str
    probabilities: dict[str, float]


def run_inference(features: FeatureVector) -> InferenceResult:
    """
    Run the full inference pipeline:
    validate → vectorize → scale → predict → confidence → severity
    """
    try:
        artifacts = get_artifacts()
        feature_dict = validate_feature_vector(features)
        validate_feature_compatibility(feature_dict)

        X = vectorize_features(feature_dict, artifacts.metadata["categorical_encoders"])
        X_scaled = artifacts.scaler.transform(X)

        predicted_label = str(artifacts.model.predict(X_scaled)[0])
        probabilities = artifacts.model.predict_proba(X_scaled)[0]
        class_names = list(artifacts.model.classes_)
        proba_map = {
            str(cls): float(prob) for cls, prob in zip(class_names, probabilities)
        }

        confidence = calculate_confidence(probabilities)
        threat_type = map_label_to_threat_type(predicted_label)
        severity = classify_severity(confidence, threat_type)

        prediction = PredictionResult(
            threat_detected=is_threat_detected(threat_type.value),
            threat_type=threat_type,
            confidence=round(confidence, 4),
            severity=severity,
        )
        return InferenceResult(
            prediction=prediction,
            predicted_label=predicted_label,
            probabilities=proba_map,
        )
    except ModelLoadError:
        raise
    except Exception as exc:
        raise InferenceError(str(exc)) from exc
