from concurrent.futures import ProcessPoolExecutor
from logging import getLogger, Formatter, INFO, StreamHandler
from os import linesep
from sys import stderr
from time import perf_counter
from timeit import Timer
from typing import Any, Collection, Iterable, List, Optional

from tabulate import tabulate

from aoc21.problem import Problem, Solution
from aoc21.days import PROBLEMS


HEADERS = ("Day", "Solution", "Elapsed", "Runs")


logger = getLogger("aoc21")
logger.setLevel(INFO)

_handler = StreamHandler(stderr)
_formatter = Formatter("%(message)s")
_handler.setFormatter(_formatter)

logger.addHandler(_handler)


def run(
    days: Optional[Collection[int]] = None,
    parallel: bool = True,
    benchmark: bool = False,
) -> bool:
    """
    Run solves for all days after filtering and print solutions.

    :param days: Days to solve for, or None to solve all of them.
    :param parallel: Whether to run the solvers in parallel with multiple processes.
    :param benchmark: Whether to run the solvers repeatedly to obtain a more accurate
    execution time.
    :return: True if no exceptions occurred during solving, False otherwise.
    """

    problems = []
    for problem in PROBLEMS:
        if days is None or problem.day in days:
            problems.append(problem)
        else:
            logger.info("Skipping day %d, part %d.", problem.day, problem.part)

    if not problems:
        print("", "No matching problems found.", "", sep=linesep)
        return True

    solutions = execute(problems, parallel, benchmark)
    solutions.sort(key=lambda s: (s.problem.day, s.problem.part))

    table = tabulate(
        map(_solution_as_row, solutions),
        HEADERS,
        tablefmt="pipe",
        numalign="right",
        stralign="right",
    )
    print("", table, "", sep=linesep)

    return all(s.exception is None for s in solutions)


def execute(
    problems: Iterable[Problem],
    parallel: bool = True,
    benchmark: bool = False,
) -> List[Solution]:
    """
    Run solvers for problems and print the solutions.

    :param problems: Sequence of problems to solve.
    :param parallel: Whether to run the solvers in parallel with multiple processes.
    :param benchmark: Whether to run the solvers repeatedly to obtain a more accurate
    execution time.
    :return: True if no exceptions occurred during solving, False otherwise.
    """

    solve = _solve_timed if benchmark else _solve_once
    if parallel:
        with ProcessPoolExecutor() as pool:
            return list(pool.map(solve, problems))
    else:
        return list(map(solve, problems))


def _solution_as_row(solution: Solution) -> List[Any]:
    name = f"{solution.problem.day}.{solution.problem.part}"
    if solution.exception is None:
        value = solution.value
    else:
        value = solution.exception.__class__.__name__

    return [name, value, solution.elapsed, solution.runs]


def _solve_once(problem: Problem) -> Solution:
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


def _solve_timed(problem: Problem) -> Solution:
    # Run solver initially to get solution and catch any errors.
    initial = _solve_once(problem)

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
