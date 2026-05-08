"""Logging setup for Viral Hook Intelligence System."""

import logging
import sys
from config import LOG_LEVEL, ERRORS_LOG

def setup_logger(name):
    """Configure and return a logger instance."""
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)

    # File handler for errors
    file_handler = logging.FileHandler(ERRORS_LOG)
    file_handler.setLevel(logging.ERROR)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger

# Create root logger
root_logger = setup_logger('viral_hook_system')
