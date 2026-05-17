from fastapi import APIRouter

from feature_engine.app.core.config import get_settings
from feature_engine.app.services import feature_store

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()
    return {
        "status": "healthy",
        "service": "feature-engine",
        "version": settings.app_version,
        "features_extracted": feature_store.get_feature_count(),
    }
