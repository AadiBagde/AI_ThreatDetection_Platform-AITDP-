"""Load and cache ML model artifacts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class ModelLoadError(Exception):
    """Raised when model artifacts cannot be loaded."""


@dataclass
class ModelArtifacts:
    model: RandomForestClassifier
    scaler: StandardScaler
    metadata: dict[str, Any]
    model_dir: Path


_artifacts: ModelArtifacts | None = None


def get_model_dir() -> Path:
    from ml_engine.app.core.paths import get_project_root

    return get_project_root() / "models" / "trained"


def load_models(force_reload: bool = False) -> ModelArtifacts:
    """Load model, scaler, and metadata into memory cache."""
    global _artifacts
    if _artifacts is not None and not force_reload:
        return _artifacts

    model_dir = get_model_dir()
    model_path = model_dir / "random_forest.pkl"
    scaler_path = model_dir / "scaler.pkl"
    metadata_path = model_dir / "metadata.json"

    for path in (model_path, scaler_path, metadata_path):
        if not path.exists():
            raise ModelLoadError(f"Missing model artifact: {path}")

    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ModelLoadError(f"Failed to load model artifacts: {exc}") from exc

    if not isinstance(model, RandomForestClassifier):
        raise ModelLoadError("Loaded model is not a RandomForestClassifier")

    _artifacts = ModelArtifacts(
        model=model,
        scaler=scaler,
        metadata=metadata,
        model_dir=model_dir,
    )
    return _artifacts


def get_artifacts() -> ModelArtifacts:
    if _artifacts is None:
        raise ModelLoadError("Models not loaded. Call load_models() during startup.")
    return _artifacts
