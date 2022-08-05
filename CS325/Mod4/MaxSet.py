# Author: Kevin Sekuj
# Date: 02-01-2022
# Description: Solve Dynamic Programming Problem and find its optimal solution.

"""
Given a list of numbers, return a subset of non-consecutive numbers
in the form of a list that would have the maximum sum.

Example 1: Input: [7,2,5,8,6]

Output: [7,5,6] (This will have sum of 18)

Example 2: Input: [-1, -1, 0]

Output: [0] (This is the maximum possible sum for this array) Example 3: Input: [-1, -1, -10, -34]
Output: [-1] (This is the maximum possible sum)
"""


def max_independent_set(nums: list) -> list:
    """
    Bottom up dynamic programming solution for max independent set. Since we
    can only return a subset of non-consecutive numbers, we build our recurrence
    relation such that dp[i] is the maximum of dp[i+1], the adjacent number, or
    dp[i+2] + dp[i] itself. We also include a special case to handle negative
    numbers.

    After filling our dp array, we perform a linear scan using two pointers to
    compare elements in the array. If dp[i] == dp[j], it indicates we skipped
    that number, otherwise we append it to the result array to get our maximum
    sum subarray of non-consecutive numbers.

    :param nums: Input array
    :return: subset of non-consecutive numbers that form the maximum sum
    """

    # build our 1 dimensional dp array
    dp = [0 for _ in range((len(nums)) + 1)]

    # fill in base case
    dp[len(nums) - 1] = nums[len(nums) - 1]

    # bottom up DP
    for i in range(len(nums) - 2, -1, -1):
        if nums[i] < 0:
            dp[i] = max(dp[i + 1], dp[i + 2])
        else:
            dp[i] = max(dp[i + 1], dp[i + 2] + nums[i])

    # compute our result array
    result = []
    i, k = 0, 0
    j = 1
    while i < len(dp) and j < len(dp):
        if dp[i] > dp[j]:
            result.append(nums[k])
            i += 2
            j += 2
            k += 2
        else:
            i += 2
            j += 2
            k += 1

    return result if result else [0]


if __name__ == "__main__":
    print(max_independent_set([7, 2, 5, 8, 6]) == [7, 5, 6])
    print(max_independent_set([-1, -1, 0]) == [0])
    print(max_independent_set([-1, -1, -10, -34]) == [-1])
