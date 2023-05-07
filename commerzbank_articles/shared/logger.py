import os
import logging

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

log_level = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}

logging.basicConfig(
    level=log_level.get(LOG_LEVEL, logging.INFO), format="%(asctime)s %(message)s"
)
