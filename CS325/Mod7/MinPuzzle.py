# Author: Kevin Sekuj
# Date: 2/21/2022
# Description: Implementation of Min Puzzle using a graph traversal algorithm

import heapq


def minEffort(puzzle: list) -> int:
    """
    Dijkstras algorithm implementation for solving the min effort puzzle.

    :param puzzle: 2D matrix containing cells of a given height (positive)
    :return: int, min effort of route to bottom right cell (maximum abs difference)
    """

    # initialize boundaries, destination cell, and array of neighboring cells
    rows, cols = len(puzzle), len(puzzle[0])
    end = rows - 1, cols - 1
    neighbors = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # initialize set so we don't traverse onto nodes we've already visited
    seen = set()

    # keep a running minimum effort variable, and initialize a heap with
    # the current effort for that iteration, as well as "m" and "n" positions on the matrix
    minimum_effort = 0
    heap = [(0, 0, 0)]

    while heap:
        # pop our current effort and position, add it to seen
        current_effort, m, n = heapq.heappop(heap)
        seen.add((m, n))

        # calculate our running minimum and return if at bottom right cell
        minimum_effort = max(minimum_effort, current_effort)
        if (m, n) == end:
            return minimum_effort

        # else continue dijkstra on valid neighboring cells
        for x, y in neighbors:
            new_m = m + x
            new_n = n + y
            if new_m >= rows or new_m < 0 or new_n >= cols or new_n < 0 or (new_m, new_n) in seen:
                continue

            effort = abs(puzzle[new_m][new_n] - puzzle[m][n])
            heapq.heappush(heap, (effort, new_m, new_n))

    return minimum_effort


if __name__ == "__main__":
    print(minEffort([[1, 3, 5], [2, 8, 3], [3, 4, 5]]))
