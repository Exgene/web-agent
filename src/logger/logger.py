from logging import INFO, Formatter, StreamHandler, getLogger
from typing import Dict, Optional


class LoggerManager:
    _instance: Optional['LoggerManager'] = None
    _loggers: Dict[str, getLogger] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def setup_logger(self, name: str, level: int = INFO) -> None:
        if name in self._loggers:
            return

        logger = getLogger(name)
        logger.setLevel(level)

        ch = StreamHandler()
        ch.setLevel(level)

        formatter = Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(funcName)s] - %(message)s"
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)
        self._loggers[name] = logger

    def get_logger(self, name: str):
        if name not in self._loggers:
            self.setup_logger(name)
        return self._loggers[name]

    def remove_logger(self, name: str) -> None:
        if name in self._loggers:
            logger = self._loggers[name]
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            del self._loggers[name]


def get_logger_manager() -> LoggerManager:
    return LoggerManager()


def setup_logger(name: str, level: int = INFO) -> None:
    get_logger_manager().setup_logger(name, level)


def get_logger(name: str):
    return get_logger_manager().get_logger(name)


def remove_logger(name: str) -> None:
    get_logger_manager().remove_logger(name)
