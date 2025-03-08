# src/service/main.py - The entry point file

import argparse
import logging
from pathlib import Path

import uvicorn
from prometheus_client import start_http_server

from app import create_app
from config import load_settings, update_settings
from logger import setup_logging


def parse_args():
    parser = argparse.ArgumentParser(description="Run the FastAPI services")
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to the configuration file"
    )

    parser.add_argument(
        "--host",
        type=str,
        help="Host to run the FastAPI application on"
    )

    parser.add_argument(
        "--port",
        type=int,
        help="Port to run the FastAPI application on"
    )

    parser.add_argument(
        "--metrics-port",
        type=int,
        help="Port for Prometheus metrics"
    )

    parser.add_argument(
        "--log-level",
        type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help="Log level for the application"
    )
    return parser.parse_args()


def main():
    # Parse command line arguments
    args = parse_args()

    # Configuration hierarchy:
    # 1. Default values (in Settings class)
    # 2. Environment variables
    # 3. Config file (if specified)
    # 4. Command line arguments
    settings = load_settings(args.config)
    settings = update_settings(settings, args)

    # Set up logging with the specified log level
    setup_logging(log_level=settings.log_level)
    logger = logging.getLogger(__name__)
    logger.info(f"Log level set to {settings.log_level}")

    logger.info(f"Starting application: {settings.app_name}")
    logger.info(f"Version: {settings.version}")
    logger.info(f"Commit: {settings.commit}")
    logger.info(f"Branch: {settings.branch}")
    logger.info(f"Build Date: {settings.build_date}")

    # Start the Prometheus metrics server
    start_http_server(settings.metrics_port)
    logger.info(f"Metrics server started on port {settings.metrics_port}")

    # Create the FastAPI application
    app = create_app(title=settings.app_name, version=settings.version)
    
    # Run the application with Uvicorn
    logger.info(f"Starting service on {settings.host}:{settings.port}")
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_config=None,
        access_log=False,
    )


if __name__ == "__main__":
    main()