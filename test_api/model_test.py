import unittest

from ctypes import ( c_int, c_int32, c_uint32, c_int64, c_uint64, c_double )

import yices_api as yapi

from yices_api import YicesAPIException


def isstr(s):
    return isinstance(s, str)

# pylint: disable=R0914
# pylint: disable=R0915

def define_type(name, ytype=None):
    '''Tries to emulate yices type declarations'''
    if ytype is None:
        ytyp = yapi.yices_new_uninterpreted_type()
    elif isstr(ytype):
        ytyp = yapi.yices_parse_type(ytype)
    else:
        ytyp = ytype
    yapi.yices_set_type_name(ytyp, name)
    return ytyp

def define_const(name, ytype, defn=None):
    '''Tries to emulate yices define_term
    (see eval_define_term in yices2/src/parser_utils/term_stack2)
    '''
    if defn is None:
        term = yapi.yices_new_uninterpreted_term(ytype)
        yapi.yices_set_term_name(term, name)
        return term
    # Have a defn
    if isstr(defn):
        term = yapi.yices_parse_term(defn)
    else:
        term = defn
    term_type = yapi.yices_type_of_term(term)
    if not yapi.yices_test_subtype(term_type, ytype):
        raise YicesAPIException('incompatible sort in definition')
    yapi.yices_set_term_name(term, name)
    return term

def assert_formula(formula, ctx):
    if isstr(formula):
        formula = yapi.yices_parse_term(formula)
    yapi.yices_assert_formula(ctx, formula)


