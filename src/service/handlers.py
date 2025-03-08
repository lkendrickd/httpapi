import os
from fastapi import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Summary
from config import get_settings
import platform
import psutil

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
    return {"status": "healthy"}


# get_index function to return the index page with the build info
# handles calls to the / endpoint
async def get_index():
    settings = get_settings()
    return {
        "message": "online",
        "build_info": {
            "version": settings.version,
            "commit": settings.commit,
            "branch": settings.branch,
            "build_date": settings.build_date
        }
    }

async def get_system_info():
    """
    Get system information endpoint handler.
    Returns basic information about the system.
    """ 
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            "system": {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "python_version": platform.python_version(),
                "architecture": platform.machine(),
                "processor": platform.processor()
            },
            "resources": {
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": round(memory.total / (1024**3), 2),
                "memory_available_gb": round(memory.available / (1024**3), 2),
                "memory_percent_used": memory.percent,
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_free_gb": round(disk.free / (1024**3), 2),
                "disk_percent_used": disk.percent
            }
        }
    except Exception as e:
        # In case psutil fails or is not available
        return {
            "system": {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "python_version": platform.python_version(),
                "architecture": platform.machine(),
                "processor": platform.processor()
            },
            "resources": {
                "error": f"Unable to fetch resource information: {str(e)}"
            }
        }