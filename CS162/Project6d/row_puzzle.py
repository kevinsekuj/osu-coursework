# Author: Kevin Sekuj
# Date: 2/2/21
# Description: Puzzle consisting of a row of squares containing non-negative integers,
# with a zero in the rightmost square. The token begins on the leftmost square, and can
# move left or right according to the value of its current index, to another index,
# as long as it doesn't move out of bounds on either end of the list.

def row_puzzle(num_list, index=0, memo=None):
    """
    Recursive function taking as parameters a list, and initializing index
    and memo to 0/None respectively. The function's base cases check if the
    index is out of bounds rightwards or leftwards, if the index is in the memo,
    or if the index is a zero that isn't the last index of the list. In those cases,
    the function call will be false. Otherwise, it passes "val" to the index param
    either adding or subtracting it to check valid positions in either direction.
    """
    if memo is None:
        memo = {}

    # if this current call is out of bounds
    if index > len(num_list) - 1 or index < 0:
        return False

    val = num_list[index]

    # account for a 1 element list where the element is not 0
    if index == len(num_list)-1 and num_list[index] != 0:
        return False

    # if the current value's index == last index of the list,
    # and if the value of the index == 0
    if index == len(num_list)-1:
        return True

    # if the position is in a loop/"stuck"
    if index in memo:
        return False

    # if at a zero that isn't the last 0 in the row
    if num_list[index] == 0:
        return False

    memo[index] = num_list[index]  # adding index to dict after successful conditional checks

    return row_puzzle(num_list, index + val, memo) or row_puzzle(num_list, index - val, memo)
