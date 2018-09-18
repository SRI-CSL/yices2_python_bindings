import yices


class Status(object):

    IDLE         = yices.STATUS_IDLE
    SEARCHING    = yices.STATUS_SEARCHING
    UNKNOWN      = yices.STATUS_UNKNOWN
    SAT          = yices.STATUS_SAT
    UNSAT        = yices.STATUS_UNSAT
    INTERRUPTED  = yices.STATUS_INTERRUPTED
    ERROR        = yices.STATUS_ERROR
