import logging
import json
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'funcName': record.funcName,
            'lineno': record.lineno,
        }
        return json.dumps(log_record)


def new_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    return logger


class NoopLogger:
    def info(self, *args, **kwargs) -> None:
        pass

    def error(self, *args, **kwargs) -> None:
        pass

    def warning(self, *args, **kwargs) -> None:
        pass

    def debug(self, *args, **kwargs) -> None:
        pass

    def critical(self, *args, **kwargs) -> None:
        pass


def noop() -> NoopLogger:
    return NoopLogger()
