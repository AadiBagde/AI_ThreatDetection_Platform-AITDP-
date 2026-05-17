"""Protocol normalization and encoding utilities."""

PROTOCOL_ENCODING: dict[str, int] = {
    "TCP": 1,
    "UDP": 2,
    "ICMP": 3,
}

MTU_BYTES = 1500

SENSITIVE_DESTINATION_CATEGORIES = frozenset(
    {"ssh", "ftp", "smtp", "dns", "secure_web"}
)


def normalize_protocol(protocol: str) -> str:
    """Normalize protocol name to uppercase stripped form."""
    return protocol.strip().upper()


def encode_protocol(protocol: str) -> int:
    """
    Encode protocol to integer for ML features.

    TCP=1, UDP=2, ICMP=3, Unknown=0
    """
    return PROTOCOL_ENCODING.get(normalize_protocol(protocol), 0)


def is_unknown_protocol(protocol_encoded: int) -> bool:
    return protocol_encoded == 0
