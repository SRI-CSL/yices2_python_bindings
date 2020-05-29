""" The Types class provides Pythonesque static methods for constructing and manipulating yices' types."""
import yices_api as yapi

from .YicesException import YicesException

class Types:


    NULL_TYPE = -1
    BOOL      = yapi.yices_bool_type()
    INT       = yapi.yices_int_type()
    REAL      = yapi.yices_real_type()
    BV8       = yapi.yices_bv_type(8)
    BV16      = yapi.yices_bv_type(16)
    BV32      = yapi.yices_bv_type(32)
    BV64      = yapi.yices_bv_type(64)


    @staticmethod
    def bv_type(nbits, name=None):
        if nbits <= 0:
            raise YicesException(msg="nbits must be positive")
        tau = yapi.yices_bv_type(nbits)
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def bool_type(name=None):
        tau = yapi.yices_bool_type()
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def int_type(name=None):
        tau = yapi.yices_int_type()
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def real_type(name=None):
        tau = yapi.yices_real_type()
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def new_scalar_type(card, name=None):
        if card <= 0:
            raise YicesException(msg="new_scalar_type: card must be positive")
        tau = yapi.yices_new_scalar_type(card)
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def new_uninterpreted_type(name=None):
        tau = yapi.yices_new_uninterpreted_type()
        if name and not Types.set_name(tau, name):
            return None
        return tau

    @staticmethod
    def new_tuple_type(types,  name=None):
        tau = -1
        tlen = len(types)
        if tlen <= 0:
            raise YicesException(msg="new_tuple_type: len(types) must be positive")
        if tlen == 1:
            tau = yapi.yices_tuple_type1(types[0])
        elif tlen == 2:
            tau = yapi.yices_tuple_type2(types[0], types[1])
        elif tlen == 3:
            tau = yapi.yices_tuple_type3(types[0], types[1], types[2])
        else:
            tarray = yapi.make_type_array(types)
            tau = yapi.yices_tuple_type(tlen, tarray)
        if tau == Types.NULL_TYPE:
            raise YicesException('yices_tuple_type')
        if name and not Types.set_name(tau, name):
            return None
        return tau


    @staticmethod
    def new_function_type(doms, rng, name=None):
        tau = -1
        dlen = len(doms)
        if dlen <= 0:
            raise YicesException(msg="new_function_type: len(doms) must be positive")
        if dlen == 1:
            tau = yapi.yices_function_type1(doms[0], rng)
        elif dlen == 2:
            tau = yapi.yices_function_type2(doms[0], doms[1], rng)
        elif dlen == 3:
            tau = yapi.yices_function_type3(doms[0], doms[1], doms[2], rng)
        else:
            darray = yapi.make_type_array(doms)
            tau = yapi.yices_function_type(dlen, darray, rng)
        if tau == Types.NULL_TYPE:
            raise YicesException('yices_function_type')
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
        tau =  yapi.yices_new_scalar_type(cardinality)
        if not Types.set_name(tau, name):
            return (None, None)
        elements = [None] * cardinality
        for i in range(0, cardinality):
            elements[i] = yapi.yices_constant(tau, i)
            ni = element_names[i]
            errcode = yapi.yices_set_term_name(elements[i], ni)
            if errcode == -1:
                raise YicesException('yices_set_term_name')
        return (tau, elements)


    # recognizers

    @staticmethod
    def is_bool(tau):
        return bool(yapi.yices_type_is_bool(tau))

    @staticmethod
    def is_int(tau):
        return bool(yapi.yices_type_is_int(tau))

    @staticmethod
    def is_real(tau):
        return bool(yapi.yices_type_is_real(tau))

    @staticmethod
    def is_arithmetic(tau):
        return bool(yapi.yices_type_is_arithmetic(tau))

    @staticmethod
    def is_bitvector(tau):
        return bool(yapi.yices_type_is_bitvector(tau))

    @staticmethod
    def is_scalar(tau):
        return bool(yapi.yices_type_is_scalar(tau))

    @staticmethod
    def is_uninterpreted(tau):
        return bool(yapi.yices_type_is_uninterpreted(tau))

    @staticmethod
    def is_tuple(tau):
        return bool(yapi.yices_type_is_tuple(tau))

    @staticmethod
    def is_function(tau):
        return bool(yapi.yices_type_is_function(tau))

    @staticmethod
    def is_subtype(tau0, tau1):
        return bool(yapi.yices_test_subtype(tau0, tau1))

    @staticmethod
    def compatible_types(tau0, tau1):
        return bool(yapi.yices_compatible_types(tau0, tau1))

    # type deconstruction

    @staticmethod
    def bvtype_size(tau):
        retval = yapi.yices_bvtype_size(tau)
        if retval == 0:
            raise YicesException('yices_bvtype_size')
        return retval

    @staticmethod
    def scalar_type_card(tau):
        retval = yapi.yices_scalar_type_card(tau)
        if retval == 0:
            raise YicesException('yices_scalar_type_card')
        return retval

    @staticmethod
    def num_children(tau):
        retval = yapi.yices_type_num_children(tau)
        if retval == -1:
            raise YicesException('yices_type_num_children')
        return retval

    @staticmethod
    def child(tau, i):
        retval = yapi.yices_type_child(tau, i)
        if retval == Types.NULL_TYPE:
            raise YicesException('yices_type_child')
        return retval

    @staticmethod
    def children(tau):
        typev = yapi.type_vector_t()
        yapi.yices_init_type_vector(typev)
        errcode = yapi.yices_type_children(tau, typev)
        if errcode == -1:
            yapi.yices_delete_type_vector(typev)
            raise YicesException('yices_type_children')
        retval = []
        for i in range(0, typev.size):
            retval.append(typev.data[i])
        yapi.yices_delete_type_vector(typev)
        return retval


   # parsing

    @staticmethod
    def parse_type(s):
        return yapi.yices_parse_type(s)


    # names

    @staticmethod
    def set_name(tau, name):
        if name is None:
            return False
        errcode = yapi.yices_set_type_name(tau, name)
        if errcode == -1:
            raise YicesException('yices_set_type_name')
        return True

    @staticmethod
    def remove_name(name):
        if name is None:
            return False
        yapi.yices_remove_type_name(name)
        return True


    @staticmethod
    def clear_name(tau):
        errcode = yapi.yices_clear_type_name(tau)
        return errcode == 0

    @staticmethod
    def get_name(tau):
        name = yapi.yices_get_type_name(tau)
        if name == 0:
            return None
        return name

    @staticmethod
    def get_by_name(name):
        return  yapi.yices_get_type_by_name(name)

    # printing

    @staticmethod
    def print_to_fd(fd, tau, width, height, offset):
        errcode = yapi.yices_pp_type_fd(fd, tau, int(width), int(height), int(offset))
        if errcode == -1:
            raise YicesException('yices_pp_type_fd')


    @staticmethod
    def to_string(tau, width, height, offset):
        retval = yapi.yices_type_to_string(tau, int(width), int(height), int(offset))
        if retval == 0:
            raise YicesException('yices_type_to_string')
        return retval
