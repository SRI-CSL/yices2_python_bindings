import unittest



from yices.Types import Types
from yices.Yices import Yices

# pylint: disable=W0612
# pylint: disable=R0914

class TestTypes(unittest.TestCase):

    def setUp(self):
        Yices.init()

    def tearDown(self):
        Yices.exit()

    def test_types(self):
        bool_t = Types.bool_type()
        int_t = Types.int_type()
        self.assertNotEqual(bool_t, int_t)
        real_t = Types.real_type()
        self.assertNotEqual(real_t, bool_t)
        self.assertNotEqual(real_t, int_t)
        bv_t = Types.bv_type(8)
        scal_t = Types.new_scalar_type(12)
        unint_t = Types.new_uninterpreted_type()
        tup1_t = Types.new_tuple_type([bool_t])
        tup2_t = Types.new_tuple_type([int_t, real_t])
        tup3_t = Types.new_tuple_type([bv_t, scal_t, unint_t])
        tup4_t = Types.new_tuple_type([bool_t, tup1_t, tup2_t, tup3_t])
        fun1_t = Types.new_function_type([int_t], bool_t)
        fun2_t = Types.new_function_type([real_t, bv_t], scal_t)
        fun3_t = Types.new_function_type([tup1_t, tup2_t, tup3_t], fun1_t)
        fun4_t = Types.new_function_type([bool_t, tup1_t, tup2_t, tup3_t], fun3_t)

        self.assertTrue(Types.is_bool(bool_t))
        self.assertFalse(Types.is_bool(int_t))
        self.assertTrue(Types.is_int(int_t))
        self.assertTrue(Types.is_real(real_t))
        self.assertTrue(Types.is_arithmetic(real_t))
        self.assertTrue(Types.is_bitvector(bv_t))
        self.assertTrue(Types.is_tuple(tup1_t))
        self.assertTrue(Types.is_function(fun4_t))
        self.assertTrue(Types.is_scalar(scal_t))
        self.assertTrue(Types.is_uninterpreted(unint_t))
        self.assertTrue(Types.is_subtype(int_t, real_t))
        self.assertFalse(Types.is_subtype(real_t, int_t))
        self.assertEqual(Types.bvtype_size(bv_t), 8)
        self.assertEqual(Types.scalar_type_card(scal_t), 12)
        self.assertEqual(Types.num_children(tup3_t), 3)
        self.assertEqual(Types.child(tup3_t, 1), scal_t)
        type_v = Types.children(tup4_t)
        self.assertEqual(len(type_v), 4)
        self.assertEqual(type_v[0], bool_t)
        self.assertEqual(type_v[1], tup1_t)
        self.assertEqual(type_v[2], tup2_t)
        self.assertEqual(type_v[3], tup3_t)
