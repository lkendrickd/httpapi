from fastapi import FastAPI

from error_handlers import setup_error_handlers
from handlers import get_metrics, health_check, get_index


# create_app sets up the FastAPI service with the necessary
# routes and error handlers
def create_app() -> FastAPI:
    app = FastAPI()
    setup_error_handlers(app)

    app.add_api_route("/metrics", get_metrics, methods=["GET"])
    app.add_api_route("/health", health_check, methods=["GET"])
    app.add_api_route("/", get_index, methods=["GET"])

    return app
