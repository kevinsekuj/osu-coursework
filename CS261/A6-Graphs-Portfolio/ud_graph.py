# Course: CS261 - Data Structures
# Author: Kevin Sekuj
# Assignment: Undirected and directed graph implementation.
# Description: Implementation of an undirected graph and its methods.

import heapq
from collections import deque


class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Method which adds a new vertex to the graph. If a vertex with the same
        name is already present in the graph, the method exits with no exception.
        """
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """
        Method which adds a new edge to the graph connecting two vertices with
        provided names. If the vertices don't exist in the graph, they will be
        created and an edge made between them. If the edge exists or u==v then
        the method returns.
        """
        if u == v:
            return

        self.add_vertex(u)
        self.add_vertex(v)

        if u in self.adj_list[v] or v in self.adj_list[u]:
            return

        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def remove_edge(self, v: str, u: str) -> None:
        """
        Removes an edge between two vertices with provided names. If either
        vertex names don't exist in the graph, or no edge exists between
        them, the method exits.
        """

        if v not in self.adj_list or u not in self.adj_list:
            return

        if v in self.adj_list and u in self.adj_list[v]:
            self.adj_list[v].remove(u)

        if u in self.adj_list and v in self.adj_list[u]:
            self.adj_list[u].remove(v)

    def remove_vertex(self, v: str) -> None:
        """
        Removes a vertex and all edges incident to it from the graph. If the
        vertex doesn't exist, the method exits.
        """
        if v not in self.adj_list:
            return

        del self.adj_list[v]

        for key, value in self.adj_list.items():
            if v in value:
                self.adj_list.get(key).remove(v)

    def get_vertices(self) -> []:
        """
        Returns a list of vertices of the graph
        """
        return [i for i in self.adj_list]

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph. Each edge is returned as a tuple
        of two incident vertex names.
        """
        edges = []
        for v in self.adj_list:
            for vi in self.adj_list[v]:

                if (vi, v) not in edges:
                    edges.append((v, vi))

        return edges

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list of vertex names as parameters and returns True if the
        vertices represent a valid path in the graph. Empty paths are considered
        valid as well.
        """
        if len(path) == 0:
            return True

        if len(path) == 1 and path[0] not in self.adj_list:
            return False

        for i in range(len(path)-1):
            v = path[i+1]
            if v not in self.adj_list.get(path[i]):
                return False

        return True

    def dfs(self, v_start, v_end=None) -> []:
        """
        DFS implementation returning a list of vertices visited during
        search in the order in which they were visited. Implementation based on
        pseudocode from modules.
        """
        if v_start not in self.adj_list:
            return []

        stack = [v_start]
        visited = []

        while len(stack) != 0:
            v = stack.pop()

            if v not in visited:
                visited.append(v)

                for i in reversed(sorted(self.adj_list.get(v))):
                    stack.append(i)

            if v == v_end:
                break

        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """
        BFS implementation returning a list of vertices visited during
        search in the order in which they were visited. Implementation based on
        pseudocode from modules.
        """
        if v_start not in self.adj_list:
            return []

        queue = [v_start]
        visited = []

        while len(queue) != 0:
            v = queue.pop(0)

            if v not in visited:
                visited.append(v)

                for i in (sorted(self.adj_list.get(v))):
                    queue.append(i)

            if v == v_end:
                break
        return visited

    def count_connected_components(self):
        """
        Method which counts the number of connected components in the graph.
        """
        connected, visited = 0, []

        for i in self.adj_list:
            if i not in visited:
                visited.extend(self.dfs(i))
                connected += 1

        return connected

    def has_cycle(self):
        """
        Cycle implementation which returns true if at least one cycle exists in the
        graph, returning false otherwise if the graph is acyclic.
        """
        for i in self.get_vertices():

            if self.has_cycle_helper(i):
                return True

        return False

    def has_cycle_helper(self, vertex):
        """
        Helper method for detecting cycle within a graph, similar to DFS
        implementation but instead keeping track of neighboring vertex
        in stack as well
        """
        visited = []
        stack = [(None, vertex)]

        while len(stack) != 0:
            vi, v = stack.pop()

            if v not in visited:
                visited.append(v)

                neighbors = reversed(sorted(self.adj_list.get(v)))

                for i in neighbors:

                    if i in visited:
                        if i != vi:
                            return True

                    stack.append((v, i))

        return False

if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)

    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
