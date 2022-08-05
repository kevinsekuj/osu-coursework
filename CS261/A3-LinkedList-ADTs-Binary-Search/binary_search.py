# Course: CS261 - Data Structures
# Student Name: Kevin Sekuj
# Assignment: Assignment 3 - Implementation of LL, ADTs using LL's and Binary Search
# Description: Binary search and rotated binary search implementation using
# StaticArray as underlying internal data structure.

import random
import time
from static_array import *


# ------------------- PROBLEM 1 - -------------------------------------------


def binary_search(arr: StaticArray, target: int) -> int:
    """
    Implementation of a binary search algorithm with SA as associated
    internal data storage. The method receives an integer target and
    returns the target element if it is present in the array or -1
    if not.
    """
    first = 0
    last = arr.size() - 1

    # standard binary search implementation using static arr, in ascending order
    if arr[0] < arr[last]:
        while first <= last:
            middle = (first + last) // 2
            if arr[middle] == target:
                return middle
            if arr[middle] > target:
                last = middle - 1
            else:
                first = middle + 1
        return -1
    else:
        # ditto but descending order
        while first <= last:
            middle = (first + last) // 2
            if arr[middle] == target:
                return middle
            if arr[middle] < target:
                last = middle - 1
            else:
                first = middle + 1
        return -1

# ------------------- PROBLEM 2 - -------------------------------------------


def binary_search_rotated(arr: StaticArray, target: int) -> int:
    """
    Rotated binary search implementation. On a higher level overview, this method
    is similar to a regular binary search, except that a middle "pivot point" will
    be chosen from which to "spit" the array into two "halves" and search for the
    provided target in O(logN) time. Details regarding implementation in block
    comments.
    """
    # get first and last index
    first = 0
    last = arr.size() - 1

    while first <= last:
        # get middle index of the array to use as "pivot" point
        mid = (first + last) // 2

        # if return target happens to be middle index
        if arr.get(mid) == target:
            return mid

        # "split" array in half using the middle index as a pivot point
        #  for searching array halves for target

        elif arr.get(mid) >= arr.get(first):

            # set last index to the middle if target within this half of
            # original array, which is possible as the array is guaranteed
            # to be sorted

            if arr.get(first) <= target < arr.get(mid):
                last = mid - 1

            else:
                first = mid + 1

        # if target value in second half of array
        elif arr.get(mid) <= arr.get(last):

            # adjust first if target in mid->last portion of this array, else
            # set it to mid-1
            if arr.get(mid) < target <= arr.get(last):
                first = mid + 1
            else:
                last = mid - 1

    # if value does not exist in arr
    return -1

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":
    pass

    print('\n# problem 1 example 1')
    src = (-10, -5, 0, 5, 7, 9, 11)
    targets = (7, -10, 11, 0, 8, 1, -100, 100)
    arr = StaticArray(len(src))
    for i, value in enumerate(src):
        arr[i] = value
    print([binary_search(arr, target) for target in targets])
    arr._data.reverse()
    print([binary_search(arr, target) for target in targets])


    print('\n# problem 1 example 2')
    """
    src = [random.randint(-10 ** 7, 10 ** 7) for _ in range(5_000_000)]
    src = sorted(set(src))
    arr = StaticArray(len(src))
    arr._data = src[:]

    # add 20 valid and 20 (likely) invalid targets
    targets = [-10 ** 8, 10 ** 8]
    targets += [arr[random.randint(0, len(src) - 1)] for _ in range(20)]
    targets += [random.randint(-10 ** 7, 10 ** 7) for _ in range(18)]

    result, total_time = True, 0
    for target in targets:
        total_time -= time.time()
        answer = binary_search(arr, target)
        total_time += time.time()
        result &= arr[answer] == target if target in src else answer == -1
    print(result, total_time < 0.5)

    arr._data.reverse()
    for target in targets:
        total_time -= time.time()
        answer = binary_search(arr, target)
        total_time += time.time()
        result &= arr[answer] == target if target in src else answer == -1
    print(result, total_time < 0.5)
    """


    print('\n# problem 2 example 1')
    test_cases = (
        ((6, 8, 12, 20, 0, 2, 5), 0),
        ((6, 8, 12, 20, 0, 2, 5), -1),
        ((1,), 1),
        ((1,), 0),
    )
    result = []
    for src, target in test_cases:
        arr = StaticArray(len(src))
        for i, value in enumerate(src):
            arr[i] = value
        result.append((binary_search_rotated(arr, target)))
    print(*result)


    print('\n# problem 2 example 2')
    """
    src = [random.randint(-10 ** 7, 10 ** 7) for _ in range(5_000_000)]
    src = sorted(set(src))
    arr = StaticArray(len(src))
    arr._data = src[:]

    # add 20 valid and 20 (likely) invalid targets
    targets = [-10 ** 8, 10 ** 8]
    targets += [arr[random.randint(0, len(src) - 1)] for _ in range(20)]
    targets += [random.randint(-10 ** 7, 10 ** 7) for _ in range(18)]

    result, total_time = True, 0
    for target in targets:
        # rotate arr random number of steps
        pivot = random.randint(0, len(src) - 1)
        arr._data = src[pivot:] + src[:pivot]

        total_time -= time.time()
        answer = binary_search_rotated(arr, target)
        total_time += time.time()
        result &= arr[answer] == target if target in src else answer == -1
    print(result, total_time < 0.5)
    """

