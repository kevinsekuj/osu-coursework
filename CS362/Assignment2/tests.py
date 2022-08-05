# Author: Kevin Sekuj
# Date: 07/24/21
# Description: CS362 A2: TDD Hands On - utilize and apply TDD techniques to
# implement a check_pwd function which checks input strings against a defined
# specification.

from check_pwd import check_pwd
import unittest


class TestPWD(unittest.TestCase):
    def test_empty_input(self):
        self.assertFalse(check_pwd(''))

    def test_min_length(self):
        self.assertFalse(check_pwd('1234567'))

    def test_max_length(self):
        self.assertFalse(check_pwd('123456789123456789123'))

    def test_check_lowercase(self):
        self.assertFalse(check_pwd('INVALIDPASSWORD'))

    def test_check_uppercase(self):
        self.assertFalse(check_pwd('invalidpassword'))

    def test_contains_digit(self):
        self.assertFalse(check_pwd('Passwithnodigits'))

    def test_contains_special_char(self):
        self.assertFalse(check_pwd('P4sswithnospecial'))


if __name__ == '__main__':
    unittest.main()
