"""Contexts wrap the important yices2 context_t structure.

A context contains one or more solvers and supports operations for
manipulating assertions and for checking whether these assertions are
satisfiable. If they are, a model can be constructed from the context."""

import threading

import yices_api as yapi

from .YicesException import YicesException

from .Status import Status
from .Yices import Yices

class Context:

    __population = 0

    def __init__(self, config=None):
        cfg = config.config if config else None
        self.context = Yices.new_context(cfg)
        if self.context == -1:
            raise YicesException('yices_new_context')
        Context.__population += 1

    # option is a string
    def enable_option(self, option):
        assert self.context is not None
        errcode = Yices.context_enable_option(self.context, option)
        if errcode == -1:
            raise YicesException('yices_context_enable_option')
        return True

    # option is a string
    def disable_option(self, option):
        assert self.context is not None
        errcode = Yices.context_disable_option(self.context, option)
        if errcode == -1:
            raise YicesException('yices_context_disable_option')
        return True


    def status(self):
        assert self.context is not None
        return Yices.context_status(self.context)


    def assert_formula(self, term):
        assert self.context is not None
        errcode = Yices.assert_formula(self.context, term)
        if errcode == -1:
            raise YicesException('yices_assert_formula')
        return True

    # to be very pythonesque we should handle iterables, but we do need to know the length
    def assert_formulas(self, python_array_or_tuple):
        assert self.context is not None
        alen = len(python_array_or_tuple)
        a = yapi.make_term_array(python_array_or_tuple)
        errcode = Yices.assert_formulas(self.context, alen, a)
        if errcode == -1:
            raise YicesException('yices_assert_formulas')
        return True


    def check_context(self, params=None, timeout=None):
        assert self.context is not None
        # unwrap the params object
        if params is not None:
            params = params.params
        # set the timeout
        if timeout is not None:
            timer = threading.Timer(timeout, Context.stop_search, [self])
            timer.start()
        status = Yices.check_context(self.context, params)
        if timeout is not None:
            timer.cancel()
        if status == -1:
            raise YicesException('yices_check_context')
        return status


    def stop_search(self):
        assert self.context is not None
        #yapi.yices_stop_search(self.context)
        Yices.stop_search(self.context)

    def reset_context(self):
        assert self.context is not None
        #yapi.yices_reset_context(self.context)
        Yices.reset_context(self.context)

    def assert_blocking_clause(self):
        assert self.context is not None
        errcode = Yices.assert_blocking_clause(self.context)
        if errcode == -1:
            raise YicesException('yices_assert_blocking_clause')
        return True


    def push(self):
        assert self.context is not None
        errcode = Yices.push(self.context)
        if errcode == -1:
            raise YicesException('yices_push')
        return True

    def pop(self):
        assert self.context is not None
        errcode = Yices.pop(self.context)
        if errcode == -1:
            raise YicesException('yices_pop')
        return True


    def check_context_with_assumptions(self, params, python_array_or_tuple):
        assert self.context is not None
        alen = len(python_array_or_tuple)
        a = yapi.make_term_array(python_array_or_tuple)
        status = Yices.check_context_with_assumptions(self.context, params, alen, a)
        if status == Status.ERROR:
            raise YicesException('check_context_with_assumptions')
        return status

    def check_context_with_model(self, params, model, python_array_or_tuple):
        assert self.context is not None
        assert model is not None
        alen = len(python_array_or_tuple)
        a = yapi.make_term_array(python_array_or_tuple)
        status = yapi.yices_check_context_with_model(self.context, params, model.model, alen, a)
        if status == Status.ERROR:
            raise YicesException('check_context_with_model')
        return status

    def check_context_with_model_and_hint(self, params, model, python_array_or_tuple, python_array_or_tuple_hints):
        assert self.context is not None
        assert model is not None
        m = len(python_array_or_tuple)
        alist = list(python_array_or_tuple) + list(python_array_or_tuple_hints)
        alen = len(alist)
        a = yapi.make_term_array(alist)
        status = yapi.yices_check_context_with_model_and_hint(self.context, params, model.model, alen, a, m) # pylint: disable=E1101
        if status == Status.ERROR:
            raise YicesException('check_context_with_model_and_hint')
        return status


    def mcsat_set_fixed_var_order(self, python_array_or_tuple):
        assert self.context is not None
        alen = len(python_array_or_tuple)
        a = yapi.make_term_array(python_array_or_tuple)
        status = yapi.yices_mcsat_set_fixed_var_order(self.context, alen, a) # pylint: disable=E1101
        if status == Status.ERROR:
            raise YicesException('mcsat_set_fixed_var_order')
        return status

    def mcsat_set_initial_var_order(self, python_array_or_tuple):
        assert self.context is not None
        alen = len(python_array_or_tuple)
        a = yapi.make_term_array(python_array_or_tuple)
        status = yapi.yices_mcsat_set_initial_var_order(self.context, alen, a) # pylint: disable=E1101
        if status == Status.ERROR:
            raise YicesException('mcsat_set_initial_var_order')
        return status


    def get_unsat_core(self):
        retval = []
        unsat_core = yapi.term_vector_t()
        yapi.yices_init_term_vector(unsat_core)
        errcode = Yices.get_unsat_core(self.context, unsat_core)
        if errcode == -1:
            raise YicesException('yices_get_unsat_core')

        for i in range(0, unsat_core.size):
            retval.append(unsat_core.data[i])
        return retval


    def dispose(self):
        Yices.free_context(self.context)
        self.context = None
        Context.__population -= 1

    @staticmethod
    def population():
        """returns the current live population of Context objects."""
        return Context.__population
