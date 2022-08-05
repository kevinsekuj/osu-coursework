# Author: Kevin Sekuj
# Date: 1/7/21
# Description: Unit test coverage for assignment 2's online store program. Checks the
# functionality of the program through a successful purchase, as well as other key
# functionalities of the store such as product searching and checking member premium
# status.


import unittest
from Store import Product, Customer, Store


class Tests(unittest.TestCase):

    def test_purchase_item(self):
        """
        Tests successful purchase of an item by a store customer.
        """
        store = Store()
        prod = Product('123', 'Zowie FK2', 'Ambidextrous mouse', 60, 10)
        cust = Customer('Filip', 'KUB', False)
        store.add_product(prod)
        store.add_member(cust)
        store.add_product_to_member_cart('123', 'KUB')
        store.check_out_member('KUB')

    def test_check_price(self):
        """
        Ensures correct calculation of cart price by purchase_item method.
        """
        store = Store()
        prod = Product('100', 'iPhone XR', 'Last gen mobile device from Apple', 400, 5)
        cust = Customer('Kevin', 'KEV', False)
        store.add_product(prod)
        store.add_member(cust)
        store.add_product_to_member_cart('100', 'KEV')
        store_bill = store.check_out_member('KEV')
        self.assertEqual(428, store_bill)

    def test_member_status(self):
        """
        Tests functionality of customer premium membership boolean.
        """
        cust = Customer('Eren', 'YGR', True)
        self.assertIs(Customer.is_premium_member(cust), True)

    def test_product_search(self):
        """
        Tests functionality of product_search and its ability to return a lexicographically
        ordered list.
        """
        store = Store()
        prod1 = Product('105', 'Rat poison', 'Kills all types of rats and rodents', 5, 25)
        prod2 = Product('598', 'Rattata card', 'Pokemons most famous rodent', 2, 10)
        prod3 = Product('982', 'NYC subway rodent portrait', 'A staple of the Big Apple', 20, 3)
        store.add_product(prod1)
        store.add_product(prod2)
        store.add_product(prod3)
        store.product_search('rodent')
        self.assertListEqual(store.product_search('rodent'), ['105', '598', '982'])

    def test_bad_product_id(self):
        """
        Tests whether a get product from ID request on a product that does not
        exist in the store inventory handles correctly (returns None).
        """
        store = Store()
        prod = Product('50', 'ramen', '400% your daily sodium intake', 1, 100)
        store.add_product(prod)
        self.assertIsNone(store.get_product_from_id('51'))


if __name__ == '__main__':
    unittest.main()
