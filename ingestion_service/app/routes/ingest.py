from fastapi import APIRouter, HTTPException

from ingestion_service.app.core.logging import get_logger
from ingestion_service.app.services.packet_processor import process_packet
from shared.schemas.packet_schema import PacketIngest, PacketIngestResponse

router = APIRouter(tags=["ingest"])
ingestion_logger = get_logger("ingestion")
error_logger = get_logger("error")


@router.post("/ingest", response_model=PacketIngestResponse)
def ingest_packet(packet: PacketIngest) -> PacketIngestResponse:
    try:
        record = process_packet(packet)
        ingestion_logger.info(
            "Packet ingested | %s -> %s | %s:%s | size=%s | id=%s",
            str(packet.source_ip),
            str(packet.destination_ip),
            packet.protocol.value,
            packet.destination_port,
            packet.packet_size,
            record["id"],
        )
        return PacketIngestResponse()
    except Exception as exc:
        error_logger.exception("Failed to ingest packet: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to process packet") from exc
