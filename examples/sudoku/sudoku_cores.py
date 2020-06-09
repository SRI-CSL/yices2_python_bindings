#!/usr/bin/env python


"""Using unsat cores to give hints."""

from yices.Yices import Yices
from yices.Census import Census

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

extreme_1 = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 2, 0, 0, 7, 1, 5, 0],
    [ 4, 0, 0, 0, 0, 9, 3, 0, 6],
    #
    [ 0, 1, 0, 0, 0, 3, 0, 0, 5],
    [ 0, 0, 0, 5, 2, 4, 0, 0, 0],
    [ 3, 0, 0, 7, 0, 0, 0, 6, 0],
    #
    [ 1, 0, 7, 6, 0, 0, 0, 0, 9],
    [ 0, 5, 6, 8, 0, 0, 4, 0, 0],
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

extreme_2 = [
    [ 0, 0, 0, 0, 0, 0, 7, 0, 3],
    [ 0, 0, 6, 0, 0, 8, 5, 4, 0],
    [ 5, 0, 0, 0, 7, 0, 0, 0, 0],
    #
    [ 0, 1, 9, 0, 0, 4, 8, 0, 0],
    [ 7, 0, 0, 0, 0, 0, 0, 0, 9],
    [ 0, 0, 8, 9, 0, 0, 2, 1, 0],
    #
    [ 0, 0, 0, 0, 5, 0, 0, 0, 2],
    [ 0, 5, 7, 3, 0, 0, 1, 0, 0],
    [ 4, 0, 3, 0, 0, 0, 0, 0, 0],
]

extreme_3 = [
    [ 8, 0, 1, 0, 9, 0, 0, 0, 0],
    [ 0, 7, 2, 0, 0, 1, 0, 0, 0],
    [ 0, 0, 0, 3, 0, 0, 8, 0, 0],
    #
    [ 5, 0, 0, 1, 0, 0, 0, 4, 0],
    [ 1, 0, 0, 0, 3, 0, 0, 0, 9],
    [ 0, 2, 0, 0, 0, 7, 0, 0, 5],
    #
    [ 0, 0, 5, 0, 0, 2, 0, 0, 0],
    [ 0, 0, 0, 4, 0, 0, 5, 9, 0],
    [ 0, 0, 0, 0, 8, 0, 4, 0, 3],
]

extreme_4 = [
    [ 7, 0, 0, 0, 0, 4, 0, 5, 0],
    [ 0, 0, 0, 5, 0, 0, 1, 0, 0],
    [ 0, 0, 0, 0, 0, 6, 0, 7, 8],
    #
    [ 0, 0, 4, 0, 0, 0, 8, 0, 0],
    [ 3, 5, 0, 0, 8, 0, 0, 1, 9],
    [ 0, 0, 8, 0, 0, 0, 2, 0, 0],
    #
    [ 5, 4, 0, 1, 0, 0, 0, 0, 0],
    [ 0, 0, 6, 0, 0, 5, 0, 0, 0],
    [ 0, 8, 0, 9, 0, 0, 0, 0, 1],
]

#https://www.conceptispuzzles.com/index.aspx?uri=info/article/424
hardest = [
    [ 8, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 0, 3, 6, 0, 0, 0, 0, 0],
    [ 0, 7, 0, 0, 9, 0, 2, 0, 0],
    #
    [ 0, 5, 0, 0, 0, 7, 0, 0, 0],
    [ 0, 0, 0, 0, 4, 5, 7, 0, 0],
    [ 0, 0, 0, 1, 0, 0, 0, 3, 0],
    #
    [ 0, 0, 1, 0, 0, 0, 0, 6, 8],
    [ 0, 0, 8, 5, 0, 0, 0, 1, 0],
    [ 0, 9, 0, 0, 0, 0, 4, 0, 0],
]



def analyze(rawpuzzle, name):
    puzzle = Puzzle(rawpuzzle)
    print(f'\nPuzzle ({name}):\n')
    puzzle.pprint()
    solver = Solver(puzzle)
    solution = solver.solve()

    if solution is not None:
        print(f'\nSolution ({name}):\n')
        solution.pprint()

        #<experimental zone>
        simplest = solver.filter_cores(solution)
        if simplest is not None:
            solver.show_hints(simplest)
        #</experimental zone>



def main():
    analyze(puzzle_1, "evil")
    analyze(extreme_1, "extreme #1")
    analyze(extreme_2, "extreme #2")
    analyze(extreme_3, "extreme #3")
    analyze(extreme_4, "extreme #4")
    analyze(hardest, "hardest")

if __name__ == '__main__':
    main()
    print(Census.dump())
    Yices.exit(True)
