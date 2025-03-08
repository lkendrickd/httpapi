from fastapi import FastAPI
from fastapi.responses import Response

from error_handlers import setup_error_handlers
from middleware import log_requests_middleware
from handlers import get_metrics, health_check, get_index


def create_app(title="FastAPI App", version="0.0.0") -> FastAPI:
    """
    Create and configure the FastAPI application.
    This is the central function for setting up the app with all routes and middleware.
    
    Args:
        title: The title of the application
        version: The version of the application
        
    Returns:
        FastAPI: The configured FastAPI application
    """
    app = FastAPI(title=title, version=version)
    
    # Set up middleware
    app.middleware("http")(log_requests_middleware())
    
    # Set up error handlers
    setup_error_handlers(app)
    
    # Define routes
    app.add_api_route("/metrics", get_metrics, methods=["GET"])
    
    @app.get("/health")
    async def health(response: Response):
        result = await health_check()
        if "status_code" in result:
            response.status_code = result.pop("status_code")
        return result
    
    app.add_api_route("/", get_index, methods=["GET"])    
    return app