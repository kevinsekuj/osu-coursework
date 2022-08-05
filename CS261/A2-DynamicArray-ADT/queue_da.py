# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Part 3 - Queue ADT
# Description: Implementing a Queue ADT using the Dynamic Array as its underlying
# data structure, specifically implementing the enqueue and dequeue methods.

from dynamic_array import *


class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Queue:
    def __init__(self):
        """
        Init new queue based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.da = DynamicArray()

    def __str__(self):
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "QUEUE: " + str(self.da.length()) + " elements. ["
        out += ', '.join([str(self.da[i]) for i in range(self.da.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.da.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.da.length()

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Enqueue values to the end of the queue at O(1) runtime by inserting
        directly at the last index of the queue's internal data storage.
        """
        self.da.insert_at_index(self.size(), value)

    def dequeue(self) -> object:
        """
        Removing and returning the value at the beginning of the queue in O(N)
        runtime by storing, removing, and returning the value at the first index
        of the internal DA.
        """
        if self.is_empty():
            raise QueueException

        return_obj = self.da[0]
        self.da.remove_at_index(0)

        return return_obj


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# enqueue example 1")
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)


    print("\n# dequeue example 1")
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for i in range(6):
        try:
            print(q.dequeue())
        except Exception as e:
            print("No elements in queue", type(e))
