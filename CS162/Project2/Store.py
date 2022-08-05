# Author: Kevin Sekuj
# Date: 1/7/21
# Description: Online store simulator with Product, Customer, and Store classes.
# Products and Customers are added to the Store's inventory and membership data
# members. Customers may search for products by their ID or by a key word, and
# purchase them. If they're premium members, they receive free shipping, otherwise,
# they receive a 7% shipping charge.

class InvalidCheckoutError(Exception):
    """
    Exception class handling the InvalidCheckOutError for the product's check-out
    method.
    """
    pass


class Product:
    """
    Product object representing the online store's product catalogue, displaying
    products with private data parameters including product id, title, description,
    price, and quantity/availability.
    """

    def __init__(self, ID, title, description, price, quantity_available):
        """
        Initializing the private data members of the product class.
        """
        self._id = ID
        self._title = title
        self._desc = description
        self._price = price
        self._quantity_available = quantity_available

    def get_product_id(self):
        """
        Get method for returning product id.
        """
        return self._id

    def get_title(self):
        """
        Get method for returning product title.
        """
        return self._title

    def get_description(self):
        """
        Get method for returning product description.
        """
        return self._desc

    def get_price(self):
        """
        Get method for returning product price.
        """
        return self._price

    def get_quantity_available(self):
        """
        Get method for returning availability of the product.
        """
        return self._quantity_available

    def decrease_quantity(self):
        """
        Set method for reducing quantity of the product by 1.
        """
        self._quantity_available -= 1


class Customer:
    """
    Customer object representing customers of the online store by their name and
    account ID. Customers must be members to make purchases, and premium members
    receive free shipping.
    """

    def __init__(self, name, ID, premium_member):
        """
        Initializing customer object parameters - customer name, member ID,
        premium status, and a data structure representing their
        current cart, which holds their product ID codes.
        """
        self._name = name
        self._customer_id = ID
        self._premium_member = premium_member
        self._cart = []

    def get_name(self):
        """
        Get method for returning the customer's name.
        """
        return self._name

    def get_customer_id(self):
        """
        Get method for returning the customer's member ID.
        """
        return self._customer_id

    def is_premium_member(self):
        """
        Get method for returning whether or not the customer is a premium
        member at the online store.
        """
        return self._premium_member

    def get_cart(self):
        """
        Get method for returning the customer's product cart.
        """
        return self._cart

    def add_product_to_cart(self, product):
        """
        Method for adding a product ID from the Product class to the customer's
        cart.
        """
        self._cart.append(product)

    def empty_cart(self):
        """
        Method for emptying the customer's cart.
        """
        self._cart = []


class Store:
    """
    Store object representing the store, containing products in its inventory
    and a number of customers as the store' members.
    """

    def __init__(self):
        """
        Initializing the Store object's private data members, such as its product
        inventory.
        """
        self._store_inventory = []
        self._store_membership = []

    def add_product(self, product):
        """
        Method for adding a Product object to the store inventory, via list.
        """
        self._store_inventory.append(product)

    def add_member(self, member):
        """
        Method for adding a Customer object to the store, via list.
        """
        self._store_membership.append(member)

    def get_product_from_id(self, product_id):
        """
        Get method for returning Product object when a product ID is passed.
        The function indexes through the elements in the store_inventory list
        checking each Product instance for the matching id, returning none
        if the id is not found.
        """
        for index in range(len(self._store_inventory)):
            if product_id == self._store_inventory[index].get_product_id():
                return self._store_inventory[index]
        else:
            return None

    def get_member_from_id(self, member_id):
        """
        Get method for returning Customer object when a member ID is passed.
        The function indexes through the elements in the store_membership list
        checking each Customer instance for the matching member id, returning none
        if the id is not found.
        """
        for index in range(len(self._store_membership)):
            if member_id == self._store_membership[index].get_customer_id():
                return self._store_membership[index]
        else:
            return None

    def product_search(self, query):
        """
        Method for searching for a product by its title or description. The method
        uses a for loop to index through the store inventory list containing the
        product objects. If the user's query is found within the title or description
        of the object, then the product's ID is added to a list, sorted, and returned.
        If no search query is found, it returns an empty list.
        """
        id_list = []

        for index in range(len(self._store_inventory)):

            if query.lower() in self._store_inventory[index].get_title().lower() or \
                    query.lower() in self._store_inventory[index].get_description().lower():
                id_list.append(self._store_inventory[index].get_product_id())
            else:
                id_list = []
                return id_list
        return sorted(id_list)

    def add_product_to_member_cart(self, product_id, customer_id):
        """
        Method for adding a product to a member's cart, taking the product ID
        and the customer's ID as parameters, checking if they're both valid and
        whether the item is available. If so, it is added to the customer's cart.
        """

        if self.get_product_from_id(product_id) is None:
            return 'product ID not found'
        elif self.get_member_from_id(customer_id) is None:
            return 'member ID not found'
        elif self.get_product_from_id(product_id).get_quantity_available() < 1:
            return 'product out of stock'
        else:
            self.get_member_from_id(customer_id).add_product_to_cart(product_id)
            return 'product added to cart'

    def check_out_member(self, customer_id):
        """
        Check out method which takes customer ID as a parameter. If the ID doesn't
        exist, it raises an InvalidCheckError. Otherwise, it calls the helper method
        purchase_item which calculates the total cost of cart and returns it.
        """
        if self.get_member_from_id(customer_id) is None:
            raise InvalidCheckoutError
        else:
            return self.purchase_item(customer_id)

    def purchase_item(self, customer_id):
        """
        Helper method for calculating customer cart price. The function indexes
        through their cart, casting the Product instances to the item variable.
        It checks if the item is in stock, adding it to the total price and decreasing
        quantity by 1 if so. If the product goes out of stock during calculation, it's
        not added to their total price.
        """
        total = 0
        for index in range(len(self.get_member_from_id(customer_id).get_cart())):
            item = self.get_product_from_id(self.get_member_from_id(customer_id).get_cart()[index])
            if item.get_quantity_available() > 0:
                total += item.get_price()
                item.decrease_quantity()
            else:
                continue

        if self.get_member_from_id(customer_id).is_premium_member():
            self.get_member_from_id(customer_id).empty_cart()
            return total
        else:
            self.get_member_from_id(customer_id).empty_cart()
            return total + (total * .07)  # 7% shipping fee for non-premium


def main():
    """
    Main function for try/except testing of the program. First code block contains
    non-functioning code to test the InvalidCheckoutError being raised, while
    the second code block is functioning.
    """
    # error
    try:
        p1 = Product("100", "Rat poison", "Kills all types of rats and rodents", 1, 5)
        c1 = Customer("Kevin", "AAA", False)
        my_store = Store()
        my_store.add_product(p1)
        my_store.add_member(c1)
        my_store.add_product_to_member_cart('100', 'AAA')
        #  inducing error via wrong member ID at checkout
        my_store.check_out_member('THIS_ID_IS_FAKE')
    except InvalidCheckoutError:
        print('Check-out failed! Your member ID may be invalid.')
    # functioning
    try:
        p1 = Product("100", "Rat poison", "Kills all types of rats and rodents", 1, 5)
        c2 = Customer("Bob", "XYZ", False)
        my_store = Store()
        my_store.add_product(p1)
        my_store.add_member(c2)
        my_store.add_product_to_member_cart('100', 'XYZ')
        my_store.check_out_member('XYZ')
    except InvalidCheckoutError:
        print('Check-out failed! Your member ID may be invalid.')


if __name__ == '__main__':
    main()
