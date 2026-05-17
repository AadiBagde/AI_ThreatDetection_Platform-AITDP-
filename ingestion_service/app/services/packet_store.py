from threading import Lock
from typing import Any

_lock = Lock()
_packets: list[dict[str, Any]] = []


def store_packet(packet: dict[str, Any]) -> int:
    with _lock:
        _packets.append(packet)
        return len(_packets)


def get_packet_count() -> int:
    with _lock:
        return len(_packets)


def get_recent_packets(limit: int = 100) -> list[dict[str, Any]]:
    with _lock:
        return list(_packets[-limit:])
