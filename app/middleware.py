"""Custom middleware: request ID, path, and response status logging."""

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.logging_config import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs request_id, path, method, status, and duration; adds X-Request-ID header."""

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "request_processed",
            request_id=request_id,
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        response.headers["X-Request-ID"] = request_id
        return response
