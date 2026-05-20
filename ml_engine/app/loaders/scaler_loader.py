"""Scaler access helpers."""

from sklearn.preprocessing import StandardScaler

from ml_engine.app.loaders.model_loader import ModelLoadError, get_artifacts


def get_scaler() -> StandardScaler:
    try:
        return get_artifacts().scaler
    except ModelLoadError as exc:
        raise ModelLoadError("Scaler not available") from exc
