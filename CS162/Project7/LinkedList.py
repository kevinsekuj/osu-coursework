# Author: Kevin Sekuj
# Date: 2/15/21
# Description: LinkedList class with recursive implementations of the add, remove
# contains, insert, and reverse methods as described in the modules. Has a recursive
# method named to_plain_list which returns a Python list with the current state of
# the linked list, as well as as a method for returning the Node object.

class Node:
    """
    Node object within the linked list.
    """

    def __init__(self, data):
        """
        Constructor method for the Node's private data members.
        """
        self._data = data
        self._next = None

    def set_next(self, node):
        """
        Passes a node in order to return its node.next.
        """
        self._next = node

    def get_next(self):
        """
        Get method to return the next node of the  node object.
        """
        return self._next

    def get_data(self):
        """
        Get method to return the data value of the node object.
        """
        return self._data


class LinkedList:
    """
    LinkedList class containing head node data member and recursive functions.
    """

    def __init__(self):
        """
        Constructor method containing head linked list node.
        """
        self._head = None

    def get_head(self):
        """
        Returns the head node object of the LinkedList class.
        """
        return self._head

    def set_head(self, node):
        """
        Sets the head of the linked list to the node passed to the function.
        """
        self._head = node

    def add(self, val):
        """
        Recursive implementation of a LinkedList's add method. If the LL is empty,
        the head Node is created with the passed value. Otherwise if the next node
        over is None, the new Node is added in that position. If not, it recursively
        checks each node with add_helper.
        """
        if self.get_head() is None:  # if LL is empty
            self.set_head(Node(val))

        else:
            if self.get_head().get_next() is None:
                self.get_head().set_next(Node(val))

            else:
                self.add_helper(self.get_head().get_next(), val)

    def add_helper(self, node, val):
        """
        Recursively checks each node in the linked list and adds when a null
        position is found.
        """
        if node.get_next() is None:
            node.set_next(Node(val))
            return
        else:
            node = node.get_next()
            self.add_helper(node, val)

    def remove(self, val):
        """
        Removes nodes from the linked list by passed value parameter. If the node
        isn't the head node, it passes the current head node, next head node, and
        value to remove_helper and recursively moves down the linked list.
        """
        if self.get_head() is None:  # if LL is empty
            return

        else:
            if self.get_head().get_data() == val:  # if head is node to remove
                self.set_head(self.get_head().get_next())
            else:
                self.remove_helper(self.get_head().get_next(), self.get_head(), val)

    def remove_helper(self, current, previous, val):
        """
        Recursively checks list nodes for the node with the matching value to
        remove. When the node is found, i.e, when current is not None, the "link"
        is broken and the node is "removed".
        """
        if current is not None and current.get_data() != val:
            self.remove_helper(current.get_next(), previous.get_next(), val)
        elif current is not None:
            previous.set_next(current.get_next())
            return

    def contains(self, key):
        """
        Checks for the presence of a node by passing a key to the contains_helper
        function, which recursively moves down the nodes of the linked list until
        a node with the key value is found.
        """
        return self.contains_helper(self.get_head(), key)

    def contains_helper(self, node, key):
        """
        Returns true when a node with the matching key value is found, otherwise,
        continues recursively moving down the list until the node is found, returning
        False if the node with the equivalent data does not exist.
        """
        if node is None:
            return False

        if node.get_data() == key:
            return True

        return self.contains_helper(node.get_next(), key)

    def insert(self, val, pos):
        """
        Inserts a node with value at a position in the linked list. If the list
        is empty, the passed node becomes the first node in the list.
        """
        if self.get_head() is None:  # if list is empty
            self.add(val)
            return

        if pos == 0:  # if inserted at the 0th position
            temp = self.get_head()      # uses temp var to hold current position, to allow
            self.set_head(Node(val))    # passed Node(val) to be "inserted" between those positions
            self.get_head().set_next(temp)
            return

        self.insert_helper(self.get_head(), val, pos)

    def insert_helper(self, index, val, pos):
        """
        Recursively moves down the list of nodes until the pos 'counter' has
        reached 1. In that case, the node it reaches will be the position to
        insert at.
        """
        if index.get_next() is None:      # if the next node is none, insert,
            temp = index.get_next()       # such as in cases where "pos" param
            index.set_next(Node(val))     # equals or exceeds LL length
            index.get_next().set_next(temp)
            return

        if pos == 1:
            temp = index.get_next()
            index.set_next(Node(val))
            index.get_next().set_next(temp)
            return

        return self.insert_helper(index.get_next(), val, pos - 1)

    def reverse(self):
        """
        Reverse linked list function which passes current head node to reverse_helper,
        where its links (next) with other nodes are reversed recursively. When the helper
        function has concluded, it returns the reversed linked list to this method.
        """
        # setting the "new" head node to the reversed Linked List nodes.
        self.set_head(self.reverse_helper(self.get_head()))

    def reverse_helper(self, node):
        """
        Helper method which takes the current head node and recursively reverses
        the linked list by reversing each .next connection in each recursive call,
        described in detail in in-line comments. Returns the new reversed head node.
        """

        # base cases; if the position is None, return, or if the next position is
        # none, it means that this node is already last in the linked list.

        if node is None or node.get_next() is None:
            return node

        # traverses down the linked list recursively until reaching the last node
        # in the list. when the last node is found, it is assigned to the reversed
        # head node.

        reverse_head_node = self.reverse_helper(node.get_next())

        # the second to last node in the previous callstack has its next-next property,
        # meaning the "next" of the last node, assigned to itself. i.e 3<-2 is now 3->2

        node.get_next().set_next(node)

        # the node's "next" is set to None as the above process will be repeated in each
        # recursive call moving upwards in the linked list, reversing each node

        node.set_next(None)

        return reverse_head_node    # return new list head with its reversed links

    def to_plain_list(self):
        """Returns a Python list of the data attributes of each Node object
        in the linked list."""
        if self.get_head() is None:  # list is empty/no head node
            return []

        return self.list_helper(self.get_head())

    def list_helper(self, node, val=None):
        """Recursively moves through the linked list, appending the node.get_data()
        value in each recursive call. When the end of the list is reached, the
        helper function returns the Python list containing node values."""
        if val is None:
            val = []
        if node is None:
            return val

        val.append(node.get_data())
        return self.list_helper(node.get_next(), val)
