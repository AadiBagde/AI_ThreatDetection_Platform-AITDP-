"""Temporary in-memory storage for extracted feature vectors."""

from threading import Lock
from typing import Any

_lock = Lock()
_features: list[dict[str, Any]] = []


def store_features(features: dict[str, Any]) -> int:
    with _lock:
        _features.append(features)
        return len(_features)


def get_feature_count() -> int:
    with _lock:
        return len(_features)


def get_recent_features(limit: int = 100) -> list[dict[str, Any]]:
    with _lock:
        return list(_features[-limit:])
