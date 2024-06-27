import argparse

import uvicorn
from fastapi import FastAPI
from prometheus_client import start_http_server

import middleware
from config import load_settings
from error_handlers import setup_error_handlers
from handlers import get_metrics, get_health, get_index
from logger import setup_logging


def create_app() -> FastAPI:
    app = FastAPI()
    app.middleware("http")(middleware.log_requests_middleware())
    setup_error_handlers(app)

    @app.get("/metrics")
    async def metrics():
        return await get_metrics()

    @app.get("/health")
    async def health():
        return await get_health()

    @app.get("/")
    async def root():
        return await get_index()

    return app


def main():
    parser = argparse.ArgumentParser(description="Run the FastAPI services")
    parser.add_argument("--config", type=str, help="Path to the configuration file")
    parser.add_argument("--host", type=str, help="Host to run the FastAPI application on")
    parser.add_argument("--port", type=int, help="Port to run the FastAPI application on")
    parser.add_argument("--metrics-port", type=int, help="Port for Prometheus metrics")
    parser.add_argument(
        "--log-level",
        type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Log level for the application"
    )
    args = parser.parse_args()

    # Load settings from config file and/or environment variables
    settings = load_settings(args.config)

    # Override settings with command-line arguments if provided
    if args.host:
        settings.host = args.host
    if args.port:
        settings.port = args.port
    if args.metrics_port:
        settings.metrics_port = args.metrics_port
    if args.log_level:
        settings.log_level = args.log_level

    # Set up logging with the specified log level
    setup_logging(log_level=settings.log_level)

    # Start the Prometheus metrics server
    start_http_server(settings.metrics_port)

    # Create and run the FastAPI application
    app = create_app()
    uvicorn.run(app, host=settings.host, port=settings.port, log_level=settings.log_level.lower())


if __name__ == "__main__":
    main()
