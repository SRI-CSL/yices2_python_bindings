"""The shared code used in the cores and generator scripts."""

import copy

from yices.Types import Types
from yices.Terms import Terms


int_t = Types.int_type()


def make_grid():
    """make_grid constructs a 9x9 grid all whose entries are initially None."""
    grid = [None] * 9
    for i in range(9):
        grid[i] = [None] * 9
    return grid

def make_constants():
    """make_constants makes a map from the digits 1 through 9 to the Yices constant denoting that digit."""
    constants = {}
    for i in range(1, 10):
        constants[i] = Terms.integer(i)
    return constants

def make_variables():
    """make_variables creates a 9x9 grid with each cell containing the Yices term representing that cell."""
    variables = make_grid()
    for i in range(9):
        for j in range(9):
            variables[i][j] = Terms.new_uninterpreted_term(int_t)
    return variables

class SudokuError(Exception):
    """
    An application specific error.
    """

class Syntax:

    def __init__(self):
        self.constants = make_constants()
        self.variables = make_variables()

        # maps non-trivial rules to an informative string describing them
        self.explanation = {}
        # dividing the rules into trivial and non trivial is used in getting unsat cores (of non-trivial rules)
        self.trivial_rules = self.make_trivial_rules()
        self.duplicate_rules = self.make_duplicate_rules()
        self.all_rules = self.trivial_rules.copy()
        self.all_rules.extend(self.duplicate_rules)


    def var(self, i, j):
        return self.variables[i][j]

    # x is between 1 and 9
    def between_1_and_9(self, x):
        return Terms.yor([Terms.eq(x, self.constants[i+1]) for i in range(9)])

    def make_trivial_rules(self):
        rules = []
        # Every variable is between 1 and 9 inclusive
        for i in range(9):
            for j in range(9):
                rules.append(self.between_1_and_9(self.var(i, j)))
        return rules


    def make_duplicate_rules(self):
        rules = []
        # All elements in a row must be distinct
        for i in range(9):
            rule = Terms.distinct([self.var(i, j) for j in range(9)])
            self.explanation[rule] = f'Row {i + 1} cannot contain duplicates'
            rules.append(rule)
        # All elements in a column must be distinct
        for i in range(9):
            rule = Terms.distinct([self.var(j, i) for j in range(9)]) # pylint: disable=W1114
            self.explanation[rule] = f'Column {i + 1} cannot contain duplicates'
            rules.append(rule)
        # All elements in each 3x3 square must be distinct
        def subsquare(row, column):
            rname = { 0: 'Top', 1: 'Middle', 2: 'Bottom'}
            cname = { 0: 'left', 1: 'center', 2: 'right'}
            return f'{rname[row]}-{cname[column]}'
        for row in range(3):
            for column in range(3):
                rule = Terms.distinct([self.var(i + 3 * row, j + 3 * column) for i in range(3) for j in range(3)])
                self.explanation[rule] = f'{subsquare(row,column)} subsquare cannot contain duplicates'
                rules.append(rule)
        return rules



class Puzzle:
    """Puzzle is a 9x9 grid of digits between 1 and 9 inclusive, or None."""

    def puzzle2path(self, path):
        with open(path, 'w') as fp:
            fp.write(self.to_string('', '0'))

    @staticmethod
    def path2puzzle(path):
        with open(path, 'r') as fp:
            matrix = make_grid()
            row = 0
            col = 0
            for line in fp:
                line = line.strip()
                if len(line) != 9:
                    raise SudokuError('Each line in the sudoku puzzle must be 9 chars long.')
                for char in line:
                    if not char.isdigit():
                        raise SudokuError('Valid characters for a sudoku puzzle must be in 0-9')
                    matrix[row][col] = int(char) # pylint: disable=E1137
                    col += 1
                row += 1
                col = 0
                if row == 9:
                    break
            return Puzzle(matrix)


    def __init__(self, matrix):
        self.grid = make_grid()
        if matrix is not None:
            for i in range(9):
                for j in range(9):
                    val =  matrix[i][j]
                    if val != 0:
                        self.set_cell(i, j, matrix[i][j])

    def clone(self):
        """clone creates a deep copy of the puzzle."""
        result = Puzzle(None)
        result.grid = copy.deepcopy(self.grid)
        return result

    def erase_cell(self, i, j):
        if 0 <= i <= 8 and 0 <= j <= 8:
            self.grid[i][j] = None
            return None
        raise Exception(f'Index error: {i} {j}')

    def set_cell(self, i, j, val):
        if 0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9:
            self.grid[i][j] = val
            return None
        raise Exception(f'Index error: {i} {j} {val}')

    def get_cell(self, i, j):
        if 0 <= i <= 8 and 0 <= j <= 8:
            return self.grid[i][j]
        raise Exception(f'Index error: {i} {j}')

    def to_string(self, pad='  ', blank='.', newline='\n'):
        def pp(i, j, blank='.'):
            val = self.get_cell(i, j)
            return str(val) if val is not None else blank
        rows = []
        for row in range(9):
            line = [pp(row, col, blank) for col in range(9)]
            rows.append(pad.join(line))
        return newline.join(rows)


    def pprint(self, pad='  ', blank='.', newline='\n'):
        print(self.to_string(pad, blank, newline))

class Cores:

    def __init__(self, card):
        self.core_map = {}
        self.maximum = card

    def add(self, i, j, val, core):
        key = len(core)
        entry = []
        if key not in self.core_map:
            self.core_map[key] = entry
        else:
            entry = self.core_map[key]
        entry.append(tuple([i, j, val, core]))

    def least(self, count):
        retval = []
        counter = 0
        for i in range(self.maximum + 1):
            if i in self.core_map:
                vec = self.core_map[i]
                for v in vec: # pylint: disable=C0103
                    retval.append(v)
                    print(f'OK: {v[0]} {v[1]} {v[2]}   {len(v[3])} / {self.maximum}')
                    counter += 1
                    if counter >= count:
                        return retval
        return retval
