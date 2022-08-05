# Author: Kevin Sekuj
# Date: 1/15/2021
# Description: Program with a modified insertion sort, sorting a list of strings
# instead of a list of numbers, ignoring case.

def string_sort(string_list):
    """
    Insertion sort of a list of strings, ignoring their case.
    """
    for index in range(1, len(string_list)):
        value = string_list[index]
        pos = index - 1
        while pos >= 0 and string_list[pos].lower() > value.lower():
            string_list[pos + 1] = string_list[pos]
            pos -= 1
        string_list[pos + 1] = value
