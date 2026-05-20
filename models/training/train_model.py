"""
Train a Random Forest threat classifier on synthetic security features.

Run from project root:
    python models/training/train_model.py
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from models.training.preprocessing import (  # noqa: E402
    FEATURE_NAMES,
    THREAT_CLASSES,
    build_categorical_encoders,
    features_to_array,
)

OUTPUT_DIR = PROJECT_ROOT / "models" / "trained"
RANDOM_SEED = 42


def _sample_benign() -> dict:
    return {
        "protocol_encoded": 1,
        "packet_size": random.randint(64, 800),
        "normalized_packet_size": round(random.uniform(0.05, 0.5), 4),
        "suspicious_large_packet": False,
        "is_private_source": True,
        "is_private_destination": False,
        "source_port_category": random.choice(["dynamic", "user"]),
        "destination_port_category": random.choice(["web", "secure_web", "dns"]),
        "connection_direction": "outbound",
        "risk_score": round(random.uniform(0.0, 0.25), 2),
        "label": "benign",
    }


def _sample_dos() -> dict:
    size = random.randint(1600, 9000)
    return {
        "protocol_encoded": random.choice([1, 2]),
        "packet_size": size,
        "normalized_packet_size": min(size / 1500, 1.0),
        "suspicious_large_packet": True,
        "is_private_source": random.choice([True, False]),
        "is_private_destination": random.choice([True, False]),
        "source_port_category": "dynamic",
        "destination_port_category": random.choice(["web", "system", "user"]),
        "connection_direction": random.choice(["outbound", "external", "inbound"]),
        "risk_score": round(random.uniform(0.5, 1.0), 2),
        "label": "dos",
    }


def _sample_port_scan() -> dict:
    return {
        "protocol_encoded": random.choice([1, 0]),
        "packet_size": random.randint(40, 200),
        "normalized_packet_size": round(random.uniform(0.02, 0.15), 4),
        "suspicious_large_packet": False,
        "is_private_source": True,
        "is_private_destination": True,
        "source_port_category": "dynamic",
        "destination_port_category": random.choice(["system", "ssh", "ftp", "smtp"]),
        "connection_direction": "internal",
        "risk_score": round(random.uniform(0.4, 0.8), 2),
        "label": "port_scan",
    }


def _sample_brute_force() -> dict:
    return {
        "protocol_encoded": 1,
        "packet_size": random.randint(100, 400),
        "normalized_packet_size": round(random.uniform(0.05, 0.3), 4),
        "suspicious_large_packet": False,
        "is_private_source": False,
        "is_private_destination": True,
        "source_port_category": random.choice(["dynamic", "user"]),
        "destination_port_category": random.choice(["ssh", "ftp", "smtp"]),
        "connection_direction": "inbound",
        "risk_score": round(random.uniform(0.45, 0.85), 2),
        "label": "brute_force",
    }


def _sample_suspicious() -> dict:
    return {
        "protocol_encoded": 0,
        "packet_size": random.randint(500, 1400),
        "normalized_packet_size": round(random.uniform(0.3, 0.9), 4),
        "suspicious_large_packet": random.choice([True, False]),
        "is_private_source": random.choice([True, False]),
        "is_private_destination": random.choice([True, False]),
        "source_port_category": random.choice(["user", "dynamic", "system"]),
        "destination_port_category": random.choice(["user", "system", "dns"]),
        "connection_direction": random.choice(["external", "outbound", "inbound"]),
        "risk_score": round(random.uniform(0.35, 0.75), 2),
        "label": "suspicious",
    }


def generate_dataset(samples_per_class: int = 400) -> list[dict]:
    generators = {
        "benign": _sample_benign,
        "dos": _sample_dos,
        "port_scan": _sample_port_scan,
        "brute_force": _sample_brute_force,
        "suspicious": _sample_suspicious,
    }
    data: list[dict] = []
    for label, generator in generators.items():
        for _ in range(samples_per_class):
            sample = generator()
            sample["label"] = label
            data.append(sample)
    random.shuffle(data)
    return data


def main() -> None:
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)

    dataset = generate_dataset()
    encoders = build_categorical_encoders(dataset)

    X = np.vstack([features_to_array(row, encoders) for row in dataset])
    y = np.array([row["label"] for row in dataset])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        random_state=RANDOM_SEED,
        class_weight="balanced",
    )
    model.fit(X_train_scaled, y_train)
    accuracy = model.score(X_test_scaled, y_test)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, OUTPUT_DIR / "random_forest.pkl")
    joblib.dump(scaler, OUTPUT_DIR / "scaler.pkl")

    metadata = {
        "model_version": "1.0.0",
        "model_type": "RandomForestClassifier",
        "feature_names": FEATURE_NAMES,
        "categorical_encoders": encoders,
        "threat_classes": THREAT_CLASSES,
        "training_samples": len(dataset),
        "test_accuracy": round(float(accuracy), 4),
    }
    (OUTPUT_DIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    print(f"Model saved to {OUTPUT_DIR}")
    print(f"Test accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
