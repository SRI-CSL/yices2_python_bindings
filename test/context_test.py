import unittest

from yices.Config import Config
from yices.Context import Context
from yices.Parameters import Parameters
from yices.Status import Status
from yices.Types import Types
from yices.Terms import Terms
from yices.YicesException import YicesException
from yices.Yices import Yices

# pylint: disable=R0914
# pylint: disable=W0612

def assertRaisesRegex(cxt, e, s):
    return cxt.assertRaisesRegex(e, s)

class TestContext(unittest.TestCase):

    def setUp(self):
        Yices.init()

    def tearDown(self):
        Yices.exit()

    def test_config(self):
        cfg = Config()
        # Valid call
        cfg.set_config("mode", "push-pop")
        # Invalid name
        with assertRaisesRegex(self, YicesException, 'invalid parameter'):
            cfg.set_config("baz", "bar")
        # Invalid value
        with assertRaisesRegex(self, YicesException, 'value not valid for parameter'):
            cfg.set_config("mode", "bar")
        cfg.default_config_for_logic("QF_UFNIRA")
        cfg.dispose()

    def test_context(self):
        cfg = Config()
        ctx = Context(cfg)
        stat = ctx.status()
        ret = ctx.push()
        ret = ctx.pop()
        ctx.reset_context()
        ret = ctx.enable_option("arith-elim")
        ret = ctx.disable_option("arith-elim")
        stat = ctx.status()
        self.assertEqual(stat, 0)
        ctx.reset_context()
        bool_t = Types.bool_type()
        bvar1 = Terms.new_variable(bool_t)
        with assertRaisesRegex(self, YicesException, 'assertion contains a free variable'):
            ctx.assert_formula(bvar1)
        bv_t = Types.bv_type(3)
        bvvar1 = Terms.new_uninterpreted_term(bv_t, 'x')
        bvvar2 = Terms.new_uninterpreted_term(bv_t, 'y')
        bvvar3 = Terms.new_uninterpreted_term(bv_t, 'z')
        fmla1 = Terms.parse_term('(= x (bv-add y z))')
        fmla2 = Terms.parse_term('(bv-gt y 0b000)')
        fmla3 = Terms.parse_term('(bv-gt z 0b000)')
        ctx.assert_formula(fmla1)
        ctx.assert_formulas([fmla1, fmla2, fmla3])
        smt_stat = ctx.check_context(None)
        self.assertEqual(smt_stat, Status.SAT)
        ctx.assert_blocking_clause()
        ctx.stop_search()
        param = Parameters()
        param.default_params_for_context(ctx)
        param.set_param("dyn-ack", "true")
        with assertRaisesRegex(self, YicesException, 'invalid parameter'):
            param.set_param("foo", "bar")
        with assertRaisesRegex(self, YicesException, 'value not valid for parameter'):
            param.set_param("dyn-ack", "bar")
        param.dispose()
        ctx.dispose()


if __name__ == '__main__':
    unittest.main()
