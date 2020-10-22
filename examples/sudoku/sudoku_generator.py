#!/usr/bin/env python

"""Using Yices to generate Sudoku puzzles analagous to https://github.com/arel/arels-sudoku-generator.git."""

import sys
import random
from datetime import date

from SudokuLib import Puzzle
from Solver import Solver

from yices.Context import Context
from yices.Census import Census
from yices.Yices import Yices



def make_solution():
    """make_solution loops until we're able to fill all 81 cells with numbers, while satisfying the sudoku constraints."""
    while True:
        try:
            puzzle  = [[0]*9 for i in range(9)] # start with blank puzzle
            rows    = [set(range(1,10)) for i in range(9)] # set of available
            columns = [set(range(1,10)) for i in range(9)] # numbers for each
            squares = [set(range(1,10)) for i in range(9)] # row, column and square
            for i in range(9):
                for j in range(9):
                    # pick a number for cell (i,j) from the set of remaining available numbers
                    choices = rows[i].intersection(columns[j]).intersection(squares[(i//3)*3 + j//3])
                    choice  = random.choice(list(choices))

                    puzzle[i][j] = choice

                    rows[i].discard(choice)
                    columns[j].discard(choice)
                    squares[(i//3)*3 + j//3].discard(choice)

            # success! every cell is filled.
            return puzzle

        except IndexError:
            # if there is an IndexError, we have worked ourselves in a corner (we just start over)
            pass


def pluck(puzzle, cardinality):

    # prepare our solver and context
    solver = Solver(puzzle)
    context = Context()
    solver.assert_rules(context)

    # start with a set of all 81 cells, and tries to remove one (randomly) at a time
    # but not before checking that the cell can still be deduced from the remaining cells.
    cells = set(range(81))
    cells_remaining = cells.copy()

    while len(cells) > cardinality and len(cells_remaining) != 0:
        cell = random.choice(list(cells_remaining))
        cells_remaining.discard(cell)
        row, column = cell // 9, cell % 9
        val = puzzle.get_cell(row, column)
        assert val is not None
        if solver.erasable(context, row, column, val):
            puzzle.erase_cell(row, column)
            cells.discard(cell)

    context.dispose()

    return (puzzle, len(cells))


def  run(n = 28, iterations=10):
    all_results = {}
    print(f'Using n={n} and iterations={iterations}')
    solution = make_solution()
    answer = Puzzle(solution)
    answer.pprint()

    best_so_far = 81

    for i in range(iterations):
        puzzle = answer.clone()
        (result, number_of_cells) = pluck(puzzle, n)
        if number_of_cells < best_so_far:
            best_so_far = number_of_cells
        all_results.setdefault(number_of_cells, []).append(result)
        if i % 100 == 0:
            print(f'iteration {i}: {best_so_far}')

        if number_of_cells <= n:
            print(f'success of iteration {i}')
            break

    return all_results

def best(set_of_puzzles):
    # Could run some evaluation function here. For now just pick
    # the one with the fewest "givens".
    least = min(set_of_puzzles.keys())
    print(f'least number of givens: {least}')
    return least, set_of_puzzles[least][0]

def main():
    results = None
    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        iterations = int(sys.argv[2])
        results = run(n, iterations)
    else:
        results = run()

    least, puzzle = best(results)      # use the best one of those puzzles.
    puzzle.pprint()             # display that puzzle.
    puzzle.puzzle2path(f'puzzle_{least}_{str(date.today())}.sudoku')


if __name__ == '__main__':
    main()
    print(Census.dump())
    Yices.exit(True)
