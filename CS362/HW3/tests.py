# Author: Kevin Sekuj
# Date: 07/19/21
# Description: 362 HW3: Random testing hands on - applying random testing
# techniques, practice writing random tests, and diagnose the cause of
# undiscovered bugs.

import random
import unittest
from credit_card_validator import credit_card_validator


class TestCreditCard(unittest.TestCase):
    """
    Testing suite for the credit card validation, using random testing.
    """

    def test_generate_valid_cc(self):
        """
        Generates generalized valid credit card numbers by randomly choosing
        a prefix and length for either Visa, Mastercard, or American Express.
        Because the length and prefix is chosen at random, this method will
        also produce invalid credit cards, along with cards of valid prefix
        and/or checksums.
        """
        card_lengths = [15, 16]
        card_prefixes = [4, 51, 52, 53, 54, 2221, 2720, 34, 37]
        for _ in range(50000):
            length = random.choice(card_lengths)
            prefix = random.choice(card_prefixes)

            card_no = list(str(prefix))
            while len(card_no) != length:
                card_no.append(str(random.randint(0, 9)))

            card_num = "".join(card_no)
            credit_card_validator(card_num)

    def test_generate_random_cc(self):
        """
        Generates credit cards with totally random digits within the expected
        lengths of either 15 or 16 total numbers.
        """
        card_lengths = [15, 16]
        for _ in range(50000):
            length = random.choice(card_lengths)
            prefix = random.randint(0, 9)

            card_no = list(str(prefix))
            while len(card_no) != length:
                card_no.append(str(random.randint(0, 9)))

            card_num = "".join(card_no)
            credit_card_validator(card_num)

    def test_generate_visa(self):
        """
        Generates Visa cards of random integers besides the Visa prefix 4.
        """
        for _ in range(100000):
            length = 16
            prefix = 4

            card_no = list(str(prefix))
            while len(card_no) != length:
                card_no.append(str(random.randint(0, 9)))

            card_num = "".join(card_no)
            credit_card_validator(card_num)

    def test_generate_mastercard(self):
        """
        Generates Mastercard cards of random integers besides the Mastercard
        prefixes 2221 and 2720, which were chosen as they represent the
        lower and upper bounds of the Mastercard prefix range.
        """
        card_prefixes = [2221, 2720]
        for _ in range(100000):
            length = 16
            prefix = random.choice(card_prefixes)

            card_no = list(str(prefix))
            while len(card_no) != length:
                card_no.append(str(random.randint(0, 9)))

            card_num = "".join(card_no)
            credit_card_validator(card_num)

    def test_generate_am_express(self):
        """
        Generates American Express cards by randomly choosing either of the
        valid prefixes for that card, 34 or 37.
        """
        card_prefixes = [34, 37]
        for _ in range(100000):
            length = 15
            prefix = random.choice(card_prefixes)

            card_no = list(str(prefix))
            while len(card_no) != length:
                card_no.append(str(random.randint(0, 9)))

            card_num = "".join(card_no)
            credit_card_validator(card_num)


if __name__ == '__main__':
    unittest.main()
