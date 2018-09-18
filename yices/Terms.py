import sys

import yices


class Terms(object):

    NULL_TERM = -1
    TRUE      = yices.yices_true()
    FALSE     = yices.yices_false()
    ZERO      = yices.yices_zero()
    #FIXME: int32 or int64. Ask BD?
    ONE       = yices.yices_int32(1)
    MINUS_ONE = yices.yices_int32(-1)


    #general logical term constructors

    @staticmethod
    def true():
        return Terms.TRUE


    @staticmethod
    def false():
        return Terms.FALSE

    @staticmethod
    def constant(tau, index):
        return yices.yices_constant(tau, index)

    @staticmethod
    def new_uninterpreted_term(tau, name=None):
        term = yices.yices_new_uninterpreted_term(tau)
        if name and not Terms.set_name(term, name):
            return None
        return term

    @staticmethod
    def new_variable(tau, name=None):
        term = yices.yices_new_variable(tau)
        if name and not Terms.set_name(term, name):
            return None
        return term


    @staticmethod
    def integer(value):
        return yices.yices_int64(long(value))


    @staticmethod
    def negation(term):
        return yices.yices_not(term)


    @staticmethod
    def conjunction(terms):
        tlen = len(terms)
        if not len:
            return Terms.TRUE
        if tlen == 1:
            return terms[0]
        if tlen == 2:
            return yices.yices_and2(terms[0], terms[1])
        if tlen == 3:
            return yices.yices_and3(terms[0], terms[1], terms[2])
        return yices.yices_and(tlen, yices.make_term_array(terms))

    @staticmethod
    def disjunction(terms):
        tlen = len(terms)
        if not len:
            return Terms.FALSE
        if tlen == 1:
            return terms[0]
        if tlen == 2:
            return yices.yices_or2(terms[0], terms[1])
        if tlen == 3:
            return yices.yices_or3(terms[0], terms[1], terms[2])
        return yices.yices_or(tlen, yices.make_term_array(terms))

    @staticmethod
    def xor(terms):
        assert terms
        return yices.yices_xor(len(terms), yices.make_term_array(terms))

    @staticmethod
    def application(fun, terms):
        tlen = len(terms)
        assert tlen
        if tlen == 1:
            return yices.yices_application1(fun, terms[0])
        if tlen == 2:
            return yices.yices_application2(fun, terms[0], terms[1])
        if tlen == 3:
            return yices.yices_application3(fun, terms[0], terms[1], terms[2])
        return yices.yices_application(fun, tlen, yices.make_term_array(terms))


    @staticmethod
    def ite(cond, then_term, else_term):
        return yices.yices_ite(cond, then_term, else_term)

    @staticmethod
    def eq(lhs_term, rhs_term):
        return yices.yices_eq(lhs_term, rhs_term)

    @staticmethod
    def neq(lhs_term, rhs_term):
        return yices.yices_neq(lhs_term, rhs_term)

    @staticmethod
    def iff(lhs_term, rhs_term):
        return yices.yices_iff(lhs_term, rhs_term)

    @staticmethod
    def implies(lhs_term, rhs_term):
        return yices.yices_implies(lhs_term, rhs_term)

    @staticmethod
    def tuple(terms):
        return yices.yices_tuple(len(terms), yices.make_term_array(terms))

    @staticmethod
    def select(index, tuple_term):
        return yices.yices_select(index, tuple_term)

    @staticmethod
    def tuple_update(tuple_terms, index, value):
        return yices.yices_tuple_update(tuple_terms, index, value)

    @staticmethod
    def update(fun, args, value):
        assert args
        return yices.yices_update(fun, len(args), yices.make_term_array(args), value)

    @staticmethod
    def distinct(args):
        assert args
        return yices.yices_distinct(len(args), yices.make_term_array(args))

    @staticmethod
    def forall(variables, body):
        return yices.yices_forall(len(variables), yices.make_term_array(variables), body)

    @staticmethod
    def exists(variables, body):
        return yices.yices_exists(len(variables), yices.make_term_array(variables), body)

    #arithmetic term constructors

    @staticmethod
    def new_rational(n, d):
        assert d
        return yices.yices_rational64(long(n), long(d))

    @staticmethod
    def new_rational_from_fraction(f):
        return yices.yices_rational64(long(f.numerator), long(f.denominator))

    @staticmethod
    def parse_rational(s):
        assert s
        return yices.yices_parse_rational(s)

    @staticmethod
    def parse_float(s):
        assert s
        return yices.yices_parse_float(s)

    @staticmethod
    def add(lhs, rhs):
        return yices.yices_add(lhs, rhs)

    @staticmethod
    def sub(lhs, rhs):
        return yices.yices_sub(lhs, rhs)

    @staticmethod
    def mul(lhs, rhs):
        return yices.yices_mul(lhs, rhs)

    @staticmethod
    def neg(term):
        return yices.yices_neg(term)

    @staticmethod
    def square(term):
        return yices.yices_square(term)

    @staticmethod
    def power(term, exponent):
        return yices.yices_power(term, exponent)

    @staticmethod
    def sum(terms):
        return yices.yices_sum(len(terms), yices.make_term_array(terms))

    @staticmethod
    def product(terms):
        return yices.yices_product(len(terms), yices.make_term_array(terms))

    @staticmethod
    def idiv(lhs, rhs):
        return yices.yices_idiv(lhs, rhs)

    @staticmethod
    def imod(lhs, rhs):
        return yices.yices_imod(lhs, rhs)

    @staticmethod
    def divides_atom(lhs, rhs):
        return yices.yices_divides_atom(lhs, rhs)

    @staticmethod
    def is_int_atom(term):
        return yices.yices_is_int_atom(term)

    @staticmethod
    def abs(term):
        return yices.yices_abs(term)

    @staticmethod
    def floor(term):
        return yices.yices_floor(term)

    @staticmethod
    def ceil(term):
        return yices.yices_ceil(term)

    @staticmethod
    def arith_eq_atom(lhs, rhs):
        return yices.yices_arith_eq_atom(lhs, rhs)

    @staticmethod
    def arith_neq_atom(lhs, rhs):
        return yices.yices_arith_neq_atom(lhs, rhs)

    @staticmethod
    def arith_geq_atom(lhs, rhs):
        return yices.yices_arith_geq_atom(lhs, rhs)

    @staticmethod
    def arith_leq_atom(lhs, rhs):
        return yices.yices_arith_leq_atom(lhs, rhs)

    @staticmethod
    def arith_gt_atom(lhs, rhs):
        return yices.yices_arith_gt_atom(lhs, rhs)

    @staticmethod
    def arith_eq0_atom(term):
        return yices.yices_arith_eq0_atom(term)

    @staticmethod
    def arith_neq0_atom(term):
        return yices.yices_arith_neq0_atom(term)

    @staticmethod
    def arith_geq0_atom(term):
        return yices.yices_arith_geq0_atom(term)

    @staticmethod
    def arith_leq0_atom(term):
        return yices.yices_arith_leq0_atom(term)

    @staticmethod
    def arith_gt0_atom(term):
        return yices.yices_arith_gt0_atom(term)

    @staticmethod
    def arith_lt0_atom(term):
        return yices.yices_arith_lt0_atom(term)


    #bv term constructors

    #FIXME: ask BD do we really need the uint32 uint64 int32 int64  variants?
    @staticmethod
    def bv_const_integer(nbits, i):
        return yices.yices_bvconst_int64(nbits, long(i))

    @staticmethod
    def bv_const_zero(nbits):
        return yices.yices_bvconst_zero(nbits)

    @staticmethod
    def bv_const_one(nbits):
        return yices.yices_bvconst_zero(nbits)

    @staticmethod
    def bv_const_minus_one(nbits):
        return yices.yices_bvconst_zero(nbits)

    @staticmethod
    def bv_const_from_array(array_o_bits):
        return yices.yices_bvconst_from_array(len(array_o_bits), yices.make_int32_array(array_o_bits))

    @staticmethod
    def parse_bvbin(s):
        return yices.yices_parse_bvbin(s)

    @staticmethod
    def parse_bvhex(s):
        return yices.yices_parse_bvhex(s)

    @staticmethod
    def bvadd(lhs, rhs):
        return yices.yices_bvadd(lhs, rhs)

    @staticmethod
    def bvsub(lhs, rhs):
        return yices.yices_bvsub(lhs, rhs)

    @staticmethod
    def bvneg(t):
        return yices.yices_bvneg(t)

    @staticmethod
    def bvmul(lhs, rhs):
        return yices.yices_bvmul(lhs, rhs)

    @staticmethod
    def bvsquare(t):
        return yices.yices_bvsquare(t)

    @staticmethod
    def bvpower(t, d):
        return yices.yices_bvpower(t, d)

    @staticmethod
    def bvdiv(lhs, rhs):
        return yices.yices_bvdiv(lhs, rhs)

    @staticmethod
    def bvrem(lhs, rhs):
        return yices.yices_bvrem(lhs, rhs)

    @staticmethod
    def bvsrem(lhs, rhs):
        return yices.yices_bvsrem(lhs, rhs)

    @staticmethod
    def bvsmod(lhs, rhs):
        return yices.yices_bvsmod(lhs, rhs)

    @staticmethod
    def bvnot(t):
        return yices.yices_bvnot(t)

    @staticmethod
    def bvnand(lhs, rhs):
        return yices.yices_bvnand(lhs, rhs)

    @staticmethod
    def bvnor(lhs, rhs):
        return yices.yices_bvnor(lhs, rhs)

    @staticmethod
    def bvxnor(lhs, rhs):
        return yices.yices_bvxnor(lhs, rhs)

    @staticmethod
    def bvshl(lhs, rhs):
        return yices.yices_bvshl(lhs, rhs)

    @staticmethod
    def bvlshr(lhs, rhs):
        return yices.yices_bvlshr(lhs, rhs)

    @staticmethod
    def bvashr(lhs, rhs):
        return yices.yices_bvashr(lhs, rhs)

    @staticmethod
    def bvand(terms):
        return yices.yices_bvand(len(terms), yices.make_term_array(terms))

    @staticmethod
    def bvor(terms):
        return yices.yices_bvor(len(terms), yices.make_term_array(terms))

    @staticmethod
    def bvxor(terms):
        return yices.yices_bvxor(len(terms), yices.make_term_array(terms))

    @staticmethod
    def bvsum(terms):
        return yices.yices_bvsum(len(terms), yices.make_term_array(terms))

    @staticmethod
    def bvproduct(terms):
        return yices.yices_bvproduct(len(terms), yices.make_term_array(terms))

    @staticmethod
    def shift_left0(t, n):
        return yices.yices_shift_left0(t, n)

    @staticmethod
    def shift_left1(t, n):
        return yices.yices_shift_left1(t, n)

    @staticmethod
    def shift_right0(t, n):
        return yices.yices_shift_right0(t, n)

    @staticmethod
    def shift_right1(t, n):
        return yices.yices_shift_right1(t, n)

    @staticmethod
    def ashift_right(t, n):
        return yices.yices_ashift_right(t, n)

    @staticmethod
    def rotate_left(t, n):
        return yices.yices_rotate_left(t, n)

    @staticmethod
    def rotate_right(t, n):
        return yices.yices_rotate_right(t, n)

    @staticmethod
    def bvextract(t, i, j):
        return yices.yices_bvextract(t, i, j)

    @staticmethod
    def bvconcat(terms):
        return yices.yices_bvconcat(len(terms), yices.make_term_array(terms))

    @staticmethod
    def bvrepeat(t, n):
        return yices.yices_bvrepeat(t, n)

    @staticmethod
    def sign_extend(t, n):
        return yices.yices_sign_extend(t, n)

    @staticmethod
    def zero_extend(t, n):
        return yices.yices_zero_extend(t, n)

    @staticmethod
    def redand(t):
        return yices.yices_redand(t)

    @staticmethod
    def redor(t):
        return yices.yices_redor(t)

    @staticmethod
    def redcomp(lhs, rhs):
        return yices.yices_redcomp(lhs, rhs)

    @staticmethod
    def bvarray(terms):
        return yices.yices_bvarray(len(terms), yices.make_term_array(terms))

    @staticmethod
    def bitextract(t, i):
        return yices.yices_bitextract(t, i)

    # bitvector atoms

    @staticmethod
    def bveq_atom(lhs, rhs):
        return yices.yices_bveq_atom(lhs, rhs)

    @staticmethod
    def bvneq_atom(lhs, rhs):
        return yices.yices_bvneq_atom(lhs, rhs)

    @staticmethod
    def bvge_atom(lhs, rhs):
        return yices.yices_bvge_atom(lhs, rhs)

    @staticmethod
    def bvgt_atom(lhs, rhs):
        return yices.yices_bvgt_atom(lhs, rhs)

    @staticmethod
    def bvle_atom(lhs, rhs):
        return yices.yices_bvle_atom(lhs, rhs)

    @staticmethod
    def bvlt_atom(lhs, rhs):
        return yices.yices_bvlt_atom(lhs, rhs)

    @staticmethod
    def bvsge_atom(lhs, rhs):
        return yices.yices_bvsge_atom(lhs, rhs)

    @staticmethod
    def bvsgt_atom(lhs, rhs):
        return yices.yices_bvsgt_atom(lhs, rhs)

    @staticmethod
    def bvsle_atom(lhs, rhs):
        return yices.yices_bvsle_atom(lhs, rhs)

    @staticmethod
    def bvslt_atom(lhs, rhs):
        return yices.yices_bvslt_atom(lhs, rhs)

    # parsing

    # substitutions

    # term exploration

    # names

    @staticmethod
    def set_name(term, name):
        if name is None:
            return False
        errcode = yices.yices_set_term_name(term, name)
        if errcode == -1:
            sys.stderr.write('Terms.set_name({0}, {1}): yices_set_term_name failed {2}\n', term, name, yices.yices_error_string())
            return False
        return True

    @staticmethod
    def remove_name(name):
        if name is None:
            return False
        yices.yices_remove_term_name(name)
        return True


    @staticmethod
    def clear_name(term):
        errcode = yices.yices_clear_term_name(term)
        return True if errcode == 0 else False

    @staticmethod
    def get_name(term):
        name = yices.yices_get_term_name(term)
        if name == 0:
            return None
        return name

    @staticmethod
    def get_by_name(name):
        term = yices.yices_get_term_by_name(name)
        if term == -1:
            return None
        return term
