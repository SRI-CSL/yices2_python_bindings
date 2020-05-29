"""Status wraps the smt_status_t enum, that enumerates a context's possible states."""
import yices_api as yapi

from .YicesException import YicesException

class Status:

    IDLE         = yapi.STATUS_IDLE
    SEARCHING    = yapi.STATUS_SEARCHING
    UNKNOWN      = yapi.STATUS_UNKNOWN
    SAT          = yapi.STATUS_SAT
    UNSAT        = yapi.STATUS_UNSAT
    INTERRUPTED  = yapi.STATUS_INTERRUPTED
    ERROR        = yapi.STATUS_ERROR


    @staticmethod
    def name(status):
        """given a status returns its name, a string describing it."""
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
        raise YicesException('unknown status: {0}'.format(status))
