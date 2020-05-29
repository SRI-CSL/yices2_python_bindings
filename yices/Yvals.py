"""YVals is the Python representation of the yval_t enum, the node tags of value DAGS is a Model."""
import yices_api as yapi


class Yval:

    UNKNOWN   = yapi.YVAL_UNKNOWN
    BOOL      = yapi.YVAL_BOOL
    RATIONAL  = yapi.YVAL_RATIONAL
    ALGEBRAIC = yapi.YVAL_ALGEBRAIC
    BV        = yapi.YVAL_BV
    SCALAR    = yapi.YVAL_SCALAR
    TUPLE     = yapi.YVAL_TUPLE
    FUNCTION  = yapi.YVAL_FUNCTION
    MAPPING   = yapi.YVAL_MAPPING
