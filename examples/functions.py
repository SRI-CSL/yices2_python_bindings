#! /usr/bin/env python


from yices import *


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



cfg = Config()
ctx = Context(cfg)
param = Parameters()
param.default_params_for_context(ctx)
global bool_t, int_t, real_t
bool_t = Types.bool_type()
int_t = Types.int_type()
real_t = Types.real_type()


funtype = Types.new_function_type([int_t, bool_t, real_t], real_t)
ftystr = Types.to_string(funtype, 100, 80, 0)
Types.print_to_fd(1, funtype, 100, 80, 0)
#assertEqual(ftystr, '(-> int bool real real)')
fun1 = define_const('fun1', funtype)
b1 = define_const('b1', bool_t)
i1 = define_const('i1', int_t)
r1 = define_const('r1', real_t)
assert_formula('(> (fun1 i1 b1 r1) (fun1 (+ i1 1) (not b1) (- r1 i1)))', ctx)
print(ctx.check_context(param) == Status.SAT)
mdl = Model.from_context(ctx, 1)
mdlstr = mdl.to_string(80, 100, 0)
print(mdlstr)
print('(= b1 false)\n(= i1 1463)\n(= r1 -579)\n(function fun1\n (type (-> int bool real real))\n (= (fun1 1463 false -579) 1)\n (= (fun1 1464 true -2042) 0)\n (default 2))')
fun1val = mdl.get_value(fun1)
print(fun1val((1463, False, -579)))
print(fun1val((1464, True, -2042)))
print(fun1val((1462, True, -2041)))



cfg.dispose()
ctx.dispose()
param.dispose()
Yices.exit()
