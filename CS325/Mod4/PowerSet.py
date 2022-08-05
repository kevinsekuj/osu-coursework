# Author: Kevin Sekuj
# Date: 02/01/2021
# Description: Write the implementation to solve the powerset problem discussed
# in the exercise of the exploration: Backtracking.

"""
Given a set of n distinct numbers return its power set. Write the pseudocode to return the powerset.
Example:

Input: [1,2,3]

Output: [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []]

Note: An empty set is also included in the powerset.
"""


def powerset(inputSet: list) -> list:
    """
    Takes a set of distinct numbers and returns its power set - every permutation
    of the numbers plus the empty set. Implemented with a backtracking approach.
    A subarray is constructed with each integer until we reach a solution, where
    we've hit the length of the input set. At that point, the function backtracks
    and tries to construct another solution from the previous set.

    Note: we are deep copying our answer subarrays into the result array.

    :param inputSet: set of n distinct integers
    :return: result - array containing the power set
    """
    result = []
    subarray = []

    def backtrack(i):
        """
        Nested helper function to perform dfs backtracking with access to outer
        function variables.
        """
        if i >= len(inputSet):
            result.append(subarray[:i])
            return

        subarray.append(inputSet[i])
        backtrack(i + 1)

        subarray.pop()
        backtrack(i + 1)

    backtrack(0)
    return result


if __name__ == "__main__":
    print(powerset([1, 2, 3]) == [[1, 2, 3], [1, 2], [1, 3], [1], [2, 3], [2], [3], []])
