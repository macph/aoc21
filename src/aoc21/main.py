from argparse import ArgumentParser
from sys import argv
from typing import Optional, Sequence

from aoc21.runner import run


def main(args: Optional[Sequence[str]] = None):
    """
    The entrypoint.
    """

    parser = ArgumentParser()
    parser.add_argument("days", nargs="*", type=int)

    namespace = parser.parse_args(args)
    run(namespace.days)


if __name__ == "__main__":
    main(argv)
