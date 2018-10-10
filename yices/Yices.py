import yices_api as yapi

class Yices(object):

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
