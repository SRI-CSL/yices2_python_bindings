import yices_api as yapi


class Yices(object):


    @staticmethod
    def error_string():
        return yapi.yices_error_string()


    @staticmethod
    def exit():
        yapi.yices_exit()

    @staticmethod
    def init():
        yapi.yices_init()
