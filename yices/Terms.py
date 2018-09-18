import sys

import yices_api as yapi


class Terms(object):

    NULL_TERM = -1
    TRUE      = yapi.yices_true()
    FALSE     = yapi.yices_false()
    ZERO      = yapi.yices_zero()
    #FIXME: int32 or int64. Ask BD?
    ONE       = yapi.yices_int32(1)
    MINUS_ONE = yapi.yices_int32(-1)


    #general logical term constructors

    @staticmethod
    def true():
        return Terms.TRUE


    @staticmethod
    def false():
        return Terms.FALSE

    @staticmethod
    def constant(tau, index):
        return yapi.yices_constant(tau, index)

    @staticmethod
    def new_uninterpreted_term(tau, name=None):
        term = yapi.yices_new_uninterpreted_term(tau)
        if name and not Terms.set_name(term, name):
            return None
        return term

    @staticmethod
    def new_variable(tau, name=None):
        term = yapi.yices_new_variable(tau)
        if name and not Terms.set_name(term, name):
            return None
        return term


    @staticmethod
    def integer(value):
        return yapi.yices_int64(long(value))


    @staticmethod
    def negation(term):
        return yapi.yices_not(term)


    @staticmethod
    def conjunction(terms):
        tlen = len(terms)
        if not len:
            return Terms.TRUE
        if tlen == 1:
            return terms[0]
        if tlen == 2:
            return yapi.yices_and2(terms[0], terms[1])
        if tlen == 3:
            return yapi.yices_and3(terms[0], terms[1], terms[2])
        return yapi.yices_and(tlen, yapi.make_term_array(terms))

    @staticmethod
    def disjunction(terms):
        tlen = len(terms)
        if not len:
            return Terms.FALSE
        if tlen == 1:
            return terms[0]
        if tlen == 2:
            return yapi.yices_or2(terms[0], terms[1])
        if tlen == 3:
            return yapi.yices_or3(terms[0], terms[1], terms[2])
        return yapi.yices_or(tlen, yapi.make_term_array(terms))

    @staticmethod
    def xor(terms):
        assert terms
        return yapi.yices_xor(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def application(fun, terms):
        tlen = len(terms)
        assert tlen
        if tlen == 1:
            return yapi.yices_application1(fun, terms[0])
        if tlen == 2:
            return yapi.yices_application2(fun, terms[0], terms[1])
        if tlen == 3:
            return yapi.yices_application3(fun, terms[0], terms[1], terms[2])
        return yapi.yices_application(fun, tlen, yapi.make_term_array(terms))


    @staticmethod
    def ite(cond, then_term, else_term):
        return yapi.yices_ite(cond, then_term, else_term)

    @staticmethod
    def eq(lhs_term, rhs_term):
        return yapi.yices_eq(lhs_term, rhs_term)

    @staticmethod
    def neq(lhs_term, rhs_term):
        return yapi.yices_neq(lhs_term, rhs_term)

    @staticmethod
    def iff(lhs_term, rhs_term):
        return yapi.yices_iff(lhs_term, rhs_term)

    @staticmethod
    def implies(lhs_term, rhs_term):
        return yapi.yices_implies(lhs_term, rhs_term)

    @staticmethod
    def tuple(terms):
        return yapi.yices_tuple(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def select(index, tuple_term):
        return yapi.yices_select(index, tuple_term)

    @staticmethod
    def tuple_update(tuple_terms, index, value):
        return yapi.yices_tuple_update(tuple_terms, index, value)

    @staticmethod
    def update(fun, args, value):
        assert args
        return yapi.yices_update(fun, len(args), yapi.make_term_array(args), value)

    @staticmethod
    def distinct(args):
        assert args
        return yapi.yices_distinct(len(args), yapi.make_term_array(args))

    @staticmethod
    def forall(variables, body):
        return yapi.yices_forall(len(variables), yapi.make_term_array(variables), body)

    @staticmethod
    def exists(variables, body):
        return yapi.yices_exists(len(variables), yapi.make_term_array(variables), body)

    #arithmetic term constructors

    @staticmethod
    def new_rational(n, d):
        assert d
        return yapi.yices_rational64(long(n), long(d))

    @staticmethod
    def new_rational_from_fraction(f):
        return yapi.yices_rational64(long(f.numerator), long(f.denominator))

    @staticmethod
    def parse_rational(s):
        assert s
        return yapi.yices_parse_rational(s)

    @staticmethod
    def parse_float(s):
        assert s
        return yapi.yices_parse_float(s)

    @staticmethod
    def add(lhs, rhs):
        return yapi.yices_add(lhs, rhs)

    @staticmethod
    def sub(lhs, rhs):
        return yapi.yices_sub(lhs, rhs)

    @staticmethod
    def mul(lhs, rhs):
        return yapi.yices_mul(lhs, rhs)

    @staticmethod
    def neg(term):
        return yapi.yices_neg(term)

    @staticmethod
    def square(term):
        return yapi.yices_square(term)

    @staticmethod
    def power(term, exponent):
        return yapi.yices_power(term, exponent)

    @staticmethod
    def sum(terms):
        return yapi.yices_sum(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def product(terms):
        return yapi.yices_product(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def idiv(lhs, rhs):
        return yapi.yices_idiv(lhs, rhs)

    @staticmethod
    def imod(lhs, rhs):
        return yapi.yices_imod(lhs, rhs)

    @staticmethod
    def divides_atom(lhs, rhs):
        return yapi.yices_divides_atom(lhs, rhs)

    @staticmethod
    def is_int_atom(term):
        return yapi.yices_is_int_atom(term)

    @staticmethod
    def abs(term):
        return yapi.yices_abs(term)

    @staticmethod
    def floor(term):
        return yapi.yices_floor(term)

    @staticmethod
    def ceil(term):
        return yapi.yices_ceil(term)

    @staticmethod
    def arith_eq_atom(lhs, rhs):
        return yapi.yices_arith_eq_atom(lhs, rhs)

    @staticmethod
    def arith_neq_atom(lhs, rhs):
        return yapi.yices_arith_neq_atom(lhs, rhs)

    @staticmethod
    def arith_geq_atom(lhs, rhs):
        return yapi.yices_arith_geq_atom(lhs, rhs)

    @staticmethod
    def arith_leq_atom(lhs, rhs):
        return yapi.yices_arith_leq_atom(lhs, rhs)

    @staticmethod
    def arith_gt_atom(lhs, rhs):
        return yapi.yices_arith_gt_atom(lhs, rhs)

    @staticmethod
    def arith_lt_atom(lhs, rhs):
        return yapi.yices_arith_lt_atom(lhs, rhs)

    @staticmethod
    def arith_eq0_atom(term):
        return yapi.yices_arith_eq0_atom(term)

    @staticmethod
    def arith_neq0_atom(term):
        return yapi.yices_arith_neq0_atom(term)

    @staticmethod
    def arith_geq0_atom(term):
        return yapi.yices_arith_geq0_atom(term)

    @staticmethod
    def arith_leq0_atom(term):
        return yapi.yices_arith_leq0_atom(term)

    @staticmethod
    def arith_gt0_atom(term):
        return yapi.yices_arith_gt0_atom(term)

    @staticmethod
    def arith_lt0_atom(term):
        return yapi.yices_arith_lt0_atom(term)


    #bv term constructors

    #FIXME: ask BD do we really need the uint32 uint64 int32 int64  variants?
    @staticmethod
    def bv_const_integer(nbits, i):
        return yapi.yices_bvconst_int64(nbits, long(i))

    @staticmethod
    def bv_const_zero(nbits):
        return yapi.yices_bvconst_zero(nbits)

    @staticmethod
    def bv_const_one(nbits):
        return yapi.yices_bvconst_zero(nbits)

    @staticmethod
    def bv_const_minus_one(nbits):
        return yapi.yices_bvconst_zero(nbits)

    @staticmethod
    def bv_const_from_array(array_o_bits):
        return yapi.yices_bvconst_from_array(len(array_o_bits), yapi.make_int32_array(array_o_bits))

    @staticmethod
    def parse_bvbin(s):
        return yapi.yices_parse_bvbin(s)

    @staticmethod
    def parse_bvhex(s):
        return yapi.yices_parse_bvhex(s)

    @staticmethod
    def bvadd(lhs, rhs):
        return yapi.yices_bvadd(lhs, rhs)

    @staticmethod
    def bvsub(lhs, rhs):
        return yapi.yices_bvsub(lhs, rhs)

    @staticmethod
    def bvneg(t):
        return yapi.yices_bvneg(t)

    @staticmethod
    def bvmul(lhs, rhs):
        return yapi.yices_bvmul(lhs, rhs)

    @staticmethod
    def bvsquare(t):
        return yapi.yices_bvsquare(t)

    @staticmethod
    def bvpower(t, d):
        return yapi.yices_bvpower(t, d)

    @staticmethod
    def bvdiv(lhs, rhs):
        return yapi.yices_bvdiv(lhs, rhs)

    @staticmethod
    def bvrem(lhs, rhs):
        return yapi.yices_bvrem(lhs, rhs)

    @staticmethod
    def bvsrem(lhs, rhs):
        return yapi.yices_bvsrem(lhs, rhs)

    @staticmethod
    def bvsmod(lhs, rhs):
        return yapi.yices_bvsmod(lhs, rhs)

    @staticmethod
    def bvnot(t):
        return yapi.yices_bvnot(t)

    @staticmethod
    def bvnand(lhs, rhs):
        return yapi.yices_bvnand(lhs, rhs)

    @staticmethod
    def bvnor(lhs, rhs):
        return yapi.yices_bvnor(lhs, rhs)

    @staticmethod
    def bvxnor(lhs, rhs):
        return yapi.yices_bvxnor(lhs, rhs)

    @staticmethod
    def bvshl(lhs, rhs):
        return yapi.yices_bvshl(lhs, rhs)

    @staticmethod
    def bvlshr(lhs, rhs):
        return yapi.yices_bvlshr(lhs, rhs)

    @staticmethod
    def bvashr(lhs, rhs):
        return yapi.yices_bvashr(lhs, rhs)

    @staticmethod
    def bvand(terms):
        return yapi.yices_bvand(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def bvor(terms):
        return yapi.yices_bvor(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def bvxor(terms):
        return yapi.yices_bvxor(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def bvsum(terms):
        return yapi.yices_bvsum(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def bvproduct(terms):
        return yapi.yices_bvproduct(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def shift_left0(t, n):
        return yapi.yices_shift_left0(t, n)

    @staticmethod
    def shift_left1(t, n):
        return yapi.yices_shift_left1(t, n)

    @staticmethod
    def shift_right0(t, n):
        return yapi.yices_shift_right0(t, n)

    @staticmethod
    def shift_right1(t, n):
        return yapi.yices_shift_right1(t, n)

    @staticmethod
    def ashift_right(t, n):
        return yapi.yices_ashift_right(t, n)

    @staticmethod
    def rotate_left(t, n):
        return yapi.yices_rotate_left(t, n)

    @staticmethod
    def rotate_right(t, n):
        return yapi.yices_rotate_right(t, n)

    @staticmethod
    def bvextract(t, i, j):
        return yapi.yices_bvextract(t, i, j)

    @staticmethod
    def bvconcat(terms):
        return yapi.yices_bvconcat(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def bvrepeat(t, n):
        return yapi.yices_bvrepeat(t, n)

    @staticmethod
    def sign_extend(t, n):
        return yapi.yices_sign_extend(t, n)

    @staticmethod
    def zero_extend(t, n):
        return yapi.yices_zero_extend(t, n)

    @staticmethod
    def redand(t):
        return yapi.yices_redand(t)

    @staticmethod
    def redor(t):
        return yapi.yices_redor(t)

    @staticmethod
    def redcomp(lhs, rhs):
        return yapi.yices_redcomp(lhs, rhs)

    @staticmethod
    def bvarray(terms):
        return yapi.yices_bvarray(len(terms), yapi.make_term_array(terms))

    @staticmethod
    def bitextract(t, i):
        return yapi.yices_bitextract(t, i)

    # bitvector atoms

    @staticmethod
    def bveq_atom(lhs, rhs):
        return yapi.yices_bveq_atom(lhs, rhs)

    @staticmethod
    def bvneq_atom(lhs, rhs):
        return yapi.yices_bvneq_atom(lhs, rhs)

    @staticmethod
    def bvge_atom(lhs, rhs):
        return yapi.yices_bvge_atom(lhs, rhs)

    @staticmethod
    def bvgt_atom(lhs, rhs):
        return yapi.yices_bvgt_atom(lhs, rhs)

    @staticmethod
    def bvle_atom(lhs, rhs):
        return yapi.yices_bvle_atom(lhs, rhs)

    @staticmethod
    def bvlt_atom(lhs, rhs):
        return yapi.yices_bvlt_atom(lhs, rhs)

    @staticmethod
    def bvsge_atom(lhs, rhs):
        return yapi.yices_bvsge_atom(lhs, rhs)

    @staticmethod
    def bvsgt_atom(lhs, rhs):
        return yapi.yices_bvsgt_atom(lhs, rhs)

    @staticmethod
    def bvsle_atom(lhs, rhs):
        return yapi.yices_bvsle_atom(lhs, rhs)

    @staticmethod
    def bvslt_atom(lhs, rhs):
        return yapi.yices_bvslt_atom(lhs, rhs)

    # parsing

    # substitutions

    # term exploration

    # names

    @staticmethod
    def set_name(term, name):
        if name is None:
            return False
        errcode = yapi.yices_set_term_name(term, name)
        if errcode == -1:
            sys.stderr.write('Terms.set_name({0}, {1}): yices_set_term_name failed {2}\n', term, name, yapi.yices_error_string())
            return False
        return True

    @staticmethod
    def remove_name(name):
        if name is None:
            return False
        yapi.yices_remove_term_name(name)
        return True


    @staticmethod
    def clear_name(term):
        errcode = yapi.yices_clear_term_name(term)
        return True if errcode == 0 else False

    @staticmethod
    def get_name(term):
        name = yapi.yices_get_term_name(term)
        if name == 0:
            return None
        return name

    @staticmethod
    def get_by_name(name):
        term = yapi.yices_get_term_by_name(name)
        if term == -1:
            return None
        return term
