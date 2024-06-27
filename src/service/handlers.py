import os

from fastapi import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Summary

# Initialize Summary for request time
REQUEST_TIME = Summary(
    'request_processing_seconds',
    'Time spent processing request'
)

# Define build info and pull the values from the environment variables
build_info = {
    "version": os.getenv("VERSION", "0.0.0"),
    "commit": os.getenv("COMMIT", "00000000"),
    "branch": os.getenv("BRANCH", "main"),
    "build_date": os.getenv("BUILD_DATE", "1970-01-01T00:00:00Z"),
}

###################################################################
# Handlers for the endpoints
###################################################################

"""
 Below are the handlers for the endpoints.
 This is where the logic for the endpoints is defined.
 If you add an endpoint you will need to add a handler for it here.
"""


# ADD ADDITIONAL HANDLERS HERE AS NEEDED

# get_metrics function to return the metrics in the Prometheus format
# handles calls to the /metrics endpoint
async def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# get_health function to return the health status of the service
# additional checks or function calls can be added here for health evaluation
# handles calls to the /health endpoint
async def health_check():
    return {"status": "ok"}


# get_index function to return the index page with the build info
# handles calls to the / endpoint
async def get_index():
    with REQUEST_TIME.time():
        try:
            return {
                "message": "online",
                "build_info": build_info,
            }
        except KeyError as e:
            return {"error": f"An error has occurred: {e}"}
