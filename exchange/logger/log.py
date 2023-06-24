import logging

import coloredlogs

from exchange.meta import SingletoneMeta


class Log(metaclass=SingletoneMeta):
    def __init__(self) -> None:
        logging.basicConfig(filename='log.txt')
        coloredlogs.install()

    @staticmethod
    def info(message: str) -> None:
        coloredlogs.logging.info(message)

    @staticmethod
    def debug(message: str) -> None:
        coloredlogs.logging.debug(message)

    @staticmethod
    def warn(message: str) -> None:
        coloredlogs.logging.warn(message)

    @staticmethod
    def error(message: str) -> None:
        coloredlogs.logging.error(message)
