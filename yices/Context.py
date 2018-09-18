import sys

import yices_api as yapi


class Context(object):


    def __init__(self, config=None):
        cfg = config.config if config else None
        self.context = yapi.yices_new_context(cfg)


    # option is a string
    def enable_option(self, option):
        assert self.context is not None
        errcode = yapi.yices_context_enable_option(self.context, option)
        return True if errcode == 0 else False

    # option is a string
    def disable_option(self, option):
        assert self.context is not None
        errcode = yapi.yices_context_disable_option(self.context, option)
        return True if errcode == 0 else False


    def status(self):
        assert self.context is not None
        return yapi.yices_context_status(self.context)


    def assert_formula(self, term):
        assert self.context is not None
        # FIXME: this idiom is wrong because Sam's stuff throws exceptions.
        errcode = yapi.yices_assert_formula(self.context, term)
        if errcode == 0:
            return True
        sys.stderr.write('yices_assert_formula failed {0}\n', yapi.yices_error_string())
        return False

    # to be very pythonesque we should handle iterables, but we do need to know the length
    def assert_formulas(self, python_array_or_tuple):
        assert self.context is not None
        alen = len(python_array_or_tuple)
        a = yapi.make_term_array(python_array_or_tuple)
        errcode = yapi.yices_assert_formulas(self.context, alen, a)
        if errcode == 0:
            return True
        sys.stderr.write('yices_assert_formulas failed {0}\n', yapi.yices_error_string())
        return False


    def check_context(self, params=None):
        assert self.context is not None
        return  yapi.yices_check_context(self.context, params)

    def stop_search(self):
        assert self.context is not None
        yapi.yices_stop_search(self.context)

    def reset_context(self):
        assert self.context is not None
        yapi.yices_reset_context(self.context)

    def assert_blocking_clause(self):
        assert self.context is not None
        errcode = yapi.yices_assert_blocking_clause(self.context)
        if errcode == 0:
            return True
        sys.stderr.write('yices_assert_blocking_clause failed {0}\n', yapi.yices_error_string())
        return False

    def push(self):
        assert self.context is not None
        errcode = yapi.yices_push(self.context)
        if errcode == 0:
            return True
        sys.stderr.write('yices_push failed {0}\n', yapi.yices_error_string())
        return False

    def pop(self):
        assert self.context is not None
        errcode = yapi.yices_pop(self.context)
        if errcode == 0:
            return True
        sys.stderr.write('yices_pop failed {0}\n', yapi.yices_error_string())
        return False

    def check_context_with_assumptions(self, params, python_array_or_tuple):
        alen = len(python_array_or_tuple)
        a = yapi.make_term_array(python_array_or_tuple)
        return yapi.yices_check_context_with_assumptions(self.context, params, alen, a)

    def get_unsat_core(self):
        retval = []
        unsat_core = yapi.term_vector_t()
        yapi.yices_init_term_vector(unsat_core)
        errcode = yapi.yices_get_unsat_core(self.context, unsat_core)
        if errcode == 0:
            for i in range(0, unsat_core.size):
                retval.append(unsat_core.data[i])
        else:
            sys.stderr.write('yices_get_unsat_core failed {0}\n', yapi.yices_error_string())
        return retval


    def dispose(self):
        yapi.yices_free_context(self.context)
        self.context = None
