# Author: Kevin Sekuj
# Date: 1/10/21
# Description:  Library simulator with a LibraryItem parent class, defining a
# library item object such as a book or a movie. Child classes such as Book, Movie
# and Album inherit from this superclass as well as have specific methods and data
# members for their own objects. The Library store allows Patron's defined in the
# Patron class to request, check out, and return library items, and fines 10 cents
# every day their returns are overdue.

class LibraryItem:
    """
    LibraryItem class which Book, Album, and Movie inherit from.
    """

    def __init__(self, library_item_id, title):
        """
        Initializing private data members of the LibraryItem class.
        """
        self._library_item_id = library_item_id
        self._title = title
        self._location = 'ON_SHELF'  # ON_SHELF, ON_HOLD_SHELF, CHECKED_OUT
        self._checked_out_by = None
        self._requested_by = None
        self._date_checked_out = None

    def get_location(self):
        """
        Get method for returning library item's current location.
        """
        return self._location

    def get_library_item_id(self):
        """
        Returns the ID of the library item.
        """
        return self._library_item_id

    def is_requested_by(self):
        """
        Returns who requested the library item
        """
        return self._requested_by

    def get_date_checked_out(self):
        """
        Returns the date that the library item was checked out.
        """
        return self._date_checked_out

    def set_borrower(self, name):
        """
        Set method for updating who checked out the library item.
        """
        self._checked_out_by = name

    def set_location(self, location_string):
        """
        Set method for updating the location of a recently checked out item.
        """
        self._location = location_string

    def set_date(self, date):
        """
        Sets the date checked out for a recently checked out item.
        """
        self._date_checked_out = date

    def set_requested_by(self, name):
        """
        Sets who requested the item, or sets it to None after someone checks it
        out successfully.
        """
        self._requested_by = name

    def reset_checkout_date(self):
        """
        Sets the checkout date of an item back to None after it's returned.
        """
        self._date_checked_out = None


class Book(LibraryItem):
    """
    Initializing the Book class, which inherits from LibraryItem.
    """

    def __init__(self, library_item_id, title, author):
        """
        Initializing data members of Book.
        """
        self._author = author
        self._check_out_length = 21
        super().__init__(library_item_id, title)

    def get_check_out_length(self):
        """
        Returns the number of days the book may be checked out for - 21 days.
        """
        return self._check_out_length

    def get_author(self):
        """
        Returns the author data member for the Book object.
        """
        return self._author


class Album(LibraryItem):
    """
    Initializing the Album class, which inherits from LibraryItem.
    """

    def __init__(self, library_item_id, title, artist):
        """
        Initializing data members of Album.
        """
        self._artist = artist
        self._check_out_length = 14
        super().__init__(library_item_id, title)

    def get_check_out_length(self):
        """
        Returns the number of days the album may be checked out for - 14 days.
        """
        return self._check_out_length

    def get_artist(self):
        """
        Returns the artist data member for the Album object.
        """
        return self._artist


class Movie(LibraryItem):
    """
    Initializing the Movie class, which inherits from LibraryItem.
    """

    def __init__(self, library_item_id, title, director):
        """
        Initializing data members of Movie.
        """
        self._director = director
        self._check_out_length = 7
        super().__init__(library_item_id, title)

    def get_check_out_length(self):
        """
        Returns the number of days the movie may be checked out for - 7 days.
        """
        return self._check_out_length

    def get_director(self):
        """
        Returns the artist data member for the Album object.
        """
        return self._director


class Patron:
    """
    Patron class representing patrons of the Library.
    """

    def __init__(self, patron_id, name):
        self._patron_id = patron_id
        self._patron_name = name
        self._checked_out_items = []
        self._fine_amount = 0  # late fee measured in dollars, may go negative

    def get_fine_amount(self):
        """
        Get method for returning the patron's fine amount.
        """
        return self._fine_amount

    def add_library_item(self, library_item):
        """
        Adds specified library item to patron's checked_out_items.
        """
        self._checked_out_items.append(library_item)

    def remove_library_item(self, library_item):
        """
        Removes specified library item from patron's checked_out_items.
        """
        for index in range(len(self._checked_out_items)):
            if library_item in self._checked_out_items:
                self._checked_out_items.remove(library_item)

    def amend_fine(self, amount):
        """
        Method for amending the patron's fine to the library. Positive arguments
        increase the fine amount, whereas negative ones decrease it. Possible to
        go negative.
        """
        self._fine_amount += amount

    def get_patron_id(self):
        """
        Returns the ID of the patron object.
        """
        return self._patron_id

    def get_patron_cart(self):
        """
        Method for returning the patron's library holdings collection.
        """
        return self._checked_out_items

    def check_patron_cart(self, library_item):
        """
        Method for checking the patron's collections for an item by passing
        a library item object. Used to return the proper library item.
        """
        for index in range(len(self._checked_out_items)):
            if library_item in self._checked_out_items:
                return True


