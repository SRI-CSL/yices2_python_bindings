import yices_api as yapi

# int32_t max (2^31 - 1)
MAX_VALUE = 2147483647


class Yices(object):

    # Maximal number of terms and types
    MAX_TYPES = MAX_VALUE/4
    MAX_TERMS = MAX_VALUE/4

    # Maximal arity
    MAX_ARITY = MAX_VALUE/8

    # Maximal polynomial degree
    MAX_DEGREE = MAX_VALUE

    # Maximal number of variables in quantifiers/lambdas
    MAX_VARS = MAX_VALUE/8

    # Maximal bitvector size
    MAX_BVSIZE = MAX_VALUE/8

    @staticmethod
    def error_code():
        return yapi.yices_error_code()

    @staticmethod
    def error_string():
        return yapi.yices_error_string()

    @staticmethod
    def error_report():
        return yapi.yices_error_report()

    @staticmethod
    def clear_error():
        return yapi.yices_clear_error()

    @staticmethod
    def print_error(fd):
        return yapi.yices_print_error_fd(fd)

    @staticmethod
    def init():
        yapi.yices_init()

    @staticmethod
    def is_inited():
        return yapi.yices_is_inited()

    @staticmethod
    def exit():
        yapi.yices_exit()

    @staticmethod
    def reset():
        yapi.yices_reset()
