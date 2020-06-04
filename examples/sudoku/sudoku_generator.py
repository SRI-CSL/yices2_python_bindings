#!/usr/bin/env python

"""Using Yices to generate Sudoku puzzles analagous to https://github.com/arel/arels-sudoku-generator.git."""

import sys
import random


from SudokuLib import Puzzle



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



def  run(n = 28, iterations=100):
    all_results = {}
    print(f'Using n={n} and iterations={iterations}')
    solution = make_solution()
    answer = Puzzle(solution)
    answer.pprint()

    return all_results

def main():
    results = None
    if len(sys.argv) == 3:
        n = int(sys.argv[1])
        iterations = int(sys.argv[2])
        results = run(n, iterations)
    else:
        results = run()
    print(results)





if __name__ == '__main__':
    main()
