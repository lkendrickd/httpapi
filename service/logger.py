import json
import logging
from datetime import datetime


# JsonFormatter is a custom log formatter that formats log records
# as JSON allowing for easy parsing and analysis
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'funcName': record.funcName,
            'lineno': record.lineno,
        }
        if record.exc_info:
            log_record['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(log_record)


# setup_logging is a function that sets up logging for the application
def setup_logging(log_level: str = 'ERROR'):
    root_logger = logging.getLogger()
    root_logger.info(f"setting log level to {log_level}")
    root_logger.setLevel(log_level)
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root_logger.addHandler(handler)
