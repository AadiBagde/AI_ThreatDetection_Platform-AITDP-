import sys
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def ensure_paths() -> None:
    """Register shared package and project root on sys.path."""
    project_root = get_project_root()
    shared_root = project_root / "shared"
    for path in (str(project_root), str(shared_root)):
        if path not in sys.path:
            sys.path.insert(0, path)


ensure_paths()
