import heapq
from typing import Dict, Tuple


class Solution:
    MAX_DISTANCE = 0x7ffffffff

    def dijkstra(self, graph: Dict[str, Dict[str, int]], source: str) -> Dict[str, Tuple[int, str]]:
        """

        :param graph:
        :param source: source vertex
        :return: Dict, key is the destination vertex, value is tuple (the shortest distance, previous vertex along the path)
        """
        if not graph or source not in graph:
            return dict()
        result = {source: (0, source)}
        to_visit = {v: (graph[source].get(v, self.MAX_DISTANCE), source) for v in graph if v != source}

        while to_visit:
            # get the shortest distance
            min_dis = self.MAX_DISTANCE
            picked = None
            from_v = None
            for vertex, (dis, prev) in to_visit.items():
                if dis <= min_dis:
                    min_dis = dis
                    picked = vertex
                    from_v = prev

            result[picked] = (min_dis, from_v)
            del to_visit[picked]
            # update result
            for vertex, dis in graph[picked].items():
                if vertex in to_visit and to_visit[vertex][0] > min_dis + dis:
                    to_visit[vertex] = (min_dis + dis, picked)

        return result

    def dijkstra_by_heap(self, graph: Dict[str, Dict[str, int]], source: str) -> Dict[str, Tuple[int, str]]:
        """

        :param graph:
        :param source: source vertex
        :return: Dict, key is the destination vertex, value is tuple (the shortest distance, previous vertex along the path)
        """
        if not graph or source not in graph:
            return dict()
        result = {source: (0, source)}
        # every element in heap is [distance_from_target, vertex_name, heap_idx, prev_vertex]
        # TC: O(V)
        heap = [[graph[source].get(v, self.MAX_DISTANCE), v, 0, source] for v in graph if v != source]
        # TC: O(V * logV)
        heapq.heapify(heap)

        # TC: O(V)
        for i, e in enumerate(heap):
            e[2] = i
        # {vertex_name: element_in_heap}
        to_visit = {entry[1]: entry for entry in heap}

        # TC: O(V) * ->
        while to_visit:
            # get the shortest distance
            # TC: V * logV
            entry = heapq.heappop(heap)

            # update heap element index ref
            # tail element will be moved to head after popping out the top elm, and flipped down to make the heap valid again
            # all other elements will be flipped only once except the tail elm, hence,
            # the index of flipped elm is the original index of it,
            # just following the index down until a non-flipped elm found or reaching the leaf elm
            idx = 0
            # TC: V * logV
            while len(heap) > idx != heap[idx][2]:
                heap[idx][2], idx = idx, heap[idx][2]

            min_dis, picked, prev = entry[0], entry[1], entry[3]

            result[picked] = (min_dis, prev)
            del to_visit[picked]
            # update result

            # TC: E * logV
            for vertex, dis in graph[picked].items():
                if vertex in to_visit and to_visit[vertex][0] > min_dis + dis:
                    entry = to_visit[vertex]
                    entry[0] = min_dis + dis
                    entry[3] = picked

                    # since heap is valid before the change, just bubbling up the changed value to proper position will keep the heap valid
                    cur = entry[2]
                    while cur > 0:
                        parent = (cur - 1) // 2
                        if heap[cur][0] >= heap[parent][0]:
                            break
                        heap[cur], heap[parent] = heap[parent], heap[cur]
                        heap[cur][2], heap[parent][2] = cur, parent
                        cur = parent

        return result

    def dijkstra_by_heap_v2(self, graph: Dict[str, Dict[str, int]], source: str) -> Dict[str, Tuple[int, str]]:
        """

        :param graph:
        :param source: source vertex
        :return: Dict, key is the destination vertex, value is tuple (the shortest distance, previous vertex along the path)
        """
        if not graph or source not in graph:
            return dict()
        result = {v: (self.MAX_DISTANCE, source) for v in graph}
        to_visit = {v: (self.MAX_DISTANCE, source) for v in graph}
        heap = [(0, source, source)]

        while to_visit and heap:
            min_dis, picked, prev = heapq.heappop(heap)
            if picked not in to_visit:
                continue

            del to_visit[picked]
            result[picked] = (min_dis, prev)
            for v, d in graph[picked].items():
                if v in to_visit and min_dis + d < to_visit[v][0]:
                    to_visit[v] = (min_dis + d, picked)
                    heapq.heappush(heap, (min_dis + d, v, picked))

        return result

    def bellman_ford(self, graph: Dict[str, Dict[str, int]], source: str) -> Tuple[Dict[str, Tuple[int, str]], bool]:
        """

        :param graph:
        :param source: source vertex
        :return: Dict, key is the destination vertex, value is tuple (the shortest distance, previous vertex along the path)
        """
        if not graph or source not in graph:
            return dict(), False
        result = {v: (self.MAX_DISTANCE, source) for v in graph}
        result[source] = (0, source)

        # optimization for time complexity
        # For graph as: S -> A -> B -> C -> D,  X -> Y, Y -> Z
        # 1. edges: X -> Y & Y -> Z could be ignored when calculating shortest path from S, coz they're not connected
        # 2. order of edges matters, sequence (S, A), (A, B), (B, C), (C, D) is faster than sequence (C, D), (B, C), (A, B), (S, A)
        #    coz the relaxations can happen in one iteration for sequence1 and can be stopped after 2nd iteration,
        #    while 4 iterations are needed to apply all relaxations for sequence2
        # TODO: confirm that whether edges to source can be ignored? say, negative case?
        valid_edges = []
        visited = {source}
        to_visit = [source]
        while to_visit:
            cur = to_visit.pop()
            for v, dis in graph[cur].items():
                valid_edges.append((cur, v, dis))
                if v not in visited:
                    visited.add(v)
                    to_visit.insert(0, v)

        relaxed = True
        for _ in range(len(graph.keys()) - 1):
            if not relaxed:
                break
            relaxed = False
            for u, v, dis in valid_edges:
                if result[v][0] > result[u][0] + dis:
                    result[v] = (result[u][0] + dis, u)
                    relaxed = True

        # check negative circle
        for v, edges in graph.items():
            for u, dis in edges.items():
                if result[v][0] > result[u][0] + dis:
                    return result, True

        return result, False

    def floyd_warshall(self, graph: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
        """
        Floyd-Warshall is a DP algorithm to calculate the shortest distance for every pair of vertices within the graph.
        The algorithm is not based on edges, so the shortest path cannot be backtracked directly as Dijkstra or Bellman-Ford do
        coz the other two algorithms are based on edges.
        For example:
        Given graph: A -> B -> C -> D,
        Distance(A, D) can be calculated based on Distance(A, B) + Distance(B, D) or Distance(A, C) + Distance(C, D) depending on
        how the vertices are ordered, therefore, the latest update for Distance(A, D) can be caused by vertex B, but there is no
        edge from B to D.
        :param graph: Dict, key is the source vertex, value is another Dict for edges with weight from source vertex
        :return: Dict, key is source vertex, value is Dict of the shortest distance from source to destination
        """
        if not graph:
            return dict()

        idx_map = dict()
        rev_map = []
        for i, v in enumerate(graph.keys()):
            idx_map[v] = i
            rev_map.append(v)

        dimension = len(graph.keys())

        matrix = [[self.MAX_DISTANCE if r != c else 0 for c in range(dimension)] for r in range(dimension)]

        for v, edges in graph.items():
            for u, d in edges.items():
                matrix[idx_map[v]][idx_map[u]] = d

        for k in range(dimension):
            for i in range(dimension):
                for j in range(dimension):
                    if matrix[i][j] > matrix[i][k] + matrix[k][j]:
                        matrix[i][j] = matrix[i][k] + matrix[k][j]

        result = dict()
        for r in range(dimension):
            v = rev_map[r]
            row_map = dict()
            result[v] = row_map
            for c in range(dimension):
                row_map[rev_map[c]] = matrix[r][c]

        return result
