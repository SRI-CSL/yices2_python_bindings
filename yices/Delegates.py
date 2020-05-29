"""Yices has the ability to use third-party SAT solvers as backends to the bit-vector solvers.

The Delegate class encapulates this feature of the API."""

from ctypes import pointer

import yices_api as yapi

from .Model import Model
from .Status import Status


class Delegates:

    # new in 2.6.2
    @staticmethod
    def has_delegate(delegate):
        """Returns True if the underlying libyices has been compiled with the given delegate supported.

        Valid delegates are "cadical", "cryptominisat", and "y2sat".
        """
        return yapi.yices_has_delegate(delegate) == 1


    # new in 2.6.2
    @staticmethod
    def check_formula(f, logic, delegate, model_array=None):
        """Checks whether the formula f is satisfiable in the logic using the delegate.

        If the formula is satisfiable, and the model_array is not None, then it
        inserts a model  into the beginning of the array.
        """
        model = None
        if model_array is not None:
            model = pointer(yapi.model_t(model))
        status = yapi.yices_check_formula(f, logic, model, delegate)
        if status == Status.SAT and model_array is not None:
            model_array.append(Model(model.contents))
        return status


    # new in 2.6.2
    @staticmethod
    def check_formulas(term_array, logic, delegate, model_array=None):
        """Checks whether the formulas in the array are satisfiable in the logic using the delegate.

        If the formulas are satisfiable, and the model_array is not None, then it
        inserts a model into the beginning of the array.
        """
        tarray = yapi.make_term_array(term_array)
        model = None
        if model_array is not None:
            model = pointer(yapi.model_t(model))
        status = yapi.yices_check_formulas(tarray, len(term_array), logic, model, delegate)
        if status == Status.SAT and model_array is not None:
            model_array.append(Model(model.contents))
        return status
