from enum import Enum

from pydantic import BaseModel, Field

from shared.schemas.feature_schema import FeatureVector


class ThreatType(str, Enum):
    BENIGN = "benign"
    DOS = "dos"
    PORT_SCAN = "port_scan"
    BRUTE_FORCE = "brute_force"
    SUSPICIOUS = "suspicious"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PredictionResult(BaseModel):
    threat_detected: bool = Field(
        ..., description="True when traffic is classified as non-benign"
    )
    threat_type: ThreatType = Field(..., description="Predicted attack category")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Model confidence for the predicted class",
    )
    severity: Severity = Field(..., description="Estimated threat severity")


class PredictResponse(BaseModel):
    status: str = "success"
    prediction: PredictionResult


class PredictRequest(BaseModel):
    """Feature vector input for ML inference."""

    features: FeatureVector

    model_config = {
        "json_schema_extra": {
            "example": {
                "features": {
                    "protocol_encoded": 1,
                    "packet_size": 512,
                    "normalized_packet_size": 0.341,
                    "suspicious_large_packet": False,
                    "is_private_source": True,
                    "is_private_destination": False,
                    "source_port_category": "dynamic",
                    "destination_port_category": "web",
                    "connection_direction": "outbound",
                    "risk_score": 0.2,
                }
            }
        }
    }
