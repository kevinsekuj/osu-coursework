# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Hash Maps, Min Heap, AVL Tree Implementation
# Description: Implementation of an AVL tree ADT, consisting of a self-balancing
# binary search tree.

import random


class Stack:
    """
    Class implementing STACK ADT.
    Supported methods are: push, pop, top, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty stack based on Python list """
        self._data = []

    def push(self, value: object) -> None:
        """ Add new element on top of the stack """
        self._data.append(value)

    def pop(self):
        """ Remove element from top of the stack and return its value """
        return self._data.pop()

    def top(self):
        """ Return value of top element without removing from stack """
        return self._data[-1]

    def is_empty(self):
        """ Return True if the stack is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "STACK: { " + ", ".join(data_str) + " }"


class Queue:
    """
    Class implementing QUEUE ADT.
    Supported methods are: enqueue, dequeue, is_empty

    DO NOT CHANGE THIS CLASS IN ANY WAY
    YOU ARE ALLOWED TO CREATE AND USE OBJECTS OF THIS CLASS IN YOUR SOLUTION
    """

    def __init__(self):
        """ Initialize empty queue based on Python list """
        self._data = []

    def enqueue(self, value: object) -> None:
        """ Add new element to the end of the queue """
        self._data.append(value)

    def dequeue(self):
        """ Remove element from the beginning of the queue and return its value """
        return self._data.pop(0)

    def is_empty(self):
        """ Return True if the queue is empty, return False otherwise """
        return len(self._data) == 0

    def __str__(self):
        """ Return content of the stack as a string (for use with print) """
        data_str = [str(i) for i in self._data]
        return "QUEUE { " + ", ".join(data_str) + " }"


class TreeNode:
    """
    AVL Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = 0

    def __str__(self):
        return 'AVL Node: {}'.format(self.value)


