import json
import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


# Settings class is a subclass of BaseSettings and uses Pydantic's
# Field to define the settings fields.  This enables Pydantic to
# validate the settings and provide default values
class Settings(BaseSettings):
    app_name: str = Field("FastAPI App", description="Name of the application")
    debug: bool = Field(False, description="Debug mode flag")
    host: str = Field("0.0.0.0", description="Host to bind the service to")
    port: int = Field(9000, description="Port to run the service on")
    metrics_port: int = Field(8000, description="Port for Prometheus metrics")
    log_level: str = Field("INFO", description="Logging level")

    version: str = Field("0.0.0", description="Service version")
    commit: str = Field("00000000", description="Git commit hash")
    branch: str = Field("main", description="Git branch")
    build_date: str = Field(
        default="1970-01-01T00:00:00Z",
        description="Build date of the service"
    )

    config_file: Optional[Path] = Field(
        default=None,
        description="Path to the configuration file"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.config_file:
            self._load_from_file()

    # _load_from_file method reads the configuration data
    # from the specified file
    def _load_from_file(self):
        file_path = self.config_file

        if not file_path.exists():
            raise FileNotFoundError(f"Config file not found: {file_path}")

        if file_path.suffix.lower() in ('.yaml', '.yml'):
            with open(file_path, 'r') as f:
                config_data = yaml.safe_load(f)
        elif file_path.suffix.lower() == '.json':
            with open(file_path, 'r') as f:
                config_data = json.load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

        for key, value in config_data.items():
            if hasattr(self, key):
                setattr(self, key, value)


# load_settings function creates an instance of the Settings class by loading
# the settings from the specified config file
def load_settings(config_file: Optional[str] = None) -> Settings:
    env_settings = {
        "version": os.environ.get("VERSION"),
        "commit": os.environ.get("COMMIT"),
        "branch": os.environ.get("BRANCH"),
        "build_date": os.environ.get("BUILD_DATE"),
    }
    # Remove None values
    env_settings = {k: v for k, v in env_settings.items() if v is not None}

    if config_file:
        config_file = str(config_file)
    return Settings(config_file=config_file, **env_settings)


@lru_cache()
def get_settings() -> Settings:
    return load_settings()


settings = load_settings()

def update_settings(settings, args) -> Settings:
    """
    Update settings with command line arguments.
    
    Args:
        settings: The settings object to update
        args: The parsed command line arguments
        
    Returns:
        Settings: The updated settings object
    """
    if args.host:
        settings.host = args.host
    if args.port:
        settings.port = args.port
    if args.metrics_port:
        settings.metrics_port = args.metrics_port
    if args.log_level:
        settings.log_level = args.log_level
    return settings