import unittest

import yices_api as yapi

#from yices_api import YicesAPIException

# pylint: disable=R0914

class TestContext(unittest.TestCase):

    def setUp(self):
        yapi.yices_init()

    def tearDown(self):
        yapi.yices_exit()

    def test_config(self):
        cfg = yapi.yices_new_config()
        # Valid call
        yapi.yices_set_config(cfg, "mode", "push-pop")
        # Invalid name
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'invalid parameter'):
        #iam: 9/19/2018     yapi.yices_set_config(cfg, "baz", "bar")
        errcode = yapi.yices_set_config(cfg, "baz", "bar")
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'invalid parameter')
        # Invalid value
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'value not valid for parameter'):
        #iam: 9/19/2018     yapi.yices_set_config(cfg, "mode", "bar")
        errcode = yapi.yices_set_config(cfg, "mode", "bar")
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'value not valid for parameter')
        yapi.yices_default_config_for_logic(cfg, "QF_UFNIRA")
        yapi.yices_free_config(cfg)

    def test_context(self):
        cfg = yapi.yices_new_config()
        ctx = yapi.yices_new_context(cfg)
        stat = yapi.yices_context_status(ctx)
        yapi.yices_push(ctx)
        yapi.yices_pop(ctx)
        yapi.yices_reset_context(ctx)
        yapi.yices_context_enable_option(ctx, "arith-elim")
        yapi.yices_context_disable_option(ctx, "arith-elim")
        stat = yapi.yices_context_status(ctx)
        self.assertEqual(stat, 0)
        yapi.yices_reset_context(ctx)
        bool_t = yapi.yices_bool_type()
        bvar1 = yapi.yices_new_variable(bool_t)
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'assertion contains a free variable'):
        #iam: 9/19/2018     yapi.yices_assert_formula(ctx, bvar1)
        errcode = yapi.yices_assert_formula(ctx, bvar1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'assertion contains a free variable')
        bv_t = yapi.yices_bv_type(3)
        bvvar1 = yapi.yices_new_uninterpreted_term(bv_t)
        yapi.yices_set_term_name(bvvar1, 'x')
        bvvar2 = yapi.yices_new_uninterpreted_term(bv_t)
        yapi.yices_set_term_name(bvvar2, 'y')
        bvvar3 = yapi.yices_new_uninterpreted_term(bv_t)
        yapi.yices_set_term_name(bvvar3, 'z')
        fmla1 = yapi.yices_parse_term('(= x (bv-add y z))')
        fmla2 = yapi.yices_parse_term('(bv-gt y 0b000)')
        fmla3 = yapi.yices_parse_term('(bv-gt z 0b000)')
        yapi.yices_assert_formula(ctx, fmla1)
        yapi.yices_assert_formulas(ctx, 3, yapi.make_term_array([fmla1, fmla2, fmla3]))
        smt_stat = yapi.yices_check_context(ctx, None)
        self.assertEqual(smt_stat, yapi.STATUS_SAT)
        yapi.yices_assert_blocking_clause(ctx)
        yapi.yices_stop_search(ctx)
        param = yapi.yices_new_param_record()
        yapi.yices_default_params_for_context(ctx, param)
        yapi.yices_set_param(param, "dyn-ack", "true")
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'invalid parameter'):
        #iam: 9/19/2018     yapi.yices_set_param(param, "foo", "bar")
        errcode = yapi.yices_set_param(param, "foo", "bar")
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'invalid parameter')
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'value not valid for parameter'):
        #iam: 9/19/2018    yapi.yices_set_param(param, "dyn-ack", "bar")
        errcode = yapi.yices_set_param(param, "dyn-ack", "bar")
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'value not valid for parameter')
        yapi.yices_free_param_record(param)
        yapi.yices_free_context(ctx)


if __name__ == '__main__':
    unittest.main()
