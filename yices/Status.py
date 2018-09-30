import yices_api as yapi


class Status(object):

    IDLE         = yapi.STATUS_IDLE
    SEARCHING    = yapi.STATUS_SEARCHING
    UNKNOWN      = yapi.STATUS_UNKNOWN
    SAT          = yapi.STATUS_SAT
    UNSAT        = yapi.STATUS_UNSAT
    INTERRUPTED  = yapi.STATUS_INTERRUPTED
    ERROR        = yapi.STATUS_ERROR


    @staticmethod
    def name(status):
        if status == Status.IDLE:
            return 'IDLE'
        if status == Status.SEARCHING:
            return 'SEARCHING'
        if status == Status.UNKNOWN:
            return 'UNKNOWN'
        if status == Status.SAT:
            return 'SAT'
        if status == Status.UNSAT:
            return 'UNSAT'
        if status == Status.INTERRUPTED:
            return 'INTERRUPTED'
        if status == Status.ERROR:
            return 'ERROR'
