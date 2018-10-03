import unittest

from yices.Config import Config
from yices.Context import Context
from yices.Model import Model
from yices.Parameters import Parameters
from yices.Status import Status
from yices.Types import Types
from yices.Terms import Terms
from yices.YicesException import YicesException
from yices.Yices import Yices



def define_type(name, ytype=None):
    '''Tries to emulate yices type declarations'''
    if ytype is None:
        ytyp = Types.new_uninterpreted_type()
    elif isinstance(ytype, basestring):
        ytyp = Types.parse_type(ytype)
    else:
        ytyp = ytype
    Types.set_name(ytyp, name)
    return ytyp

def define_const(name, ytype, defn=None):
    '''Tries to emulate yices define_term
    (see eval_define_term in yices2/src/parser_utils/term_stack2)
    '''
    if defn is None:
        term = Terms.new_uninterpreted_term(ytype)
        Terms.set_name(term, name)
        return term
    # Have a defn
    if isinstance(defn, basestring):
        term = Terms.parse_term(defn)
    else:
        term = defn
        term_type = Terms.type_of_term(term)
    if not Types.is_subtype(term_type, ytype):
        raise YicesException(msg='incompatible sort in definition')
    Terms.set_name(term, name)
    return term

def assert_formula(formula, ctx):
    if isinstance(formula, basestring):
        formula = Terms.parse_term(formula)
    ctx.assert_formula(formula)


