from fastapi import APIRouter

from ml_engine.app.core.config import get_settings
from ml_engine.app.loaders.model_loader import ModelLoadError, get_artifacts
from ml_engine.app.services import prediction_store

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()
    model_loaded = True
    model_version = None
    try:
        artifacts = get_artifacts()
        model_version = artifacts.metadata.get("model_version")
    except ModelLoadError:
        model_loaded = False

    return {
        "status": "healthy",
        "service": "ml-engine",
        "version": settings.app_version,
        "model_loaded": model_loaded,
        "model_version": model_version,
        "predictions_served": prediction_store.get_prediction_count(),
    }
