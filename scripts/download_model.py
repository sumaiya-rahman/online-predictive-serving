"""
Download or generate the random forest ONNX model for the API.

1. If MODEL_URL env is set, try to download from that URL.
2. Otherwise run scripts/export_onnx.py to generate models/random_forest.onnx.

Run from repo root: python scripts/download_model.py
Or: make download-model
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = REPO_ROOT / "models"
MODEL_PATH = MODELS_DIR / "random_forest.onnx"
EXPORT_SCRIPT = REPO_ROOT / "scripts" / "export_onnx.py"


def download_from_url(url: str) -> bool:
    """Download model from URL to MODEL_PATH. Return True on success."""
    try:
        import urllib.request

        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, MODEL_PATH)
        if MODEL_PATH.is_file() and MODEL_PATH.stat().st_size > 0:
            print(f"Downloaded model to {MODEL_PATH}")
            return True
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)
    return False


def generate_via_export() -> bool:
    """Run export_onnx.py to generate the model. Return True on success."""
    if not EXPORT_SCRIPT.exists():
        print(f"Export script not found: {EXPORT_SCRIPT}", file=sys.stderr)
        return False
    try:
        subprocess.run(
            [sys.executable, str(EXPORT_SCRIPT)],
            cwd=str(REPO_ROOT),
            check=True,
        )
        return MODEL_PATH.is_file()
    except subprocess.CalledProcessError as e:
        print(f"Export failed: {e}", file=sys.stderr)
        return False


def main() -> int:
    if MODEL_PATH.is_file():
        print(f"Model already exists: {MODEL_PATH}")
        return 0

    url = os.environ.get("MODEL_URL", "").strip()
    if url and download_from_url(url):
        return 0

    print("Generating model via scripts/export_onnx.py (requires scikit-learn, skl2onnx)...")
    if generate_via_export():
        return 0

    print("Failed to obtain model. Install dev deps (make install) then run again.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
