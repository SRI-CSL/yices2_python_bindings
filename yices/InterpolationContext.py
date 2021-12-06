""" The InterpolationContext class mimics, but doesn't wrap the yices interpolation_context_t struct.

It provides access to the yices_check_context_with_interpolation api call in a pythonesque manner.
"""
from ctypes import (
    c_int32,
    pointer,
    )


import yices_api as yapi
from .Status import Status
from .Model import Model

class InterpolationContext:

    def __init__(self, ctx_a, ctx_b):
        self.ctx_a = ctx_a
        self.ctx_b = ctx_b
        self.model = None
        self.interpolant = None

    def check(self, params, build_model):
        interpolation_ctx = yapi.interpolation_context_t(self.ctx_a.context, self.ctx_b.context, 0, 0)
        parameters = 0 if not params else params.params
        build = c_int32(1 if build_model else 0)
        status = yapi.yices_check_context_with_interpolation(pointer(interpolation_ctx), parameters, build)
        if status == Status.UNSAT:
            # get the interpolant
            self.interpolant = interpolation_ctx.interpolant
        elif status == Status.SAT:
            # get the model
            self.model = Model(interpolation_ctx.model)
        return status
