# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Assignment 3 - Implementation of LL, ADTs using LL's and Binary Search
# Description: Implementation of a singly linked list ADT.


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class SLNode:
    """
    Singly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.value = value


class LinkedList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with front and back sentinels
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.head = SLNode(None)
        self.tail = SLNode(None)
        self.head.next = self.tail

        # populate SLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        if self.head.next != self.tail:
            cur = self.head.next.next
            out = out + str(self.head.next.value)
            while cur != self.tail:
                out = out + ' -> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        cur = self.head
        while cur.next != self.tail:
            cur = cur.next
            length += 1
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.head.next == self.tail

    # ------------------------------------------------------------------ #

    def add_front(self, value: object) -> None:
        """
        Adding a new node to the beginning of the Linked List. First, the SLNode
        instance is created with the value passed to the method. Then, next.node
        is pointed to head.next, which would be the tail sentinel in the first
        addition. Finally, the head node's next is pointed to the new node.
        """

        # create SLNode object with value
        node = SLNode(value)

        # link node to self.head.next (tail in first add) and point head to new node
        node.next = self.head.next
        self.head.next = node

    def add_back(self, value: object) -> None:
        """
        Add back method for adding a new SLNode object to the end
        of the LL, before the tail sentinel. If the linked list consists of
        just two sentinels, it's added after the head sentinel. Otherwise, it
        calls add_back_helper to traverse the list and find the node whose next
        is the tail sentinel, and inserts the new node at that position.
        """

        # create SLNode object with value
        node = SLNode(value)

        # if the LL consists of just sentinel nodes
        if self.head.next == self.tail:
            self.head.next = node
            node.next = self.tail

            return

        self.add_back_helper(node, self.head)

    def add_back_helper(self, node: SLNode, cur: SLNode) -> None:
        """
        Helper method for adding to the end of the LinkedList. If the current
        node's next is the tail sentinel, its next is pointed to the new node
        and the new node's next points to the tail sentinel. Else, it continues
        traversing the LL.
        """
        if cur.next == self.tail:
            cur.next = node
            node.next = self.tail
        else:
            self.add_back_helper(node, cur.next)

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserting at the given index. If the index is out of range, an
        exception is raised. If the index is 0, add_front is called with the
        value passed to insert a new node at that index. Otherwise, insert_helper
        is called to traverse down the LL until the index is found.
        """

        # raise SLL exception if index out of range
        if index < 0 or index > self.length():
            raise SLLException

        # insert at front if index is 0
        if index == 0:
            return self.add_front(value)

        # create new node
        node = SLNode(value)

        self.insert_helper(self.head, node, index)

    def insert_helper(self, cur: SLNode, node: SLNode, index: int) -> None:
        """
        Takes the current head node, new node, and index and traverses the list
        until the index is found, by decrementing the index on each node it moves
        through. If the index is 0, the position has been found, and an insertion
        takes places.
        """

        # point new node to current node's next, and point current node to new node
        if index == 0:
            node.next = cur.next
            cur.next = node
        else:
            self.insert_helper(cur.next, node, index - 1)

    def remove_front(self) -> None:
        """
        Point front sentinel's next to the original front node's next. If
        the LL is empty, raise exception.
        """
        if self.is_empty():
            raise SLLException

        front = self.head.next
        self.head.next = front.next

    def remove_back(self) -> None:
        """
        Find the node preceding the tail sentinel and remove it from the LL.
        """
        if self.is_empty():
            raise SLLException

        self.remove_back_helper(self.head, self.head.next)

    def remove_back_helper(self, cur: SLNode, next: SLNode) -> None:
        """
        Helper method which traverses the LL until the node preceding the tail
        sentinel is found and removed.
        """
        if next.next == self.tail:
            cur.next = self.tail
        else:
            self.remove_back_helper(cur.next, next.next)

    def remove_at_index(self, index: int) -> None:
        """
        Remove a node at the given index by using the passed index parameter as
        a counter. The LL is traversed decrementing index until it equals 0, at
        which point the proper node has been reached to be removed.
        """

        # raise SLL exception if index out of range
        if index < 0 or index > self.length() - 1:
            raise SLLException

        # remove at front if index is 0
        if index == 0:
            return self.remove_front()

        self.remove_index_helper(self.head, index)

    def remove_index_helper(self, cur, index):
        """
        The LL is traversed decrementing index until it equals 0. When index
        is 0, the current node's next attribute is pointed to next.next.
        """
        if index == 0:
            cur.next = cur.next.next
        else:
            self.remove_index_helper(cur.next, index - 1)

    def get_front(self) -> object:
        """
        Returns the value from the first node in the list not including the front
        sentinel.
        """
        if self.is_empty():
            raise SLLException

        return self.head.next.value

    def get_back(self) -> object:
        """
        Returns the value from the last node in the list not including the tail
        sentinel.
        """
        if self.is_empty():
            raise SLLException

        return self.get_last(self.head.next)

    def get_last(self, cur: SLNode) -> object:
        """
        Helper method for traversing the linked list to return the last node's
        value.
        """
        if cur.next == self.tail:
            return cur.value

        return self.get_last(cur.next)

    def remove(self, value: object) -> bool:
        """
        Remove implementation, traversing the linked list for the node matching
        the value passed to the method and removing it.
        """

        # if LL is empty
        if self.is_empty():
            return False

        # if LL consists of just sentinel head and tail
        if self.head.next is None:
            return False

        # case where value is first node
        if self.head.next.value == value:
            self.head.next = self.head.next.next
            return True

        if self.remove_helper(self.head.next, self.head.next.next, value):
            return True

        return False

    def remove_helper(self, prev: SLNode, cur: SLNode, val: object) -> bool:
        """
        Helper method for checking if the current node is equal to the value
        passed. If so, the previous node is also tracked, and is made to point
        to the current node's next node.
        """
        if cur.value is None:
            return False

        if cur.value == val:
            prev.next = cur.next
            return True

        return self.remove_helper(prev.next, cur.next, val)

    def count(self, value: object) -> int:
        """
        Counts the number of nodes in the linked list which have a value equal
        to the value passed to the method.
        # """
        # return 0 if LL is empty or consists of only sentinels
        if self.is_empty():
            return 0

        if self.head.next == self.tail:
            return 0

        # pass counter, node, value
        count = 0
        return self.count_helper(self.head.next, count, value)

    def count_helper(self, cur: SLNode, count: int, val: object) -> int:
        """
        Checks if current node equals value, incrementing counter if so. Returns
        counter when LL is traversed.
        """
        if cur.value == val:
            count += 1

        if cur.next == self.tail:
            return count

        return self.count_helper(cur.next, count, val)

    def slice(self, start_index: int, size: int) -> object:
        """
        Recursive slice implementation for SLL. If the current LL is empty, or
        the provided parameters are invalid, such as being out of range or having
        a size greater than the size of the current LL, an SLL exception is raised.

        Otherwise, a starting index param is created along wth provided start
        index and end index which is calculated. These parameters along with
        the first node after the sentinel are passed to slice_helper which calls
        add_back on the nodes within that index until the index range is exhausted.
        """

        # if LL is empty
        if self.is_empty():
            raise SLLException

        # if starting or ending indices are out of range
        if start_index < 0 or start_index > self.length() - 1:
            raise SLLException

        # if size/starting index parameters are invalid for LL size
        if size + start_index > self.length():
            raise SLLException

        # ditto
        if size < 0:
            raise SLLException

        # index variable to keep track of the amount of nodes to be added
        index = 0

        # ending index
        end = (start_index + size) - 1

        # call recursive helper with params and new LL instance
        return self.slice_helper(start_index, end, self.head.next, LinkedList(), index)

    def slice_helper(self, start: int, end: int, node: SLNode, sliced_list, index: int) -> object:
        """
        Recursive helper method which calls add_back to fill a sliced array with
        SLL nodes.
        """
        # return when SL indices exhausted
        if index == end+1:
            return sliced_list

        # else insert sliced nodes whilst index within range
        if start <= index <= end:
            sliced_list.add_back(node.value)

        return self.slice_helper(start, end, node.next, sliced_list, index+1)


