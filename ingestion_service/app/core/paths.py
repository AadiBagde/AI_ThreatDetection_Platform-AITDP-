import sys
from pathlib import Path


def ensure_shared_on_path() -> None:
    """Add shared package root so `from shared.schemas...` resolves."""
    project_root = Path(__file__).resolve().parents[3]
    shared_root = project_root / "shared"
    shared_path = str(shared_root)
    if shared_path not in sys.path:
        sys.path.insert(0, shared_path)


ensure_shared_on_path()
