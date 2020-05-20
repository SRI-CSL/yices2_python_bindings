import sys
import unittest

from yices.Config import Config
from yices.Context import Context
from yices.Delegates import Delegates
from yices.Status import Status
from yices.Terms import Terms
from yices.Types import Types
from yices.Yices import Yices

def make_formulas():
    tau = Types.bv_type(20)
    x0 = Terms.new_uninterpreted_term(tau, "x")
    y0 = Terms.new_uninterpreted_term(tau, "y")
    z0 = Terms.new_uninterpreted_term(tau, "z")
    f0 = Terms.bveq_atom(Terms.bvmul(x0, y0), Terms.bvconst_integer(20, 12289))
    f1 = Terms.bveq_atom(Terms.bvmul(y0, z0), Terms.bvconst_integer(20, 20031))
    f2 = Terms.bveq_atom(Terms.bvmul(x0, z0), Terms.bvconst_integer(20, 10227))
    return [f0, f1, f2]

def truncate(formulas, n):
    """Returns an array of the first n members of formulas."""
    if n >= len(formulas):
        return formulas
    return formulas[0:n]

def conjoin(formulas, n):
    return Terms.yand(truncate(formulas, n))


def notify(message):
    sys.stdout.write(message)
    sys.stdout.flush()


class TestDelegates(unittest.TestCase):

    def setUp(self):
        Yices.init()

    def tearDown(self):
        Yices.exit()

    def delgado(self, delegate):

        if not Delegates.has_delegate(delegate):
            notify(f'delgado skipping missing delegate {delegate}\n')
            return

        formulas = make_formulas()

        bound = len(formulas) + 1

        for i in range(1, bound):
            config = Config()
            config.default_config_for_logic("QF_BV")
            context = Context(config)
            terms = truncate(formulas, i)
            context.assert_formulas(terms)
            status = context.check_context()
            notify(f'delgado status = {Status.name(status)} for i = {i}\n')
            self.assertEqual(status, Status.SAT if i < 3 else Status.UNSAT)
            config.dispose()
            context.dispose()


        for i in range(1, bound):
            model = []
            terms = truncate(formulas, i)
            status = Delegates.check_formulas(terms, "QF_BV", delegate, model)
            notify(f'delagdo({delegate}) status = {Status.name(status)} for i = {i}\n')
            self.assertEqual(status, Status.SAT if i < 3 else Status.UNSAT)
            if status is Status.SAT:
                notify(f'delagdo({delegate}) model = {model[0].to_string(80, 100, 0)} for i = {i}\n')
            else:
                self.assertEqual(len(model), 0)


        for i in range(1, bound):
            model = []
            term = conjoin(formulas, i)
            status = Delegates.check_formula(term, "QF_BV", delegate, model)
            notify(f'delagdo({delegate}) status = {Status.name(status)} for i = {i}\n')
            self.assertEqual(status, Status.SAT if i < 3 else Status.UNSAT)
            if status is Status.SAT:
                notify(f'delagdo({delegate}) model = {model[0].to_string(80, 100, 0)} for i = {i}\n')
            else:
                self.assertEqual(len(model), 0)





    def test_cadical(self):
        Yices.reset()
        self.delgado("cadical")

    def test_cryptominisat(self):
        Yices.reset()
        self.delgado("cryptominisat")

    def test_y2sat(self):
        Yices.reset()
        self.delgado("y2sat")
