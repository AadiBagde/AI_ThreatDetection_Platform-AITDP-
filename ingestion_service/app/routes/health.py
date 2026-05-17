from fastapi import APIRouter

from ingestion_service.app.core.config import get_settings
from ingestion_service.app.services import packet_store

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    settings = get_settings()
    return {
        "status": "healthy",
        "service": "ingestion",
        "version": settings.app_version,
        "packets_stored": packet_store.get_packet_count(),
    }
