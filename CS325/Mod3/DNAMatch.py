# Author: Kevin Sekuj
# Date: 1/25/2022
# Description: Given two DNA strings find the length of the longest common string
# alignment between them (it need not be continuous). Assume empty string does not match with anything.
# Solve them with both top down and bottom up DP implementations.

def dna_match_topdown(DNA1: str, DNA2: str) -> int:
    """
    Top down implementation for longest common string alignment between two
    DNA sequences represented by strings. A hashmap is initialized to store
    subproblems, but a DP table of size m x n (length of input strings) would
    also work.

    A nested helper function is used to conduct top down dfs and have easy
    access to input params, storing subproblems in the cache.

    :param DNA1: input DNA sequence string 1
    :param DNA2: input DNA sequence string 2
    :return: longest common string alignment between DNA string sequences
    """

    cache = {}

    def dfs(i, j):
        if i == len(DNA1) or j == len(DNA2):
            return 0

        if (i, j) in cache:
            return cache[(i, j)]

        if DNA1[i] == DNA2[j]:
            cache[(i, j)] = 1 + dfs(i + 1, j + 1)

        else:
            cache[(i, j)] = max(dfs(i + 1, j), dfs(i, j + 1))

        return cache[(i, j)]

    return dfs(0, 0)


def dna_match_bottomup(DNA1: str, DNA2: str) -> int:
    """
    Bottom up implementation for longest common string alignment between two
    DNA sequences represented by strings. A DP table of size m x n is used to
    store subproblem computations.

    We compute subproblems by iterating through each string in reverse starting
    at one character, and return the 0th index in the DP table which contains
    our main problem result.

    :param DNA1: input DNA sequence string 1
    :param DNA2: input DNA sequence string 2
    :return: longest common string alignment between DNA string sequences
    """
    dp = [[0 for _ in range(len(DNA2) + 1)] for _ in range(len(DNA1) + 1)]

    for i in range(len(DNA1) - 1, -1, -1):
        for j in range(len(DNA2) - 1, -1, -1):

            if DNA1[i] == DNA2[j]:
                dp[i][j] = 1 + dp[i + 1][j + 1]

            else:
                dp[i][j] = max(dp[i][j + 1], dp[i + 1][j])

    return dp[0][0]
