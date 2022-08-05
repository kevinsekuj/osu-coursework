# Author: Kevin Sekuj
# Date: 11/11/20
# Description: Program which takes a list of numbers as a parameter and
# reverses the order of the elements without using slicing. Rather, it
# moves through the first list element to the last element of the list,
# and iterates progressively inwards swapping the elements at either end each time.

def reverse_list(num_list):
    """
    function which reverses the order values on either end of a list
    progressively inwards until it produces a reversed list.
    """
    swap_one = 0  # to get first list element
    swap_two = len(num_list) - 1  # to get last list element
    while swap_one < swap_two:
        temp_var = num_list[swap_one]  # temp variable to store first list element
        num_list[swap_one] = num_list[swap_two]  # swaps first and last element
        # sets last element to temp var, which has stored the first element
        # producing an order "swap" without using slicing
        num_list[swap_two] = temp_var
        swap_one += 1  # moves on to the next element
        swap_two -= 1  # moves inwards from the last element