if __name__ == '__main__':
    pass

    print('\n# add_front example 1')
    list = LinkedList()
    print(list)
    list.add_front('A')
    list.add_front('B')
    list.add_front('C')
    print(list)

    print('\n# add_back example 1')
    list = LinkedList()
    print(list)
    list.add_back('C')
    list.add_back('B')
    list.add_back('A')
    print(list)

    print('\n# insert_at_index example 1')
    list = LinkedList()
    test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    for index, value in test_cases:
        print('Insert of', value, 'at', index, ': ', end='')
        try:
            list.insert_at_index(index, value)
            print(list)
        except Exception as e:
            print(type(e))


    print('\n# remove_front example 1')
    list = LinkedList([1, 2])
    print(list)
    for i in range(3):
        try:
            list.remove_front()
            print('Successful removal', list)
        except Exception as e:
            print(type(e))



    print('\n# remove_back example 1')
    list = LinkedList()
    try:
        list.remove_back()
    except Exception as e:
        print(type(e))
    list.add_front('Z')
    list.remove_back()
    print(list)
    list.add_front('Y')
    list.add_back('Z')
    list.add_front('X')
    print(list)
    list.remove_back()
    print(list)

    print('\n# remove_at_index example 1')
    list = LinkedList([1, 2, 3, 4, 5, 6])
    print(list)
    for index in [0, 0, 0, 2, 2, -2]:
        print('Removed at index:', index, ': ', end='')
        try:
            list.remove_at_index(index)
            print(list)
        except Exception as e:
            print(type(e))
    print(list)


    print('\n# get_front example 1')
    list = LinkedList(['A', 'B'])
    print(list.get_front())
    print(list.get_front())
    list.remove_front()
    print(list.get_front())
    list.remove_back()
    try:
        print(list.get_front())
    except Exception as e:
        print(type(e))

    print('\n# get_back example 1')
    list = LinkedList([1, 2, 3])
    list.add_back(4)
    print(list.get_back())
    list.remove_back()
    print(list)
    print(list.get_back())

    print('\n# remove example 1')
    list = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(list)
    for value in [7, 3, 3, 3, 3]:
        print(list.remove(value), list.length(), list)

    print('\n# count example 1')
    list = LinkedList([1, 2, 3, 1, 2, 2])
    print(list, list.count(1), list.count(2), list.count(3), list.count(4))

    print('\n# slice example 1')
    list = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = list.slice(1, 3)
    print(list, ll_slice, sep="\n")
    ll_slice.remove_at_index(0)
    print(list, ll_slice, sep="\n")

    print('\n# slice example 2')
    list = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", list)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Slice", index, "/", size, end="")
        try:
            print(" --- OK: ", list.slice(index, size))
        except:
            print(" --- exception occurred.")
