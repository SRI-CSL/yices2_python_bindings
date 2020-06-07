"""The Parameters class wraps the yicesparameter record structure param_t .

A parameter record stores search parameters and options that control the heuristics used by a solver.
"""


import yices_api as yapi

from .YicesException import YicesException

class Parameters:

    __population = 0

    def __init__(self):
        self.params =  yapi.yices_new_param_record()
        Parameters.__population += 1

    def set_param(self, key, value):
        assert self.params is not None
        errcode = yapi.yices_set_param(self.params, key, value)
        if errcode == -1:
            raise YicesException('yices_set_param')
        return True


    def default_params_for_context(self, context):
        yapi.yices_default_params_for_context(context.context, self.params)

    def dispose(self):
        assert self.params is not None
        yapi.yices_free_param_record(self.params)
        self.params = None
        Parameters.__population -= 1

    @staticmethod
    def population():
        """returns the current live population of Parameters objects."""
        return Parameters.__population
