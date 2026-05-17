from typing import Any

from shared.schemas.packet_schema import PacketIngest

from ingestion_service.app.services import packet_store


def process_packet(packet: PacketIngest) -> dict[str, Any]:
    record = packet.model_dump(mode="json")
    packet_id = packet_store.store_packet(record)
    record["id"] = packet_id
    return record
