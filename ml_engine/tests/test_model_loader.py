from ml_engine.app.loaders.model_loader import get_artifacts, load_models


def test_model_loads_successfully():
    artifacts = load_models(force_reload=True)
    assert artifacts.model is not None
    assert artifacts.scaler is not None
    assert "threat_classes" in artifacts.metadata
    assert "categorical_encoders" in artifacts.metadata


def test_model_cached_in_memory():
    first = get_artifacts()
    second = get_artifacts()
    assert first.model is second.model
