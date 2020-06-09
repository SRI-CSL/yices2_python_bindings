from yices.Terms import Terms

from yices.Context import Context

from yices.Status import Status

from yices.Model import Model

from SudokuLib import make_grid
from SudokuLib import Syntax, Puzzle, Cores


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

    def assert_trivial_rules(self, ctx):
        ctx.assert_formulas(self.trivial_rules)

    def assert_duplicate_rules(self, ctx):
        ctx.assert_formulas(self.duplicate_rules)

    def _equality(self, i, j, val):
        return Terms.arith_eq_atom(self.var(i,j), self.constants[val])

    def _inequality(self, i, j, val):
        return Terms.arith_neq_atom(self.var(i,j), self.constants[val])

    def assert_value(self, ctx, i, j, val):
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        ctx.assert_formula(self._equality(i, j, val))

    def assert_not_value(self, ctx, i, j, val):
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        ctx.assert_formula(self._inequality(i, j, val))

    def assert_puzzle(self, ctx):
        terms = []
        for i in range(9):
            for j in range(9):
                val = self.puzzle.get_cell(i, j)
                if val is not None:
                    terms.append(self._equality(i, j, val))
        ctx.assert_formulas(terms)

    def assert_puzzle_except(self, ctx, row, col, ans):
        assert ans == self.puzzle.get_cell(row, col)
        terms = []
        for i in range(9):
            for j in range(9):
                if i != row and j != col:
                    val = self.puzzle.get_cell(i, j)
                    if val is not None:
                        terms.append(self._equality(i, j, val))
        ctx.assert_formulas(terms)


    def puzzle_from_model(self, model):
        if model is None:
            return None
        matrix = make_grid()
        for i in range(9):
            for j in range(9):
                matrix[i][j] = model.get_value(self.var(i, j))
        return Puzzle(matrix)

    def solve(self):
        context = Context()
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

    def filter_cores(self, solution, cutoff=5):
        cores = self.compute_cores(solution)
        if cores is None:
            return None
        print('\nCores:\n')
        smallest = cores.least(cutoff)
        filtered = Cores(len(self.duplicate_rules))
        for core in smallest:
            ncore = self.filter_core(core)
            filtered.add(*ncore)
        print('\nFiltered Cores:\n')
        smallest = filtered.least(5)
        return smallest

    def compute_cores(self, solution, reduced=False):
        cores = Cores(len(self.duplicate_rules))
        if solution is not None:
            for i in range(9):
                for j in range(9):
                    slot = self.puzzle.get_cell(i, j)
                    if slot is None:
                        ans = solution.get_cell(i, j)
                        core = self.compute_reduced_core(i, j, ans) if reduced else self.compute_core(i, j, ans)
                        if core is None:
                            return None
                        cores.add(*core)
        return cores

    def compute_core(self, i, j, val):
        """We compute the unsat core of the duplicate_rules when asserting self.var(i, j) != val w.r.t the puzzle (val is assumed to be the unique solution)."""
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        context = Context()
        self.assert_puzzle(context)
        self.assert_not_value(context, i, j, val)
        self.assert_trivial_rules(context)
        smt_stat = context.check_context_with_assumptions(None, self.duplicate_rules)
        # a valid puzzle should have a unique solution, so this should not happen, if it does we bail
        if smt_stat != Status.UNSAT:
            print(f'Error: {i} {j} {val} - not UNSAT: {Status.name(smt_stat)}')
            model = Model.from_context(context, 1)
            answer = self.puzzle_from_model(model)
            print('Counter example (i.e. origonal puzzle does not have a unique solution):')
            answer.pprint()
            model.dispose()
            context.dispose()
            return None
        core = context.get_unsat_core()
        context.dispose()
        print(f'Core: {i} {j} {val}   {len(core)} / {len(self.duplicate_rules)}')
        return (i, j, val, core)

    def compute_reduced_core(self, i, j, val):
        """We compute the unsat core then remove any unnecessary terms."""
        if not (0 <= i <= 8 and 0 <= j <= 8 and 1 <= val <= 9):
            raise Exception(f'Index error: {i} {j} {val}')
        context = Context()
        self.assert_puzzle(context)
        self.assert_not_value(context, i, j, val)
        self.assert_trivial_rules(context)
        smt_stat = context.check_context_with_assumptions(None, self.duplicate_rules)
        # a valid puzzle should have a unique solution, so this should not happen, if it does we bail
        if smt_stat != Status.UNSAT:
            print(f'Error: {i} {j} {val} - not UNSAT: {Status.name(smt_stat)}')
            model = Model.from_context(context, 1)
            answer = self.puzzle_from_model(model)
            print('Counter example (i.e. origonal puzzle does not have a unique solution):')
            answer.pprint()
            model.dispose()
            context.dispose()
            return None
        core = context.get_unsat_core()
        filtered = core.copy()
        for term in core:
            filtered.remove(term)
            smt_stat = context.check_context_with_assumptions(None, filtered)
            if smt_stat != Status.UNSAT:
                filtered.append(term)
        context.dispose()
        print(f'Core: {i} {j} {val}   {len(filtered)} / {len(self.duplicate_rules)}')
        return (i, j, val, filtered)

    def filter_core(self, core):
        i, j, val, terms = core
        context = Context()
        self.assert_puzzle(context)
        self.assert_not_value(context, i, j, val)
        self.assert_trivial_rules(context)
        filtered = terms.copy()
        for term in terms:
            filtered.remove(term)
            smt_stat = context.check_context_with_assumptions(None, filtered)
            if smt_stat != Status.UNSAT:
                filtered.append(term)
        context.dispose()
        return (i, j, val, filtered)

    def erasable(self, ctx, i, j, val):
        """erasable returns True if puzzle (with [row, col] = val omitted) implies that [row, col] = val, it returns False otherwise.

        It is assumed that puzzle.get_cell(i,j) == val
        The context has already been informed of the rules.
        """
        ctx.push()
        self.assert_puzzle_except(ctx, i, j, val)
        self.assert_not_value(ctx, i, j, val)
        smt_stat = ctx.check_context(None)
        ctx.pop()
        return smt_stat == Status.UNSAT

    def show_hints(self, cores):
        for core in cores:
            i, j, val, terms = core
            print(f'[{i}, {j}] = {val} is forced by the following rules:')
            for term in terms:
                print(f'\t{self.syntax.explanation[term]}')
