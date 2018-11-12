from logging import (
    Formatter,
    getLogger,
    StreamHandler,
)


class LoggerFactory(object):

    level = None

    @classmethod
    def create_logger(cls, name):
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
