# Author: Kevin Sekuj
# Date: 2/1/21
# Description: Recursive function that takes a list of numbers as parameters,
# returning true if the elements are decreasing consecutively, or returning
# false if they aren't. Does not use loops, vars defined outside of the
# function, or mutable default arguments.


def is_decreasing(num_list, index=0):
    """
    Takes a list as a parameter and checks if the current number, the value
    at the current list index, is greater than the index at the previous index.
    Stops when the list is traversed, and returns True if the list is in strict
    descending order.
    """
    if index == len(num_list):
        return True

    num = num_list[index]

    if index != 0 and num >= num_list[index-1]:
        return False

    return is_decreasing(num_list, index+1)
