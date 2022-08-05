# Author: Kevin Sekuj
# Date: 11/02/20
# Description: Function which takes a parameter as a list of numbers,
# then returns the median of those numbers via list sorting.

def find_median(num_list):
    """
    Function which returns median of a sorted list, by checking if len(num_list)
    is odd, and if so, indexing the integer in the middle by len of the nums
    divided by 2 via floor division. If len(num_list) is even, it indexes
    the two middle integers, adding them and dividing by 2 which would
    return the median in that case.
    """

    num_list.sort()  # sorts list of integers numerically
    if (len(num_list)) % 2 != 0:
        return num_list[len(num_list) // 2]
    else:
        return (num_list[len(num_list) // 2-1] + num_list[len(num_list) // 2]) / 2
