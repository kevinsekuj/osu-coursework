# Author: Kevin Sekuj
# Date: 3/8/2022
# Description: Implement Traveling Salesman Problem


def solve_tsp(G):
    """
    TSP implementation based on greedy approach presented in modules. We start
    at a source node (0) and check our lowest cost neighboring node. When we
    find that node, we add it to our visited set, update our current node,
    and increment our running cost.

    We walk back to our starting node to complete our cycle, so we return our
    running cost plus the cost from that end node to the start node.
    """
    source = ans = 0
    seen = {0}

    def closest_neighbor(dest, weight):
        nonlocal ans

        for nei, nei_weight in enumerate(G[source]):
            if nei in seen:
                continue

            if nei_weight < weight:
                dest, weight = nei, nei_weight

        seen.add(dest)
        ans += weight
        return dest

    while len(seen) < len(G):
        source = closest_neighbor(float('inf'), float('inf'))

    return ans + G[source][0]
