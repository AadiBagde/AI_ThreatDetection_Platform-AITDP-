"""IP address classification utilities using the ipaddress module."""

from dataclasses import dataclass
from ipaddress import ip_address

from shared.schemas.feature_schema import ConnectionDirection


@dataclass(frozen=True)
class IPClassification:
    """Classification result for a single IP address."""

    address: str
    is_private: bool
    is_public: bool
    is_loopback: bool
    is_multicast: bool
    is_reserved: bool


def classify_ip(ip: str) -> IPClassification:
    """Classify an IP address into network categories."""
    addr = ip_address(ip)
    is_private = addr.is_private
    is_loopback = addr.is_loopback
    is_multicast = addr.is_multicast
    is_reserved = addr.is_reserved
    is_public = not (
        is_private or is_loopback or is_multicast or is_reserved or addr.is_unspecified
    )
    return IPClassification(
        address=ip,
        is_private=is_private,
        is_public=is_public,
        is_loopback=is_loopback,
        is_multicast=is_multicast,
        is_reserved=is_reserved,
    )


def determine_connection_direction(
    source: IPClassification, destination: IPClassification
) -> ConnectionDirection:
    """Determine traffic direction from source and destination classifications."""
    if source.is_private and destination.is_private:
        return ConnectionDirection.INTERNAL
    if source.is_private and destination.is_public:
        return ConnectionDirection.OUTBOUND
    if source.is_public and destination.is_private:
        return ConnectionDirection.INBOUND
    return ConnectionDirection.EXTERNAL
