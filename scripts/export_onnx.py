"""
One-time script to export a small RandomForestClassifier to ONNX.
Run from repo root: python scripts/export_onnx.py
Output: models/random_forest.onnx (input shape (1, 4), float32).
"""

from pathlib import Path

import numpy as np
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

def main():
    X, y = make_classification(
        n_samples=200, n_features=4, n_informative=2, n_redundant=0, random_state=42
    )
    model = RandomForestClassifier(n_estimators=5, max_depth=3, random_state=42)
    model.fit(X, y)

    out_dir = Path(__file__).resolve().parent.parent / "models"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "random_forest.onnx"

    initial_type = [("float_input", FloatTensorType([None, 4]))]
    onnx_model = convert_sklearn(model, initial_types=initial_type)
    with open(out_path, "wb") as f:
        f.write(onnx_model.SerializeToString())
    print(f"Exported to {out_path}")

if __name__ == "__main__":
    main()
