import sys

import yices

class Types(object):


    NULL_TYPE = -1
    BOOL      = yices.yices_bool_type()
    INT       = yices.yices_int_type()
    REAL      = yices.yices_real_type()
    BV8       = yices.yices_bv_type(8)
    BV16      = yices.yices_bv_type(16)
    BV32      = yices.yices_bv_type(32)
    BV64      = yices.yices_bv_type(64)


    @staticmethod
    def bv_type(nbits, name=None):
        if nbits <= 0:
            raise Exception("nbits must be positive")
        tau = yices.yices_bv_type(nbits)
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def int_type(name=None):
        tau = yices.yices_int_type()
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def real_type(name=None):
        tau = yices.yices_real_type()
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def new_scalar_type(card, name=None):
        if card <= 0:
            raise Exception("new_scalar_type: card must be positive")
        tau = yices.yices_new_scalar_type(card)
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def new_uninterpreted_type(name=None):
        tau = yices.yices_new_uninterpreted_type()
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def new_tuple_type(types,  name=None):
        tau = -1
        tlen = len(types)
        if tlen <= 0:
            raise Exception("new_tuple_type: len(types) must be positive")
        elif tlen == 1:
            tau = yices.yices_tuple_type1(types[0])
        elif tlen == 2:
            tau = yices.yices_tuple_type2(types[0], types[1])
        elif tlen == 3:
            tau = yices.yices_tuple_type3(types[0], types[1], types[3])
        else:
            tarray = yices.make_type_array(types)
            tau = yices.yices_tuple_type(tlen, tarray)
        if tau == -1:
            #FIXME: which will we do CONSISTENTLY? return None or throw and exception
            sys.stderr.write('new_tuple_type({0}) failed {1}\n', types, yices.yices_error_string())
            return None
        if name and not Types.set_name(tau, name):
            return None
        return tau


    @staticmethod
    def new_function_type(doms, rng, name=None):
        tau = -1
        dlen = len(doms)
        if dlen <= 0:
            raise Exception("new_function_type: len(doms) must be positive")
        elif dlen == 1:
            tau = yices.yices_function_type1(doms[0], rng)
        elif dlen == 2:
            tau = yices.yices_function_type2(doms[0], doms[1], rng)
        elif dlen == 3:
            tau = yices.yices_function_type3(doms[0], doms[1], doms[2], rng)
        else:
            darray = yices.make_type_array(doms)
            tau = yices.yices_function_type(dlen, darray, rng)
        if tau == -1:
            #FIXME: which will we do CONSISTENTLY? return None or throw and exception
            sys.stderr.write('new_function_type({0}, {1}) failed {2}\n', doms, rng, yices.yices_error_string())
            return None
        if name and not Types.set_name(tau, name):
            return None
        return tau



    @staticmethod
    def declare_enum(name, element_names):
        """Declares a new scalar type with the given element_names, which
        should all be distinct.

        It returns the yices term for the type, and the list of yices terms
        corresponding to the element with the associated name.
        """
        assert name
        assert element_names
        cardinality = len(element_names)
        tau =  yices.yices_new_scalar_type(cardinality)
        if not Types.set_name(tau, name):
            return (None, None)
        elements = [None] * cardinality
        for i in range(0, cardinality):
            elements[i] = yices.yices_constant(tau, i)
            ni = element_names[i]
            errcode = yices.yices_set_term_name(elements[i], ni)
            if errcode == -1:
                sys.stderr.write('declare_finite_set: yices_set_term_name({0}, {1}) failed {2}\n', elements[i], ni, yices.yices_error_string())
                return (None, None)
        return (tau, elements)


    # recognizers
    # FIXME: TBD


    # names

    @staticmethod
    def set_name(tau, name):
        if name is None:
            return False
        errcode = yices.yices_set_type_name(tau, name)
        if errcode == -1:
            sys.stderr.write('Types.set_name({0}, {1}): yices_set_type_name failed {2}\n', tau, name, yices.yices_error_string())
            return False
        return True

    @staticmethod
    def remove_name(name):
        if name is None:
            return False
        yices.yices_remove_type_name(name)
        return True


    @staticmethod
    def clear_name(tau):
        errcode = yices.yices_clear_type_name(tau)
        return True if errcode == 0 else False

    @staticmethod
    def get_name(tau):
        name = yices.yices_get_type_name(tau)
        if name == 0:
            return None
        return name

    @staticmethod
    def get_by_name(name):
        tau = yices.yices_get_type_by_name(name)
        if tau == -1:
            return None
        return tau
