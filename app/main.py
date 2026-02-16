"""FastAPI app: routes and middleware registration."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.logging_config import configure_logging, get_logger
from app.middleware import RequestLoggingMiddleware
from app.metrics import setup_metrics

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: configure logging and load model; shutdown: cleanup."""
    configure_logging()
    logger.info("startup", message="Configuring app")
    from app.inference import load_model  # noqa: F401

    load_model()
    yield
    logger.info("shutdown", message="App shutting down")


app = FastAPI(title="API Project", lifespan=lifespan)

app.add_middleware(RequestLoggingMiddleware)

setup_metrics(app)


@app.get("/health")
async def health():
    """Return health status for liveness/readiness."""
    return {"status": "healthy", "service": "api"}


@app.get("/get")
async def get_example():
    """GET example: JSON response with 200."""
    return {"message": "Hello", "ok": True}


@app.post("/post")
async def post_echo(body: dict):
    """Echo request body and add timestamp."""
    from datetime import datetime, timezone

    response = {**body, "timestamp": datetime.now(timezone.utc).isoformat()}
    return response


@app.post("/predict")
async def predict(body: dict):
    """Run random forest ONNX model. Body: {"features": [float, ...]} with 4 features."""
    from datetime import datetime, timezone

    from app.inference import EXPECTED_FEATURES, predict as run_inference

    features = body.get("features")
    if not isinstance(features, list) or len(features) != EXPECTED_FEATURES:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=400,
            detail=f"Expected 'features' array of {EXPECTED_FEATURES} floats",
        )
    try:
        import numpy as np

        arr = np.array(features, dtype=np.float32)
    except (TypeError, ValueError):
        from fastapi import HTTPException

        raise HTTPException(status_code=400, detail="All features must be numbers")
    try:
        result = run_inference(arr)
        # Convert numpy array to list for JSON (e.g. probabilities or label)
        if hasattr(result, "tolist"):
            result = result.tolist()
        return {"prediction": result, "timestamp": datetime.now(timezone.utc).isoformat()}
    except FileNotFoundError:
        from fastapi import HTTPException

        raise HTTPException(status_code=503, detail="Model not loaded")
