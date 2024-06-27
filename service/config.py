import json
import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic_settings import BaseSettings


# Settings class is a subclass of BaseSettings this is used to load settings from
# environment variables and config files
class Settings(BaseSettings):
    app_name: str = "FastAPI App"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 9000
    metrics_port: int = 8000
    log_level: str = "INFO"

    version: str = "0.0.0"
    commit: str = "00000000"
    branch: str = "main"
    build_date: str = "1970-01-01T00:00:00Z"

    config_file: Optional[Path] = None

    class Config:
        env_file = ".env"
        env_prefix = "SERVICE_"  # This will look for environment variables prefixed with "SERVICE_"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_from_env()
        if self.config_file:
            self._load_from_file(self.config_file)

    def _load_from_env(self):
        for field in self.__fields__:
            env_var = f"SERVICE_{field.upper()}"  # Prefix environment variables with "SERVICE_" to avoid conflicts
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
