from enum import Enum

from pydantic import BaseModel, Field


class ConnectionDirection(str, Enum):
    OUTBOUND = "outbound"
    INBOUND = "inbound"
    INTERNAL = "internal"
    EXTERNAL = "external"


class FeatureVector(BaseModel):
    """ML-ready feature vector extracted from packet metadata."""

    protocol_encoded: int = Field(
        ...,
        ge=0,
        le=3,
        description="Encoded protocol: TCP=1, UDP=2, ICMP=3, Unknown=0",
    )
    packet_size: int = Field(..., gt=0, description="Raw packet size in bytes")
    normalized_packet_size: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Packet size normalized against MTU (1500 bytes)",
    )
    suspicious_large_packet: bool = Field(
        ...,
        description="True when packet_size exceeds 1500 bytes",
    )
    is_private_source: bool = Field(..., description="Source IP is private")
    is_private_destination: bool = Field(..., description="Destination IP is private")
    source_port_category: str = Field(
        ..., description="Port/service category for source port"
    )
    destination_port_category: str = Field(
        ..., description="Port/service category for destination port"
    )
    connection_direction: ConnectionDirection = Field(
        ..., description="Traffic direction classification"
    )
    risk_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Heuristic risk score between 0.0 and 1.0",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "protocol_encoded": 1,
                "packet_size": 512,
                "normalized_packet_size": 0.341,
                "suspicious_large_packet": False,
                "is_private_source": True,
                "is_private_destination": False,
                "source_port_category": "dynamic",
                "destination_port_category": "web",
                "connection_direction": "outbound",
                "risk_score": 0.25,
            }
        }
    }


class ExtractResponse(BaseModel):
    status: str = "success"
    features: FeatureVector
