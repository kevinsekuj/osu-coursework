# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Hash Maps, Min Heap, AVL Tree Implementation
# Description: Implementation of the minheap ADT with internal storage of
# a DA.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass

class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        Add implementation for the MinHeap in O(logN) time. Heap property is
        maintained by ensuring each node's value is <= the value in the node's
        children.
        """

        if self.heap.length() == 0:
            self.heap.append(node)
            return

        self.heap.append(node)
        index = self.heap.length() - 1

        self.add_helper(node, index)

    def add_helper(self, node: object, index: int) -> None:
        """
        Helper method for MinHeap add implementation. Method recurses through
        heap percolating nodes upwards depending on whether the value maintains
        minheep properties by being less than its parent node.
        """
        if index == 0:
            return

        parent = self.heap.get_at_index((index - 1) // 2)

        if node > parent:
            return

        parent_index = (index - 1) // 2
        self.heap.swap(index, parent_index)

        index = parent_index
        self.add_helper(node, index)

    def get_min(self) -> object:
        """
        Returns the object with the minimum key in the minheap without
        removing it from the heap in constant time.
        """
        if self.heap.length() == 0:
            raise MinHeapException
        return self.heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Returns the object with with the minimum key in the heap and removes
        it from the heap in logN time.
        """
        if self.heap.length() == 0:
            raise MinHeapException

        # swap and pop
        self.heap.swap(0, self.heap.length() - 1)
        old_min = self.heap.pop()

        if self.heap.length() == 1:
            return old_min

        self.remove_helper()

        return old_min

    def remove_helper(self, index=0) -> None:
        """
        Helper method for removing the minimum value of the minheap recursively
        and returning it. If the heap is empty, the parent method returns
        a MinHeap exception.
        """
        # get index of children
        left = index * 2 + 1
        right = index * 2 + 2

        # if both out of bounds, stop
        if left > self.heap.length() - 1 and right > self.heap.length() - 1:
            return

        if left > self.heap.length() - 1:
            child = right
        elif right > self.heap.length() - 1:
            child = left
        else:
            if self.heap.get_at_index(left) <= self.heap.get_at_index(right):
                child = left
            else:
                child = right

        if self.heap.get_at_index(index) > self.heap.get_at_index(child):
            self.heap.swap(index, child)

            self.remove_helper(index=child)

        return

    def build_heap(self, da: DynamicArray) -> None:
        """
        Receives dynamic array with objects in order and builds minheap
        thereby removing current content of minheap in linear time.
        """
        self.heap = DynamicArray()

        for i in range(da.length()):
            self.heap.append(da.get_at_index(i))

        # first non-leaf element
        index = self.heap.length() // 2 - 1

        for i in range(index, -1, -1):
            self.build_heap_helper(i)

    def build_heap_helper(self, index=0):
        """
        Helper method for building heap, similar method to remove helper, which
        percolates bottom-up.
        """
        # get index of children
        left = index * 2 + 1
        right = index * 2 + 2

        # if both out of bounds, stop
        if left > self.heap.length() - 1 and right > self.heap.length() - 1:
            return

        if left > self.heap.length() - 1:
            child = right
        elif right > self.heap.length() - 1:
            child = left
        else:
            if self.heap.get_at_index(left) <= self.heap.get_at_index(right):
                child = left
            else:
                child = right

        if self.heap.get_at_index(index) > self.heap.get_at_index(child):
            self.heap.swap(index, child)

            self.remove_helper(index=child)
        return


