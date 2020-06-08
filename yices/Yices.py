"""Yices is the top level interface with the yices library."""


import yices_api as yapi

from .Profiler import Profiler, profile




class Yices:
    """A thin wrapper to the yices_api class used for things like profiling."""

    version = yapi.yices_version

    build_arch = yapi.yices_build_arch

    build_mode = yapi.yices_build_mode

    build_date = yapi.yices_build_date

    @staticmethod
    @profile
    def has_mcsat():
        """Return true if the underlying libyices has been compiled with mcsat support, false otherwise."""
        return yapi.yices_has_mcsat() == 1

    @staticmethod
    def is_thread_safe():
        """Return true if the underlying libyices has been compiled with thread safety enabled, false otherwise."""
        return yapi.yices_is_thread_safe() == 1


    # new in 2.6.2
    @staticmethod
    def has_delegate(delegate):
        """Returns True if the underlying libyices has been compiled with the given delegate supported.

        Valid delegates are "cadical", "cryptominisat", and "y2sat".
        """
        return yapi.yices_has_delegate(delegate) == 1

    @staticmethod
    def error_code():
        """Return the last error code, see yices_types.h for a full list."""
        return yapi.yices_error_code()

    @staticmethod
    def error_string():
        """Returns a string explaining the last error."""
        return yapi.yices_error_string()

    @staticmethod
    def error_report():
        """Return the latest error report, see yices.h."""
        return yapi.yices_error_report()

    @staticmethod
    def clear_error():
        """Clears the error reprt structure."""
        return yapi.yices_clear_error()

    @staticmethod
    def print_error(fd):
        """Prints the error report out to the given file descriptor."""
        return yapi.yices_print_error_fd(fd)

    @staticmethod
    def init():
        """Must be called before any other API routine (other than is_inited), to initialize internal data structures."""
        yapi.yices_init()

    @staticmethod
    def is_inited():
        """Return True if the library has been initialized, False otherwise."""
        return yapi.yices_is_inited()

    @staticmethod
    def exit(show_profile=False):
        """Deletes all the internal data structure, must be called on exiting to prevent leaks."""
        if show_profile:
            print(Profiler.dump())
        yapi.yices_exit()

    @staticmethod
    def reset():
        """Resets all the internal data structures."""
        yapi.yices_reset()


    #################
    #   CONTEXTS    #
    #################

    @staticmethod
    @profile
    def new_context(config):
        """Returns a newly allocated context; a context is a stack of assertions."""
        return yapi.yices_new_context(config)

    @staticmethod
    @profile
    def free_context(ctx):
        """Frees the given context."""
        yapi.yices_free_context(ctx)

    @staticmethod
    @profile
    def context_status(ctx):
        """The context status."""
        return yapi.yices_context_status(ctx)

    @staticmethod
    @profile
    def reset_context(ctx):
        """Removes all assertions from the context."""
        yapi.yices_reset_context(ctx)

    @staticmethod
    @profile
    def push(ctx):
        """Marks a backtrack point in the context."""
        return yapi.yices_push(ctx)

    @staticmethod
    @profile
    def pop(ctx):
        """Backtracks to the previous backtrack point."""
        return yapi.yices_pop(ctx)

    @staticmethod
    @profile
    def context_enable_option(ctx, option):
        """Used to tune the amount of simplification used when evaluating assertions."""
        return yapi.yices_context_enable_option(ctx, option)

    @staticmethod
    @profile
    def context_disable_option(ctx, option):
        """Used to tune the amount of simplification used when evaluating assertions."""
        return yapi.yices_context_disable_option(ctx, option)

    @staticmethod
    @profile
    def assert_formula(ctx, t):
        """Assert the formula t in the context ctx."""
        return yapi.yices_assert_formula(ctx, t)

    @staticmethod
    @profile
    def assert_formulas(ctx, n, t):
        """Assert an array of formulas of length n in the context ctx."""
        return yapi.yices_assert_formulas(ctx, n, t)

    @staticmethod
    @profile
    def check_context(ctx, params):
        """Checks whether all the assertions stored in the context ctx are satisfiable."""
        return yapi.yices_check_context(ctx, params)

    @staticmethod
    @profile
    def check_context_with_assumptions(ctx, params, n, t):
        """Checks whether the assertions in the context ctx together with n assumptions are satisfiable."""
        return yapi.yices_check_context_with_assumptions(ctx, params, n, t)

    @staticmethod
    @profile
    def assert_blocking_clause(ctx):
        """Adds a blocking clause, this is intended to help enumerate different models for a set of assertions."""
        return yapi.yices_assert_blocking_clause(ctx)

    @staticmethod
    @profile
    def stop_search(ctx):
        """Interupts the search."""
        yapi.yices_stop_search(ctx)

#################
#  UNSAT CORES  #
#################

    @staticmethod
    @profile
    def get_unsat_core(ctx, v):
        """Compute an unsat core after a call to yices_check_with_assumptions."""
        return yapi.yices_get_unsat_core(ctx, v)

################
#   MODELS     #
################

    @staticmethod
    @profile
    def get_model(ctx, keep_subst):
        """Builds a model from the context ctx."""
        return yapi.yices_get_model(ctx, keep_subst)

    @staticmethod
    @profile
    def free_model(mdl):
        """Frees the model."""
        yapi.yices_free_model(mdl)

    @staticmethod
    @profile
    def model_from_map(n, var, mp):
        """Builds a model from a term to term mapping."""
        return yapi.yices_model_from_map(n, var, mp)

    @staticmethod
    @profile
    def model_collect_defined_terms(mdl, v):
        """Collects all the uninterpreted terms that have a value in mdl and store them in v."""
        return yapi.yices_model_collect_defined_terms(mdl, v)

     # new in 2.6.2
    @staticmethod
    @profile
    def check_formula(f, logic, model, delegate):
        return yapi.yices_check_formula(f, logic, model, delegate)

    # new in 2.6.2
    @staticmethod
    @profile
    def check_formulas(f, n, logic, model, delegate):
        return yapi.yices_check_formulas(f, n, logic, model, delegate)

    # new in 2.6.2
    @staticmethod
    @profile
    def export_formula_to_dimacs(f, filename, simplify_cnf, status):
        """Bit-blast then export the CNF to a file."""
        return yapi.yices_export_formula_to_dimacs(f, filename, simplify_cnf, status)


    # new in 2.6.2
    @staticmethod
    @profile
    def export_formulas_to_dimacs(f, n, filename, simplify_cnf, status):
        """Bit-blast then export the CNF to a file."""
        return yapi.yices_export_formulas_to_dimacs(f, n, filename, simplify_cnf, status)

    # new in 2.6.2
    @staticmethod
    @profile
    def model_term_support(mdl, t, v):
        """Get the support of a term t in mdl."""
        return yapi.yices_model_term_support(mdl, t, v)

    # new in 2.6.2
    @staticmethod
    @profile
    def model_term_array_support(mdl, n, t, v):
        """Get the support of a term t in mdl."""
        return yapi.yices_model_term_array_support(mdl, n, t, v)


########################
#  VALUES IN A MODEL  #
########################
