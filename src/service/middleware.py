import logging
import re
import time
from typing import Callable, Awaitable, List
from urllib.parse import quote

import fastapi
from fastapi import Request, Response

# Pre-compile the regex for ANSI escape sequences for performance
ANSI_ESCAPE_RE = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')

# Middleware is a type alias for a callable that takes a Request
# and a callable that returns an Awaitable[Response]
# This enables us to define a middleware as a function.
Middleware: object = Callable[
    [Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]
]


def sanitize_for_logging(value: str) -> str:
    """Sanitizes a string for logging, removing newlines and ANSI escape codes."""
    # Remove ANSI escape sequences
    value = ANSI_ESCAPE_RE.sub('', value)
    # Remove newlines and carriage returns
    value = value.replace('\n', '').replace('\r', '')
    return value


# add_custom_header_middleware is a middleware that adds
# a custom header to the response
def add_custom_header_middleware() -> Middleware:
    async def middleware(
            request: Request,
            call_next: Callable[
                [Request],
                Awaitable[Response],
            ]
    ) -> Response:
        response = await call_next(request)
        response.headers["X-Custom-Header"] = "processed by middleware"
        return response

    return middleware


# log_requests_middleware is a middleware that logs request details
# and response status code
def log_requests_middleware() -> Middleware:
    async def middleware(
            request: Request,
            call_next: Callable[
                [Request],
                Awaitable[Response]
            ]
    ) -> Response:
        logger = logging.getLogger()
        start_time = time.time()

        # Sanitize URL and query parameters for logging
        safe_url = quote(sanitize_for_logging(str(request.url)), safe=':/?=&%')
        safe_query_params = quote(sanitize_for_logging(str(request.query_params)))

        # Log request details for debugging
        logger.info(
            f"Request details: method={request.method}, url={safe_url}, "
            f"params={safe_query_params}"
        )

        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"{request.method} {safe_url} {response.status_code} Completed "
            f"in {process_time:.2f} sec"
        )
        return response

    return middleware


# setup_middlewares is a function that sets up middlewares for the FastAPI app
def setup_middlewares(
        app: fastapi.FastAPI, middlewares: List[Callable[[], Middleware]]
) -> None:
    """
    Setup middlewares for the FastAPI service.

    :param app: FastAPI application instance
    :param middlewares: List of middleware factory functions
    """
    for middleware_func in middlewares:
        app.middleware("http")(middleware_func())
