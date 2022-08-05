# Author: Kevin Sekuj
# Date: 2/1/21
# Description: Recursive function which takes a list of numbers as a parameter,
# returning the maximum value, without using max(), loops, helpers, or mutable
# default arguments.

def list_max(num_list, index=0, max_num=None):
    """
    Recursive function which takes a list as a parameter, and initializes the index
    and max_num parameters to None. Max_num is then checked against the value of
    each list index and is updated if it's greater.
    """
    if max_num is None:
        max_num = num_list[index]

    if index == len(num_list):
        return max_num

    if num_list[index] > max_num:
        max_num = num_list[index]

    return list_max(num_list, index + 1, max_num)
