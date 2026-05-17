from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field, IPvAnyAddress


class Protocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    OTHER = "OTHER"


class PacketIngest(BaseModel):
    source_ip: IPvAnyAddress = Field(..., description="Source IP address")
    destination_ip: IPvAnyAddress = Field(..., description="Destination IP address")
    source_port: int = Field(..., ge=1, le=65535)
    destination_port: int = Field(..., ge=1, le=65535)
    protocol: Protocol
    packet_size: int = Field(..., gt=0, description="Packet size in bytes")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Packet capture timestamp (UTC)",
    )

    model_config = {"json_schema_extra": {
        "example": {
            "source_ip": "192.168.1.10",
            "destination_ip": "8.8.8.8",
            "source_port": 44321,
            "destination_port": 80,
            "protocol": "TCP",
            "packet_size": 512,
        }
    }}


class PacketIngestResponse(BaseModel):
    status: str = "success"
    message: str = "Packet received"
