# Author: Kevin Sekuj
# Date: 1/15/2021
# Description: Program with bubble sort and insertion functions that count
# the number of comparisons and exchanges made between values that are being
# sorted. A tuple containing comparisons and exchanges is then returned.

def insertion_count(count_list):
    """
    Modified insertion sort function which counts the number of comparisons and
    exchanges made when sorting a list, returning a tuple of these value.
    """
    comp_count = 0  # number of comparisons
    ex_count = 0  # number of exchanges
    for index in range(1, len(count_list)):
        value = count_list[index]
        pos = index - 1

        # while pos >= 0 and count_list[pos] > value broken up into separate
        # statements to properly reflect comparisons where two index values
        # are compared, but pos not > value. Otherwise, the statement wouldn't
        # have entered the loop at all to count the comparison. Break used to
        # avoid infinite loop.

        while pos >= 0:
            comp_count += 1
            if count_list[pos] > value:
                count_list[pos + 1] = count_list[pos]
                pos -= 1
                ex_count += 1
                count_list[pos + 1] = value
            else:
                break
    return comp_count, ex_count


def bubble_count(count_list):
    """
    Modified bubble sort which counts the number of comparisons and exchanges
    made when sorting a list, returning a tuple of these two values.
    """
    comp_count = 0  # number of comparisons
    ex_count = 0  # number of exchanges
    for pass_num in range(len(count_list) - 1):
        for index in range(len(count_list) - 1 - pass_num):
            comp_count += 1
            if count_list[index] > count_list[index + 1]:
                temp = count_list[index]
                count_list[index] = count_list[index + 1]
                count_list[index + 1] = temp
                ex_count += 1
    return comp_count, ex_count
