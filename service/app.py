from fastapi import FastAPI

import middleware
from error_handlers import setup_error_handlers
from handlers import get_metrics, health_check, get_index

"""
class Service(fastapi.FastAPI):
    logger:  logger.Logger
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_api_route("/metrics", get_metrics)
        self.add_api_route("/health", health_check)
        self.add_api_route("/", get_index)
"""


def create_app() -> FastAPI:
    app = FastAPI()
    app.middleware("http")(middleware.log_requests_middleware())
    setup_error_handlers(app)

    app.add_api_route("/metrics", get_metrics, methods=["GET"])
    app.add_api_route("/health", health_check, methods=["GET"])
    app.add_api_route("/", get_index, methods=["GET"])

    return app
