import time

from fastapi import APIRouter, HTTPException

from ml_engine.app.inference.predictor import InferenceError, run_inference
from ml_engine.app.loaders.model_loader import ModelLoadError
from ml_engine.app.services import prediction_store
from ml_engine.app.services.prediction_logger import (
    log_prediction_failure,
    log_prediction_success,
)
from shared.schemas.feature_schema import FeatureVector
from shared.schemas.prediction_schema import PredictRequest, PredictResponse

router = APIRouter(tags=["predict"])


@router.post("/predict", response_model=PredictResponse)
def predict_threat(body: PredictRequest) -> PredictResponse:
    """Run ML inference on a feature vector and return threat intelligence."""
    return _predict(body.features)


@router.post("/predict/features", response_model=PredictResponse, include_in_schema=False)
def predict_threat_direct(features: FeatureVector) -> PredictResponse:
    """Alternate endpoint accepting a flat feature vector."""
    return _predict(features)


def _predict(features: FeatureVector) -> PredictResponse:
    start = time.perf_counter()
    try:
        result = run_inference(features)
        latency_ms = (time.perf_counter() - start) * 1000

        prediction_store.store_prediction(result.prediction.model_dump(mode="json"))
        log_prediction_success(
            threat_type=result.prediction.threat_type.value,
            confidence=result.prediction.confidence,
            severity=result.prediction.severity.value,
            latency_ms=latency_ms,
            threat_detected=result.prediction.threat_detected,
        )
        return PredictResponse(prediction=result.prediction)

    except ModelLoadError as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        log_prediction_failure(str(exc), latency_ms)
        raise HTTPException(status_code=503, detail="ML model not loaded") from exc
    except InferenceError as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        log_prediction_failure(str(exc), latency_ms)
        raise HTTPException(
            status_code=422, detail=f"Inference failed: {exc}"
        ) from exc
    except Exception as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        log_prediction_failure(str(exc), latency_ms)
        raise HTTPException(
            status_code=500, detail="Internal prediction error"
        ) from exc
