"""
Evaluate the trained Random Forest model.

Run from project root:
    python models/training/evaluate_model.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import classification_report

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from models.training.preprocessing import features_to_array  # noqa: E402
from models.training.train_model import generate_dataset  # noqa: E402

MODEL_DIR = PROJECT_ROOT / "models" / "trained"


def main() -> None:
    model = joblib.load(MODEL_DIR / "random_forest.pkl")
    scaler = joblib.load(MODEL_DIR / "scaler.pkl")
    metadata = json.loads((MODEL_DIR / "metadata.json").read_text(encoding="utf-8"))
    encoders = metadata["categorical_encoders"]

    dataset = generate_dataset(samples_per_class=100)
    X = np.vstack([features_to_array(row, encoders) for row in dataset])
    y = [row["label"] for row in dataset]
    X_scaled = scaler.transform(X)
    y_pred = model.predict(X_scaled)

    print(classification_report(y, y_pred, target_names=metadata["threat_classes"]))


if __name__ == "__main__":
    main()