class AVL:
    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.root = None

        # populate AVL with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of AVL in human-readable form using pre-order traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self.root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, cur, values):
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if cur:
            values.append(str(cur.value))
            self._str_helper(cur.left, values)
            self._str_helper(cur.right, values)

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        s = Stack()
        s.push(self.root)
        while not s.is_empty():
            node = s.pop()
            if node:
                # check for correct height (relative to children)
                l = node.left.height if node.left else -1
                r = node.right.height if node.right else -1
                if node.height != 1 + max(l, r):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self.root:
                        return False
                s.push(node.right)
                s.push(node.left)
        return True

    # -----------------------------------------------------------------------

    def insert(self, value: object) -> TreeNode or None:
        """
        Adding a new value to the tree, maintaining BST properties. Duplicate
        values are placed in the right subtree.
        """
        # if the BST is empty, node should be inserted as root
        if self.root is None:
            self.root = TreeNode(value)
            return self.root

        # set node to root and initialize parent
        node = self.root
        parent = None

        # traverse BST until leaf is reached, with direction depending on value
        while node is not None:

            if value < node.value:
                parent = node
                node = node.left
            elif value > node.value:
                parent = node
                node = node.right
            else:
                return

        # insert node at position depending on whether k > parent.value
        if value > parent.value:
            parent.right = TreeNode(value)
            parent.right.parent = parent

            node = parent.right

        elif value < parent.value:
            parent.left = TreeNode(value)
            parent.left.parent = parent

            node = parent.left

        # if duplicate node inserted
        else:
            return

        return node

    def rotate_left(self, node: TreeNode) -> TreeNode:
        """
        Helper method for performing a left rotation on a node when the BST
        must self-balance. Taken from pseudocode from module summary.
        """
        c = node.right
        node.right = c.left

        if node.right:
            node.right.parent = node

        c.left = node
        node.parent = c

        self.update_height(node)
        self.update_height(c)

        return c

    def rotate_right(self, node) -> TreeNode:
        """
        Helper method for performing a right rotation on a node when the BST
        must self-balance. Taken from pseudocode from module summary.
        """
        c = node.left
        node.left = c.right

        if node.left:
            node.left.parent = node

        c.right = node
        node.parent = c

        self.update_height(node)
        self.update_height(c)

        return c

    def update_height(self, node) -> None:
        """
        Method for updating the height of a given node depending on its structure
        after a rebalancing has taken place. Height update will be based on
        the structure of the subtree in terms of no children, left child only, etc.
        """
        # no children
        if not node.left and not node.right:
            node.height = 0

        # no right node
        elif not node.right:
            node.height = node.left.height + 1

        # no left node
        elif not node.left:
            node.height = node.right.height + 1

        # subtree of 2 children
        else:
            node.height = max(node.left.height, node.right.height) + 1

    def rebalance(self, node: TreeNode) -> None:
        """
        Rebalance implementation. AVL trees rebalance in response to operations
        which change the structure of the tree, specifically adding or removing
        nodes in the case of this program. Node rebalancing will involve a rotation
        depending on the structure of the subtree, such as if it is imbalanced, etc.
        This method is implemented based on the pseudocode offered in the AVL module.
        """

        if self.balance_factor(node) < -1:
            rotated_parent = node.parent

            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
                node.left.parent = node

            new_subtree_root = self.rotate_right(node)
            new_subtree_root.parent = rotated_parent

            if node is self.root:
                self.root = new_subtree_root
                return

            else:
                if new_subtree_root.value < rotated_parent.value:
                    new_subtree_root.parent = rotated_parent
                    rotated_parent.left = new_subtree_root

                else:
                    new_subtree_root.parent = rotated_parent
                    rotated_parent.right = new_subtree_root

        elif self.balance_factor(node) > 1:
            rotated_parent = node.parent

            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
                node.right.parent = node

            new_subtree_root = self.rotate_left(node)
            new_subtree_root.parent = rotated_parent

            if node is self.root:
                self.root = new_subtree_root
                return

            else:
                if new_subtree_root.value < rotated_parent.value:
                    rotated_parent.left = new_subtree_root

                else:
                    rotated_parent.right = new_subtree_root

        else:
            self.update_height(node)

    def inorder_successor(self, node: TreeNode) -> TreeNode:
        """
        Helper method for determining the in-order successor in deletion
        of a node, similar to the method used in the BST implementation.
        In this case however the parent node will be returned.
        """
        parent = node.parent

        while node.left:
            parent = node
            node = node.left

        return parent

    def balance_factor(self, node) -> int:
        """
        Method for determining the balance factor of a particular particular
        node. If a balance factor is detected a rotation will be required to
        restore height balance.
        """
        left = None
        right = None

        if not node.left:
            left = -1
        else:
            left = node.left.height

        if not node.right:
            right = -1
        else:
            right = node.right.height

        return right - left

    def add(self, value: object) -> None:
        """
        Implementation for adding a node to the AVL tree. The node from the
        passed value is inserted into the tree normally with a BST operation,
        and then rebalancing the tree after the insertion.
        """
        node = self.insert(value)

        if not node:
            return

        p = node.parent
        while p:
            self.rebalance(p)
            p = p.parent

    def remove(self, value: object) -> bool:
        """
        Implementation of remove for removing nodes from the AVL tree.
        The node is removed using remove_node, a modified BST remove
        function which returns the removed node as well as the parent
        successor so that they may be used for the rebalancing operation
        which will follow.
        """
        # remove Node w normal BST removal
        removed, succ_parent = self.remove_node(value)

        # bool containing whether or not value removed
        if not removed:
            return False

        if not succ_parent:
            p = self.find(value)
        else:
            p = succ_parent

        while p is not None:
            self.rebalance(p)
            p = p.parent

        return True

    def find(self, value: object) -> TreeNode or object:
        """
        Helper method for finding a node and its parent in a given BST based
         on its value.
        """
        if self.root is None:
            return

        node = self.root

        while node.value != value:
            if value < node.value:
                node = node.left
            else:
                node = node.right

            if not node:
                break

        return node

    def remove_first(self) -> bool or tuple:
        """
        Method which removes the root node from the binary tree, returning false
        if the tree is empty. Otherwise, it removes the root node and replaces it
        with the successor and swaps tree node pointers as necessary, specific
        details in comments.
        """
        # if the tree is empty
        if not self.root:
            return False, None

        # removing root with no children
        if not self.root.left and not self.root.right:
            self.root = None
            return True, None

        # root with only left subtree
        if not self.root.right:
            self.root = self.root.left
            return True, None

        # root with only right subtree
        if not self.root.left:
            self.root = self.root.right
            return True, None

        # else find leftmost child of right subtree (in-order successor)
        # and replace root with that value
        parent = self.root
        node = self.root.right
        while node.left:
            parent = node
            node = node.left

        if parent == self.root:
            node.left = self.root.left
            node.left.parent = node
            self.root = node
            self.root.parent = None

            return True, self.root

        else:
            # point successor's children to parent
            parent.left = node.right
            if parent.left:
                parent.left.parent = parent

            # make successor root and point to right subtree
            node.right = self.root.right
            node.right.parent = node
            node.left = self.root.left
            node.left.parent = node
            self.root = node
            self.root.parent = None

            return True, parent

    def remove_node(self, value: object) -> tuple or object:
        """
        Method for removing the first instance of the value in the binary tree.
        If the tree does not contain the value, or the tree is empty, the
        method returns false. If the value is the root node, then the remove_first
        method is called to handle that case. Otherwise, it recurses through the
        tree with remove_helper to find the node to remove and replacing it
        with its in-order successor.
        """
        # return false if value doesn't exist in tree
        if self.contains(value) is False:
            return False, None

        # if root doesn't exist; tree is empty
        if not self.root:
            return False, None

        # if value is root
        if self.root.value == value:
            return self.remove_first()

        node, successor_parent = self.remove_helper(self.root, value)
        return True, successor_parent

    def remove_helper(self, node: TreeNode, value: object) -> tuple or object:
        """
        Helper method for traversing the tree recursively, comparing each node
        to the value parameter. If the value kq iis less than the node's current
        value, then it checks the child nodes of that tree, and vice versa for
        if kq is greater. Detailed description in section comments.
        """
        # base cases: traverse BST depending on value compared to current
        # node's value. if value k_q is less than the node's current value,
        # then the node continues towards its child and repeats, vice versa
        # for if k_q is greater

        if node.value > value:
            node.left, parent = self.remove_helper(node.left, value)

            return node, parent

        elif node.value < value:
            node.right, parent = self.remove_helper(node.right, value)

            return node, parent

        # find node to be removed
        else:

            # if node has no children
            if not node.left and not node.right:
                return None, node.parent

            # if node has no left children
            if not node.left:
                if node.value < node.parent.value:
                    node.parent.left = node.right
                    node.right.parent = node.parent
                else:
                    node.parent.right = node.right
                    node.right.parent = node.parent

                return node.right, node.parent

            # if node has no right children
            if not node.right:
                if node.value < node.parent.value:
                    node.parent.left = node.left
                    node.left.parent = node.parent
                else:
                    node.parent.right = node.left
                    node.left.parent = node.parent

                return node.left, node.parent

            # else, node has two children, so traverse leftwards in the right
            # subtree until reaching the successor, which is the leftmost node in
            # N's right subtree

            # cast right subtree node to temp variable
            temp_node = node.right
            # traverse leftwards until reaching the leftmost node in that subtree
            while temp_node.left is not None:
                temp_node = temp_node.left

            # update treenode value and remove values in right tree
            node.value = temp_node.value
            node.right = self.remove_helper(node.right, temp_node.value)[0]

            return node, temp_node.parent

    def contains(self, value: object) -> bool:
        """
        Searches for a value within the tree, returning false if the value
        is not present.
        """
        # if tree is empty, return false
        if self.root is None:
            return False

        # first check if root equals value
        if self.root.value == value:
            return True

        # traverse tree looking for node equaling value param, traversing
        # left or right depending on current node's value
        node = self.root
        while node is not None:
            if node.value == value:
                return True
            elif value < node.value:
                node = node.left
            else:
                node = node.right

        return False


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (5, 1, 3, 9, 7, 13, 11, 15)
    avl = AVL(test_cases)
    avl.remove(1)
    print(avl)
    for tree, del_value in test_cases:
        avl = AVL(tree)
        print('INPUT  :', avl, "DEL:", del_value)
        avl.remove(del_value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    avl = AVL(case)

    avl.remove(-9)
    print('RESULT :', avl)
    avl.remove(-7)
    print('RESULT :', avl)
    avl.remove(-5)
    print('RESULT :', avl)
    avl.remove(-3)
    print('RESULT :', avl)
    avl.remove(-1)
    print('RESULT :', avl)
    avl.remove(1)
    print('RESULT :', avl)
    avl.remove(3)
    print('RESULT :', avl)
    avl.remove(5)
    print('RESULT :', avl)
    avl.remove(7)
    print('RESULT :', avl)
    avl.remove(9)
    print('RESULT :', avl)
    avl.remove(11)
    print('RESULT :', avl)
    avl.remove(13)
    print('RESULT :', avl)
    avl.remove(15)
    print('RESULT :', avl)

    for del_value in case:
        print('INPUT  :', avl, del_value)
        avl.remove(del_value)
        print('RESULT :', avl)
        print('RESULT :', avl.by_level_traversal())
        print()

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    avl = AVL(case)

    for _ in case[:-2]:
        print('INPUT  :', avl, avl.root.value)
        avl.remove(avl.root.value)
        print('RESULT :', avl)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    count = 0
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        avl = AVL(case)
        for value in case[::2]:
            count += 1
            print(count, value)
            avl.remove(value)
            if not avl.is_valid_avl():
                raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')