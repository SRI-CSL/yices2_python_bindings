from ctypes import pointer

import yices_api as yapi


class Dimacs:


    # new in 2.6.2
    @staticmethod
    def export_formula(f, filename, simplify):
        """Bit-blast then export the CNF to a file, return the formula's status.

        If the simplify flag is true, then is also possible for CNF
        simplification to detect that the CNF is sat or unsat. In this
        case, no DIMACS file is produced and a non-idle status is returned.
        """
        status = pointer(yapi.smt_status_t(yapi.STATUS_IDLE))
        # ignore the code because it will raise an exception if something goes pear shaped
        yapi.yices_export_formula_to_dimacs(f, filename, simplify, status)
        return status.contents

    # new in 2.6.2
    @staticmethod
    def export_formulas(f_array, filename, simplify):
        """Bit-blast then export the CNFs to a file, return their status.

        If the simplify flag is true, then is also possible for CNF
        simplification to detect that the CNFs are sat or unsat. In this
        case, no DIMACS file is produced and a non-idle status is returned.
        """
        farray = yapi.make_term_array(f_array)
        status = pointer(yapi.smt_status_t(yapi.STATUS_IDLE))
        # ignore the code because it will raise an exception if something goes pear shaped
        yapi.yices_export_formulas_to_dimacs(farray, len(f_array), filename, simplify, status)
        return status.contents
