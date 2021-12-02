from logging import getLogger, Formatter, INFO, StreamHandler
from sys import stderr
from time import perf_counter
from timeit import Timer
from typing import Optional, Sequence

from tabulate import tabulate

from aoc21.problem import Problem, Solution
from aoc21.days import PROBLEMS


HEADERS = ("Problem", "Solution", "Elapsed", "Runs")


logger = getLogger("aoc21")
logger.setLevel(INFO)

_handler = StreamHandler(stderr)
_formatter = Formatter("%(message)s")
_handler.setFormatter(_formatter)

logger.addHandler(_handler)


def run(days: Optional[Sequence[int]] = None, benchmark: bool = False) -> bool:
    """
    Run solvers for problems and print the solutions.

    :param days: The days to select, or None to run them all.
    :param benchmark: Whether to run the solvers repeatedly to obtain a more accurate
    execution time.
    :return: True if no exceptions occurred during solving, False otherwise.
    """

    solutions = []
    rows = []

    for problem in PROBLEMS:
        if days is not None and problem.day not in days:
            logger.info("Skipping day %d, part %d.", problem.day, problem.part)
            continue

        solution = _solve(problem, benchmark)
        solutions.append(solution)

        name = f"{solution.problem.day}.{solution.problem.part}"
        if solution.exception is None:
            value = solution.value
        else:
            value = solution.exception.__class__.__name__

        rows.append([name, value, solution.elapsed, solution.runs])

    print()

    if rows:
        table = tabulate(
            rows, HEADERS, tablefmt="pipe", numalign="right", stralign="right"
        )
        print(table)
    else:
        print("No matching problems found.")

    print()

    return all(s.exception is None for s in solutions)


def _solve(problem: Problem, benchmark: bool = False) -> Solution:
    if benchmark:
        return _time_runs(problem)
    else:
        return _run_once(problem)


def _run_once(problem: Problem) -> Solution:
    # Run solver once.
    logger.info("Solving day %d, part %d...", problem.day, problem.part)
    start = perf_counter()
    try:
        value = problem.solver()
    except Exception as e:
        logger.error("Day %d, part %d failed.", problem.day, problem.part, exc_info=e)
        value = None
        exception = e
    else:
        exception = None

    end = perf_counter()
    elapsed = end - start

    return Solution(problem, value, exception, elapsed, 1)


def _time_runs(problem: Problem) -> Solution:
    # Run solver initially to get solution and catch any errors.
    initial = _run_once(problem)

    if initial.exception is not None:
        # An exception has occurred during initial execution so skip any benchmarking.
        return initial

    timer = Timer(problem.solver)

    logger.info("Warming up for day %d, part %d...", problem.day, problem.part)
    runs, _ = timer.autorange()

    # Repeat the timing procedure and get the minimum elapsed time before dividing
    # by number of runs.
    repeat = 5
    logger.info(
        "Benchmarking day %d, part %d (%d x %d runs)...",
        problem.day,
        problem.part,
        repeat,
        runs,
    )
    results = timer.repeat(repeat, runs)
    elapsed = min(results) / runs

    return Solution(problem, initial.value, None, elapsed, runs)
