"""ONNX inference: load random forest model and run predictions."""

import os
from pathlib import Path

import numpy as np

# Session and model path set at runtime
_session = None
_MODEL_PATH: str | None = None

# Expected feature count for the bundled random_forest.onnx (match export script)
EXPECTED_FEATURES = 4


def _model_path() -> str:
    global _MODEL_PATH
    if _MODEL_PATH is not None:
        return _MODEL_PATH
    base = Path(__file__).resolve().parent.parent
    path = os.environ.get("ONNX_MODEL_PATH", str(base / "models" / "random_forest.onnx"))
    _MODEL_PATH = path
    return path


def load_model() -> None:
    """Load the ONNX model once at startup."""
    global _session
    if _session is not None:
        return
    import onnxruntime as ort

    path = _model_path()
    if not Path(path).exists():
        raise FileNotFoundError(f"ONNX model not found: {path}")
    _session = ort.InferenceSession(path, providers=["CPUExecutionProvider"])


def get_session():
    """Return the loaded session (for tests)."""
    return _session


def get_input_name() -> str:
    """Return the model input name."""
    if _session is None:
        load_model()
    return _session.get_inputs()[0].name


def get_output_name() -> str:
    """Return the first output name."""
    if _session is None:
        load_model()
    return _session.get_outputs()[0].name


def predict(features: np.ndarray) -> np.ndarray:
    """
    Run inference. features: shape (1, n) or (n,) with n == EXPECTED_FEATURES.
    Returns model output (e.g. probabilities or label).
    """
    if _session is None:
        load_model()
    features = np.asarray(features, dtype=np.float32)
    if features.ndim == 1:
        features = features.reshape(1, -1)
    if features.shape[1] != EXPECTED_FEATURES:
        raise ValueError(f"Expected {EXPECTED_FEATURES} features, got {features.shape[1]}")
    input_name = get_input_name()
    output_name = get_output_name()
    out = _session.run([output_name], {input_name: features})
    return out[0]
