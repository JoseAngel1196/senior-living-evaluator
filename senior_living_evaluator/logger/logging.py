import logging


class Logger:
    def __init__(self, name: str, level: int | None = logging.DEBUG) -> None:
        """Construct an instance of Logger"""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(name)

    def info(self, msg: str, *args, **kwargs):
        self.logger.info(*args, **kwargs)