# BASIC TESTING
if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap(
        [-990, -986, -986, -979, -980, -978, -965, -979, -937, -961, -971, -864, -962, -897, -957, -930, -955, -905,
         -919, -952, -959, -962, -913, -796, -774, -814, -917, -755, -861, -937, -928, -877, -820, -886, -935, -885,
         -726, -916, -869, -915, -942, -949, -853, -938, -956, -895, -649, -719, -727, -672, -700, -730, -766, -861,
         -881, -735, -690, -683, -803, -892, -924, -898, -544, -803, -807, -627, -772, -792, -852, -837, -908, -817,
         -726, -542, -726, -741, -871, -552, -841, -796, -891, -889, -934, -852, -943, -395, -842, -910, -928, -946,
         -441, -842, -552, -520, -540, -441, -569, -187, -621, -572, -619, -371, -586, -442, -453, -391, -586, -431,
         -226, -149, -875, 28, -338, -257, -505, 157, -529, -551, -739, -541, -824, -525, -739, -785, -822, -250, -316,
         -483, -756, -716, -663, -514, -560, -698, -515, -664, -769, -836, -321, -485, -703, -643, -810, -634, -789,
         -692, -648, -398, -497, -653, -309, -727, -243, -712, -823, -534, -513, -827, -539, -141, -777, -345, -828,
         -718, -756, -898, -713, -769, -843, -370, -648, -381, -319, -775, -559, -395, -818, -719, -926, -781, -899,
         -155, -430, -576, -750, -59, -440, 477, 150, -483, -364, -316, -330, 89, -523, 386, 259, 399, 201, -289, -569,
         -488, -373, -341, -256, -39, -508, 30, -376, -193, -428, 264, -212, -309, -473, -342, -40, -145, -156, 75, 97,
         -411, -781, 497, 192, 344, 333, 298, -115, -172, -378, 191, 485, 97, -238, 820, -236, -107, -510, -67, 307,
         -760, -1, 287, -45, 408, -355, -775, 143, -80, -812, -21, -98, 211, -219, -180, -415, -571, -144, 41, -471,
         360, -527, -177, 157, -282, -529, -587, -614, -228, -120, -559, -203, -282, -534, 285, 120, 412, -216, -367,
         125, -506, -518, 571, 184, -462, -547, -245, -591, -591, -717, 63, -352, -182, -314, -23, -75, -356, 10, -411,
         -611, 477, 178, -574, -584, -12, 580, -669, 283, -347, -491, -298, -318, -470, -402, -8, -464, -133, -466,
         -131, -89, 316, 190, -111, -335, -404, -784, -412, -326, -554, -663, -149, -617, -513, -595, 179, -430, -650,
         -667, -103, 162, -645, -263, -88, 199, 75, -71, -537, -523, -510, -376, -227, -74, -292, -783, -624, -412,
         -109, -901, 145, -767, 217, -843, 159, -152, -165, -194, -414, -417, -435, -724, 773, 852, 643, 392, 931, 795,
         918, 794, -328, -376, 301, -51, 492, 233, 419, 178, 163, 693, 680, 35, 819, 745, 905, 422, 410, 962, 397, 273,
         561, -174, 951, -319, 80, 500, 420, -365, 966, 160, 336, -234, 318, 517, 261, 502, 847, 416, 525, -208, 645,
         47, 733, -271, 920, 803, 229, -67, -268, -171, 630, -460, 495, -171, 966, -7, 937, 76, 72, 412, 668, 399, 306,
         706, 998, 194, 355, -589, 799, 522, 739, 646, 724, 424, 675, 576, 744, 666, 76, 601, 27, 924, 63, 271, 797,
         400, 578, 981, 793, 480, 884, 285, 922, 880, 297, 697, 717, 396, 634, 170, 622, 558, 831, 603, 134, -596, 257,
         703, 390, 729, 583, 484, 648, 577, 296, 20, 68, -234, 370, 996, 785, 411, -38, -283, 877, 762, 873, 602, 496,
         279, 619, 185, 791, 504, 739, 41, 768, 560, 898, 182, 875, 606, 259, 137, 498, 465, 191, 729, 783, 208, 402,
         172, 542, -209, 400, 70, 704, 528, 941, -401, 236, 932, -39, -92, 652, 38, 230, 39, 750, 468, 765, -460, 698,
         688, 689, 273, 884, 806, 547, -57, 781, 623, 372, 426, -20, -102, 793, -225, 985, 857, 860, 359, 801, 499, 950,
         500, 991, -25, 860, 261, 269, 225, 936, -231, 333, 815, 492, 143, 548, 881, 615, -142, 874, 24, 184, 526, 959,
         -125, 692, 696, 303, -171, 770, -310, 873, 545, 975, 683, 329, 176, -21, -297, 14, 394, 917, 812, 917, -29,
         958, 380, 805, 364, 762, -113, 101, -148, 484, -247, -197, 52, 641, 384, 532, 154, 23, -324, 404, 874, -236,
         -281, 991, 638, 694, 815, 711, 418, 328, 270, 413, 136, 83, -247, 636, 217, 253, -635, 566, -84, 231, 950, 722,
         -93, -87, 344, 294, 441, 889, -16, 227, 9, 266, -423, 813, 686, 378, -157, 575, 270, 780, -448, 548, 648, 718,
         651, 645, 89, 180, 166, 244, 81, 318, 256, 825, 904, 927, 159, 892, 134, 5, 745, -180, 262, 587, 469, 975, 159,
         825, -62, 736, 813, 722, -486, 681, -578, 590, -355, 486, 41, 257, -600, 671, 461, 887, 695, 530, 520, 368,
         353, 633, 537, 467, 275, 702, 106, 528, 355, 851, -255, 833, -128, 164, -319])
    while not h.is_empty():
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)
    da.set_at_index(0, 500)
    print(da)
    print(h)
