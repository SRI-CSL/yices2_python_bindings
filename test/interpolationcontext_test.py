import unittest

from yices.Config import Config
from yices.Context import Context
from yices.Parameters import Parameters
from yices.Status import Status
from yices.InterpolationContext import InterpolationContext
from yices.Types import Types
from yices.Terms import Terms
#from yices.YicesException import YicesException
from yices.Yices import Yices

# pylint: disable=E0401
from .utils import define_const, assert_formula

class TestInterpolationContext(unittest.TestCase):

    def setUp(self):
        Yices.init()
        self.real_t = Types.real_type()

    def tearDown(self):
        Yices.exit()


    def test_trivial_ok(self):
        cfg = Config()
        cfg.set_config("solver-type", "mcsat")
        cfg.set_config("model-interpolation", "true")
        ctx_a = Context(cfg)
        ctx_b = Context(cfg)
        param = Parameters()
        param.default_params_for_context(ctx_a)
        ictx = InterpolationContext(ctx_a, ctx_b)
        status = ictx.check(param, True)
        print(f'Status = {Status.name(status)}')
        print(f'Yices.error_string() = {Yices.error_string()}')
        self.assertEqual(status, Status.SAT)
        param.dispose()
        ctx_a.dispose()
        ctx_b.dispose()
        cfg.dispose()

    def test_trivial_bad(self):
        cfg = Config()
        ctx_a = Context(cfg)
        ctx_b = Context(cfg)
        param = Parameters()
        param.default_params_for_context(ctx_a)
        ictx = InterpolationContext(ctx_a, ctx_b)
        status = ictx.check(param, True)
        print(f'Status = {Status.name(status)}')
        print(f'Yices.error_string() = {Yices.error_string()}')
        self.assertEqual(status, Status.ERROR)
        self.assertEqual(Yices.error_string(), "operation not supported by the context")
        param.dispose()
        ctx_a.dispose()
        ctx_b.dispose()
        cfg.dispose()


    def test_model_sat(self):
        cfg = Config()
        cfg.set_config("solver-type", "mcsat")
        cfg.set_config("model-interpolation", "true")
        ctx_a = Context(cfg)
        ctx_b = Context(cfg)

        r1 = define_const('r1', self.real_t)
        r2 = define_const('r2', self.real_t)
        assert_formula('(> r1 3)', ctx_a)
        assert_formula('(< r1 4)', ctx_a)
        assert_formula('(< (- r1 r2) 0)', ctx_a)


        ictx = InterpolationContext(ctx_a, ctx_b)
        param = Parameters()
        param.default_params_for_context(ctx_a)
        status = ictx.check(param, True)
        print(f'Yices.error_string() = {Yices.error_string()}')
        print(f'Status = {Status.name(status)}')
        print(f'Model = {ictx.model}')
        self.assertEqual(status, Status.SAT)

        v1 = ictx.model.get_fraction_value(r1)
        v2 = ictx.model.get_fraction_value(r2)

        print(v1, v2)
        self.assertEqual(v1.numerator, 7)
        self.assertEqual(v1.denominator, 2)
        self.assertEqual(v2.numerator, 5)
        self.assertEqual(v2.denominator, 1)

        param.dispose()
        ctx_a.dispose()
        ctx_b.dispose()
        cfg.dispose()


    def test_model_unsat(self):
        cfg = Config()
        cfg.set_config("solver-type", "mcsat")
        cfg.set_config("model-interpolation", "true")
        ctx_a = Context(cfg)
        ctx_b = Context(cfg)

        define_const('r1', self.real_t)
        define_const('r2', self.real_t)
        assert_formula('(> r1 3)', ctx_a)
        assert_formula('(< r1 4)', ctx_a)
        assert_formula('(< (- r1 r2) 0)', ctx_a)

        assert_formula('(< r2 3)', ctx_b)

        ictx = InterpolationContext(ctx_a, ctx_b)
        param = Parameters()
        param.default_params_for_context(ctx_a)
        status = ictx.check(param, True)
        print(f'Yices.error_string() = {Yices.error_string()}')
        print(f'Status = {Status.name(status)}')
        print(f'Interpolant = {Terms.to_string(ictx.interpolant)}')
        self.assertEqual(status, Status.UNSAT)
        self.assertTrue(ictx.interpolant > 0)

        param.dispose()
        ctx_a.dispose()
        ctx_b.dispose()
        cfg.dispose()





if __name__ == '__main__':
    unittest.main()
