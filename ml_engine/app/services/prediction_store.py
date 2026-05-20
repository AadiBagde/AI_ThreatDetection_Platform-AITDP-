"""Temporary in-memory storage for threat predictions."""

from threading import Lock
from typing import Any

_lock = Lock()
_predictions: list[dict[str, Any]] = []


def store_prediction(prediction: dict[str, Any]) -> int:
    with _lock:
        _predictions.append(prediction)
        return len(_predictions)


def get_prediction_count() -> int:
    with _lock:
        return len(_predictions)


def get_recent_predictions(limit: int = 100) -> list[dict[str, Any]]:
    with _lock:
        return list(_predictions[-limit:])
