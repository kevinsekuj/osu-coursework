# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Assignment 3 - Implementation of LL, ADTs using LL's and Binary Search
# Description: Implementation of a circular doubly linked list ADT.


class CDLLException(Exception):
    """
    Custom exception class to be used by Circular Doubly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DLNode:
    """
    Doubly Linked List Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        self.next = None
        self.prev = None
        self.value = value


class CircularList:
    def __init__(self, start_list=None):
        """
        Initializes a new linked list with sentinel
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.sentinel = DLNode(None)
        self.sentinel.next = self.sentinel
        self.sentinel.prev = self.sentinel

        # populate CDLL with initial values (if provided)
        # before using this feature, implement add_back() method
        if start_list is not None:
            for value in start_list:
                self.add_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'CDLL ['
        if self.sentinel.next != self.sentinel:
            cur = self.sentinel.next.next
            out = out + str(self.sentinel.next.value)
            while cur != self.sentinel:
                out = out + ' <-> ' + str(cur.value)
                cur = cur.next
        out = out + ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        This can also be used as troubleshooting method. This method works
        by independently measuring length during forward and backward
        traverse of the list and return the length if results agree or error
        code of -1 or -2 if thr measurements are different.
        Return values:
        >= 0 - length of the list
        -1 - list likely has an infinite loop (forward or backward)
        -2 - list has some other kind of problem
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        # length of the list measured traversing forward
        count_forward = 0
        cur = self.sentinel.next
        while cur != self.sentinel and count_forward < 101_000:
            count_forward += 1
            cur = cur.next

        # length of the list measured traversing backwards
        count_backward = 0
        cur = self.sentinel.prev
        while cur != self.sentinel and count_backward < 101_000:
            count_backward += 1
            cur = cur.prev

        # if any of the result is > 100,000 -> list has a loop
        if count_forward > 100_000 or count_backward > 100_000:
            return -1

        # if counters have different values -> there is some other problem
        return count_forward if count_forward == count_backward else -2

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.sentinel.next == self.sentinel

    # ------------------------------------------------------------------ #

    def add_front(self, value: object) -> None:
        """
        Node insertion at the front of a circular doubly linked list.
        """
        # new DL node object
        node = DLNode(value)

        # point inserted node to previous front node, point prev to sentinel
        node.next = self.sentinel.next
        node.prev = self.sentinel

        # point previous head node's prev member to the new head node
        # finally point sentinel to new head node
        node.next.prev = node
        self.sentinel.next = node

    def add_back(self, value: object) -> None:
        """
        Node insertion at the end of a circular doubly linked list.
        """
        node = DLNode(value)

        # point inserted node's next to sentinel to maintain circular LL
        # sentinel.prev points to old end node, point to inserted node's prev
        node.next = self.sentinel
        node.prev = self.sentinel.prev

        # point 2nd to last end node to newly inserted end node
        # and point sentinel prev attribute to new end node
        node.prev.next = node
        self.sentinel.prev = node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Inserting at a specified index in the CDLL. If the index is out of range,
        the method raises a CDLL exception. Otherwise, it indexes through the CDLL
        starting at the sentinel until it reaches the specified index. Then, the
        the new node's prev and next point to the previous and next nodes at that
        index, and those nodes are made to point to the newly inserted node.
        """

        # raise CDLL exception if index out of range
        if index < 0 or index > self.length():
            raise CDLLException

        cur = self.sentinel
        node = DLNode(value)

        for i in range(index):
            cur = cur.next

        # point new node's prev to node at index we're inserting at, then point
        # its next attrib to the node in front of it (cur.next)
        node.prev = cur
        node.next = cur.next

        # point cur node to inserted node and node in front of inserted note
        # back towards inserted node
        cur.next = node
        cur.next.next.prev = node

    def remove_front(self) -> None:
        """
        Remove the front node of the CDLL by pointing sentinel to the 2nd front
        node, and pointing that front node's prev attribute to the sentinel.
        """
        if self.is_empty():
            raise CDLLException

        new_front = self.sentinel.next.next

        self.sentinel.next = new_front
        new_front.prev = self.sentinel

    def remove_back(self) -> None:
        """
        Remove the back node of the CDLL by pointing sentinel to the 2nd to
        last node, and pointing the 2nd to last node's next attrib to sentinel.
        """
        if self.is_empty():
            raise CDLLException

        new_back = self.sentinel.prev.prev

        new_back.next = self.sentinel
        self.sentinel.prev = new_back

    def remove_at_index(self, index: int) -> None:
        """
        Remove a node at the given index iteratively. The LL is traversed
        up to index+1 (as it is N-1 inclusive) and removes the specified
        node.
        """
        # raise CDLL exception if index out of range
        if index < 0 or index > self.length() - 1:
            raise CDLLException

        # iterate to specified node
        cur = self.sentinel
        for i in range(index + 1):
            cur = cur.next

        # swap pointers
        cur.next.prev = cur.prev
        cur.prev.next = cur.next

    def get_front(self) -> object:
        """
        Return the node at the front of the CDLL (excl. sentinel node).
        """
        if self.is_empty():
            raise CDLLException

        return self.sentinel.next.value

    def get_back(self) -> object:
        """
        Return node at the end of the CDLL.
        """
        if self.is_empty():
            raise CDLLException

        return self.sentinel.prev.value

    def remove(self, value: object) -> bool:
        """
        Remove implementation, taking a value as a parameter and removing the first
        node which matches the provided value object.
        """
        # if LL is empty
        if self.is_empty():
            return False

        # iterate through CDLL until match is found, else return false
        cur = self.sentinel
        for i in range(self.length() + 1):
            if cur.value == value:
                cur.prev.next = cur.next
                cur.next.prev = cur.prev
                return True

            cur = cur.next

        return False

    def count(self, value: object) -> int:
        """
        Checks if current node equals value, incrementing counter if so. Returns
        counter when LL is traversed.
        """
        # return 0 if LL is empty or consists of only sentinel
        if self.is_empty():
            return 0

        count = 0
        cur = self.sentinel.next

        for i in range(self.length()):
            if cur.value == value:
                count += 1
            cur = cur.next

        return count

    def swap_pairs(self, index1: int, index2: int) -> None:
        """
        Swap pair implementation for CDLL. Takes two indices as parameters and
        iterates to those nodes, swapping them by pointing them to each node's
        neighbors. If the nodes are next to each other, the method calls swap_adjacent
        which handles that swap.
        """

        # if index out of bounds or CDLL is empty
        if (index1 < 0 or index1 > self.length() - 1) or \
                (index2 < 0 or index2 > self.length() - 1) or \
                self.is_empty():
            raise CDLLException

        # init pairs to be swapped
        cur1 = self.sentinel.next
        cur2 = self.sentinel.next

        # iterate through CDLL (except sentinel) to get node pairs
        for i in range(index1):
            cur1 = cur1.next

        for i in range(index2):
            cur2 = cur2.next

        # keep reference to cur2 adjacent nodes to link to cur1
        # else we'll be in an infinite loop
        cur2_prev = cur2.prev
        cur2_next = cur2.next

        # call helper for the case where the swapped nodes are adjacent
        if (index1 - index2 == 1) or (index2 - index1 == 1):
            return self.swap_adjacent(cur1, cur2, index1, index2)

        # point cur1's adjacent nodes to cur2
        cur1.prev.next = cur2
        cur1.next.prev = cur2

        # point cur2 to to cur1's adjacent nodes
        cur2.prev = cur1.prev
        cur2.next = cur1.next

        # point cur2's adjacent nodes to cur1
        cur2_prev.next = cur1
        cur2_next.prev = cur1

        # point cur1 to cur2's adjacent nodes
        cur1.prev = cur2_prev
        cur1.next = cur2_next

    def swap_adjacent(self, cur1: DLNode, cur2: DLNode, index1: int, index2: int) -> None:
        """
        Helper method for handling adjacent node swap. If the second index is
        greater than the first index, than the 2nd node is "in front" of the
        first node, otherwise, the method enters the second conditional.
        """
        # reference to cur1.next and cur2.next for swapping node pointers
        cur1_next = cur1.next
        cur2_next = cur2.next

        # if cur2 is "in front" of cur1
        if index2 > index1:

            # point cur2 to cur1
            cur2.next = cur1
            cur2.prev = cur1.prev

            # point cur1's prev node to cur2
            cur1.prev.next = cur2

            # point cur1 to cur2's original next node
            cur1.next = cur2_next
            cur2_next.prev = cur1

            # point prev to cur2
            cur1.prev = cur2

        # if cur2 is "behind" cur1
        else:
            cur1.next = cur2
            cur1.prev = cur2.prev

            cur2.prev.next = cur1

            cur2.next = cur1_next
            cur1_next.prev = cur2

            cur2.prev = cur1

    def reverse(self) -> None:
        """
        Reversing the CDLL by iterating inwards from the starting and ending
        indices (besides sentinel) and swapping those pairs. A bool is used
        to handle arrays of even length in the swap_helper helper method.
        """

        # initialize pointers/iterators/bool
        even_arr = None
        left = self.sentinel.next
        right = self.sentinel.prev
        i = 0

        if self.length() % 2 == 0:
            size = (self.length()) / 2
            even_arr = True
        else:
            size = (self.length() - 1) // 2

        while i < size:
            next_left = left.next
            next_right = right.prev

            if i == size - 1 and even_arr:
                self.swap_helper(left, right, True)
            else:
                self.swap_helper(left, right, False)

            left = next_left
            right = next_right
            i += 1

    def swap_helper(self, cur1, cur2, even_arr=False):
        """
        Helper method for swapping values, takes a pair of node as parameters
        as well as a bool which defaults to false. If the bool is true, it calls
        another helper to process adjacent pairs.
        """
        if even_arr:
            return self.swap_adjacent_helper(cur1, cur2)

        # keep reference to cur2 adjacent nodes to link to cur1
        # else we'll be in an infinite loop
        cur2_prev = cur2.prev
        cur2_next = cur2.next

        # point cur1's adjacent nodes to cur2
        cur1.prev.next = cur2
        cur1.next.prev = cur2

        # point cur2 to to cur1's adjacent nodes
        cur2.prev = cur1.prev
        cur2.next = cur1.next

        # point cur2's adjacent nodes to cur1
        cur2_prev.next = cur1
        cur2_next.prev = cur1

        # point cur1 to cur2's adjacent nodes
        cur1.prev = cur2_prev
        cur1.next = cur2_next

    def swap_adjacent_helper(self, cur1, cur2):
        """
        Helper method used for swapping nodes which are adjacent to one
        another in the case of arrays of even length.
        """
        # reference to cur2.next for swapping node pointers
        cur2_next = cur2.next

        # point cur2 to cur1
        cur2.next = cur1
        cur2.prev = cur1.prev

        # point cur1's prev node to cur2
        cur1.prev.next = cur2

        # point cur1 to cur2's original next node
        cur1.next = cur2_next
        cur2_next.prev = cur1

        # point prev to cur2
        cur1.prev = cur2

    def sort(self) -> None:
        """
        Modified bubble sort algorithm used to sort a CDLL in non-descending order.
        All nodes are sorted in place.
        """

        # exit method if empty array
        if self.is_empty():
            return

        for i in range(self.length() - 1):
            cur = self.sentinel.next
            for j in range(self.length() - i - 1):
                cur_next = cur.next
                if cur.value > cur.next.value:
                    # point cur's previous node to cur.next, e.g. swapped node
                    cur.prev.next = cur.next

                    # point cur to the node after the swapped node
                    cur.next = cur.next.next

                    # point node after original cur.next to new cur
                    cur.next.prev = cur

                    # point swapped node to original cur.prev
                    cur_next.prev = cur.prev

                    # point original cur.next swapped node to new cur.next (original cur)
                    cur_next.next = cur

                    # set original cur's prev, now cur.next, to swapped node
                    cur.prev = cur_next

                # if no valid swap, continue traversing CDLL
                else:
                    cur = cur.next

    def rotate(self, steps: int) -> None:
        """
        Rotate implementation which rotates the CDLL by shifting its elements left
        or right depending on the steps parameter received. If the array is empty
        or if the steps provided equate to zero, the method exits.
        """

        # break if empty array or invalid steps
        if self.is_empty() or steps == 0 or \
                steps % self.length() == 0:
            return

        # positive bool for determining whether steps are positive to ensure
        # proper rotation
        positive = True
        if steps < 0:
            positive = False

        # traverse the CDLL starting from sentinel with steps % length as
        # range
        cur = self.sentinel
        for _ in range(abs(steps) % self.length()):
            # traverse leftwards if positive step, else rightwards
            if positive:
                cur = cur.prev
            else:
                cur = cur.next

        if steps < 0:
            cur = cur.next

        # break sentinel links and point sentinel's adjacent nodes to each other
        # point node in front of sentinel to node behind sentinel
        self.sentinel.next.prev = self.sentinel.prev

        # vice versa but for the node behind the sentinel
        self.sentinel.prev.next = self.sentinel.next

        # point cur.prev to sentinel for new sentinel position
        cur.prev.next = self.sentinel
        self.sentinel.prev = cur.prev

        # "insert" sentinel into new position which points to cur and is linked
        # to cur.prev.prev
        cur.prev = self.sentinel
        self.sentinel.next = cur

    def remove_duplicates(self) -> None:
        """
        Remove duplicates implementation removing all nodes with duplicated
        values from sorted CDLL. The method traverses an array with pointers
        "prev" and "nxt" nodes beginning at sentinel and sentinel.next,
        respectively. If duplicate node.values are found during CDLL traversing,
        a bool is set and a conditional is entered to remove those duplicate notes
        by adjusting node pointers to "excise" them from the CDLL.
        """
        # exit method if empty CDLL
        if self.is_empty():
            return

        # bool to handle entering conditional to swap node pointers
        clone = None
        # starting nodes to traverse CDLL
        nxt = self.sentinel.next
        prev = self.sentinel

        # traverse CDLL keeping track of duplicate values when found and breaking
        # pointer links to them if necessary
        for i in range(self.length()):
            val = nxt.value
            nxt = nxt.next

            if val != nxt.value:
                if not clone:
                    prev = prev.next
                else:
                    prev.next = nxt
                    nxt.prev = prev
                    clone = False
            else:
                clone = True

    def odd_even(self) -> None:
        """
        Odd even implementation which uses a two-pointer approach starting from
        trail and lead pointers. Since the algorithm for this method starts with
        1-indexing, a "pos" value is initialized at 2 and node pointers are
        initialized as the 1st and 2nd indices.

        The lead pointer traverses the CDLL, linking odd nodes towards the first
         "half" of the CDLL if the pos value ahead of the lead is an odd index.
        """

        # move even index values (starting from 1 to right half of CDLL and vice versa)
        # if CDLL is length of 2, return
        if self.length() <= 2:
            return

        trail = self.sentinel.next
        lead = self.sentinel.next.next

        pos = 2
        while lead.next != self.sentinel:
            # if lead.next is odd, swap to "edge"
            if (pos + 1) % 2 != 0:

                # comments depict first pointer swap in list traversal to better
                # visualize method

                # 3
                swap = lead.next

                # 4
                right = lead.next.next

                # 2
                trail_right = trail.next

                # 1 <-> 3
                swap.prev = trail
                trail.next = swap

                # 3 <-> 2
                swap.next = trail_right
                trail_right.prev = swap.next

                # 2 <-> 4
                lead.next = right
                right.prev = lead

                # 1 <-> 3 <-> 2 <-> 4
                # increment trail
                trail = trail.next
            else:
                lead = lead.next
            pos += 1
        trail.next.prev = trail

    def add_integer(self, num: int) -> None:
        """
        Add integer method which takes a number as a parameter and adds it to
        the CDLL. This method uses carry division to process sums where the
        value is greater than 9, using modulo and floor division to insert
        the results in the necessary CDLL nodes while also carrying over
        the remainder when necessary.

        Once the CDLL is exhausted, the main while loop breaks and any necessary
        nodes are added depending on whether or not a remainder is left.
        """
        # initialize current node and carry var
        cur = self.sentinel.prev
        carry = 0

        # get rightmost digit via modulo
        while cur != self.sentinel:
            if carry > 0 or num > 0:
                # store node value to process carry
                temp = cur.value

                val = num % 10
                num //= 10
                cur.value = (cur.value + carry + val) % 10
                carry = (temp + carry + val) // 10

                cur = cur.prev
            else:
                break

        # insert nodes for any remainders
        while num > 0:
            val = num % 10
            num //= 10
            self.add_front((val + carry) % 10)
            carry = (carry + val) // 10

        # edge case where some carry value still remains after number is exhausted
        if carry > 0:
            self.add_front(carry)


