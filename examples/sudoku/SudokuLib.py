"""The shared code used in the cores and generator scripts."""

import copy

from yices.Types import Types
from yices.Terms import Terms


int_t = Types.int_type()

#seems logical to make the terms in a grid.
def make_grid():
    grid = [None] * 9
    for i in range(9):
        grid[i] = [None] * 9
    return grid

#make the constants that we will need
def make_constants():
    constants = {}
    for i in range(1, 10):
        constants[i] = Terms.integer(i)
    return constants

#make the variables that we will need
def make_variables():
    variables = make_grid()
    for i in range(9):
        for j in range(9):
            variables[i][j] = Terms.new_uninterpreted_term(int_t)
    return variables

def subsquare(row, column):
    rname = { 0: 'Top', 1: 'Middle', 2: 'Bottom'}
    cname = { 0: 'left', 1: 'center', 2: 'right'}
    return f'{rname[row]}-{cname[column]}'


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
        for row in range(3):
            for column in range(3):
                rule = Terms.distinct([self.var(i + 3 * row, j + 3 * column) for i in range(3) for j in range(3)])
                self.explanation[rule] = f'{subsquare(row,column)} subsquare cannot contain duplicates'
                rules.append(rule)
        return rules


class Puzzle:

    def __init__(self, matrix):
        self.grid = make_grid()
        if matrix is not None:
            for i in range(9):
                for j in range(9):
                    val =  matrix[i][j]
                    if val != 0:
                        self.set_slot(i, j, matrix[i][j])

    def clone(self):
        result = Puzzle(None)
        result.grid = copy.deepcopy(self.grid)
        return result

    def erase_slot(self, i, j):
        if 0 <= i <= 8 and 0 <= j <= 8:
            self.grid[i][j] = None
            return None
        raise Exception(f'Index error: {i} {j}')

    def set_slot(self, i, j, val):
        if 0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9:
            self.grid[i][j] = val
            return None
        raise Exception(f'Index error: {i} {j} {val}')

    def get_slot(self, i, j):
        if 0 <= i <= 8 and 0 <= j <= 8:
            return self.grid[i][j]
        raise Exception(f'Index error: {i} {j}')

    def pp(self, i, j):
        val = self.get_slot(i,j)
        return f' {val} ' if val is not None else ' . '

    def pprint(self):
        for row in range(9):
            print(f'{self.pp(row,0)}{self.pp(row,1)}{self.pp(row,2)}{self.pp(row,3)}{self.pp(row,4)}{self.pp(row,5)}{self.pp(row,6)}{self.pp(row,7)}{self.pp(row,8)}')


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
