from yices.Types import Types
from yices.Terms import Terms
from yices.YicesException import YicesException


def isstr(s):
    return isinstance(s, str)


def define_type(name, ytype=None):
    '''Tries to emulate yices type declarations'''
    if ytype is None:
        ytyp = Types.new_uninterpreted_type()
    elif isstr(ytype):
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
    if isstr(defn):
        term = Terms.parse_term(defn)
    else:
        term = defn
        term_type = Terms.type_of_term(term)
    if not Types.is_subtype(term_type, ytype):
        raise YicesException(msg='incompatible sort in definition')
    Terms.set_name(term, name)
    return term

def assert_formula(formula, ctx):
    if isstr(formula):
        formula = Terms.parse_term(formula)
    ctx.assert_formula(formula)
