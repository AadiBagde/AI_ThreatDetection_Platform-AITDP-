import time

from fastapi import APIRouter, HTTPException

from feature_engine.app.core.logging import get_logger
from feature_engine.app.processors.feature_pipeline import (
    FeatureExtractionError,
    run_feature_pipeline,
)
from feature_engine.app.services import feature_store
from shared.schemas.feature_schema import ExtractResponse
from shared.schemas.packet_schema import PacketIngest

router = APIRouter(tags=["extract"])
extraction_logger = get_logger("extraction")
error_logger = get_logger("error")


@router.post("/extract", response_model=ExtractResponse)
def extract_features(packet: PacketIngest) -> ExtractResponse:
    """Validate packet metadata, extract ML-ready features, and return vector."""
    start = time.perf_counter()
    protocol_label = packet.protocol.value

    try:
        features = run_feature_pipeline(packet)
        feature_store.store_features(features.model_dump(mode="json"))
        duration_ms = (time.perf_counter() - start) * 1000

        if features.suspicious_large_packet:
            extraction_logger.warning(
                "Suspicious large packet detected | size=%s | protocol=%s",
                features.packet_size,
                protocol_label,
            )

        if features.protocol_encoded == 0:
            extraction_logger.warning(
                "Unknown protocol encoded | protocol=%s", protocol_label
            )

        extraction_logger.info(
            "Features extracted successfully | protocol=%s | direction=%s | "
            "risk_score=%.2f | extraction_time=%.2fms | "
            "src=%s:%s -> dst=%s:%s",
            protocol_label,
            features.connection_direction.value,
            features.risk_score,
            duration_ms,
            packet.source_ip,
            packet.source_port,
            packet.destination_ip,
            packet.destination_port,
        )

        return ExtractResponse(features=features)

    except FeatureExtractionError as exc:
        duration_ms = (time.perf_counter() - start) * 1000
        error_logger.error(
            "Feature extraction failed | reason=%s | extraction_time=%.2fms",
            exc,
            duration_ms,
        )
        raise HTTPException(
            status_code=422,
            detail=f"Feature extraction failed: {exc}",
        ) from exc
    except Exception as exc:
        duration_ms = (time.perf_counter() - start) * 1000
        error_logger.exception(
            "Unexpected extraction error | extraction_time=%.2fms", duration_ms
        )
        raise HTTPException(
            status_code=500,
            detail="Internal feature extraction error",
        ) from exc
