"""Structured, configurable logging (structlog)."""

import logging
import os

import structlog


def get_logger(name: str):
    """Return a structlog logger bound to the given name."""
    return structlog.get_logger(name)


def configure_logging() -> None:
    """Configure structlog from env: LOG_LEVEL, LOG_FORMAT (json|console)."""
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_format = os.environ.get("LOG_FORMAT", "console").lower()

    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
    ]

    if log_format == "json":
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    else:
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level, logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
