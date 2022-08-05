# Course: CS261 - Data Structures
# Author: Kevin Sekuj
# Assignment: Undirected and Directed Graphs
# Description: Implementation of a directed graph and its methods including dijkstra's
# algorithm.

import heapq

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adding a new vertex to the graph, where the first index created will be
        assigned index 0, with subsequent vertices being 1, 2, 3, etc.
        """
        self.adj_matrix.append([0 for _ in range(self.v_count)])

        for vertex in self.adj_matrix:
            vertex.append(0)

        self.v_count += 1
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Method for adding a new edge to the graph. If either or both indices don't
        exist in the graph or if weight isn't positive, or src and dst refer
        to the same vertex, the method returns.
        """
        if weight < 1:
            return
        if src == dst:
            return
        if src > len(self.adj_matrix) - 1 or dst > len(self.adj_matrix) - 1:
            return
        if src < 0 or dst < 0:
            return

        self.adj_matrix[src][dst] = weight

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removing an edge between two vertices with provided indices. If either
        or both vertex do not exist in the graph or no edge exists between
        them, the method does nothing.
        """
        if src < 0 or dst < 0:
            return

        if src > len(self.adj_matrix) - 1 or dst > len(self.adj_matrix) - 1:
            return

        if src == dst:
            return

        self.adj_matrix[src][dst] = 0

    def get_vertices(self) -> []:
        """
        Returns an array containing vertices in the graph.
        """
        return [vertices for vertices in range(self.v_count)]

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph as a tuple of two incident vertices
        and weight.
        """
        edges = []
        for i in range(self.v_count):
            for j in range(self.v_count):
                if self.adj_matrix[i][j] > 0:
                    weight = self.adj_matrix[i][j]

                    edges.append((i, j, weight))
        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list of vertices and determines whether the sequence of the vertices
        represents a valid path in the graph, an empty path is also considered valid.
        """
        if len(path) == 0:
            return True

        for i in range(len(path) - 1):
            v = path[i]
            v_adj = path[i + 1]

            if self.adj_matrix[v][v_adj] == 0:
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        DFS implementation using pseudocode from the module readings. Returns a
        list of vertices visited during the search in the order they were visited.
        Returns an empty list if Vstart is not on the list, and breaks when the
        end vertex is reached.
        """
        if v_start not in self.get_vertices():
            return []

        stack = [v_start]
        visited = []
        vi = 0
        vn = 1

        while len(stack) > 0:
            v = stack.pop()

            if v not in visited:
                visited.append(v)

                neighbors = []
                for i in range(len(self.get_edges())):
                    if v == self.get_edges()[i][vi]:
                        neighbors.append(self.get_edges()[i][vn])

                neighbors.sort(reverse=True)
                for i in neighbors:
                    stack.append(i)

            if v == v_end:
                break

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        Implementation of BFS for directed graph working along the same lines as
        DFS with specific BST properties such as use of a queue.
        """
        if v_start not in self.get_vertices():
            return []

        queue = [v_start]
        visited = []
        vi = 0
        vn = 1

        while len(queue) > 0:
            v = queue.pop(0)

            if v not in visited:
                visited.append(v)

                neighbors = []
                for i in range(len(self.get_edges())):
                    if v == self.get_edges()[i][vi]:
                        neighbors.append(self.get_edges()[i][vn])

                neighbors.sort(reverse=False)
                for i in neighbors:
                    queue.append(i)

            if v == v_end:
                break

        return visited

    def has_cycle(self) -> bool:
        """
        Cycle implementation which returns  True if a cycle is detected in the graph,
        returning false otherwise. Algorithm adopted from extra module readings graph
        traversal.
        """
        # vertices which are not processed
        white = set()
        # vertices currently processed w DFS
        grey = set()
        # vertices which DFS is completed, assigning vertices black
        black = set()

        for i in range(len(self.adj_matrix)):
            white.add(i)

        while len(white) > 0:
            i = white.pop()
            if self.cycle_helper(i, white, grey, black):
                return True

        return False

    def cycle_helper(self, v, white, grey, black) -> bool:
        """
        Helper method for detecting cycles within directed graph.
        """
        white.discard(v)
        grey.add(v)
        for i in range(len(self.adj_matrix[v])):
            va = self.adj_matrix[v][i]

            if va != 0:
                if i in grey:
                    return True

                if i in black:
                    continue

                if self.cycle_helper(i, white, grey, black):
                    return True

        grey.remove(v)
        black.add(v)

        return False

    def dijkstra(self, src: int) -> []:
        """
        Implementation of Dijkstra's algorithm to compute the length of the
        shortest  path from a given vertex to other vertices in the graph,
        returning a list of one value per each vertex in the graph.
        If a vertex is not reachable from src, it should return infinity.
        Uses a priority que ADT.
        """
        visited = {}
        heap = []

        # dst src
        heapq.heappush(heap, (0, src))

        while len(heap) != 0:
            # unpack dist and source
            vd, v = heapq.heappop(heap)
            if v not in visited:
                visited[v] = vd

                neighbors = []
                for i in range(len(self.get_edges())):
                    if v == self.get_edges()[i][0]:
                        neighbors.append(self.get_edges()[i][1])

                for neighbor in neighbors:
                    di = self.adj_matrix[v][neighbor]
                    heapq.heappush(heap, (vd + di, neighbor))

        out = []
        for _ in range(len(self.adj_matrix)):
            out.append(float('inf'))

        for key in visited:
            out[key] = visited[key]
        return out


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))

    #
    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
