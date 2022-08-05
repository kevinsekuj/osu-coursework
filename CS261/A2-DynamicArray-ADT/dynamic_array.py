# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Assignment 2 - Dynamic Array, Bag, Stack, Queue
# Description: DynamicArray class consisting of a Dynamic Array object with a
# StaticArray as associated internal storage. This class contains numerous
# array methods such as appending values to the array, resizing the array,
# merging two DA's, and so forth.

from static_array import *


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.size = 0
        self.capacity = 4
        self.first = 0  # do not use / change this value
        self.data = StaticArray(self.capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self.size) + "/" + str(self.capacity) + ' ['
        out += ', '.join([str(self.data[_]) for _ in range(self.size)])
        return out + ']'

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        return self.data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self.size:
            raise DynamicArrayException
        self.data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.size

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resizes the DA's data member by creating a new StaticArray of the given
        capacity and appending the old values to it.
        """
        # exit if invalid capacity
        if new_capacity <= 0 or new_capacity < self.size:
            return

        # create new array SA with new capacity
        new_arr = StaticArray(new_capacity)

        # append values from original array
        for i in range(self.size):
            new_arr[i] = self.data[i]

        # update data members
        self.data = new_arr
        self.capacity = new_capacity

    def append(self, value: object) -> None:
        """
        Appends values to the end of the DA, checking first if internal storage
        (data SA) is full and doubling the capacity if so by resizing the SA.
        Then, it inserts into the DA's storage using size as an index, which
        tracks the number of (non-None) elements in the array. Size is then
        updated to reflect the element added.
        """

        # if DA's internal storage is full, double capacity of data
        if self.size == self.capacity:
            self.resize(self.capacity * 2)

        # append value to end of the DA by inserting into SA using size as index
        self.data[self.size] = value
        self.size += 1  # update array size

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserting a value at a specific index by shifting over all elements
        up to that index to the right, iterating in reverse. If there is
        no space to do so, the array capacity is doubled.
        """

        # raise exception err if invalid index
        if index < 0 or index > self.size:
            raise DynamicArrayException

        # resize internal storage if necessary
        if self.size == self.capacity:
            self.resize(self.capacity * 2)

        # shift elements over one space to the right
        for i in range(self.size, index, -1):
            self.data[i] = self.data[i - 1]

        # insert value at specified index
        self.data[index] = value
        self.size += 1

    def remove_at_index(self, index: int) -> None:
        """
        Removing values at the specified index by shifting all elements leftwards
        and decrementing size, and resizing the array if necessary.
        """

        # raise exception err if invalid index
        if index < 0 or index > self.size - 1:
            raise DynamicArrayException

        # capacity check
        if self.capacity > 10:
            self.capacity_check()

        # if removing last element
        if index == self.size - 1:
            self.data[index] = None
            self.size -= 1
            return

        # remove element
        self.data[index] = None

        # shift elements after deletion to the left to fill spots
        for i in range(index + 1, self.size):
            self.data[i - 1] = self.data[i]

        self.size -= 1

    def capacity_check(self) -> None:
        """
        Reducing capacity to twice the number of current elements if the current
        number of elements is less than 1/4th of its current capacity.
        """
        if self.size < (self.capacity / 4):
            self.capacity = self.size * 2

        if self.capacity < 10:
            self.capacity = 10

    def slice(self, start_index: int, size: int) -> object:
        """
        Returns a new DynamicArray object with a slice of original array elements
        starting from start_index up to the given size. The index and size are
        first validated with validate_slice, and then the elements are sliced.
        """

        self.validate_slice(start_index, size)

        # return empty DynamicArray instance if size is 0
        if size == 0:
            dynamic_arr = DynamicArray()
            return dynamic_arr

        # add values to new SA
        slice_arr = StaticArray(size)
        j = 0
        for i in range(start_index, self.size):
            if size == 0:
                break
            slice_arr[j] = self.data[i]
            j += 1
            size -= 1

        # create new DA instance and append values
        dynamic_arr = DynamicArray()
        for i in range(slice_arr.size()):
            dynamic_arr.append(slice_arr[i])

        return dynamic_arr

    def validate_slice(self, start_index, size) -> None:
        """
        Helper method for validating the starting index and size passed to
        the slice method. If the index is out of bounds or the index and
        the size are out of bounds, it will raise an exception error.
        """
        # validate starting index
        if start_index < 0 or start_index > self.size - 1:
            raise DynamicArrayException

        # validate size
        if size < 0 or size > self.size:
            raise DynamicArrayException

        # validate that size doesn't move out of bounds
        if start_index + size > self.size:
            raise DynamicArrayException

    def merge(self, second_da: object) -> None:
        """
        Merge implementation using the DA's append method to append a second DA
        to the current DA instance.
        """

        if second_da.size == 0:
            return

        for i in range(second_da.data.size()):
            if second_da.data[i] is not None:
                self.append(second_da.data[i])

    def map(self, map_func) -> object:
        """
        Map implementation where values in the original dynamic array's associated
        data member are mapped to a new static array and appended to a new dynamic
        array. The elements are derived from a given map_func.
        """
        static_arr = StaticArray(self.size)

        i = 0
        while i < self.size:
            static_arr[i] = map_func(self.data[i])
            i += 1

        # create new DA instance and append values
        dynamic_arr = DynamicArray()
        for i in range(static_arr.size()):
            dynamic_arr.append(static_arr[i])

        return dynamic_arr

    def filter(self, filter_func) -> object:
        """
        Filter method implementation. A static array is created with
        filter_helper containing the amount of elements which have
        been filtered. Then, the returned SA from the helper method
        is iterated through, filling in filtered elements from the
        original array. Finally these values are appended to a dynamic array
        and returned as a new DA instance.
        """

        # return empty DynamicArray if internal data is empty
        if self.size == 0:
            dynamic_arr = DynamicArray()
            return dynamic_arr

        # if helper returns bool instead of obj then there are no valid elements
        static_arr = self.filter_helper(filter_func)
        if type(static_arr) is bool:
            dynamic_arr = DynamicArray()
            return dynamic_arr

        # iterate through data filling in SA with filtered elements
        i = 0
        j = 0
        while i < self.size:
            if filter_func(self.data[i]):
                static_arr[j] = self.data[i]
                j += 1
            i += 1

        # create new DA instance and append values
        dynamic_arr = DynamicArray()
        for i in range(static_arr.size()):
            dynamic_arr.append(static_arr[i])

        return dynamic_arr

    def filter_helper(self, filter_func) -> StaticArray or bool:
        """
        Helper method which counts the amount of filtered elements in the
        original DynamicArray and returns a SA with a size of that count.
        """

        # get count of valid elements for SA creation
        count = 0
        for i in range(self.data.size()):
            if self.data[i] is not None and filter_func(self.data[i]):
                count += 1

        #  if no valid filters
        if count == 0:
            return False

        return StaticArray(count)

    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Reduce implementation. If an initializer is given, the reduce function
        passes in the initializer as the first parameter to the reduce_func and
        iterates through the original array. Otherwise, the first value of the
        array acts as the initializer and the array begins from index 1.
        """

        start = 1
        if initializer:
            result = initializer
            start = 0
        else:
            result = self.data[0]

        for i in range(start, self.size):
            result = reduce_func(result, self.data[i])

        return result


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":
    print("\n# resize - example 1")
    da = DynamicArray()
    print(da.size, da.capacity, da.data)
    da.resize(8)
    print(da.size, da.capacity, da.data)
    da.resize(2)
    print(da.size, da.capacity, da.data)
    da.resize(0)
    print(da.size, da.capacity, da.data)

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    print(da.size, da.capacity, da.data)
    da.append(1)
    print(da.size, da.capacity, da.data)
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.size)
    print(da.capacity)

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.size, da.capacity)
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.size, da.capacity)
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.size, da.capacity)
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.size, da.capacity)
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.size, da.capacity)
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.size, da.capacity)

    for i in range(14):
        print("Before remove_at_index(): ", da.size, da.capacity, end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.size, da.capacity)

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
