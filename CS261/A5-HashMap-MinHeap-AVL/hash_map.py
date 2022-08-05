# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: 5: Hash Maps, Min Heap, AVL Tree Implementation
# Description: Implementation of  hash map ADT consisting of internal storage of
# DA with chains of key/value pairs as LLs.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def bucket(self, key: str) -> object:
        """
        Helper method for returning bucket computed from hashing function. Takes
        key as parameter.
        """
        return self.hash_function(key) % self.capacity

    def clear(self) -> None:
        """
        Clears the content of the hash map without changing the hash map's underlying
        capacity, by instantiating new LL at each index.
        """
        for i in range(self.buckets.length()):
            self.buckets.set_at_index(i, LinkedList())

        self.size = 0

    def get(self, key: str) -> object:
        """
        Implementation for returning the value associated with a given key,
        returning None if they key isn't in the hashmap.
        """
        # compute hash
        index = self.bucket(key)

        for i in self.buckets.get_at_index(index):
            if key == i.key:
                return i.value
        return None

    def put(self, key: str, value: object) -> None:
        """
        Method for updating key/value pair in the hash, replacing the value if
        its key already exists in the hash map, adding the pair otherwise.
        """
        # compute hash and find bucket
        index = self.bucket(key)
        bucket = self.buckets.get_at_index(index)

        # get bucket that maps to this computed index and use contains LL
        # class method to see if key/val pair exist, adding it otherwise
        node = bucket.contains(key)

        if node:
            node.value = value
        else:
            bucket.insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        Removes the given key and associated value from the hashmap, or
        no action if the key doesn't exist.
        """
        bucket = self.buckets.get_at_index(self.bucket(key))

        if self.contains_key(key):
            bucket.remove(key)
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        Checks whether the key exists in the given hash map returning true
        if so.
        """
        bucket = self.buckets.get_at_index(self.bucket(key))

        if bucket.contains(key):
            return True
        return False

    def empty_buckets(self) -> int:
        """
        Iterates over the hashmap's buckets, counting and returning the frequency
        of empty buckets.
        """
        empty = 0
        for i in range(self.buckets.length()):
            if not self.buckets.get_at_index(i).length():
                empty += 1
        return empty

    def table_load(self) -> float:
        """
        Returns the load factor of the hash table using by dividing the table's
        size by capacity, a formula provided within the module notes for Hash maps.
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the internal capacity of the hash table, rehashing the table
        links. This method instantiates a new hash map in a temporary variable
        and inserts the existing key/value pairs, then sets the current hash
        table's buckets to the temp table's buckets, and updating capacity.
        """
        if new_capacity < 1:
            return

        temp = HashMap(new_capacity, self.hash_function)

        for i in range(self.capacity):
            for j in self.buckets.get_at_index(i):
                temp.put(j.key, j.value)

        self.capacity = new_capacity
        self.buckets = temp.buckets

    def get_keys(self) -> DynamicArray:
        """
        Iterates through hash table's buckets appending the keys stored in the hash
        map to a new DA and returning that DA.
        """
        output = DynamicArray()
        for i in range(self.buckets.length()):
            for j in self.buckets.get_at_index(i):
                output.append(j.key)

        return output


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    #
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    #

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
