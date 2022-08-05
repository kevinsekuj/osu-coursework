# Author: Kevin Sekuj
# Date: 1/15/2021
# Description: Modified binary search function which raise a TargetNotFound exception
# when the target value is not found in the list.

class TargetNotFound(Exception):
    """
    Exception class handling TargetNotFound error for bin_except's
    binary search function.
    """
    pass


def bin_except(bin_list, target):
    """
    Searches a list for an occurrence of a target value. If the value is found, it
    returns the index of its position in the list, otherwise, it raises a
    TargetNotFound exception if the value is not in the list.
    """
    first = 0
    last = len(bin_list) - 1
    while first <= last:
        middle = (first + last) // 2
        if bin_list[middle] == target:
            return middle
        if bin_list[middle] > target:
            last = middle - 1
        else:
            first = middle + 1
    raise TargetNotFound
