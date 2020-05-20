import sys
import unittest
import os.path

from yices.Config import Config
from yices.Context import Context
from yices.Dimacs import Dimacs
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


class TestDimacs(unittest.TestCase):

    def setUp(self):
        Yices.init()

    def tearDown(self):
        Yices.exit()

    def test_dimacs(self):

        formulas = make_formulas()

        bound = len(formulas) + 1

        simplified = [None] * bound

        # first round, don't simplify the CNF
        for i in range(1, bound):
            simplify = False
            filename = f'/tmp/basic{1}.cnf'
            terms = truncate(formulas, i)

            file_ok, status = Dimacs.export_formulas(terms, filename, simplify)

            notify(f'Round 1: {file_ok}, {Status.name(status)} = export@{i}({terms}, {filename}, {simplify})\n')

            if file_ok:
                self.assertEqual(os.path.exists(filename), True)
            else:
                self.assertEqual(status in [Status.SAT, Status.UNSAT], True)

            term = Terms.yand(terms)
            file_ok_c, status_c = Dimacs.export_formula(term, filename, simplify)

            notify(f'Round 1: {file_ok_c}, {Status.name(status_c)} = export@{i}({term}, {filename}, {simplify})\n')



        # second round, simplify the CNF
        for i in range(1, bound):
            simplify = True
            filename = f'/tmp/simplify{i}.cnf'
            terms = truncate(formulas, i)

            file_ok, status = Dimacs.export_formulas(terms, filename, simplify)

            # save the status for later
            simplified[i] = status

            notify(f'Round 2: {file_ok}, {Status.name(status)} = export@{i}({terms}, {filename}, {simplify})\n')

            if file_ok:
                self.assertEqual(os.path.exists(filename), True)
            else:
                self.assertEqual(status in [Status.SAT, Status.UNSAT], True)

            term = Terms.yand(terms)
            file_ok_c, status_c = Dimacs.export_formula(term, filename, simplify)

            notify(f'Round 2: {file_ok_c}, {Status.name(status_c)} = export@{i}({term}, {filename}, {simplify})\n')

            self.assertEqual(status_c, simplified[i])


        # third round check the results
        for i in range(1, bound):
            config = Config()
            config.default_config_for_logic("QF_BV")
            context = Context(config)
            terms = truncate(formulas, i)
            context.assert_formulas(terms)
            status = context.check_context()
            notify(f'Round 3: status = {Status.name(status)} for i = {i}\n')
            self.assertEqual(status, simplified[i])
            config.dispose()
            context.dispose()