class Library:
    """
    Library class where the library's collection and other data
    members are represented.
    """

    def __init__(self):
        """
        Initializing Library's private data members.
        """
        self._holdings = []  # collection of LibraryItems belonging to library
        self._members = []  # patrons who are members of the library
        self._current_date = 0  # current date as num of days since Library created

    def add_library_item(self, library_item):
        """
        Adds library item to Library's members collection.
        """
        self._holdings.append(library_item)

    def add_patron(self, patron):
        """
        Adds patron to Library's members collection.
        """
        self._members.append(patron)

    def get_date(self):
        """
        Returns the current date since the library class was created.
        """
        return self._current_date

    def get_library_item_from_id(self, item_id):
        """
        Returns the LibraryItem object corresponding to the item id passed,
        or None if the item isn't in the library's holdings.
        """
        for index in range(len(self._holdings)):
            if item_id == self._holdings[index].get_library_item_id():
                return self._holdings[index]
        else:
            return None

    def get_patron_from_id(self, patron_id):
        """
        Returns the Patron corresponding to the patron id passed,
        or None if that id doesn't correspond to a library member.
        """
        for index in range(len(self._members)):
            if patron_id == self._members[index].get_patron_id():
                return self._members[index]
        else:
            return None

    def check_out_library_item(self, patron_id, library_item_id):
        """
        Method for checking out the library item, taking in the patron's id
        and the id of the library item as parameters.
        """
        patron = self.get_patron_from_id(patron_id)
        item = self.get_library_item_from_id(library_item_id)

        if patron is None:
            return "patron not found"
        elif item is None:
            return "item not found"
        elif item.get_location() == 'CHECKED_OUT':
            return "item already checked out"
        elif item.get_location() == 'ON_HOLD_SHELF' and item.is_requested_by() != patron:
            return "item on hold by other patron"
        else:
            item.set_borrower(patron)
            item.set_date(self._current_date)
            item.set_requested_by(None)
            item.set_location('CHECKED_OUT')
            patron.add_library_item(item)
            return 'check out successful'

    def return_library_item(self, library_item_id):
        """
        Method for returning a library item, taking the library item's
        id as a parameter.
        """
        item = self.get_library_item_from_id(library_item_id)

        if item is None:
            return 'item not found'
        elif item.get_location() != 'CHECKED_OUT':
            return 'item already in library'
        else:
            for patron in self._members:
                if patron.check_patron_cart(item):
                    patron.remove_library_item(item)
                    item.reset_checkout_date()
                    item.set_borrower(None)

            if item.is_requested_by() is not None:
                item.set_location('ON_HOLD_SHELF')
            else:
                item.set_location('ON_SHELF')

            return 'return successful'

    def request_library_item(self, patron_id, library_item_id):
        """
        Method for requesting a library item in the library's holdings
        by passing a patron id and library item id.
        """
        patron = self.get_patron_from_id(patron_id)
        item = self.get_library_item_from_id(library_item_id)

        if patron is None:
            return "patron not found"
        elif item is None:
            return "item not found"
        elif item.is_requested_by() is not None:
            return 'item already on hold'
        else:
            item.set_requested_by(patron)
            if item.get_location() == 'ON_SHELF':
                item.set_location('ON_HOLD_SHELF')
            return 'request successful'

    def pay_fine(self, patron_id, amount):
        """
        Method to allow a patron to pay their fines to the library, taking
        their ID and the amount in dollars as parameters. Assumes user will
        not enter nonsensical numerical value (i.e, not paying negative dollars).
        """
        patron = self.get_patron_from_id(patron_id)
        if patron is None:
            return 'patron not found'
        else:
            patron.amend_fine(-amount)
            return 'payment successful'

    def increment_current_date(self):
        """
        Simulates the current date since the library class was created, in days.
        If a patron is overdue for returning a library item, they will have
        10 cents added to their fees each day they are overdue.
        """
        self._current_date += 1
        for patron in self._members:
            for item in patron.get_patron_cart():
                if (self.get_date() - item.get_date_checked_out()) > item.get_check_out_length():
                    patron.amend_fine(.1)
