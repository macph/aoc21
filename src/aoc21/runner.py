from typing import Optional, Sequence

from tabulate import tabulate


HEADERS = ("Problem", "Solution", "Elapsed")
PROBLEMS = []


def run(days: Optional[Sequence[int]] = None):
    """
    Run solvers for problems and print the solutions.

    :param days: The days to select, or None to run them all.
    """

    solutions = []

    for problem in PROBLEMS:
        if days is not None and problem.day in days:
            print(f"Skipping day {problem.day}, part {problem.part}.")
            continue

        print(f"Solving day {problem.day}, part {problem.part}...")
        solution = problem.solve()
        solutions.append(solution)

    print()

    rows = [
        [f"{s.problem.day}.{s.problem.part}", s.solution, s.elapsed] for s in solutions
    ]

    if rows:
        table = tabulate(
            rows, HEADERS, tablefmt="pipe", numalign="right", stralign="right"
        )
        print(table)
    else:
        print("No matching problems found.")

    print()
