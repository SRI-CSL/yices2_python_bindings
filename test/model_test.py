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