if __name__ == '__main__':
    pass

    print('\n# add_front example 1')
    lst = CircularList()
    print(lst)
    lst.add_front('A')
    lst.add_front('B')
    lst.add_front('C')
    print(lst)

    print('\n# add_back example 1')
    lst = CircularList()
    print(lst)
    lst.add_back('C')
    lst.add_back('B')
    lst.add_back('A')
    print(lst)

    print('\n# insert_at_index example 1')
    lst = CircularList()
    test_cases = [(0, 'A'), (0, 'B'), (1, 'C'), (3, 'D'), (-1, 'E'), (5, 'F')]
    for index, value in test_cases:
        print('Insert of', value, 'at', index, ': ', end='')
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print('\n# remove_front example 1')
    lst = CircularList([1, 2])
    print(lst)
    for i in range(3):
        try:
            lst.remove_front()
            print('Successful removal', lst)
        except Exception as e:
            print(type(e))

    print('\n# remove_back example 1')
    lst = CircularList()
    try:
        lst.remove_back()
    except Exception as e:
        print(type(e))
    lst.add_front('Z')
    lst.remove_back()
    print(lst)
    lst.add_front('Y')
    lst.add_back('Z')
    lst.add_front('X')
    print(lst)
    lst.remove_back()
    print(lst)

    print('\n# remove_at_index example 1')
    lst = CircularList([1, 2, 3, 4, 5, 6])
    print(lst)
    for index in [0, 0, 0, 2, 2, -2]:
        print('Removed at index:', index, ': ', end='')
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))
    print(lst)

    print('\n# get_front example 1')
    lst = CircularList(['A', 'B'])
    print(lst.get_front())
    print(lst.get_front())
    lst.remove_front()
    print(lst.get_front())
    lst.remove_back()
    try:
        print(lst.get_front())
    except Exception as e:
        print(type(e))

    print('\n# get_back example 1')
    lst = CircularList([1, 2, 3])
    lst.add_back(4)
    print(lst.get_back())
    lst.remove_back()
    print(lst)
    print(lst.get_back())

    print('\n# remove example 1')
    lst = CircularList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(lst)
    for value in [7, 3, 3, 3, 3]:
        print(lst.remove(value), lst.length(), lst)

    print('\n# count example 1')
    lst = CircularList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print('\n# swap_pairs example 1')
    lst = CircularList([0, 1, 2, 3, 4, 5, 6])
    test_cases = ((0, 6), (0, 7), (-1, 6), (1, 5),
                  (4, 2), (3, 3), (1, 2), (2, 1))

    for i, j in test_cases:
        print('Swap nodes ', i, j, ' ', end='')
        try:
            lst.swap_pairs(i, j)
            print(lst)
        except Exception as e:
            print(type(e))

    print('\n# reverse example 1')
    test_cases = (
        [1, 2, 3, 3, 4, 5],
        [1, 2, 3, 4, 5],
        ['A', 'B', 'C', 'D']
    )
    for case in test_cases:
        lst = CircularList(case)
        lst.reverse()
        print(lst)

    print('\n# reverse example 2')
    lst = CircularList()
    print(lst)
    lst.reverse()
    print(lst)
    lst.add_back(2)
    lst.add_back(3)
    lst.add_front(1)
    lst.reverse()
    print(lst)

    print('\n# reverse example 3')


    class Student:
        def __init__(self, name, age):
            self.name, self.age = name, age

        def __eq__(self, other):
            return self.age == other.age

        def __str__(self):
            return str(self.name) + ' ' + str(self.age)


    s1, s2 = Student('John', 20), Student('Andy', 20)
    lst = CircularList([s1, s2])
    print(lst)
    lst.reverse()
    print(lst)
    print(s1 == s2)

    print('\n# reverse example 4')
    lst = CircularList([1, 'A'])
    lst.reverse()
    print(lst)

    print('\n# sort example 1')
    test_cases = (
        [1, 10, 2, 20, 3, 30, 4, 40, 5],
        ['zebra2', 'apple', 'tomato', 'apple', 'zebra1'],
        [(1, 1), (20, 1), (1, 20), (2, 20)]
    )
    for case in test_cases:
        lst = CircularList(case)
        print(lst)
        lst.sort()
        print(lst)

    print('\n# rotate example 1')
    source = [_ for _ in range(-20, 20, 7)]
    for steps in [1, 2, 0, -1, -2, 28, -100]:
        lst = CircularList(source)
        lst.rotate(steps)
        print(lst, steps)

    print('\n# rotate example 2')
    lst = CircularList([10, 20, 30, 40])
    for j in range(-1, 2, 2):
        for _ in range(3):
            lst.rotate(j)
            print(lst)

    print('\n# rotate example 3')
    lst = CircularList()
    lst.rotate(10)
    print(lst)



    print('\n# remove_duplicates example 1')
    test_cases = (
        [1, 2, 3, 4, 5], [1, 1, 1, 1, 1],
        [], [1], [1, 1], [1, 1, 1, 2, 2, 2],
        [0, 1, 1, 2, 3, 3, 4, 5, 5, 6],
        list("abccd"),
        list("005BCDDEEFI")
    )

    for case in test_cases:
        lst = CircularList(case)
        print('INPUT :', lst)
        lst.remove_duplicates()
        print('OUTPUT:', lst)

    print('\n# odd_even example 1')
    test_cases = (
        [1, 2, 3, 4, 5], list('ABCDE'),
        [], [100], [100, 200], [100, 200, 300],
        [100, 200, 300, 400],
        [10, 'A', 20, 'B', 30, 'C', 40, 'D', 50, 'E']
    )

    for case in test_cases:
        lst = CircularList(case)
        print('INPUT :', lst)
        lst.odd_even()
        print('OUTPUT:', lst)

    print('\n# add_integer example 1')
    test_cases = (
        ([1, 2, 3], 10456),
        ([], 25),
        ([2, 0, 9, 0, 7], 108),
        ([9, 9, 9], 9_999_999),
    )
    for list_content, integer in test_cases:
        lst = CircularList(list_content)
        print('INPUT :', lst, 'INTEGER', integer)
        lst.add_integer(integer)
        print('OUTPUT:', lst)
