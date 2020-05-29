"""Yices allows one to bit blast and then export the results out to a file in the DIMACS format.

This class encapsulates this feature."""

from ctypes import pointer

import yices_api as yapi


class Dimacs:


    # new in 2.6.2
    @staticmethod
    def export_formula(f, filename, simplify):
        """Bit-blast then export the CNF to a file, returns a pair consisting of a boolean
        and a status. The boolean is True if the file was written, or False indicating
        that the status of the formulas was determined, and is the second component.

        If the simplify flag is true, then is also possible for CNF
        simplification to detect that the CNF is sat or unsat.
        """
        status = pointer(yapi.smt_status_t(yapi.STATUS_IDLE))
        code = yapi.yices_export_formula_to_dimacs(f, filename, simplify, status)
        return (code == 1, status.contents.value)

    # new in 2.6.2
    @staticmethod
    def export_formulas(f_array, filename, simplify):
        """Bit-blast then export the CNFs to a file, returns a pair consisting of a boolean
        and a status. The boolean is True if the file was written, or False indicating
        that the status of the formulas was determined, and is the second component.

        If the simplify flag is true, then is also possible for CNF
        simplification to detect that the CNF is sat or unsat.
        """
        farray = yapi.make_term_array(f_array)
        status = pointer(yapi.smt_status_t(yapi.STATUS_IDLE))
        code = yapi.yices_export_formulas_to_dimacs(farray, len(f_array), filename, simplify, status)
        return (code == 1, status.contents.value)
