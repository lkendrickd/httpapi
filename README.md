# HTTPAPI

<img src="images/httpapi.webp" alt="HTTPAPI Logo" width="400"/>

This project is a robust FastAPI-based service with configuration management, error handling, and observability
features.

## Project Structure

- `service/`
    - `main.py`: The entry point of the application. Sets up the FastAPI app and starts the server.
    - `app.py`: Contains the `create_app` function to configure the FastAPI application.
    - `config.py`: Defines the `Settings` class for configuration management.
    - `error_handlers.py`: Contains custom error handlers for the application.
    - `handlers.py`: Defines the request handlers for various endpoints.
    - `logger.py`: Sets up logging for the application.
    - `middleware.py`: Contains custom middleware, including request logging and custom headers.

- `tests/`: Contains test files for the application.
- `build/`: Contains build-related files, including the Dockerfile.
- `Makefile`: Defines various commands for building, running, and managing the application.
- `requirements.txt`: Lists the Python dependencies for the project.
- `config.yaml`: (Generated) Contains configuration settings for the application.

## Key Files and Their Purposes

### service/main.py

The main entry point for the FastAPI service. It sets up the application and starts the server.

### service/config.py

Manages application configuration. It uses Pydantic's `BaseSettings` to load configuration from environment
variables, `.env` files, and YAML/JSON config files.

### service/error_handlers.py

Defines custom exception handlers for the application, ensuring graceful error responses.

### service/handlers.py

Contains the logic for various API endpoints, including health checks and metrics. Included a system-info endpoint that this readme will guide you through even though added you can see the implementation.

### service/logger.py

Sets up logging for the application, configuring log formats and levels.

### service/middleware.py

Defines custom middleware, such as request logging, which is applied to all routes.

### Makefile

Provides various commands for managing the application:

- `make dependency-install`: Installs dependencies
- `make dependency-freeze`: Freezes dependencies to `requirements.txt`
- `make run`: Runs the application
- `make test`: Runs unit tests
- `make lint`: Runs the linter
- `make config`: Generates a config file
- `make docker-build`: Builds a Docker image
- `make docker-run`: Runs the application in a Docker container

### Dockerfile

Defines how to build a Docker image for the application, ensuring it can run in containerized environments.

## Getting Started

1. Clone the repository
2. Run `make dependency-install` to install dependencies
3. Run `make config` to generate a default configuration file
4. Run `make run` to start the application

For more detailed information on each command, run `make help`.

## Configuration

The application can be configured through:

1. Environment variables (prefixed with `SERVICE_`)
2. A `config.yaml` file (generate with `make config`)
3. Command-line arguments

The order of preference is:

- Command-line arguments > Environment variables > Config file > Default values.

**Default values (in Settings class):** The Settings class defines default values for each configuration setting using
pydantic.Field.

**Environment variables:** Pydantic automatically reads environment variables prefixed with SERVICE_ due to
Config.env_prefix = "SERVICE_" and loads them into corresponding settings if found.

**Config file (if specified):** The load_settings function accepts a --config argument, which specifies a YAML or JSON
file (Settings.config_file) from which settings are loaded and override defaults.

**Command line arguments:** The parse_args function uses argparse to parse command line arguments (--host, --port,
--metrics-port, --log-level) and updates the Settings instance accordingly.

## Docker

To run the application in a Docker container:

1. Run `make docker-build` to build the Docker image
2. Run `make docker-run` to start a container

## Testing

Run tests with `make test`. This will execute all tests in the `tests/` directory.

## Linting

Run the linter with `make lint` to check code quality.


## Developer Guide: Adding New Endpoints
Follow these steps to add new endpoints to the FastAPI service, using thr /system-info endpoint as an example.

#### Step 1: Create a Handler Function
First, add a new handler function in src/service/handlers.py:

```python
async def get_system_info():
    """
    Get system information endpoint handler.
    Returns basic information about the system.
    """
    import platform
    import psutil
    
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
        # Fallback to basic system info if resource stats fail
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
```
#### Step 2: Update Dependencies (if needed)
If your endpoint requires additional libraries, add them to requirements.txt:

```
psutil~=7.0.0
```

#### Install the new dependencies:
```sh
make dependency_install
```

#### Step 3: Register the Route
Add your route to the create_app() function in src/service/app.py:

```python
def create_app(title="FastAPI App", version="0.0.0") -> FastAPI:
    app = FastAPI(title=title, version=version)
    
    # Set up middleware and error handlers...
    
    # Existing routes
    app.add_api_route("/metrics", get_metrics, methods=["GET"])
    app.add_api_route("/health", health_check, methods=["GET"])
    app.add_api_route("/", get_index, methods=["GET"])
    
    # Add your new route
    app.add_api_route("/system-info", get_system_info, methods=["GET"])
    
    return app
```
You can use either decorator syntax or add_api_route() - both work in FastAPI:
```python
# Decorator syntax alternative
@app.get("/system-info")
async def system_info():
    return await get_system_info()
```
#### Step 4: Add Documentation (Optional)
FastAPI automatically generates OpenAPI documentation. Enhance it by adding docstrings and type hints:
```python
from typing import Dict, Any

async def get_system_info() -> Dict[str, Any]:
    """
    Get system information including platform details and resource usage.
    
    Returns:
        Dict containing system information and resource statistics
    """
    # Implementation...
```

#### Step 5: Test Your New Endpoint

**Run the service:**
```sh
make run
```

**Test the endpoint:**
```sh
curl http://localhost:9000/system-info
```

## Docs
The API documentation is available at `/docs` endpoint. This include an interactive API explorer and documentation for all the endpoints.

## License - MIT
