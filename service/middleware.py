from fastapi import FastAPI, Request
import logging
import time


def setup_middlewares(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        logger = logging.getLogger("uvicorn.access")
        start_time = time.time()

        # Log request details for debugging
        logger.info(f"Request details: method={request.method}, url={request.url}, params={request.query_params}")

        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url} {response.status_code} Completed in {process_time:.2f} sec")
        return response
