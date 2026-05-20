from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "trained" / "random_forest.pkl"


@pytest.fixture(scope="session", autouse=True)
def ensure_trained_model():
    if not MODEL_PATH.exists():
        from models.training.train_model import main

        main()

    from ml_engine.app.loaders.model_loader import load_models

    load_models(force_reload=True)
