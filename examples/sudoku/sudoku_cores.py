#!/usr/bin/env python


"""Using unsat cores to give hints."""

from yices.Yices import Yices

from SudokuLib import Puzzle
from Solver import Solver


puzzle_blank = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


puzzle_1 = [
    [ 0, 6, 0, 0, 0, 8, 0, 7, 3],
    [ 0, 0, 2, 0, 0, 0, 0, 4, 0],
    [ 5, 0, 0, 0, 6, 0, 0, 0, 0],
    #
    [ 0, 0, 0, 6, 0, 2, 0, 0, 5],
    [ 0, 0, 4, 0, 0, 0, 1, 0, 0],
    [ 6, 0, 0, 8, 0, 7, 0, 0, 0],
    #
    [ 0, 0, 0, 0, 7, 0, 0, 0, 1],
    [ 0, 5, 0, 0, 0, 0, 3, 0, 0],
    [ 4, 3, 0, 1, 0, 0, 0, 8, 0],
]


# puzzle_2 come from here:
# https://puzzling.stackexchange.com/questions/29/what-are-the-criteria-for-determining-the-difficulty-of-sudoku-puzzle
# where it is claimed to be the "hardest sudoku in the world"
# but in fact is not a valid sudoku since it has more than one solution. tut tut.
# I added it to one of the predefined boards ('escargot') of SudokuSensei and
# it has 29 non isomorphic models (aka solutions).
puzzle_ai_escargot = [
    [ 1, 0, 0, 0, 0, 7, 0, 9, 0],
    [ 0, 3, 0, 0, 2, 0, 0, 0, 8],
    [ 0, 0, 9, 6, 0, 0, 5, 0, 0],
    #
    [ 0, 0, 5, 3, 0, 0, 9, 0, 0],
    [ 0, 1, 0, 0, 8, 0, 0, 0, 2],
    [ 6, 0, 0, 0, 0, 4, 0, 0, 0],
    #
    [ 3, 0, 0, 0, 0, 0, 0, 1, 0],
    [ 0, 4, 0, 0, 0, 0, 0, 0, 7],
    [ 0, 0, 7, 0, 0, 0, 0, 3, 0],
]





def analyze(rawpuzzle):
    puzzle = Puzzle(rawpuzzle)
    puzzle.pprint()
    solver = Solver(puzzle)
    solution = solver.solve()

    if solution is not None:
        print('\nSolution:\n')
        solution.pprint()

        #<experimental zone>
        simplest = solver.filter_cores(solution)
        if simplest is not None:
            solver.show_hints(simplest)
        #</experimental zone>

analyze(puzzle_1)

analyze(puzzle_ai_escargot)

print('\nCensus:')
Yices.exit(True)
