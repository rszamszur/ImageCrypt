from logging import (
    Formatter,
    getLogger,
    StreamHandler,
)


class LoggerFactory(object):

    _level = None

    @property
    def level(self):
        return self.level

    @level.setter
    def level(self, value):
        self._level = value

    @classmethod
    def create_logger(cls, name):
        loggers = getLogger().manager.loggerDict
        if name in loggers:
            return loggers[name]
        formatter = Formatter(
            "%(asctime)s %(levelname)8s: %(name)s: %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        console = StreamHandler()
        console.setFormatter(formatter)
        logger = getLogger(name)
        logger.addHandler(console)
        logger.propagate = False
        logger.setLevel(cls.level)
        return logger
