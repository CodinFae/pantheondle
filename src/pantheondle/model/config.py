import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def data_path() -> Path:
    if override := os.environ.get("PANTHEONDLE_DATA"):
        return Path(override)
    return PROJECT_ROOT / "data" / "persons.parquet"
