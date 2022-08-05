# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Part 5 - Queue ADT
# Description: Queue ADT implementation using MaxStack ADT as the underlying
# internal data storage.

from max_stack_da import *


class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class Queue:
    def __init__(self):
        """
        Init new Queue based on two stacks
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.s1 = MaxStack()  # use as main storage
        self.s2 = MaxStack()  # use as temp storage

    def __str__(self) -> str:
        """
        Return content of queue in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "QUEUE: " + str(self.s1.size()) + " elements. "
        out += str(self.s1)
        return out

    def is_empty(self) -> bool:
        """
        Return True if queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.s1.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.s1.size()

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Enqueue method implementation for adding a new value to the end
        of the queue, in O(1) runtime.
        """
        self.s1.push(value)

    def dequeue(self) -> object:
        """
        Dequeue method, removing and returning the value at the beginning of
        the queue. The elements of the original stack are popped and pushed into
        a temporary stack, except for the first element. The first element is
        then stored and popped. Lastly, the elements of the temporary stack
        are pushed back onto the original stack, which will create a queue with
        the original beginning value removed.
        """
        if self.is_empty():
            raise QueueException

        # store elements > first index in temp stack
        for i in range(self.s1.size()-1):
            self.s2.push(self.s1.pop())

        # store and pop first element, push values back onto original stack
        val = self.s1.pop()
        for i in range(self.s2.size()):
            self.s1.push(self.s2.pop())

        return val

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print('\n# enqueue example 1')
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)


    print('\n# dequeue example 1')
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for i in range(6):
        try:
            print(q.dequeue(), q)
        except Exception as e:
            print("No elements in queue", type(e))
