import logging
import os

from dotenv import load_dotenv


load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/app.log")


def setup_logging():

    os.makedirs(
        os.path.dirname(LOG_FILE),
        exist_ok=True
    )

    log_format = (
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    )

    # Definition of Formatter
    formatter = logging.Formatter(
        log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Creation of logger
    logger = logging.getLogger()

    logger.setLevel(LOG_LEVEL)

    file_handler = logging.FileHandler(
        LOG_FILE,
        mode="a"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    
    return logger