import logging
from pathlib import Path


def get_logger(name: str = "main", filename: str = "default.txt") -> logging.Logger:

    logger = logging.getLogger(name)

    path = Path("__file__").resolve().parent / "logs"
    Path.mkdir(path, exist_ok=True)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(path / filename, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s :%(levelname)s : %(filename)s at line %(lineno)d => %(message)s", datefmt="%d-%m-%Y (%H:%M:%S)")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.debug("********************** LAST START HERE BEGIN HERE ***************************")

    return logger

