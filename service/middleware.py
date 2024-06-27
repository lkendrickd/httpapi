import logging
import time
from typing import Callable, Awaitable, List

import fastapi
from fastapi import Request, Response

# Middleware is a type alias for a callable that takes a Request and a callable that returns an Awaitable[Response]
# this enables us to define a middleware as a function.
Middleware = Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]


# add_custom_header_middleware is a middleware that adds a custom header to the response
def add_custom_header_middleware() -> Middleware:
    async def middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        response = await call_next(request)
        response.headers["X-Custom-Header"] = "processed by middleware"
        return response

    return middleware


# log_requests_middleware is a middleware that logs request details and response status code
def log_requests_middleware() -> Middleware:
    async def middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        logger = logging.getLogger()
        start_time = time.time()

        # Log request details for debugging
        logger.info(f"Request details: method={request.method}, url={request.url}, params={request.query_params}")

        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url} {response.status_code} Completed in {process_time:.2f} sec")
        return response

    return middleware


# setup_middlewares is a function that sets up middlewares for the FastAPI app
def setup_middlewares(app: fastapi, middlewares: List[Callable[[], Middleware]]) -> None:
    """
    Setup middlewares for the FastAPI service.

    :param app: FastAPI application instance
    :param middlewares: List of middleware factory functions
    """
    for middleware in middlewares:
        app.middleware("http")(middleware())
