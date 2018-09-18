import yices


class Yices(object):


    @staticmethod
    def error_string():
        return yices.yices_error_string()


    @staticmethod
    def exit():
        yices.yices_exit()
