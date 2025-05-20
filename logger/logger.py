from logging import INFO, Formatter, StreamHandler, getLogger


def setup_logger(name: str, level: int = INFO) -> None:
    """
    Set up a logger with the specified name and level.

    Args:
        name (str): The name of the logger.
        level (int): The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    logger = getLogger(name)
    logger.setLevel(level)

    ch = StreamHandler()
    ch.setLevel(level)

    formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s] - %(message)s"
    )
    ch.setFormatter(formatter)

    logger.addHandler(ch)


def get_logger(name: str):
    """
    Get a logger with the specified name.

    Args:
        name (str): The name of the logger.
    """
    return getLogger(name)


def remove_logger(name: str) -> None:
    """
    Remove a logger with the specified name.

    Args:
        name (str): The name of the logger.
    """
    logger = getLogger(name)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
