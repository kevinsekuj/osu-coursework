# Author: Kevin Sekuj
# Date: 3/1/2022
# Description: Implementation of Prim's algorithm to find a minimum spanning tree


import heapq
from collections import defaultdict


def Prims(G):
    """
    Prims algorithm implementation using a minheap.

    :param G: input matrix
    :return: [(source node, destination node, edge cost)], total MST cost
    """

    # convert adjacency matrix to adjacency list
    adj = convert_adjacency(G)

    heap, edges, result = [[0, 0, None]], [], 0
    visit = set()

    while len(visit) < len(G):
        cost, cur_node, src_node = heapq.heappop(heap)
        if cur_node in visit:
            continue

        result += cost
        visit.add(cur_node)

        if src_node is not None:
            edges.append((src_node, cur_node, cost))

        # go through node's neighbors in adj list
        for neighbor_cost, nei in adj[cur_node]:
            # skip nodes we've already seen
            if nei not in visit:
                heapq.heappush(heap, [neighbor_cost, nei, cur_node])

    return edges, result


def convert_adjacency(matrix):
    """
    Helper function for converting input adjacency matrix into an adjacency
    list
    """
    adj = defaultdict(list)
    rows, cols = len(matrix), len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j]:
                # (cost, source, destination)
                adj[i].append((matrix[i][j], j))
    return adj


if __name__ == '__main__':
    G = [[0, 9, 75, 0, 0],
         [9, 0, 95, 19, 42],
         [75, 95, 0, 51, 66],
         [0, 19, 51, 0, 31],
         [0, 42, 66, 31, 0]]
    print(Prims(G))
