# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Part 2 - Implement Bag ADT
# Description: Implementing a Bag ADT with add, remove, count, clear and equal
# methods using the DynamicArray class implemented in part 1 as the underlying
# data storage.

from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self.da.length()) + " elements. ["
        out += ', '.join([str(self.da.get_at_index(_))
                          for _ in range(self.da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS CLASS IN ANY WAY
        """
        return self.da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Adds a new element to the bag in O(1) amortized runtime, using the DA's
        append method.
        """
        self.da.append(value)

    def remove(self, value: object) -> bool:
        """
        Bag remove implementation by iterating through the internal data structure
        to find the matching value, then removing it using DA's remove_at_index
        method if found, returning True, or False otherwise.
        """
        for i in range(self.size()):
            if self.da[i] == value:
                self.da.remove_at_index(i)
                return True
        return False

    def count(self, value: object) -> int:
        """
        Returns the number of elements in the bag that match the provided
        value.
        """
        count = 0
        for i in range(self.size()):
            if self.da[i] == value:
                count += 1
        return count

    def clear(self) -> None:
        """
        Clears the contents of the bags implemented in O(1) runtime complexity,
        by setting it to a new DynamicArray with no elements.
        """
        self.da = DynamicArray(None)

    def equal(self, second_bag: object) -> bool:
        """
        Method for returning a bool depending on the equality of the current
        bag instance and another bag passed to the method. If both bags are empty
        or if they're of different lengths, they are immediately equal or unequal,
        respectively. Otherwise, each element in the current bag can be passed
        to the count method, ditto for the second bag, and if they share all the
        same elements with the same counts, then they're equal.
        """

        # if both bags are empty
        if self.size() == 0 and second_bag.size() == 0:
            return True

        # if sizes aren't equal, immediately false
        if self.size() != second_bag.size():
            return False

        # both bags must have the same count of each element
        for i in range(self.size()):
            if self.count(self.da[i]) != \
                    second_bag.count(self.da[i]):
                return False
        return True

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)


    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)


    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))


    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)


    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30])
    print(bag1.equal(bag2))
