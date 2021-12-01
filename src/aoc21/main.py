from argparse import ArgumentParser
from sys import argv
from typing import Optional, Sequence

from aoc21.runner import run


def main(args: Optional[Sequence[str]] = None):
    """
    The entrypoint.
    """

    parser = ArgumentParser(description="Run solvers for Advent of Code 2021 problems.")
    parser.add_argument("days", nargs="*", type=int, help="Filter problems by days.")
    parser.add_argument(
        "-b",
        "--benchmark",
        dest="benchmark",
        action="store_true",
        help="Benchmark solvers in addition to running them.",
    )

    namespace = parser.parse_args(args)
    run(namespace.days or None, namespace.benchmark)


if __name__ == "__main__":
    main(argv)
