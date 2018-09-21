import unittest

from yices.Config import Config
from yices.Context import Context
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
        pass

    def test_bool_models(self):
        return
        b1 = define_const('b1', bool_t)
        b2 = define_const('b2', bool_t)
        b3 = define_const('b3', bool_t)
        b_fml1 = Terms.parse_term('(or b1 b2 b3)')
        self.ctx.assert_formula(b_fml1)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        b_mdl1 = Model.from_context(self.ctx, 1)
        self.assertNotEqual(b_mdl1, None)
        # init to -1 to make sure they get updated
        bval1 = b_mdl1.get_bool_value(b1)
        bval2 = b_mdl1.get_bool_value(b2)
        bval3 = b_mdl1.get_bool_value(b3)
        self.assertEqual(bval1, 0)
        self.assertEqual(bval2, 0)
        self.assertEqual(bval3, 1)
        b_fmla2 = Terms.parse_term('(not b3)')
        self.ctx.assert_formula(b_fmla2)
        self.assertEqual(self.ctx.check_context(self.param), Status.SAT)
        b_mdl1 = Model.from_context(self.ctx, 1)
        self.assertNotEqual(b_mdl1, None)
        bval1 = b_mdl1.get_bool_value(b1)
        bval2 = b_mdl1.get_bool_value(b2)
        bval3 = b_mdl1.get_bool_value(b3)
        self.assertEqual(bval1, 0)
        self.assertEqual(bval2, 1)
        self.assertEqual(bval3, 0)
        #v1 = b_mdl1.get_value(b1)
        #self.assertEqual(v1, 0)
