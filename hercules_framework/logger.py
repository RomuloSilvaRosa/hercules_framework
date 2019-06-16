import logging
import sys
from uuid import uuid4


def get_logger(logger_name: str = str(uuid4())):
    logger = logging.getLogger(logger_name)
    fmt = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s[%(name)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    if not logger.handlers:
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setLevel(logging.INFO)
        stdout.setFormatter(fmt)

        stderr = logging.StreamHandler(sys.stderr)
        stderr.setLevel(logging.WARNING)
        stderr.setFormatter(fmt)

        logger.propagate = False

        logger.addHandler(stdout)
        logger.addHandler(stderr)
    # create console handler
    logger.setLevel(logging.INFO)
    return logger


def set_transaction_id(app):
    app.logger.set_transaction_id(str(uuid4()))