class TestModels(unittest.TestCase):

    def setUp(self):
        # this is required for some strange reason.
        # seems like yices/__init__.py does not get evaluated
        Yices.init()
        self.cfg = Config()
        self.ctx = Context(self.cfg)
        self.param = Parameters()
        self.param.default_params_for_context(self.ctx)
        global bool_t, int_t, real_t
        bool_t = Types.bool_type()
        int_t = Types.int_type()
        real_t = Types.real_type()


    def tearDown(self):
        self.cfg.dispose()
        self.ctx.dispose()
        self.param.dispose()
        Yices.exit()

    def test_bool_models(self):
        b1 = define_const('b1', bool_t)
        b2 = define_const('b2', bool_t)
        b3 = define_const('b3', bool_t)
        b_fml1 = Terms.parse_term('(or b1 b2 b3)')
        self.ctx.assert_formula(b_fml1)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        b_mdl1 = Model.from_context(self.ctx, 1)
        self.assertNotEqual(b_mdl1, None)
        bval1 = b_mdl1.get_bool_value(b1)
        bval2 = b_mdl1.get_bool_value(b2)
        bval3 = b_mdl1.get_bool_value(b3)
        self.assertEqual(bval1, False)
        self.assertEqual(bval2, False)
        self.assertEqual(bval3, True)
        b_fmla2 = Terms.parse_term('(not b3)')
        self.ctx.assert_formula(b_fmla2)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        b_mdl1 = Model.from_context(self.ctx, 1)
        self.assertNotEqual(b_mdl1, None)
        bval1 = b_mdl1.get_bool_value(b1)
        bval2 = b_mdl1.get_bool_value(b2)
        bval3 = b_mdl1.get_bool_value(b3)
        val1 = b_mdl1.get_value(b1)
        val2 = b_mdl1.get_value(b2)
        val3 = b_mdl1.get_value(b3)
        self.assertEqual(bval1, False)
        self.assertEqual(bval2, True)
        self.assertEqual(bval3, False)
        self.assertEqual(bval1, val1)
        self.assertEqual(bval2, val2)
        self.assertEqual(bval3, val3)

    def test_int_models(self):
        ''' int32, int64 '''
        i1 = define_const('i1', int_t)
        i2 = define_const('i2', int_t)
        assert_formula('(> i1 3)', self.ctx)
        assert_formula('(< i2 i1)', self.ctx)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        mdl = Model.from_context(self.ctx, 1)
        i32v1 = mdl.get_integer_value(i1)
        i32v2 = mdl.get_integer_value(i2)
        self.assertEqual(i32v1, 4)
        self.assertEqual(i32v2, 3)
        mdl.print_to_fd(1)
        mdl.print_to_fd(1, 80, 100, 0)
        mdlstr = mdl.to_string(80, 100, 0)
        self.assertEqual(mdlstr, '(= i1 4)\n(= i2 3)')

    def test_rat_models(self):
        ''' rational32, rational64, double '''
        r1 = define_const('r1', real_t)
        r2 = define_const('r2', real_t)
        assert_formula('(> r1 3)', self.ctx)
        assert_formula('(< r1 4)', self.ctx)
        assert_formula('(< (- r1 r2) 0)', self.ctx)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        mdl = Model.from_context(self.ctx, 1)
        v1 = mdl.get_fraction_value(r1)
        v2 = mdl.get_fraction_value(r2)
        # r1 = 7/2, r2 = 4/1
        self.assertEqual(v1.numerator, 7)
        self.assertEqual(v1.denominator, 2)
        self.assertEqual(v2.numerator, 4)
        self.assertEqual(v2.denominator, 1)
        rdoub1 = mdl.get_float_value(r1)
        rdoub2 = mdl.get_float_value(r2)
        self.assertEqual(rdoub1, 3.5)
        self.assertEqual(rdoub2, 4.0)
        val1 = mdl.get_value(r1)
        val2 = mdl.get_value(r2)
        self.assertEqual(val1, 3.5)
        self.assertEqual(val2, 4.0)


    def test_bv_models(self):
        bv_t = Types.bv_type(3)
        bv1 = define_const('bv1', bv_t)
        bv2 = define_const('bv2', bv_t)
        bv3 = define_const('bv3', bv_t)
        fmla1 = Terms.parse_term('(= bv1 (bv-add bv2 bv3))')
        fmla2 = Terms.parse_term('(bv-gt bv2 0b000)')
        fmla3 = Terms.parse_term('(bv-gt bv3 0b000)')
        self.ctx.assert_formula(fmla1)
        self.ctx.assert_formulas([fmla1, fmla2, fmla3])
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        mdl1 = Model.from_context(self.ctx, 1)
        val1 = mdl1.get_value(bv1)
        self.assertEqual(val1[0], 0)
        self.assertEqual(val1[1], 0)
        self.assertEqual(val1[2], 0)
        val2 = mdl1.get_value(bv2)
        self.assertEqual(val2[0], 0)
        self.assertEqual(val2[1], 0)
        self.assertEqual(val2[2], 1)
        val3 = mdl1.get_value(bv3)
        self.assertEqual(val3[0], 0)
        self.assertEqual(val3[1], 0)
        self.assertEqual(val3[2], 1)
        mdl1.dispose()


    def test_tuple_models(self):
        tup_t = Types.new_tuple_type([bool_t, real_t, int_t])
        t1 = define_const('t1', tup_t)
        assert_formula('(ite (select t1 1) (< (select t1 2) (select t1 3)) (> (select t1 2) (select t1 3)))', self.ctx)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        mdl = Model.from_context(self.ctx, 1)
        mdlstr = mdl.to_string(80, 100, 0)
        self.assertEqual(mdlstr, '(= t1 (mk-tuple false 1 0))')
        val = mdl.get_value(t1)
        self.assertEqual(val[0], False)
        self.assertEqual(val[1], 1)
        self.assertEqual(val[2], 0)


    def test_model_from_map(self):
        bv_t = Types.bv_type(8)
        i1 = define_const('i1', int_t)
        r1 = define_const('r1', real_t)
        bv1 = define_const('bv1', bv_t)
        iconst1 = Terms.integer(42)
        rconst1 = Terms.rational(13, 131)
        bvconst1 = Terms.bvconst_integer(8, 134)
        mapping = { i1: iconst1, r1: rconst1, bv1: bvconst1  }
        mdl = Model.from_map(mapping)
        mdlstr = mdl.to_string(80, 100, 0)
        self.assertEqual(mdlstr, '(= i1 42)\n(= r1 13/131)\n(= bv1 0b10000110)')
        mdl.dispose()


    def test_implicant(self):
        i1 = define_const('i1', int_t)
        assert_formula('(and (> i1 2) (< i1 8) (/= i1 4))', self.ctx)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        mdl = Model.from_context(self.ctx, 1)
        mdlstr = mdl.to_string(80, 100, 0)
        self.assertEqual(mdlstr, '(= i1 7)')
        fml = Terms.parse_term('(>= i1 3)')
        tarray = mdl.implicant_for_formula(fml)
        self.assertEqual(len(tarray), 1)
        implstr = Terms.to_string(tarray[0], 200, 10, 0)
        self.assertEqual(implstr, '(>= (+ -3 i1) 0)')
        fml2 = Terms.parse_term('(<= i1 9)')
        tarray2 = mdl.implicant_for_formulas([fml, fml2])
        self.assertEqual(len(tarray2), 2)
        implstr2 = Terms.to_string(tarray2[0], 200, 10, 0)
        self.assertEqual(implstr2, '(>= (+ -3 i1) 0)')
        implstr3 = Terms.to_string(tarray2[1], 200, 10, 0)
        self.assertEqual(implstr3, '(>= (+ 9 (* -1 i1)) 0)')
