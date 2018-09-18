import yices_api as yapi


class Status(object):

    IDLE         = yapi.STATUS_IDLE
    SEARCHING    = yapi.STATUS_SEARCHING
    UNKNOWN      = yapi.STATUS_UNKNOWN
    SAT          = yapi.STATUS_SAT
    UNSAT        = yapi.STATUS_UNSAT
    INTERRUPTED  = yapi.STATUS_INTERRUPTED
    ERROR        = yapi.STATUS_ERROR
