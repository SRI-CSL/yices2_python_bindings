#! /usr/bin/env python

from yices import *


cfg = Config()
cfg.default_config_for_logic('QF_BV')
ctx = Context(cfg)

bv32_t = Types.bv_type(32)
x = Terms.new_uninterpreted_term(bv32_t, 'x')
y = Terms.new_uninterpreted_term(bv32_t, 'y')


zero = Terms.bvconst_integer(32, 0)
fmla0 = Terms.bvsgt_atom(x, zero)
fmla1 = Terms.bvsgt_atom(y, zero)
fmla2 = Terms.bvslt_atom(Terms.bvadd(x, y), x)

ctx.assert_formulas([fmla0, fmla1, fmla2])

status = ctx.check_context()

if status == Status.SAT:
    model = Model.from_context(ctx, 1)
    model_string = model.to_string(80, 100, 0)
    print(model_string)
    xval = model.get_value(x)
    yval = model.get_value(y)
    print('x = {0}\ny = {1}'.format(xval, yval))

cfg.dispose()
ctx.dispose()
Yices.exit()
