# Author: Kevin Sekuj
# Date: 07/05/21
# Description: 362 HW1: Writing Black Box Tests - test suite for a credit card
# validation function that is passed a sequence of digits as a string, using
# the black box testing technique.

import unittest
from credit_card_validator import credit_card_validator


class TestValidCreditCard(unittest.TestCase):
    """
    Unittest suite for credit card validation (Visa, American Express,
    Mastercard).
    """

    # Verifies if a credit card with an invalid input (empty string) returns
    # False. Picked using Error Guessing.
    def test_number_exists(self):
        self.assertFalse(credit_card_validator(''))

    # Verifies if a credit card with an invalid input (integer) returns False.
    # Picked using Error Guessing.
    def test_card_input_int(self):
        self.assertFalse(credit_card_validator(4278975412433021))

    # Verifies if a credit card with an invalid input (None type) returns
    # False. Picked using Error Guessing.
    def test_card_input_null(self):
        self.assertFalse(credit_card_validator(None))

    # Verifies that a Visa with an invalid checksum will return False.
    # Picked using Partition Testing.
    def test_invalid_checksum_visa(self):
        self.assertFalse(credit_card_validator('4278975412433022'))

    # Verifies that an AmExpress with an invalid checksum will return False.
    # Picked using Partition Testing.
    def test_invalid_checksum_american_express(self):
        self.assertFalse(credit_card_validator('370024283041574'))

    # Verifies that a Mastercard with an invalid checksum will return False.
    # Picked using Partition Testing.
    def test_invalid_checksum_mastercard(self):
        self.assertFalse(credit_card_validator('5574729517233581'))

    # Verifies if a Visa card with valid prefix, checksum, and length returns
    # True. Picked using Partition Testing.
    def test_valid_prefix_checksum_visa(self):
        self.assertTrue(credit_card_validator('4278975412433021'))

    # Verifies if an American Express card with valid prefix (34), checksum,
    # and length returns True. Picked using Boundary Testing.
    def test_valid_prefix_checksum_american_express(self):
        self.assertTrue(credit_card_validator('349799180478205'))

    # Verifies if an American Express card with valid prefix (37), checksum,
    # and length returns True. Picked using Boundary Testing.
    def test_valid_prefix_checksum_american_express2(self):
        self.assertTrue(credit_card_validator('370024283041574'))

    # Verifies if a Mastercard card with valid prefix (51), checksum,
    # and length returns True. Picked using Boundary Testing.
    def test_valid_prefix_checksum_mastercard(self):
        self.assertTrue(credit_card_validator('5174725888287167'))

    # Verifies if a Mastercard card with valid prefix (52), checksum,
    # and length returns True. Picked using Partition Testing.
    def test_valid_prefix_checksum_mastercard2(self):
        self.assertTrue(credit_card_validator('5274729517233583'))

    # Verifies if a Mastercard card with valid prefix (53), checksum,
    # and length returns True. Picked using Partition Testing.
    def test_valid_prefix_checksum_mastercard3(self):
        self.assertTrue(credit_card_validator('5372071724882162'))

    # Verifies if a Mastercard card with valid prefix (54), checksum,
    # and length returns True. Picked using Partition Testing.
    def test_valid_prefix_checksum_mastercard4(self):
        self.assertTrue(credit_card_validator('5474729517233581'))

    # Verifies if a Mastercard card with valid prefix (55), checksum,
    # and length returns True. Picked using Boundary Testing.
    def test_valid_prefix_checksum_mastercard5(self):
        self.assertTrue(credit_card_validator('5574729471184522'))

    # Verifies if a Mastercard card with valid prefix (2222), checksum,
    # and length returns True. Picked using Boundary Testing.
    def test_valid_prefix_checksum_mastercard6(self):
        self.assertTrue(credit_card_validator('2221729517233584'))

    # Verifies if a Mastercard card with valid prefix (2270), checksum,
    # and length returns True. Picked using Boundary Testing.
    def test_valid_prefix_checksum_mastercard7(self):
        self.assertTrue(credit_card_validator('2720729517233580'))

    # Verifies a Visa with an invalid length returns False. Picked using
    # Partition Testing.
    def test_card_length_min_visa(self):
        self.assertFalse(credit_card_validator('427897541'))

    # Verifies a AmExpress with an invalid length returns False. Picked
    # using Partition Testing.
    def test_card_length_min_american_express(self):
        self.assertFalse(credit_card_validator('370024283'))

    # Verifies a Mastercard with an invalid length returns False. Picked
    # using Partition Testing.
    def test_card_length_min_mastercard(self):
        self.assertFalse(credit_card_validator('557472951'))

    # Verifies a Visa with an invalid length (max) returns False. Picked
    # using Partition Testing.
    def test_card_length_max_visa(self):
        self.assertFalse(credit_card_validator('4278975411243302111'))

    # Verifies a AmExpress (max) with an invalid length returns False.
    # Picked using Partition Testing.
    def test_card_length_max_american_express(self):
        self.assertFalse(credit_card_validator('3700242813041574444'))

    # Verifies a Mastercard with an invalid length (max) returns False.
    # Picked using Partition Testing.
    def test_card_length_max_mastercard(self):
        self.assertFalse(credit_card_validator('5574729511723358000'))

    # Verifies that a valid visa with a length of 17 characters returns
    # False. Picked using Partition Testing.
    def test_card_length_max_visa_valid_prefix_checksum(self):
        self.assertFalse(credit_card_validator('41360908064818000'))

    # Verifies that a valid AmExpress with a length of 16 characters
    # returns False. Picked using Partition Testing.
    def test_card_length_max_american_express_valid_prefix_checksum(self):
        self.assertFalse(credit_card_validator('3496763230320754'))

    # Verifies that a valid MasterCard with a length of 17 characters
    # returns False. Picked using Partition Testing.
    def test_card_length_max_mastercard_valid_prefix_checksum(self):
        self.assertFalse(credit_card_validator('55742966768265885'))

    # Verifies that a valid Visa with a length of 15 characters returns
    # False. Picked using Partition Testing.
    def test_card_length_min_visa_valid_prefix_checksum(self):
        self.assertTrue(credit_card_validator('456152627252230'))

    # Verifies that a valid AmExpress with a length of 14 characters
    # returns False. Picked using Partition Testing.
    def test_card_length_min_american_express_valid_prefix_checksum(self):
        self.assertTrue(credit_card_validator('34934338227549'))

    # Verifies that a valid MasterCard with a length of 15 characters
    # returns False. Picked using Partition Testing.
    def test_card_length_min_mastercard_valid_prefix_checksum(self):
        self.assertTrue(credit_card_validator('537207106151445'))


if __name__ == '__main__':
    unittest.main()
