"""Modular feature extraction pipeline."""

from shared.schemas.feature_schema import FeatureVector
from shared.schemas.packet_schema import PacketIngest

from feature_engine.app.extractors.ip_extractor import extract_ip_features
from feature_engine.app.extractors.port_extractor import extract_port_features
from feature_engine.app.extractors.protocol_extractor import extract_protocol_features
from feature_engine.app.extractors.risk_extractor import extract_risk_score
from feature_engine.app.extractors.traffic_extractor import extract_traffic_features


class FeatureExtractionError(Exception):
    """Raised when the feature pipeline cannot process a packet."""


def run_feature_pipeline(packet: PacketIngest) -> FeatureVector:
    """
    Run all extractors and combine results into a feature vector.

    Designed for extension: add new extractors and merge their output here.
    """
    try:
        protocol = extract_protocol_features(packet.protocol.value)
        ip_features = extract_ip_features(
            str(packet.source_ip), str(packet.destination_ip)
        )
        port_features = extract_port_features(
            packet.source_port, packet.destination_port
        )
        traffic = extract_traffic_features(packet.packet_size)

        risk_score = extract_risk_score(
            connection_direction=ip_features.connection_direction,
            suspicious_large_packet=traffic.suspicious_large_packet,
            protocol_encoded=protocol.protocol_encoded,
            destination_port_category=port_features.destination_port_category,
        )

        return FeatureVector(
            protocol_encoded=protocol.protocol_encoded,
            packet_size=traffic.packet_size,
            normalized_packet_size=traffic.normalized_packet_size,
            suspicious_large_packet=traffic.suspicious_large_packet,
            is_private_source=ip_features.is_private_source,
            is_private_destination=ip_features.is_private_destination,
            source_port_category=port_features.source_port_category,
            destination_port_category=port_features.destination_port_category,
            connection_direction=ip_features.connection_direction,
            risk_score=risk_score,
        )
    except Exception as exc:
        raise FeatureExtractionError(str(exc)) from exc
