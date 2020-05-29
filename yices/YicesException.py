"""YicesException is the base class for exceptions from the Pythonesque Yices Package."""

import yices_api as yapi


class YicesException(Exception):
    """Base class for exceptions from the Pythonesque Yices Package."""


    LONG_MSG = 'The function {0} failed because: {1}'

    def __init__(self, function=None, msg=None):
        if function is None:
            super(YicesException, self).__init__('' if msg is None else msg)
        else:
            super(YicesException, self).__init__(YicesException.LONG_MSG.format(function, yapi.yices_error_string()))
