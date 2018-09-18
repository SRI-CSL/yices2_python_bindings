import sys

import yices_api as yapi


class Parameters(object):

    def __init__(self):
        self.params =  yapi.yices_new_param_record()

    def set_param(self, key, value):
        assert self.params is not None
        errcode = yapi.yices_set_param(self.params, key, value)
        if errcode == 0:
            return True
        sys.stderr.write('yices_set_param failed {0}\n', yapi.yices_error_string())
        return False


    def dispose(self):
        assert self.params is not None
        yapi.yices_free_param_record(self.params)
        self.params = None
