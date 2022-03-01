import unittest
import functions

class FunctionsTestCase(unittest.TestCase):

    def test_check_dates_if_true(self):
       test_check_dates = functions.check_dates('2021-11-11', '2021-11-20')
       self.assertTrue(test_check_dates, True)

    def test_check_dates_if_before(self):
       test_check_dates = functions.check_dates('2022-11-11', '2021-11-20')
       self.assertRaises()

