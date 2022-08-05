# Author: Kevin Sekuj
# Date: 01/18/2022
# Description: Implement the function kthElement(Arr1, Arr2, k) that was written in part a.
# Name your file KthElement.py.
# Source: this merge procedure code was inspired by the pseudocode provided
# in the Divide and Conquer algorithm module.


def kthElement(arr1: list, arr2: list, k: int) -> object:
    """
    Given two sorted arrays of size m and n respectively, find the element that
    would be at the kth position in combined sorted array.
    :param arr1: input array 1
    :param arr2: input array 2
    :param k: kth position
    :return: element at k
    """

    # Corner case - null arrays
    if not arr1 and not arr2:
        return -1

    n = len(arr1) + len(arr2)

    # Invalid k
    if k > n or k < 0:
        return -1

    # Initialize empty array of combined array lengths
    arr1_len, arr2_len = len(arr1), len(arr2)
    combined = [0] * n
    arr1_idx, arr2_idx, new_idx = 0, 0, 0

    # Merge portion - merging arrays of sorted elements by checking single
    # elements, using a two pointer technique.
    while arr1_idx < arr1_len and arr2_idx < arr2_len:

        if arr1[arr1_idx] < arr2[arr2_idx]:
            combined[new_idx] = arr1[arr1_idx]
            arr1_idx += 1

        else:
            combined[new_idx] = arr2[arr2_idx]
            arr2_idx += 1

        if k == new_idx:
            return combined[k - 1]

        new_idx += 1

    # If any elements are remaining, copy them over to combined array
    while arr1_idx < arr1_len:
        combined[new_idx] = arr1[arr1_idx]
        arr1_idx += 1

        new_idx += 1

    while arr2_idx < arr2_len:
        combined[new_idx] = arr2[arr2_idx]
        arr2_idx += 1
        new_idx += 1

    return combined[k - 1]
