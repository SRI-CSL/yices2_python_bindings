import yices


class Yval(object):

    UNKNOWN = yices.YVAL_UNKNOWN
    BOOL = yices.YVAL_BOOL
    RATIONAL = yices.YVAL_RATIONAL
    ALGEBRAIC = yices.YVAL_ALGEBRAIC
    BV = yices.YVAL_BV
    SCALAR = yices.YVAL_SCALAR
    TUPLE = yices.YVAL_TUPLE
    FUNCTION = yices.YVAL_FUNCTION
    MAPPING = yices.YVAL_MAPPING
