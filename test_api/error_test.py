import unittest

import yices_api as yapi

#from yices_api import YicesAPIException


class TestError(unittest.TestCase):

    def setUp(self):
        yapi.yices_init()

    def tearDown(self):
        yapi.yices_exit()

    def test_error(self):
        yapi.yices_reset()

        # First with no error
        errcode = yapi.yices_error_code()
        self.assertEqual(errcode, 0)
        errep = yapi.yices_error_report()
        self.assertEqual(errep.code, 0)
        yapi.yices_clear_error()
        errstr = yapi.yices_error_string()
        self.assertEqual(errstr, 'no error')
        yapi.yices_print_error_fd(1)

        # Illegal - only scalar or uninterpreted types allowed
        bool_t = yapi.yices_bool_type()
        self.assertTrue(yapi.yices_type_is_bool(bool_t))
        #iam: 9/19/2018 with self.assertRaisesRegexp(YicesAPIException, 'invalid type in constant creation'):
        #iam: 9/19/2018    const1 = yices_constant(bool_t, 0)
        const1 = yapi.yices_constant(bool_t, 0)
        error_string = yapi.yices_error_string()
        self.assertEqual(const1, -1)
        self.assertEqual(error_string, 'invalid type in constant creation')
        yapi.yices_clear_error()
        errpt = yapi.yices_error_report()
        self.assertEqual(yapi.yices_error_code(), 0)
        self.assertEqual(yapi.yices_error_code(), errpt.code)
        errstr = yapi.yices_error_string()
        self.assertEqual(errstr, 'no error')
        yapi.yices_print_error_fd(1)
        yapi.yices_clear_error()
        self.assertEqual(yapi.yices_error_code(), 0)
