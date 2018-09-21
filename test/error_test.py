import unittest

from yices.Terms import Terms
from yices.Types import Types
from yices.Yices import Yices
from yices.YicesException import YicesException

class TestError(unittest.TestCase):

    def setUp(self):
        Yices.init()

    def tearDown(self):
        Yices.exit()

    def test_error(self):
        Yices.reset()

        # First with no error
        errcode = Yices.error_code()
        self.assertEqual(errcode, 0L)
        errep = Yices.error_report()
        self.assertEqual(errep.code, 0L)
        Yices.clear_error()
        errstr = Yices.error_string()
        self.assertEqual(errstr, 'no error')
        Yices.print_error(1)

        # Illegal - only scalar or uninterpreted types allowed
        bool_t = Types.bool_type()
        self.assertTrue(Types.is_bool(bool_t))
        with self.assertRaisesRegexp(YicesException, 'The function yices_constant failed because: invalid type in constant creation'):
            const1 = Terms.constant(bool_t, 0)
        Yices.clear_error()
        errpt = Yices.error_report()
        self.assertEqual(Yices.error_code(), 0)
        self.assertEqual(Yices.error_code(), errpt.code)
        errstr = Yices.error_string()
        self.assertEqual(errstr, 'no error')
        Yices.print_error(1)
        Yices.clear_error()
        self.assertEqual(Yices.error_code(), 0L)
