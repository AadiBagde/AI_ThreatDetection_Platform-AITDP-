"""Structured prediction logging service."""

from ml_engine.app.core.logging import get_logger

prediction_logger = get_logger("prediction")
error_logger = get_logger("error")


def log_prediction_success(
    *,
    threat_type: str,
    confidence: float,
    severity: str,
    latency_ms: float,
    threat_detected: bool,
) -> None:
    prediction_logger.info(
        "Threat predicted | detected=%s | type=%s | confidence=%.2f | severity=%s | latency=%.2fms",
        threat_detected,
        threat_type,
        confidence,
        severity,
        latency_ms,
    )


def log_prediction_failure(reason: str, latency_ms: float) -> None:
    error_logger.error(
        "Prediction failed | reason=%s | latency=%.2fms", reason, latency_ms
    )


def log_malformed_features(errors: object) -> None:
    error_logger.warning("Malformed feature vector | errors=%s", errors)


def log_model_loaded(model_version: str, model_type: str, accuracy: float | None) -> None:
    prediction_logger.info(
        "Model loaded | version=%s | type=%s | test_accuracy=%s",
        model_version,
        model_type,
        accuracy,
    )
