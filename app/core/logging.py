import logging
import os

# Create log directory if it doesn't exist
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Log file paths
AUDIT_LOG_PATH = os.path.join(LOG_DIR, 'audit.log')
ERROR_LOG_PATH = os.path.join(LOG_DIR, 'error.log')

# Formatters
LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'

# Audit Handler
_audit_handler = logging.FileHandler(AUDIT_LOG_PATH)
_audit_handler.setLevel(logging.INFO)
_audit_handler.setFormatter(logging.Formatter(LOG_FORMAT))
_audit_handler.addFilter(lambda record: record.levelno == logging.INFO)

# Error Handler
_error_handler = logging.FileHandler(ERROR_LOG_PATH)
_error_handler.setLevel(logging.ERROR)
_error_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Root logger configuration
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[_audit_handler, _error_handler])

def get_audit_logger(name: str = "audit") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == AUDIT_LOG_PATH for h in logger.handlers):
        logger.addHandler(_audit_handler)
    return logger

def get_error_logger(name: str = "error") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    if not any(isinstance(h, logging.FileHandler) and h.baseFilename == ERROR_LOG_PATH for h in logger.handlers):
        logger.addHandler(_error_handler)
    return logger
