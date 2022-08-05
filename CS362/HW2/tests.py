# Author: Kevin Sekuj
# Date: 07/11/21
# Description: 362 HW2: Improving coverage - applying white box testing
# techniques to achieve 100% branch and condition coverage.

import unittest
from contrived_func import contrived_func


class TestContrivedCase(unittest.TestCase):
    """
    Testing suite for the contrived case function, as an example of white box
    testing to achieve full coverage.
    """
    def test1(self):
        """
        Trigger C1 with first condition: if val < 150
        """
        self.assertTrue(contrived_func(149))

    def test2(self):
        """
        Trigger C2 with second condition: return False if val == 6
        """
        self.assertFalse(contrived_func(6))

    def test3(self):
        """
        Trigger C4, C7, C8, when val != 6
        """
        self.assertTrue(contrived_func(7))

    def test4(self):
        """
        Trigger C2, C5, C11 - val/2 not < 24
        """
        self.assertTrue(contrived_func(50))

    def test5(self):
        """
        Trigger C12 - val > 75 or val / 8 < 10 and val**val % 5 == 0
        """
        self.assertFalse(contrived_func(53))

    def test6(self):
        """
        Trigger C3 - val not less than 151 in first conditional
        """
        self.assertFalse(contrived_func(151))

    def test7(self):
        """
        Trigger C9
        """
        self.assertFalse(contrived_func(1000))


if __name__ == '__main__':
    unittest.main()
