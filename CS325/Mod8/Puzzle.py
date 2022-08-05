# Author: Kevin Sekuj
# Date: 3/1/2022
# Description: Apply graph traversal to solve a problem

from collections import deque


def solve_puzzle(Board, Source, Destination):
    """
    BFS algorithm to compute the shortest path from a given start cell to a
    given destination cell, ignoring barrier cells marked by #.
    """
    start_x, start_y = Source
    rows, cols = len(Board), len(Board[0])

    # initialize set to keep track of visited positions, and an array of tuples
    # so we can easily BFS onto our neighbors and keep track of our path so far
    seen = set()
    neighbors = [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'D'), (-1, 0, 'U')]

    if not Board:
        return None

    if Source == Destination:
        return 0

    def bfs(i, j):
        # (pos_x, pos_y), distance, [path]
        queue = deque([((i, j), 0, [])])
        while queue:
            coord, dist, path = queue.popleft()
            x, y = coord

            if coord == Destination:
                return dist-1, ''.join(path)

            for nei in neighbors:
                new_x, new_y = x + nei[0], y + nei[1]

                # check if this neighbor is out of bounds or a barrier cell
                if new_x >= rows or new_x < 0 or new_y >= cols or new_y < 0 or\
                        (new_x, new_y) in seen or Board[new_x][new_y] == '#':
                    continue

                seen.add((new_x, new_y))
                queue.append(((new_x, new_y), dist + 1, path + [nei[-1]]))

    return bfs(start_x, start_y) or None


if __name__ == '__main__':
    game_board = [
        ['-', '-', '-', '-', '-'],
        ['-', '-', '#', '-', '-'],
        ['-', '-', '-', '-', '-'],
        ['#', '-', '#', '#', '-'],
        ['-', '#', '-', '-', '-']
    ]
    print(solve_puzzle(game_board, (0, 2), (2, 2)))
    print(solve_puzzle(game_board, (0, 0), (4, 4)))
    print(solve_puzzle(game_board, (0, 2), (3, 1)))
    print(solve_puzzle(game_board, (4, 2), (3, 1)))
    print(solve_puzzle(game_board, (1, 1), (5, 1)))
    print(solve_puzzle(game_board, (3, 2), (3, 3)))
    print(solve_puzzle(game_board, (0, 0), (0, 0)))


