# FastAPI Service

This project is a robust FastAPI-based service with configuration management, error handling, and observability
features.

## Project Structure

- `service/`
    - `main.py`: The entry point of the application. Sets up the FastAPI app and routes.
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

The main entry point for the FastAPI service. It sets up the app, configures routes, and starts the server.

### service/config.py

Manages application configuration. It uses Pydantic's `BaseSettings` to load configuration from environment
variables, `.env` files, and YAML/JSON config files.

### service/error_handlers.py

Defines custom exception handlers for the application, ensuring graceful error responses.

### service/handlers.py

Contains the logic for various API endpoints, including health checks and metrics.

### service/logger.py

Sets up logging for the application, configuring log formats and levels.

### service/middleware.py

Defines custom middleware, such as request logging, which is applied to all routes.

### Makefile

Provides various commands for managing the application:

- `make build`: Installs dependencies
- `make run`: Runs the application
- `make test`: Runs tests
- `make lint`: Runs the linter
- `make config`: Generates a config file
- `make docker-build`: Builds a Docker image
- `make docker-run`: Runs the application in a Docker container

### Dockerfile

Defines how to build a Docker image for the application, ensuring it can run in containerized environments.

## Getting Started

1. Clone the repository
2. Run `make build` to install dependencies
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

## License - MIT
