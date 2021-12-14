from logging import getLogger, INFO, Formatter, StreamHandler, WARNING
from sys import stderr


def setup_logging(verbosity: int):
    logger = getLogger("aoc21")
    logger.setLevel(INFO if verbosity > 0 else WARNING)

    inner_logger = getLogger("aoc21.days")
    inner_logger.setLevel(INFO if verbosity > 1 else WARNING)

    handler = StreamHandler(stderr)
    formatter = Formatter("%(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
