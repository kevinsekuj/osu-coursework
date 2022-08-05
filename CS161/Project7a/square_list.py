# Author: Kevin Sekuj
# Date: 11/10/20
# Description: Program which takes a list of numbers as a parameter and
# replaces each value with a square of that value.

def square_list(num_list):
    """
    iterates through the list of numbers using a range function
    and replacing the values with their squares.
    """
    for num in range(len(num_list)):
        num_list[num] = num_list[num] * num_list[num]
