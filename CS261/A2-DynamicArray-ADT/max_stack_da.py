# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Part 4 - MaxStack ADT implementation
# Description: Implementing a MaxStack ADT class by using a DynamicArray
# as the underlying data storage.

from dynamic_array import *


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class MaxStack:
    def __init__(self):
        """
        Init new stack based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.da_val = DynamicArray()
        self.da_max = DynamicArray()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "MAX STACK: " + str(self.da_val.length()) + " elements. ["
        out += ', '.join([str(self.da_val[i]) for i in range(self.da_val.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.da_val.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.da_val.length()

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Adding an element to the top of the stack using internal DA's
        insert method. The max element DA is also updated with each
        new element.
        """
        # if stack is empty, push value onto stack and max stack
        if self.is_empty():
            self.da_val.append(value)
            self.da_max.append(value)

        # else insert onto the stack
        else:
            self.da_val.append(value)

            # if new max, push onto max stack, else duplicate old max
            if value > self.da_max.get_at_index(self.size()-2):
                self.da_max.append(value)
            else:
                # size-2 as size of max has yet to to be updated with append
                duplicate = self.da_max.get_at_index(self.size()-2)
                self.da_max.append(duplicate)

    def pop(self) -> object:
        """
        Removing an element from the top of the stack and returning its value.
        """
        if self.is_empty():
            raise StackException

        # save element at top of stack to return, and remove it
        popped = self.da_val.get_at_index(self.size()-1)
        self.da_val.remove_at_index(self.size()-1)

        # update max stack
        self.da_max.remove_at_index(self.size())

        return popped

    def top(self) -> object:
        """
        Return the value at the top of the stack, raising a StackException
        error if the stack is empty.
        """
        if self.is_empty():
            raise StackException

        return self.da_val.get_at_index(self.size()-1)

    def get_max(self) -> object:
        """
        Returning the current value of the max stack, in other words the max of
        the stack in O(1) time. The max stack is updated with each push/pop onto
        the value stack. If a new value pushed onto the stack is not a new max,
        then the old max is duplicated. Then, when non-max values are popped from
        the value stack, the max stack will still contain the running maximum.
        """
        if self.is_empty():
            raise StackException

        return self.da_max.get_at_index(self.size()-1)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = MaxStack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)


    print("\n# pop example 1")
    s = MaxStack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))


    print("\n# top example 1")
    s = MaxStack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)


    print('\n# get_max example 1')
    s = MaxStack()
    for value in [1, -20, 15, 21, 21, 40, 50]:
        print(s, ' ', end='')
        try:
            print(s.get_max())
        except Exception as e:
            print(type(e))
        s.push(value)
    while not s.is_empty():
        print(s.size(), end='')
        print(' Pop value:', s.pop(), ' get_max after: ', end='')
        try:
            print(s.get_max())
        except Exception as e:
            print(type(e))
