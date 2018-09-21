import unittest

from yices.Terms import Terms
from yices.Types import Types
from yices.Yices import Yices

class TestTerms(unittest.TestCase):

    def setUp(self):
        Yices.init()

    def tearDown(self):
        Yices.exit()

    def test_terms(self):

        self.assertTrue(Yices.is_inited())

        true_ = Terms.true()
        false_ = Terms.false()
        bool_t = Types.bool_type()
        int_t = Types.int_type()
        unint_t = Types.new_uninterpreted_type()
        self.assertNotEqual(true_, false_)
        const1 = Terms.constant(unint_t, 0)
        const2 = Terms.new_uninterpreted_term(unint_t)
        bconst1 = Terms.new_uninterpreted_term(bool_t)
        iconst1 = Terms.new_uninterpreted_term(int_t)
        var1 = Terms.new_variable(unint_t)
        bvar1 = Terms.new_variable(bool_t)
        ivar1 = Terms.new_variable(int_t)
        ivar2 = Terms.new_variable(int_t)
        ivar3 = Terms.new_variable(int_t)
        ivar4 = Terms.new_variable(int_t)
        zero = Terms.zero()
        int1 = Terms.integer(13)
        int2 = Terms.integer(17)
        self.assertEqual(zero, Terms.integer(0))
        fun1_t = Types.new_function_type([int_t], bool_t)
        fun1 = Terms.new_variable(fun1_t)
        app1 = Terms.application(fun1, [int1])
        fun2_t = Types.new_function_type([int_t, int_t], bool_t)
        fun2 = Terms.new_variable(fun2_t)
        app2 = Terms.application(fun2, [int1, int1])
        fun3_t = Types.new_function_type([int_t, int_t, int_t], bool_t)
        fun3 = Terms.new_variable(fun3_t)
        app3 = Terms.application(fun3, [int1, int1, int1])
        tup3_t = Types.new_tuple_type([bool_t, int_t, unint_t])
        tupconst1 = Terms.new_variable(tup3_t)
        #ta4 = yapi.make_type_array([int_t, int_t, int_t, int_t])
        #int4 = yapi.make_type_array([int1, int2, iconst1, ivar1])
        #int4_2 = yapi.make_term_array([ivar1, ivar2, ivar3, ivar4])
        fun4_t = Types.new_function_type([int_t, int_t, int_t, int_t], bool_t)
        fun4 = Terms.new_variable(fun4_t)
        app4 = Terms.application(fun4,[int1, int2, iconst1, ivar1] )
        ite1 = Terms.ite(bconst1, int1, int2)
        eq1 = Terms.eq(int1, int1)
        neq1 = Terms.neq(int1, int1)
        not1 = Terms.negation(false_)
        #bool5 = yapi.make_term_array([false_, eq1, neq1, app4, false_])
        or1 = Terms.disjunction([false_, eq1, neq1, app4, false_])
        and1 = Terms.conjunction([false_, eq1, neq1, app4, false_])
        xor1 = Terms.xor([false_, eq1, neq1, app4, false_])
        or2 = Terms.disjunction([or1, and1])
        and2 = Terms.conjunction([or1, and1])
        xor2 = Terms.xor([or1, and1])
        or3 = Terms.disjunction([or1, and1, or2])
        and3 = Terms.conjunction([or1, and1, and2])
        xor3 = Terms.xor([or1, and1, xor2])
        iff1 = Terms.iff(and1, or1)
        implies1 = Terms.implies(and1, or1)
        tup1 = Terms.tuple([int1, int2, iconst1, ivar1])
        pair1 = Terms.tuple([eq1, xor2])
        triple1 = Terms.tuple([ite1, fun4, or3])
        select1 = Terms.select(2, tup1)
        select2 = Terms.select(2, tupconst1)
        tupup1 = Terms.tuple_update(tup1, 2, int2)
        update1 = Terms.update(fun1, [int1], false_)
        update2 = Terms.update(fun2, [int1, int1], false_)
        update3 = Terms.update(fun3, [int1, int1, int1], false_)
        update4 = Terms.update(fun4, [int1, int2, iconst1, ivar1], false_)
        distinct1 = Terms.distinct([int1, int2, iconst1, ivar1])
        var2 = Terms.new_variable(unint_t)
        vareq = Terms.eq(var1, var2)
        #vars2 = yapi.make_term_array([var1, var2])
        forall1 = Terms.forall([var1, var2], vareq)
        exists1 = Terms.exists([var1, var2], vareq)
        lambda1 = Terms.ylambda([var1, var2], vareq)
        zero = Terms.zero()
        int64_1 = Terms.integer(42)
        rat32_1 = Terms.rational(13, 7)
        rat64_1 = Terms.rational(-47, 111)
        rat1 = Terms.parse_rational('-3/117')
        float1 = Terms.parse_float('-3.117e-2')
        add1 = Terms.add(int1, int1)
        sub1 = Terms.sub(int1, zero)
        neg1 = Terms.neg(int1)
        self.assertEqual(Terms.neg(zero), zero)
        self.assertNotEqual(neg1, int1)
        mul1 = Terms.mul(int1, int1)
        square1 = Terms.square(int1)
        self.assertEqual(mul1, square1)
        power1 = Terms.power(int1, 4)
        sum1 = Terms.sum([int1, int2, iconst1, ivar1])
        product1 = Terms.product([int1, int2, iconst1, ivar1])
        product2 = Terms.product([ivar1, ivar2, ivar3, ivar4])
        div1 = Terms.division(int1, int1)
        idiv1 = Terms.idiv(int1, int1)
        imod1 = Terms.imod(int1, int1)
        divatom1 = Terms.divides_atom(int1, int1)
        intatom1 = Terms.is_int_atom(int1)
        abs1 = Terms.abs(neg1)
        self.assertEqual(abs1, int1)
        floor1 = Terms.floor(rat1)
        ceil1 = Terms.ceil(rat1)
        areqatom1 = Terms.arith_eq_atom(int1, zero)
        arneqatom1 = Terms.arith_neq_atom(int1, zero)
        argeqatom1 = Terms.arith_geq_atom(int1, zero)
        arleqatom1 = Terms.arith_leq_atom(int1, zero)
        argtatom1 = Terms.arith_gt_atom(int1, zero)
        arltatom1 = Terms.arith_lt_atom(int1, zero)
        areq0atom1 = Terms.arith_eq0_atom(int1)
        arneq0atom1 = Terms.arith_neq0_atom(int1)
        argeq0atom1 = Terms.arith_geq0_atom(int1)
        arleq0atom1 = Terms.arith_leq0_atom(int1)
        argt0atom1 = Terms.arith_gt0_atom(int1)
        arlt0atom1 = Terms.arith_lt0_atom(int1)
        bv_t = Types.bv_type(8)
        bvconstu32_1 = Terms.bvconst_integer(8, 42)
        bvconstu64_1 = Terms.bvconst_integer(8, 42)
        bvconst32_1 = Terms.bvconst_integer(8, 42)
        bvconst64_1 = Terms.bvconst_integer(8, 42)
        bvconstzero_1 = Terms.bvconst_zero(16)
        bvconstone_1 = Terms.bvconst_one(16)
        bvconstminusone_1 = Terms.bvconst_minus_one(32)
        bvvar1 = Terms.new_variable(bv_t)
        bvvar2 = Terms.new_variable(bv_t)
        bvvar3 = Terms.new_variable(bv_t)
        bvvar4 = Terms.new_variable(bv_t)
        bvbin1 = Terms.parse_bvbin('100101')
        bvhex1 = Terms.parse_bvhex('f0a1b3')
        bvadd1 = Terms.bvadd(bvbin1, bvbin1)
        bvsub1 = Terms.bvsub(bvbin1, bvbin1)
        bvneg1 = Terms.bvneg(bvbin1)
        bvmul1 = Terms.bvmul(bvbin1, bvbin1)
        bvsquare1 = Terms.bvsquare(bvbin1)
        bvpower1 = Terms.bvpower(bvbin1, 3)
        bvdiv1 = Terms.bvdiv(bvbin1, bvbin1)
        bvrem1 = Terms.bvrem(bvbin1, bvbin1)
        bvsdiv1 = Terms.bvsdiv(bvbin1, bvbin1)
        bvsrem1 = Terms.bvsrem(bvbin1, bvbin1)
        bvsmod1 = Terms.bvsmod(bvbin1, bvbin1)
        bvnot1 = Terms.bvnot(bvbin1)
        bvnand1 = Terms.bvnand(bvbin1, bvbin1)
        bvnor1 = Terms.bvnor(bvbin1, bvbin1)
        bvxnor1 = Terms.bvxnor(bvbin1, bvbin1)
        bvshl1 = Terms.bvshl(bvbin1, bvbin1)
        bvlshr1 = Terms.bvlshr(bvbin1, bvbin1)
        bvashr1 = Terms.bvashr(bvbin1, bvbin1)
        bvand1 = Terms.bvand([bvbin1, bvbin1, bvbin1, bvbin1])
        bvor1 = Terms.bvor([bvbin1, bvbin1, bvbin1, bvbin1])
        bvand2_1 = Terms.bvand([bvbin1, bvbin1])
        bvor2_1 = Terms.bvor([bvbin1, bvbin1])
        bvxor2_1 = Terms.bvxor([bvbin1, bvbin1])
        bvand3_1 = Terms.bvand([bvbin1, bvbin1, bvbin1])
        bvor3_1 = Terms.bvor([bvbin1, bvbin1, bvbin1])
        bvxor3_1 = Terms.bvxor([bvbin1, bvbin1, bvbin1])
        bvsum1 = Terms.bvsum([bvbin1, bvbin1, bvbin1, bvbin1])
        bvsum2 = Terms.bvsum([bvvar1, bvvar2, bvvar3, bvvar4])
        bvproduct1 = Terms.bvproduct([bvbin1, bvbin1, bvbin1, bvbin1])
        shleft0_1 = Terms.shift_left0(bvbin1, 5)
        shleft1_1 = Terms.shift_left1(bvbin1, 4)
        shright0_1 = Terms.shift_right0(bvbin1, 3)
        shright1_1 = Terms.shift_right1(bvbin1, 2)
        ashright_1 = Terms.ashift_right(bvbin1, 1)
        rotleft_1 = Terms.rotate_left(bvbin1, 6)
        rotright_1 = Terms.rotate_right(bvbin1, 5)
        bvextract1 = Terms.bvextract(bvbin1, 2, 4)
        bvconcat2_1 = Terms.bvconcat([bvbin1, bvbin1])
        bvconcat_1 = Terms.bvconcat([bvbin1, bvbin1, bvbin1, bvbin1])
        bvrepeat1 = Terms.bvrepeat(bvbin1, 8)
        signext1 = Terms.sign_extend(bvbin1, 3)
        zeroext1 = Terms.zero_extend(bvbin1, 4)
        redand1 = Terms.redand(bvbin1)
        redor1 = Terms.redor(bvbin1)
        redcomp1 = Terms.redcomp(bvbin1, bvbin1)
        bvarray1 = Terms.bvarray([true_, false_, true_, false_])
        bitextract1 = Terms.bitextract(bvbin1, 3)
        bveqatom1 = Terms.bveq_atom(bvbin1, bvbin1)
        bvneqatom1 = Terms.bvneq_atom(bvbin1, bvbin1)
        bvgeatom1 = Terms.bvge_atom(bvbin1, bvbin1)
        bvgtatom1 = Terms.bvgt_atom(bvbin1, bvbin1)
        bvleatom1 = Terms.bvle_atom(bvbin1, bvbin1)
        bvltatom1 = Terms.bvlt_atom(bvbin1, bvbin1)
        bvsgeatom1 = Terms.bvsge_atom(bvbin1, bvbin1)
        bvsgtatom1 = Terms.bvsgt_atom(bvbin1, bvbin1)
        bvsleatom1 = Terms.bvsle_atom(bvbin1, bvbin1)
        bvsltatom1 = Terms.bvslt_atom(bvbin1, bvbin1)
        ptype1 = Types.parse_type('int')
        self.assertEqual(ptype1, Types.int_type())
        pterm1 = Terms.parse_term('42')
        self.assertEqual(pterm1, Terms.integer(42))
        subst1 = Terms.subst([Terms.new_variable(ptype1),Terms.new_variable(ptype1)],
                             [Terms.integer(2), Terms.integer(3)],
                             Terms.integer(42))
        substarr1 = Terms.substs([Terms.new_variable(ptype1), Terms.new_variable(ptype1)],
                                 [Terms.integer(2), Terms.integer(3)],
                                 [Terms.integer(2), Terms.integer(3), Terms.integer(7)])
        settypename1 = Types.set_name(ptype1, 'I')
        self.assertTrue(settypename1)
        settermname1 = Terms.set_name(pterm1, 'answer')
        self.assertTrue(settermname1)
        gettype1 = Types.get_by_name('I')
        self.assertEqual(gettype1, ptype1)
        getterm1 = Terms.get_by_name('answer')
        self.assertEqual(getterm1, pterm1)
        gettypename1 = Types.get_name(ptype1)
        self.assertEqual(gettypename1, 'I')
        gettermname1 = Terms.get_name(pterm1)
        self.assertEqual(gettermname1, 'answer')
        Types.remove_name('I')
        Terms.remove_name('answer')
        Types.clear_name(ptype1)
        Terms.clear_name(pterm1)
        typeofterm1 = Terms.type_of_term(pterm1)
        self.assertEqual(typeofterm1, Types.int_type())
        self.assertEqual(Terms.is_bool(false_), 1)
        self.assertEqual(Terms.is_bool(pterm1), 0)
        self.assertEqual(Terms.is_int(false_), 0)
        self.assertEqual(Terms.is_int(pterm1), 1)
        self.assertEqual(Terms.is_real(false_), 0)
        self.assertEqual(Terms.is_real(pterm1), 0)
        self.assertEqual(Terms.is_arithmetic(false_), 0)
        self.assertEqual(Terms.is_arithmetic(pterm1), 1)
        self.assertEqual(Terms.is_bitvector(false_), 0)
        self.assertEqual(Terms.is_bitvector(bvbin1), 1)
        self.assertEqual(Terms.is_tuple(false_), 0)
        self.assertEqual(Terms.is_tuple(tup1), 1)
        self.assertEqual(Terms.is_function(false_), 0)
        self.assertEqual(Terms.is_function(fun1), 1)
        self.assertEqual(Terms.is_scalar(false_), 0)
        self.assertEqual(Terms.is_scalar(fun1), 0)
        self.assertEqual(Terms.bitsize(bvbin1), 6L)
        self.assertEqual(Terms.is_ground(false_), 1)
        self.assertEqual(Terms.is_ground(var1), 0)
        self.assertEqual(Terms.is_atomic(false_), 1)
        # or1 is atomic because it simplifies to true
        self.assertEqual(Terms.is_atomic(or1), 1)
        self.assertEqual(Terms.is_composite(false_), 0)
        self.assertEqual(Terms.is_composite(ite1), 1)
        self.assertEqual(Terms.is_composite(tup1), 1)
        self.assertEqual(Terms.is_projection(false_), 0)
        # Select1 simplifies
        self.assertEqual(Terms.is_projection(select1), 0)
        self.assertEqual(Terms.is_projection(select2), 1)
        self.assertEqual(Terms.is_sum(ite1), 0)
        self.assertEqual(Terms.is_sum(sum1), 1)
        self.assertEqual(Terms.is_bvsum(select1), 0)
        # bvsum1 simplifies since the terms are all numbers
        self.assertEqual(Terms.is_bvsum(bvsum1), 0)
        self.assertEqual(Terms.is_bvsum(bvsum2), 1)
        self.assertEqual(Terms.is_product(ite1), 0)
        self.assertEqual(Terms.is_product(product1), 0)
        self.assertEqual(Terms.is_product(product2), 1)
        self.assertEqual(Terms.constructor(true_), 0L)
        self.assertEqual(Terms.constructor(int1), 1L)
        self.assertEqual(Terms.constructor(bvconst32_1), 2L)
        self.assertEqual(Terms.num_children(bvconst32_1), 0L)
        self.assertEqual(Terms.num_children(select2), 1L)
        self.assertEqual(Terms.num_children(tup1), 4L)
        self.assertEqual(Terms.child(tup1, 2), iconst1)
        projarg1 = Terms.proj_arg(select2)
        self.assertEqual(Terms.proj_index(select2), 2)
        self.assertEqual(Terms.proj_arg(select2), tupconst1)
