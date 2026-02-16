"""Prometheus metrics for at least two endpoints (/health, /predict)."""

from prometheus_client import Counter, Histogram

from fastapi import FastAPI

REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "Request duration in seconds",
    ["method", "path"],
    buckets=(0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0),
)
PREDICTIONS_TOTAL = Counter("predictions_total", "Total /predict calls")
INFERENCE_DURATION = Histogram(
    "inference_duration_seconds",
    "ONNX inference duration in seconds",
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0),
)


def setup_metrics(app: FastAPI) -> None:
    """Mount /metrics and optionally add middleware to record request metrics."""
    from prometheus_client import make_asgi_app

    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
