import json
import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings


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
    build_date: str = Field("1970-01-01T00:00:00Z", description="Build date of the service")

    config_file: Optional[Path] = Field(None, description="Path to the configuration file")

    def to_service_config(self):
        return Settings(
            app_name=self.app_name,
            debug=self.debug,
            host=self.host,
            port=self.port,
            metrics_port=self.metrics_port,
            log_level=self.log_level,
            version=self.version,
            commit=self.commit,
            branch=self.branch,
            build_date=self.build_date
        )

    class Config:
        env_file = ".env"
        env_prefix = "SERVICE_"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_from_env()
        if self.config_file:
            self._load_from_file(self.config_file)

    def _load_from_env(self):
        for field in self.__fields__:
            env_var = f"SERVICE_{field.upper()}"
            if env_var in os.environ:
                setattr(self, field, os.environ[env_var])

    def _load_from_file(self, file_path: Path):
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


def load_settings(config_file: Optional[str] = None) -> Settings:
    return Settings(config_file=Path(config_file) if config_file else None)


settings = load_settings()