class TestModels(unittest.TestCase):

    def setUp(self):
        yapi.yices_init()
        self.cfg = yapi.yices_new_config()
        self.ctx = yapi.yices_new_context(self.cfg)
        self.param = yapi.yices_new_param_record()
        yapi.yices_default_params_for_context(self.ctx, self.param)
        self.bool_t = yapi.yices_bool_type()
        self.int_t = yapi.yices_int_type()
        self.real_t = yapi.yices_real_type()


    def tearDown(self):
        #yapi.yices_exit()
        pass


    def test_bool_models(self):
        b1 = define_const('b1', self.bool_t)
        b2 = define_const('b2', self.bool_t)
        b3 = define_const('b3', self.bool_t)
        b_fml1 = yapi.yices_parse_term('(or b1 b2 b3)')
        yapi.yices_assert_formula(self.ctx, b_fml1)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        b_mdl1 = yapi.yices_get_model(self.ctx, 1)
        self.assertNotEqual(b_mdl1, None)
        # init to -1 to make sure they get updated
        bval1 = c_int32()
        bval2 = c_int32()
        bval3 = c_int32()
        yapi.yices_get_bool_value(b_mdl1, b1, bval1)
        yapi.yices_get_bool_value(b_mdl1, b2, bval2)
        yapi.yices_get_bool_value(b_mdl1, b3, bval3)
        self.assertEqual(bval1.value, 0)
        self.assertEqual(bval2.value, 0)
        self.assertEqual(bval3.value, 1)
        b_fmla2 = yapi.yices_parse_term('(not b3)')
        yapi.yices_assert_formula(self.ctx, b_fmla2)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        b_mdl1 = yapi.yices_get_model(self.ctx, 1)
        self.assertNotEqual(b_mdl1, None)
        yapi.yices_get_bool_value(b_mdl1, b1, bval1)
        yapi.yices_get_bool_value(b_mdl1, b2, bval2)
        yapi.yices_get_bool_value(b_mdl1, b3, bval3)
        self.assertEqual(bval1.value, 0)
        self.assertEqual(bval2.value, 1)
        self.assertEqual(bval3.value, 0)
        yv1 = yapi.yval_t()
        yapi.yices_get_value(b_mdl1, b1, yv1)
        self.assertEqual(yv1.node_tag, yapi.YVAL_BOOL)
        yapi.yices_val_get_bool(b_mdl1, yv1, bval1)
        self.assertEqual(bval1.value, 0)

    def test_int_models(self):
        ''' int32, int64 '''
        i1 = define_const('i1', self.int_t)
        i2 = define_const('i2', self.int_t)
        assert_formula('(> i1 3)', self.ctx)
        assert_formula('(< i2 i1)', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        i32v1 = c_int32()
        i32v2 = c_int32()
        yapi.yices_get_int32_value(mdl, i1, i32v1)
        yapi.yices_get_int32_value(mdl, i2, i32v2)
        self.assertEqual(i32v1.value, 4)
        self.assertEqual(i32v2.value, 3)
        i64v1 = c_int64()
        i64v2 = c_int64()
        yapi.yices_get_int64_value(mdl, i1, i64v1)
        yapi.yices_get_int64_value(mdl, i2, i64v2)
        self.assertEqual(i64v1.value, 4)
        self.assertEqual(i64v2.value, 3)
        yapi.yices_print_model_fd(1, mdl)
        yapi.yices_pp_model_fd(1, mdl, 80, 100, 0)
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= i1 4)\n(= i2 3)')
        #alg1 = yapi.lp_algebraic_number_t()
        #yapi.yices_get_algebraic_number_value(mdl, i1, alg1)


    def test_rat_models(self):
        ''' rational32, rational64, double '''
        r1 = define_const('r1', self.real_t)
        r2 = define_const('r2', self.real_t)
        assert_formula('(> r1 3)', self.ctx)
        assert_formula('(< r1 4)', self.ctx)
        assert_formula('(< (- r1 r2) 0)', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        r32v1num = c_int32()
        r32v1den = c_uint32()
        r32v2num = c_int32()
        r32v2den = c_uint32()
        yapi.yices_get_rational32_value(mdl, r1, r32v1num, r32v1den)
        yapi.yices_get_rational32_value(mdl, r2, r32v2num, r32v2den)
        # r1 = 7/2, r2 = 4/1
        self.assertEqual(r32v1num.value, 7)
        self.assertEqual(r32v1den.value, 2)
        self.assertEqual(r32v2num.value, 4)
        self.assertEqual(r32v2den.value, 1)
        r64v1num = c_int64()
        r64v1den = c_uint64()
        r64v2num = c_int64()
        r64v2den = c_uint64()
        yapi.yices_get_rational64_value(mdl, r1, r64v1num, r64v1den)
        yapi.yices_get_rational64_value(mdl, r2, r64v2num, r64v2den)
        # r1 = 7/2, r2 = 4/1
        self.assertEqual(r64v1num.value, 7)
        self.assertEqual(r64v1den.value, 2)
        self.assertEqual(r64v2num.value, 4)
        self.assertEqual(r64v2den.value, 1)
        rdoub1 = c_double()
        rdoub2 = c_double()
        yapi.yices_get_double_value(mdl, r1, rdoub1)
        yapi.yices_get_double_value(mdl, r2, rdoub2)
        self.assertEqual(rdoub1.value, 3.5)
        self.assertEqual(rdoub2.value, 4.0)

    def test_mpz_models(self):
        i1 = define_const('i1', self.int_t)
        i2 = define_const('i2', self.int_t)
        assert_formula('(> i1 987654321987654321987654321)', self.ctx)
        assert_formula('(< i2 i1)', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= i1 987654321987654321987654322)\n(= i2 987654321987654321987654321)')
        i32v1 = c_int32()
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException,
        #iam: 9/19/2018                              'eval error: the term value does not fit the expected type'):
        #iam: 9/19/2018     yapi.yices_get_int32_value(mdl, i1, i32v1)
        errcode = yapi.yices_get_int32_value(mdl, i1, i32v1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'eval error: the term value does not fit the expected type')
        i64v1 = c_int64()
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException,
        #iam: 9/19/2018                              'eval error: the term value does not fit the expected type'):
        #iam: 9/19/2018     yapi.yices_get_int64_value(mdl, i1, i64v1)
        errcode = yapi.yices_get_int64_value(mdl, i1, i64v1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'eval error: the term value does not fit the expected type')
        gmpz1 = yapi.yices_new_mpz()
        gmpz2 = yapi.yices_new_mpz()
        yapi.yices_get_mpz_value(mdl, i1, gmpz1)
        yapi.yices_get_mpz_value(mdl, i2, gmpz2)
        mpz1 = yapi.yices_mpz(gmpz1)
        mpz2 = yapi.yices_mpz(gmpz2)
        self.assertEqual(yapi.yices_term_to_string(mpz1, 200, 10, 0), '987654321987654321987654322')
        self.assertEqual(yapi.yices_term_to_string(mpz2, 200, 10, 0), '987654321987654321987654321')
        if not yapi.yices_has_mcsat():
            return
        yapi.yices_pp_term_fd(1, mpz1, 100, 10, 0)
        alg1 = yapi.lp_algebraic_number_t()
        #yapi.yices_get_algebraic_number_value(mdl, i1, alg1)
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException,
        #iam: 9/19/2018                              'could not convert value \(in model\) to a term'):
        #iam: 9/19/2018     yapi.yices_get_algebraic_number_value(mdl, i1, alg1)
        errcode = yapi.yices_get_algebraic_number_value(mdl, i1, alg1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'could not convert value (in model) to a term')


    def test_mpq_models(self):
        r1 = define_const('r1', self.real_t)
        r2 = define_const('r2', self.real_t)
        assert_formula('(> (* r1 3456666334217777794) 987654321987654321987654321)', self.ctx)
        assert_formula('(< r2 r1)', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= r1 987654325444320656205432115/3456666334217777794)\n(= r2 987654321987654321987654321/3456666334217777794)')
        r32num1 = c_int32()
        r32den1 = c_uint32()
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException,
        #iam: 9/19/2018                              'eval error: the term value does not fit the expected type'):
        #iam: 9/19/2018     yapi.yices_get_rational32_value(mdl, r1, r32num1, r32den1)
        errcode = yapi.yices_get_rational32_value(mdl, r1, r32num1, r32den1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'eval error: the term value does not fit the expected type')

        r64num1 = c_int64()
        r64den1 = c_uint64()
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException,
        #iam: 9/19/2018                              'eval error: the term value does not fit the expected type'):
        #iam: 9/19/2018     yapi.yices_get_rational64_value(mdl, r1, r64num1, r64den1)
        errcode = yapi.yices_get_rational64_value(mdl, r1, r64num1, r64den1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'eval error: the term value does not fit the expected type')
        gmpq1 = yapi.yices_new_mpq()
        gmpq2 = yapi.yices_new_mpq()
        yapi.yices_get_mpq_value(mdl, r1, gmpq1)
        yapi.yices_get_mpq_value(mdl, r2, gmpq2)
        mpq1 = yapi.yices_mpq(gmpq1)
        mpq2 = yapi.yices_mpq(gmpq2)
        self.assertEqual(yapi.yices_term_to_string(mpq1, 200, 10, 0), '987654325444320656205432115/3456666334217777794')
        self.assertEqual(yapi.yices_term_to_string(mpq2, 200, 10, 0), '987654321987654321987654321/3456666334217777794')

    def test_algebraic_numbers(self):
        if not yapi.yices_has_mcsat():
            return
        # Need a different context
        cfg = yapi.yices_new_config()
        yapi.yices_default_config_for_logic(cfg, "QF_NRA")
        yapi.yices_set_config(cfg, "mode", "one-shot")
        ctx = yapi.yices_new_context(cfg)
        x0 = define_const('x', self.real_t)
        assert_formula('(= (* x x) 2)', ctx)
        self.assertEqual(yapi.yices_check_context(ctx, None), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(ctx, 1)
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= x -1.414214)')
        alg1 = yapi.lp_algebraic_number_t()
        yapi.yices_get_algebraic_number_value(mdl, x0, alg1)
        yv1 = yapi.yval_t()
        yapi.yices_get_value(mdl, x0, yv1)
        alg2 = yapi.lp_algebraic_number_t()
        yapi.yices_val_get_algebraic_number(mdl, yv1, alg2)

    def test_bv_models(self):
        bv_t = yapi.yices_bv_type(3)
        bv1 = define_const('bv1', bv_t)
        bv2 = define_const('bv2', bv_t)
        bv3 = define_const('bv3', bv_t)
        fmla1 = yapi.yices_parse_term('(= bv1 (bv-add bv2 bv3))')
        fmla2 = yapi.yices_parse_term('(bv-gt bv2 0b000)')
        fmla3 = yapi.yices_parse_term('(bv-gt bv3 0b000)')
        yapi.yices_assert_formula(self.ctx, fmla1)
        yapi.yices_assert_formulas(self.ctx, 3, yapi.make_term_array([fmla1, fmla2, fmla3]))
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), 3)
        mdl1 = yapi.yices_get_model(self.ctx, 1)
        val1 = yapi.make_empty_int32_array(3)
        val2 = yapi.make_empty_int32_array(3)
        val3 = yapi.make_empty_int32_array(3)
        yapi.yices_get_bv_value(mdl1, bv1, val1)
        self.assertEqual(val1[0], 0)
        self.assertEqual(val1[1], 0)
        self.assertEqual(val1[2], 0)
        yapi.yices_get_bv_value(mdl1, bv2, val2)
        self.assertEqual(val2[0], 0)
        self.assertEqual(val2[1], 0)
        self.assertEqual(val2[2], 1)
        yapi.yices_get_bv_value(mdl1, bv3, val3)
        self.assertEqual(val3[0], 0)
        self.assertEqual(val3[1], 0)
        self.assertEqual(val3[2], 1)
        yv1 = yapi.yval_t()
        yapi.yices_get_value(mdl1, bv2, yv1)
        self.assertEqual(yapi.yices_val_bitsize(mdl1, yv1), 3)
        self.assertEqual(yv1.node_tag, yapi.YVAL_BV)
        yapi.yices_val_get_bv(mdl1, yv1, val1)
        self.assertEqual(yapi.yices_val_bitsize(mdl1, yv1), 3)
        self.assertEqual(val1[0], 0)
        self.assertEqual(val1[1], 0)
        self.assertEqual(val1[2], 1)
        yapi.yices_free_model(mdl1)

    def test_tuple_models(self):
        tup_t = yapi.yices_tuple_type3(self.bool_t, self.real_t, self.int_t)
        t1 = define_const('t1', tup_t)
        assert_formula('(ite (select t1 1) (< (select t1 2) (select t1 3)) (> (select t1 2) (select t1 3)))', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), 3)
        mdl = yapi.yices_get_model(self.ctx, 1)
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= t1 (mk-tuple false 1 0))')
        yv1 = yapi.yval_t()
        yapi.yices_get_value(mdl, t1, yv1)
        self.assertEqual(yv1.node_tag, yapi.YVAL_TUPLE)
        self.assertEqual(yapi.yices_val_tuple_arity(mdl, yv1), 3)
        yvarr = yapi.make_empty_yval_array(3)
        yapi.yices_val_expand_tuple(mdl, yv1, yvarr)
        self.assertEqual(yvarr[0].node_tag, yapi.YVAL_BOOL)
        bval1 = c_int32()
        ival1 = c_int32()
        yapi.yices_val_get_bool(mdl, yvarr[0], bval1)
        self.assertEqual(bval1.value, 0)
        yapi.yices_val_get_int32(mdl, yvarr[1], ival1)
        self.assertEqual(ival1.value, 1)

    # bus error
    def test_function_models(self):
        funtype = yapi.yices_function_type3(self.int_t, self.bool_t, self.real_t, self.real_t)
        ftystr = yapi.yices_type_to_string(funtype, 100, 80, 0)
        yapi.yices_pp_type_fd(1, funtype, 100, 80, 0)
        self.assertEqual(ftystr, '(-> int bool real real)')
        fun1 = define_const('fun1', funtype)
        define_const('b1', self.bool_t)
        i1 = define_const('i1', self.int_t)
        r1 = define_const('r1', self.real_t)
        assert_formula('(> (fun1 i1 b1 r1) (fun1 (+ i1 1) (not b1) (- r1 i1)))', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= b1 false)\n(= i1 1463)\n(= r1 -579)\n(function fun1\n (type (-> int bool real real))\n (= (fun1 1463 false -579) 1)\n (= (fun1 1464 true -2042) 0)\n (default 2))')
        yv1 = yapi.yval_t()
        yapi.yices_get_value(mdl, fun1, yv1)
        self.assertEqual(yv1.node_tag, yapi.YVAL_FUNCTION)
        self.assertEqual(yapi.yices_val_function_arity(mdl, yv1), 3)
        def1 = yapi.yval_t()
        vec1 = yapi.yval_vector_t()
        yapi.yices_init_yval_vector(vec1)
        yapi.yices_val_expand_function(mdl, yv1, def1, vec1)
        self.assertEqual(def1.node_tag, yapi.YVAL_RATIONAL)
        i32val1 = c_int32()
        yapi.yices_val_get_int32(mdl, def1, i32val1)
        self.assertEqual(i32val1.value, 2)
        self.assertEqual(vec1.size, 2)
        map1 = vec1.data[0]
        map2 = vec1.data[1]
        self.assertEqual(map1.node_tag, yapi.YVAL_MAPPING)
        self.assertEqual(map2.node_tag, yapi.YVAL_MAPPING)
        self.assertEqual(yapi.yices_val_mapping_arity(mdl, map1), 3)
        self.assertEqual(yapi.yices_val_mapping_arity(mdl, map2), 3)
        # First mapping
        args1 = yapi.make_empty_yval_array(3)
        yval1 = yapi.yval_t()
        yapi.yices_val_expand_mapping(mdl, map1, args1, yval1)
        self.assertEqual(yval1.node_tag, yapi.YVAL_RATIONAL)
        self.assertEqual(yapi.yices_val_is_int32(mdl, yval1), 1)
        val1 = c_int32()
        yapi.yices_val_get_int32(mdl, yval1, val1)
        self.assertEqual(val1.value, 1)
        self.assertEqual(args1[0].node_tag, yapi.YVAL_RATIONAL)
        self.assertEqual(yapi.yices_val_is_int32(mdl, args1[0]), 1)
        m1arg1 = c_int32()
        yapi.yices_val_get_int32(mdl, args1[0], m1arg1)
        self.assertEqual(m1arg1.value, 1463)
        self.assertEqual(args1[1].node_tag, yapi.YVAL_BOOL)
        m1arg2 = c_int()
        yapi.yices_val_get_bool(mdl, args1[1], m1arg2)
        self.assertEqual(m1arg2.value, 0)
        m1arg3 = c_int32()
        yapi.yices_val_get_int32(mdl, args1[2], m1arg3)
        self.assertEqual(m1arg3.value, -579)
        # Second mapping
        args2 = yapi.make_empty_yval_array(3)
        yval2 = yapi.yval_t()
        yapi.yices_val_expand_mapping(mdl, map2, args2, yval2)
        self.assertEqual(yval2.node_tag, yapi.YVAL_RATIONAL)
        self.assertEqual(yapi.yices_val_is_int32(mdl, yval2), 1)
        val2 = c_int32()
        yapi.yices_val_get_int32(mdl, yval2, val2)
        self.assertEqual(val2.value, 0)
        self.assertEqual(args2[0].node_tag, yapi.YVAL_RATIONAL)
        self.assertEqual(yapi.yices_val_is_int32(mdl, args2[0]), 1)
        m2arg2 = c_int32()
        yapi.yices_val_get_int32(mdl, args2[0], m2arg2)
        self.assertEqual(m2arg2.value, 1464)
        self.assertEqual(args2[1].node_tag, yapi.YVAL_BOOL)
        m2arg2 = c_int()
        yapi.yices_val_get_bool(mdl, args2[1], m2arg2)
        self.assertEqual(m2arg2.value, 1)
        m2arg3 = c_int32()
        yapi.yices_val_get_int32(mdl, args2[2], m2arg3)
        self.assertEqual(m2arg3.value, -2042)
        fmla = yapi.yices_parse_term('(> i1 r1)')
        self.assertEqual(yapi.yices_formula_true_in_model(mdl, fmla), 1)
        a_arr = yapi.make_term_array([i1, fmla, r1])
        b_arr = yapi.make_empty_term_array(3)
        yapi.yices_term_array_value(mdl, 3, a_arr, b_arr)
        self.assertEqual(b_arr[0], yapi.yices_int32(1463))
        self.assertEqual(b_arr[1], yapi.yices_true())
        self.assertEqual(b_arr[2], yapi.yices_int32(-579))
        yapi.yices_pp_term_array_fd(1, 3, b_arr, 100, 10, 0, 0)
        tvec3 = yapi.term_vector_t()
        yapi.yices_init_term_vector(tvec3)
        yapi.yices_generalize_model(mdl, fmla, 1, a_arr, 0, tvec3)
        yapi.yices_delete_term_vector(tvec3)


    def test_scalar_models(self):
        scalar_t = yapi.yices_new_scalar_type(10)
        sc1 = define_const('sc1', scalar_t)
        sc2 = define_const('sc2', scalar_t)
        sc3 = define_const('sc3', scalar_t)
        assert_formula('(/= sc1 sc2)', self.ctx)
        assert_formula('(/= sc1 sc3)', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        val1 = c_int32()
        val2 = c_int32()
        val3 = c_int32()
        yapi.yices_get_scalar_value(mdl, sc1, val1)
        yapi.yices_get_scalar_value(mdl, sc2, val2)
        yapi.yices_get_scalar_value(mdl, sc3, val3)
        self.assertEqual(val1.value, 9)
        self.assertEqual(val2.value, 8)
        self.assertEqual(val3.value, 8)
        yv1 = yapi.yval_t()
        ty1 = c_int32()
        self.assertEqual(yapi.yices_term_is_scalar(sc1), 1)
        sc1val = yapi.yices_get_value_as_term(mdl, sc1)
        self.assertEqual(yapi.yices_term_is_scalar(sc1val), 1)
        self.assertEqual(yapi.yices_get_value(mdl, sc1, yv1), 0)
        # yapi.YVAL_SCALAR
        self.assertEqual(yv1.node_tag, yapi.YVAL_SCALAR)
        yapi.yices_val_get_scalar(mdl, yv1, val1, ty1)
        self.assertEqual(val1.value, 9)

    def test_yval_numeric_models(self):
        i1 = define_const('i1', self.int_t)
        define_const('i2', self.int_t)
        assert_formula('(> i1 3)', self.ctx)
        assert_formula('(< i2 i1)', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        yv1 = yapi.yval_t()
        yapi.yices_get_value(mdl, i1, yv1)
        self.assertEqual(yapi.yices_val_is_int32(mdl, yv1), 1)
        self.assertEqual(yapi.yices_val_is_int64(mdl, yv1), 1)
        self.assertEqual(yapi.yices_val_is_rational32(mdl, yv1), 1)
        self.assertEqual(yapi.yices_val_is_rational64(mdl, yv1), 1)
        self.assertEqual(yapi.yices_val_is_integer(mdl, yv1), 1)
        # The next four just return 0 since yval is not a bv, tuple, mapping, or function
        self.assertEqual(yapi.yices_val_bitsize(mdl, yv1), 0)
        # Note that the next three aren't real tests, since 0 is returned if the tag is wrong
        self.assertEqual(yapi.yices_val_tuple_arity(mdl, yv1), 0)
        self.assertEqual(yapi.yices_val_mapping_arity(mdl, yv1), 0)
        self.assertEqual(yapi.yices_val_function_arity(mdl, yv1), 0)
        bval1 = c_int32()
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'invalid operation on yval'):
        #iam: 9/19/2018     yapi.yices_val_get_bool(mdl, yv1, bval1)
        errcode = yapi.yices_val_get_bool(mdl, yv1, bval1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'invalid operation on yval')
        i32val1 = c_int32()
        yapi.yices_val_get_int32(mdl, yv1, i32val1)
        self.assertEqual(i32val1.value, 4)
        i64val1 = c_int64()
        yapi.yices_val_get_int64(mdl, yv1, i64val1)
        self.assertEqual(i64val1.value, 4)
        r32num1 = c_int32()
        r32den1 = c_uint32()
        yapi.yices_val_get_rational32(mdl, yv1, r32num1, r32den1)
        self.assertEqual(r32num1.value, 4)
        self.assertEqual(r32den1.value, 1)
        r64num1 = c_int64()
        r64den1 = c_uint64()
        yapi.yices_val_get_rational64(mdl, yv1, r64num1, r64den1)
        self.assertEqual(r64num1.value, 4)
        self.assertEqual(r64den1.value, 1)
        rdoub1 = c_double()
        yapi.yices_val_get_double(mdl, yv1, rdoub1)
        self.assertEqual(rdoub1.value, 4.0)
        gmpz1 = yapi.yices_new_mpz()
        yapi.yices_val_get_mpz(mdl, yv1, gmpz1)
        mpz1 = yapi.yices_mpz(gmpz1)
        self.assertEqual(yapi.yices_term_to_string(mpz1, 200, 10, 0), '4')
        gmpq1 = yapi.yices_new_mpq()
        yapi.yices_val_get_mpq(mdl, yv1, gmpq1)
        mpq1 = yapi.yices_mpq(gmpq1)
        self.assertEqual(yapi.yices_term_to_string(mpq1, 200, 10, 0), '4')
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'invalid operation on yval'):
        #iam: 9/19/2018     yapi.yices_val_get_bv(mdl, yv1, bval1)
        errcode = yapi.yices_val_get_bv(mdl, yv1, bval1)
        error_string = yapi.yices_error_string()
        self.assertEqual(errcode, -1)
        self.assertEqual(error_string, 'invalid operation on yval')

    def test_model_from_map(self):
        bv_t = yapi.yices_bv_type(8)
        i1 = define_const('i1', self.int_t)
        r1 = define_const('r1', self.real_t)
        bv1 = define_const('bv1', bv_t)
        iconst1 = yapi.yices_int32(42)
        rconst1 = yapi.yices_rational32(13, 131)
        bvconst1 = yapi.yices_bvconst_int32(8, 134)
        mdl = yapi.yices_model_from_map(3, yapi.make_term_array([i1, r1, bv1]), yapi.make_term_array([iconst1, rconst1, bvconst1]))
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= i1 42)\n(= r1 13/131)\n(= bv1 0b10000110)')
        yapi.yices_free_model(mdl)

    def test_implicant(self):
        i1 = define_const('i1', self.int_t)
        assert_formula('(and (> i1 2) (< i1 8) (/= i1 4))', self.ctx)
        self.assertEqual(yapi.yices_check_context(self.ctx, self.param), yapi.STATUS_SAT)
        mdl = yapi.yices_get_model(self.ctx, 1)
        print('yices_get_model', mdl)
        mdlstr = yapi.yices_model_to_string(mdl, 80, 100, 0)
        self.assertEqual(mdlstr, '(= i1 7)')
        fml = yapi.yices_parse_term('(>= i1 3)')
        tvec = yapi.term_vector_t()
        yapi.yices_init_term_vector(tvec)
        yapi.yices_implicant_for_formula(mdl, fml, tvec)
        self.assertEqual(tvec.size, 1)
        implstr = yapi.yices_term_to_string(tvec.data[0], 200, 10, 0)
        self.assertEqual(implstr, '(>= (+ -3 i1) 0)')
        fml2 = yapi.yices_parse_term('(<= i1 9)')
        fmls = yapi.make_term_array([fml, fml2])
        tvec2 = yapi.term_vector_t()
        yapi.yices_init_term_vector(tvec2)
        yapi.yices_implicant_for_formulas(mdl, 2, fmls, tvec2)
        self.assertEqual(tvec2.size, 2)
        implstr2 = yapi.yices_term_to_string(tvec2.data[0], 200, 10, 0)
        self.assertEqual(implstr2, '(>= (+ -3 i1) 0)')
        implstr3 = yapi.yices_term_to_string(tvec2.data[1], 200, 10, 0)
        self.assertEqual(implstr3, '(>= (+ 9 (* -1 i1)) 0)')
        tvec3 = yapi.term_vector_t()
        yapi.yices_init_term_vector(tvec3)
        a_arr = yapi.term_t(i1)
        yapi.yices_generalize_model_array(mdl, 2, fmls, 1, a_arr, 0, tvec3)


    def test_2_6_4(self):
        mdl = yapi.yices_new_model()
        self.assertNotEqual(mdl, None)

        # bool set and then get
        var = define_const('b1', self.bool_t)
        val = yapi.yices_true()
        code = yapi.yices_model_set_bool(mdl, var, val)
        self.assertEqual(code, 0)
        bval = c_int32()
        code = yapi.yices_get_bool_value(mdl, var, bval)
        self.assertEqual(code, 0)
        self.assertEqual(bool(bval.value), True)

        # can test all the new routines like this, but it might just be easier
        # to do the equivalent tests in the pythonesque versions.

        yapi.yices_free_model(mdl)
