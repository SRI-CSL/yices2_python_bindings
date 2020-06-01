#!/usr/bin/env python

from enum import Enum, auto

from yices.Types import Types

from yices.Terms import Terms

from yices.Config import Config

from yices.Context import Context

from yices.Status import Status

from yices.Model import Model

from yices.Yices import Yices


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

C = make_constants()
one = C[1]
nine = C[9]

# x is between 1 and 9
def between_1_and_9(x):
    return Terms.yand([Terms.arith_leq_atom(one, x), Terms.arith_leq_atom(x, nine)])


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


class Puzzle:

    def __init__(self, matrix):
        self.grid = make_grid()
        for i in range(9):
            for j in range(9):
                val =  matrix[i][j]
                if val != 0:
                    self.set_slot(i, j, matrix[i][j])


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



class Rules(Enum):
    BETWEEN_1_AND_9 = auto()
    ROWS_HAVE_NO_DUPLICATES = auto()
    COLUMNS_HAVE_NO_DUPLICATES = auto()
    SUBSQUARES_HAVE_NO_DUPLICATES = auto()

    @staticmethod
    def all_rules():
        return tuple(Rules)

    @staticmethod
    def duplicate_rules():
        rlist = list(Rules)
        rlist.remove(Rules.BETWEEN_1_AND_9)
        return tuple(rlist)

    @staticmethod
    def numeral_rules():
        return [Rules.BETWEEN_1_AND_9]


class Cores:

    def __init__(self, univ):
        self.core_map = {}
        self.universe = univ
        self.maximum = len(univ) + 1

    def add(self, i, j, val, core):
        key = len(core)
        entry = []
        if key not in self.core_map:
            self.core_map[key] = entry
        else:
            entry = self.core_map[key]
        entry.append(tuple([i, j, val, core]))

    def show(self, count):
        counter = 0
        for i in range(self.maximum + 1):
            if i in self.core_map:
                vec = self.core_map[i]
                for v in vec: # pylint: disable=C0103
                    print(f'OK: {v[0]} {v[1]} {v[2]}   {len(v[3])} / {self.maximum}')
                counter += 1
                if counter >= count:
                    return


class Solver:

    def __init__(self, pzl):
        self.puzzle = pzl
        self.variables = make_grid()
        for i in range(9):
            for j in range(9):
                self.variables[i][j] = Terms.new_uninterpreted_term(int_t)
        self.all_rules = self.make_rules()
        self.duplicate_rules = self.make_rules(Rules.duplicate_rules())
        self.numeral_rules = self.make_rules(Rules.numeral_rules())

    def var(self, i, j):
        return self.variables[i][j]


    # make the rules of the game as a list of yices terms.
    def make_rules(self, rules_wanted=Rules.all_rules()):
        rules = []
        # Every element is between 1 and 9
        if Rules.BETWEEN_1_AND_9 in rules_wanted:
            for i in range(9):
                for j in range(9):
                    rules.append(between_1_and_9(self.var(i, j)))
        # All elements in a row must be distinct
        if Rules.ROWS_HAVE_NO_DUPLICATES in rules_wanted:
            for i in range(9):
                rules.append(Terms.distinct([self.var(i, j) for j in range(9)]))
        # All elements in a column must be distinct
        if Rules.COLUMNS_HAVE_NO_DUPLICATES in rules_wanted:
            for i in range(9):
                rules.append(Terms.distinct([self.var(j, i) for j in range(9)])) # pylint: disable=W1114
        # All elements in each 3x3 square must be distinct
        if Rules.SUBSQUARES_HAVE_NO_DUPLICATES in rules_wanted:
            for k in range(3):
                for l in range(3): # pylint: disable=C0103
                    rules.append(Terms.distinct([self.var(i + 3 * l, j + 3 * k) for i in range(3) for j in range(3)]))
        return rules

    def assert_rules(self, ctx):
        ctx.assert_formulas(self.all_rules)


    def assert_value(self, ctx, i, j, val):
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        ctx.assert_formula(Terms.arith_eq_atom(self.var(i,j), C[val]))

    def assert_not_value(self, ctx, i, j, val):
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        ctx.assert_formula(Terms.arith_neq_atom(self.var(i,j), C[val]))


    def assert_puzzle(self, ctx):
        for i in range(9):
            for j in range(9):
                val = puzzle.get_slot(i, j)
                if val is not None:
                    self.assert_value(ctx, i, j, val)

    def puzzle_from_model(self, model):
        if model is None:
            return None
        matrix = make_grid()
        for i in range(9):
            for j in range(9):
                matrix[i][j] = model.get_value(self.var(i, j))
        return Puzzle(matrix)

    def solve(self):
        config = Config()
        config.default_config_for_logic("QF_LIA")
        context = Context(config)
        config.dispose()
        self.assert_rules(context)
        self.assert_puzzle(context)
        smt_stat = context.check_context(None)
        answer = None
        if smt_stat == Status.SAT:
            model = Model.from_context(context, 1)
            answer =  self.puzzle_from_model(model)
            model.dispose()
        context.dispose()
        return answer


    def investigate(self, i, j, val):
        """We look at the unsat core of asserting self.var(i, j) != val (val is assumed to be the unique solution)."""
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        config = Config()
        config.default_config_for_logic("QF_LIA")
        context = Context(config)
        config.dispose()
        self.assert_puzzle(context)
        self.assert_not_value(context, i, j, val)
        context.assert_formulas(self.numeral_rules)
        smt_stat = context.check_context_with_assumptions(None, self.duplicate_rules)
        if smt_stat != Status.UNSAT:
            print(f'Error: {i} {j} {val} - not UNSAT: {Status.name(smt_stat)}')
            model = Model.from_context(context, 1)
            answer = self.puzzle_from_model(model)
            answer.pprint()
            model.dispose()
        else:
            core = context.get_unsat_core()
            #print(f'OK: {i} {j} {val}   {len(core)} / {len(self.duplicate_rules)}')
        context.dispose()
        return core

    def show_cores(self, sln):
        cores = Cores(self.duplicate_rules)
        if sln is not None:
            for i in range(9):
                for j in range(9):
                    slot = self.puzzle.get_slot(i, j)
                    if slot is None:
                        ans = sln.get_slot(i, j)
                        core = self.investigate(i, j, ans)
                        cores.add(i, j, ans, core)
        print('\nCores:\n')
        cores.show(4)


puzzle = Puzzle(puzzle_1)

puzzle.pprint()

solver = Solver(puzzle)

solution = solver.solve()

if solution is not None:
    print('\nSolution:\n')
    solution.pprint()

#<experimental zone>
solver.show_cores(solution)
#</experimental zone>


print('\nCensus:\n')
Yices.exit(True)
