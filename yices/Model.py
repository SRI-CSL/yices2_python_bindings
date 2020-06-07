"""The Model class wraps the Yices model_t structure.

If a context is satisfiable, Yices can build a model of the context’s
assertions. Functions are provided to extract the values of terms in a
model. Atomic values (e.g., integer or bitvector constants) can be
obtained directly. Non-atomic values—that is, tuples or functions—are
represented internally as nodes in a DAG. The API includes functions
to explore this DAG and get the values of tuples or functions.
"""

import ctypes

from fractions import Fraction

import yices_api as yapi

from .Yvals import Yval
from .YicesException import YicesException
from .Yices import Yices

class Model:

    GEN_DEFAULT    = yapi.YICES_GEN_DEFAULT
    GEN_BY_SUBST   = yapi.YICES_GEN_BY_SUBST
    GEN_BY_PROJ    = yapi.YICES_GEN_BY_PROJ


    __population = 0


    def __init__(self, model=None):
        self.model =  model
        Model.__population += 1


    @staticmethod
    def from_context(context, keep_subst):
        #model = yapi.yices_get_model(context.context, keep_subst)
        model = Yices.get_model(context.context, keep_subst)
        if model == 0:
            raise YicesException('yices_get_model')
        return Model(model)


    @staticmethod
    def from_map(mapping):
        dom = mapping.keys()
        rng = [ mapping[d] for d in dom]
        #model = yapi.yices_model_from_map(len(dom), yapi.make_term_array(dom), yapi.make_term_array(rng))
        model = Yices.model_from_map(len(dom), yapi.make_term_array(dom), yapi.make_term_array(rng))
        if model == 0:
            raise YicesException('yices_model_from_map')
        return Model(model)


    def collect_defined_terms(self):
        defined_terms = yapi.term_vector_t()
        yapi.yices_init_term_vector(defined_terms)
        #yapi.yices_model_collect_defined_terms(self.model, defined_terms)
        Yices.model_collect_defined_terms(self.model, defined_terms)
        retval = []
        for i in range(0, defined_terms.size):
            retval.append(defined_terms.data[i])
        yapi.yices_delete_term_vector(defined_terms)
        return retval

    def dispose(self):
        assert self.model is not None
        #yapi.yices_free_model(self.model)
        Yices.free_model(self.model)
        self.model = None
        Model.__population -= 1


    def get_bool_value(self, term):
        ytval = ctypes.c_int32()
        errcode = yapi.yices_get_bool_value(self.model, term, ytval)
        if errcode == -1:
            raise YicesException('yices_get_bool_value')
        return bool(ytval.value)


    def get_integer_value(self, term):
        ytval = ctypes.c_int64()
        errcode = yapi.yices_get_int64_value(self.model, term, ytval)
        if errcode == -1:
            raise YicesException('yices_get_int64_value')
        return ytval.value

    def get_fraction_value(self, term):
        ytnum = ctypes.c_int64()
        ytden = ctypes.c_uint64()
        errcode = yapi.yices_get_rational64_value(self.model, term, ytnum, ytden)
        if errcode == -1:
            raise YicesException('yices_get_rational64_value')
        return Fraction(ytnum.value, ytden.value)


    def get_float_value(self, term):
        ytval = ctypes.c_double()
        errcode = yapi.yices_get_double_value(self.model, term, ytval)
        if errcode == -1:
            raise YicesException('yices_get_double_value')
        return ytval.value

    def get_scalar_value(self, term):
        """ Returns the index of the value. This is the low level version, and does not use yapi.yices_constant. """
        ytval = ctypes.c_int32()
        errcode = yapi.yices_get_scalar_value(self.model, term, ytval)
        if errcode == -1:
            raise YicesException('yices_get_scalar_value')
        return ytval.value


    def formula_true_in_model(self, term):
        return yapi.yices_formula_true_in_model(self.model, term) == 1
        #return Yices.formula_true_in_model(self.model, term) == 1

    def formulas_true_in_model(self, term_array):
        tarray = yapi.make_term_array(term_array)
        return yapi.yices_formulas_true_in_model(self.model, len(term_array), tarray) == 1
        #return Yices.yices_formulas_true_in_model(self.model, len(term_array), tarray) == 1

    def get_value_from_rational_yval(self, yval):
        if yapi.yices_val_is_int64(self.model, yval):
            val = ctypes.c_int64()
            errcode = yapi.yices_val_get_int64(self.model,  yval, val)
            if errcode == -1:
                raise YicesException('yices_val_get_int64')
            return val.value
        if yapi.yices_val_is_rational64(self.model, yval):
            ytnum = ctypes.c_int64()
            ytden = ctypes.c_uint64()
            errcode = yapi.yices_val_get_rational64(self.model,  yval, ytnum, ytden)
            if errcode == -1:
                raise YicesException('yices_val_get_rational64')
            return Fraction(ytnum.value, ytden.value)
        val = ctypes.c_double()
        errcode = yapi.yices_val_get_double(self.model,  yval, val)
        if errcode == -1:
            raise YicesException('yices_val_get_double')
        return val.value

    def get_value_from_bool_yval(self, yval):
        value = ctypes.c_int32()
        errcode =  yapi.yices_val_get_bool(self.model, yval, value)
        if errcode == -1:
            raise YicesException('yices_val_get_bool')
        return bool(value.value)

    def get_value_from_scalar_yval(self, yval):
        value = ctypes.c_int32()
        typev = ctypes.c_int32()
        errcode =  yapi.yices_val_get_scalar(self.model, yval, value, typev)
        if errcode == -1:
            raise YicesException('yices_val_get_scalar')
        return yapi.yices_constant(typev.value, value.value)

    def get_value_from_bv_yval(self, yval):
        bvsize = yapi.yices_val_bitsize(self.model, yval)
        if bvsize <= 0:
            return None
        bvarray = yapi.make_empty_int32_array(bvsize)
        errcode = yapi.yices_val_get_bv(self.model, yval, bvarray)
        if errcode == -1:
            raise YicesException('yices_val_get_bv')
        return [ bvarray[i] for i in range(0, bvsize) ]

    #this problem is part of the gmp libpoly conundrum
    def get_value_from_algebraic_yval(self, yval):
        val = ctypes.c_double()
        errcode = yapi.yices_val_get_double(self.model,  yval, val)
        if errcode == -1:
            raise YicesException('yices_val_get_double')
        return val.value

    def get_value_from_tuple_yval(self, yval):
        tuple_size = yapi.yices_val_tuple_arity(self.model, yval)
        if tuple_size <= 0:
            return None
        yval_array = yapi.make_empty_yval_array(tuple_size)
        errcode = yapi.yices_val_expand_tuple(self.model, yval, yval_array)
        if errcode == -1:
            raise YicesException('yices_val_expand_tuple')
        retval = [ self.get_value_from_yval(yval_array[i]) for i in range(0, tuple_size) ]
        return tuple(retval)

    def get_value_from_mapping_yval(self, yval):
        mapping_size = yapi.yices_val_mapping_arity(self.model, yval)
        if mapping_size <= 0:
            return None
        ytgt = yapi.yval_t()
        ysrc = yapi.make_empty_yval_array(mapping_size)
        errcode = yapi.yices_val_expand_mapping(self.model, yval, ysrc, ytgt)
        if errcode == -1:
            raise YicesException('yices_val_expand_mapping')
        src = [self.get_value_from_yval(ysrc[i]) for i in range(0, mapping_size) ]
        tgt = self.get_value_from_yval(ytgt)
        return (tuple(src), tgt)

    def get_value_from_function_yval(self, yval):
        function_size = yapi.yices_val_function_arity(self.model, yval)
        if function_size <= 0:
            return None
        ydefault = yapi.yval_t()
        ymapping = yapi.yval_vector_t()
        yapi.yices_init_yval_vector(ymapping)
        errcode = yapi.yices_val_expand_function(self.model, yval, ydefault, ymapping)
        if errcode == -1:
            yapi.yices_delete_yval_vector(ymapping)
            raise YicesException('yices_val_expand_function')
        default = self.get_value_from_yval(ydefault)
        mapping = [ self.get_value_from_yval(ymapping.data[i]) for i in range(0, ymapping.size) ]
        dict_map = {}
        for (src, tgt) in mapping:
            dict_map[src] = tgt
        yapi.yices_delete_yval_vector(ymapping)
        def retfun(src):
            if src in dict_map:
                return dict_map[src]
            return default
        return retfun


    def get_value_from_yval(self, yval):
        tag = yval.node_tag
        if tag == Yval.BOOL:
            return self.get_value_from_bool_yval(yval)
        if tag == Yval.RATIONAL:
            return self.get_value_from_rational_yval(yval)
        if tag == Yval.SCALAR:
            return self.get_value_from_scalar_yval(yval)
        if tag == Yval.BV:
            return self.get_value_from_bv_yval(yval)
        if tag == Yval.ALGEBRAIC:
            return self.get_value_from_algebraic_yval(yval)
        if tag == Yval.TUPLE:
            return self.get_value_from_tuple_yval(yval)
        if tag == Yval.MAPPING:
            return self.get_value_from_mapping_yval(yval)
        if tag == Yval.FUNCTION:
            return self.get_value_from_function_yval(yval)
        raise YicesException(msg='Model.get_value_from_yval: unexpected yval tag {0}\n'.format(tag))



    def get_value(self, term):
        yval = yapi.yval_t()
        errcode = yapi.yices_get_value(self.model, term, yval)
        if errcode == -1:
            raise YicesException('yices_get_value')
        return self.get_value_from_yval(yval)


    #yices tuples should be returned as python tuples

    #yices functions should be returned as closures (i.e functions)

    def get_value_as_term(self, term):
        return yapi.yices_get_value_as_term(self.model, term)

    def implicant_for_formula(self, term):
        termv = yapi.term_vector_t()
        yapi.yices_init_term_vector(termv)
        try:
            code = yapi.yices_implicant_for_formula(self.model, term, termv)
            retval = []
            if code != -1:
                for i in range(0, termv.size):
                    retval.append(termv.data[i])
            yapi.yices_delete_term_vector(termv)
            return retval
        except yapi.YicesAPIException:
            yapi.yices_delete_term_vector(termv)
            raise YicesException('implicant_for_formula')


    def implicant_for_formulas(self, term_array):
        tarray = yapi.make_term_array(term_array)
        termv = yapi.term_vector_t()
        yapi.yices_init_term_vector(termv)
        try:
            code = yapi.yices_implicant_for_formulas(self.model, len(term_array), tarray, termv)
            retval = []
            if code != -1:
                for i in range(0, termv.size):
                    retval.append(termv.data[i])
            yapi.yices_delete_term_vector(termv)
            return retval
        except yapi.YicesAPIException:
            yapi.yices_delete_term_vector(termv)
            raise YicesException('implicant_for_formulas')

    def generalize_model(self, term, elim_array, mode):
        var_array = yapi.make_term_array(elim_array)
        termv = yapi.term_vector_t()
        yapi.yices_init_term_vector(termv)
        errcode = yapi.yices_generalize_model(self.model, term, len(elim_array), var_array, mode, termv)
        if errcode == -1:
            yapi.yices_delete_term_vector(termv)
            raise YicesException('yices_generalize_model')
        retval = []
        for i in range(0, termv.size):
            retval.append(termv.data[i])
        yapi.yices_delete_term_vector(termv)
        return retval

    def generalize_model_array(self, term_array, elim_array, mode):
        tarray = yapi.make_term_array(term_array)
        var_array = yapi.make_term_array(elim_array)
        termv = yapi.term_vector_t()
        yapi.yices_init_term_vector(termv)
        errcode = yapi.yices_generalize_model_array(self.model, len(term_array), tarray, len(elim_array), var_array, mode, termv)
        if errcode == -1:
            yapi.yices_delete_term_vector(termv)
            raise YicesException('yices_generalize_model_array')
        retval = []
        for i in range(0, termv.size):
            retval.append(termv.data[i])
        yapi.yices_delete_term_vector(termv)
        return retval

    # new in 2.6.2
    # term support
    def support_for_term(self, term):
        """Returns the list of uninterpreted terms that fix the value of the given term in the model."""
        termv = yapi.term_vector_t()
        yapi.yices_init_term_vector(termv)
        try:
            code = yapi.yices_model_term_support(self.model, term, termv)
            retval = []
            if code != -1:
                for i in range(0, termv.size):
                    retval.append(termv.data[i])
            yapi.yices_delete_term_vector(termv)
            return retval
        except yapi.YicesAPIException:
            yapi.yices_delete_term_vector(termv)
            raise YicesException('support_for_term')

    # new in 2.6.2
    # term array support
    def support_for_terms(self, term_array):
        """Returns the list of uninterpreted terms that fix the value in the model of every term in the given array."""
        tarray = yapi.make_term_array(term_array)
        termv = yapi.term_vector_t()
        try:
            yapi.yices_init_term_vector(termv)
            code = yapi.yices_model_term_array_support(self.model, len(term_array), tarray, termv)
            retval = []
            if code != -1:
                for i in range(0, termv.size):
                    retval.append(termv.data[i])
            yapi.yices_delete_term_vector(termv)
            return retval
        except yapi.YicesAPIException:
            yapi.yices_delete_term_vector(termv)
            raise YicesException('support_for_terms')


    # printing

    def print_to_fd(self, fd, width=None, height=None, offset=None):
        if (width is None) or (height is None) or (offset is None):
            errcode = yapi.yices_print_model_fd(fd, self.model)
            if errcode == -1:
                raise YicesException('yices_print_model_fd')
        else:
            errcode = yapi.yices_pp_model_fd(fd, self.model, int(width), int(height), int(offset))
            if errcode == -1:
                raise YicesException('yices_pp_print_model_fd')

    def print_term_values(self, fd, term_array, width=None, height=None, offset=None):
        """Print the values of the terms in the model to the file descriptor, pretty print if width, height, and offset are supplied."""
        tarray = yapi.make_term_array(term_array)
        if (width is None) or (height is None) or (offset is None):
            yapi.yices_print_term_values_fd(fd, self.model, len(term_array), tarray)
        else:
            yapi.yices_pp_term_values_fd(fd, self.model, len(term_array), tarray, int(width), int(height), int(offset))


    def to_string(self, width, height, offset):
        #this gonna just have to leak
        return yapi.yices_model_to_string(self.model, int(width), int(height), int(offset))


    @staticmethod
    def population():
        """returns the current live population of Model objects."""
        return Model.__population
