# Author: Kevin Sekuj
# Date: 2/1/21
# Description: Recursive function that takes two string parameters, and returns
# True if the first string is a subsequence of the second, meaning it's possible
# to delete 0 or more letters from the second string and derive the first string.
# Does so without using loops, vars defined outside the function, or mutable default
# args.


def is_subsequence(string_a, string_b, pos_a=-1, pos_b=-1):
    """
    Recursively checks if the letter at the last index of each string are the same.
    If so, it traverses left towards the start of the string for both strings.

    If string_a has a length less than the absolute value of the current pos_a index, it
    has been totally traversed and is a subsequence of string_b, returning True.

    If the letters don't match, only string_b traverses left on its index, and
    returns False if it has been completely traversed.
    """

    if len(string_a) < abs(pos_a):
        return True

    if len(string_b) < abs(pos_b):
        return False

    if string_a[pos_a] == string_b[pos_b]:
        return is_subsequence(string_a, string_b, pos_a - 1, pos_b - 1)

    return is_subsequence(string_a, string_b, pos_a, pos_b - 1)
