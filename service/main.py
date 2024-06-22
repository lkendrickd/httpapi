from fastapi import FastAPI, Response
from prometheus_client import start_http_server, Summary, generate_latest, CONTENT_TYPE_LATEST
import logging
import argparse
import os
from daphne.server import Server

from middleware import setup_middlewares
from error_handlers import setup_error_handlers

app = FastAPI()
setup_middlewares(app)
setup_error_handlers(app)

# Initialize Summary for request time
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Define build info and pull the values from the environment variables
build_info = {
    "version": os.getenv("VERSION", "0.0.0"),
    "commit": os.getenv("COMMIT", "00000000"),
    "branch": os.getenv("BRANCH", "main"),
    "build_date": os.getenv("BUILD_DATE", "1970-01-01T00:00:00Z"),
}

# /metrics endpoint to expose metrics in Prometheus format
@app.get("/metrics")
async def metrics():
    # Generate latest metrics in Prometheus format
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# /health endpoint to check the health of the application
# Simple response however extended checks can be added here
@app.get("/health")
async def health():
    return {"status": "ok"}

# / endpoint for the index page returning the build info
@app.get("/")
async def root():
    with REQUEST_TIME.time():
        try:
            return {
                "message": "online",
                "build_info": build_info,
            }
        except KeyError as e:
            return {"error": f"An error has occurred: {e}"}


# Run the FastAPI application
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the FastAPI application")
    parser.add_argument("--port", type=int, default=9000, help="Port to run the FastAPI application on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to run the FastAPI application on")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    # Start the Prometheus metrics server
    start_http_server(8000)

    # Start the server
    server = Server(
        application=app,
        endpoints=[f"tcp:port={args.port}:interface={args.host}"],
        signal_handlers=True
    )
    server.run()
