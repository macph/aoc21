from argparse import ArgumentParser
from typing import Optional, Sequence

from aoc21.runner import run


def main_fn(args: Optional[Sequence[str]] = None) -> int:
    """
    Parse arguments and run solvers.
    :param args: The command line arguments.
    :return: The exit code.
    """

    parser = ArgumentParser(description="Run solvers for Advent of Code 2021 problems.")
    parser.add_argument("days", nargs="*", type=int, help="Filter problems by days.")
    parser.add_argument(
        "-s",
        "--sequential",
        dest="sequential",
        action="store_true",
        help="Run solvers in sequence without using multiple processes.",
    )
    parser.add_argument(
        "-b",
        "--benchmark",
        dest="benchmark",
        action="store_true",
        help="Benchmark solvers in addition to running them.",
    )

    namespace = parser.parse_args(args)
    result = run(namespace.days or None, not namespace.sequential, namespace.benchmark)

    return 0 if result else 1


def main():
    """
    The entrypoint.
    """

    exit(main_fn())


if __name__ == "__main__":
    main()
