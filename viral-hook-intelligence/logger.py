"""
Logging Configuration
"""
import logging
import sys
from pathlib import Path
from config import LOG_LEVEL, LOGS_DIR

# Color codes
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': BLUE,
        'INFO': GREEN,
        'WARNING': YELLOW,
        'ERROR': RED,
        'CRITICAL': RED
    }

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, RESET)
        record.levelname = f"{log_color}{record.levelname}{RESET}"
        return super().format(record)


def setup_logger(name, log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_formatter = ColoredFormatter(
        '%(levelname)s | %(name)s | %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler if log_file specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


# Main logger
logger = setup_logger(
    'viral-hook-intelligence',
    log_file=LOGS_DIR / 'system.log'
)

# Phase loggers
scraper_logger = setup_logger(
    'scraper',
    log_file=LOGS_DIR / 'scraper.log'
)

analyzer_logger = setup_logger(
    'analyzer',
    log_file=LOGS_DIR / 'analyzer.log'
)

classifier_logger = setup_logger(
    'classifier',
    log_file=LOGS_DIR / 'classifier.log'
)

reporter_logger = setup_logger(
    'reporter',
    log_file=LOGS_DIR / 'reporter.log'
)

error_logger = setup_logger(
    'errors',
    log_file=LOGS_DIR / 'errors.log'
)
