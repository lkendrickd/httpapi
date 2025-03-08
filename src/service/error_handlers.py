import json_logger

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

# setup logging
json_logger.setup_logging(log_level="INFO")

# Call the getLogger function with __name__ parameter
logger = json_logger.getLogger(__name__)

# setup_error_handlers is a function that sets up error handlers for the app
def setup_error_handlers(app: FastAPI):
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "message": "An unexpected error occurred."
            },
        )