#!/usr/bin/env python

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

#make the variables that we will need
def make_variables():
    variables = make_grid()
    for i in range(9):
        for j in range(9):
            variables[i][j] = Terms.new_uninterpreted_term(int_t)
    return variables

def make_context():
    #config = Config()
    #config.default_config_for_logic("QF_LIA")
    #context = Context(config)
    #config.dispose()
    #return context
    return Context()

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

class Solver:

    def __init__(self, pzl):
        self.puzzle = pzl

        # isolate all the syntax in one place
        self.syntax = Syntax()

        self.variables = self.syntax.variables
        self.constants = self.syntax.constants

        self.duplicate_rules = self.syntax.duplicate_rules
        self.trivial_rules = self.syntax.trivial_rules
        self.all_rules = self.syntax.all_rules

    def var(self, i, j):
        return self.variables[i][j]

    def assert_rules(self, ctx):
        ctx.assert_formulas(self.all_rules)


    def assert_value(self, ctx, i, j, val):
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        ctx.assert_formula(Terms.arith_eq_atom(self.var(i,j), self.constants[val]))

    def assert_not_value(self, ctx, i, j, val):
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        ctx.assert_formula(Terms.arith_neq_atom(self.var(i,j), self.constants[val]))


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
        context = make_context()
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
        context = make_context()
        self.assert_puzzle(context)
        self.assert_not_value(context, i, j, val)
        context.assert_formulas(self.trivial_rules)
        smt_stat = context.check_context_with_assumptions(None, self.duplicate_rules)
        if smt_stat != Status.UNSAT:
            print(f'Error: {i} {j} {val} - not UNSAT: {Status.name(smt_stat)}')
            model = Model.from_context(context, 1)
            answer = self.puzzle_from_model(model)
            answer.pprint()
            model.dispose()
        else:
            core = context.get_unsat_core()
            #print(f'Before: {i} {j} {val}   {len(core)} / {len(self.duplicate_rules)}')
        context.dispose()
        return core

    def filter_cores(self, sln):
        cores = Cores(len(self.duplicate_rules))
        if sln is not None:
            for i in range(9):
                for j in range(9):
                    slot = self.puzzle.get_slot(i, j)
                    if slot is None:
                        ans = sln.get_slot(i, j)
                        core = self.investigate(i, j, ans)
                        cores.add(i, j, ans, core)
        print('\nCores:\n')
        smallest = cores.least(5)
        filtered = Cores(len(self.duplicate_rules))
        for core in smallest:
            ncore = self.filter_core(core)
            filtered.add(*ncore)
        print('\nFiltered Cores:\n')
        smallest = filtered.least(5)
        return smallest

    def filter_core(self, core):
        i, j, val, terms = core
        context = make_context()
        self.assert_puzzle(context)
        self.assert_not_value(context, i, j, val)
        context.assert_formulas(self.trivial_rules)
        filtered = terms.copy()
        for term in terms:
            filtered.remove(term)
            smt_stat = context.check_context_with_assumptions(None, filtered)
            if smt_stat != Status.UNSAT:
                filtered.append(term)
        #print(f'Original: {len(terms)} Filtered: {len(filtered)}')
        context.dispose()
        return (i, j, val, filtered)


    def show_hints(self, cores):
        for core in cores:
            i, j, val, terms = core
            print(f'[{i}, {j}] = {val} is forced by the following rules:')
            for term in terms:
                print(f'\t{self.syntax.explanation[term]}')


puzzle = Puzzle(puzzle_1)

puzzle.pprint()

solver = Solver(puzzle)

solution = solver.solve()

if solution is not None:
    print('\nSolution:\n')
    solution.pprint()

#<experimental zone>
simplest = solver.filter_cores(solution)
solver.show_hints(simplest)
#</experimental zone>


print('\nCensus:\n')
Yices.exit(True)
