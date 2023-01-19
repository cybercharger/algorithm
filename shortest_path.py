import heapq
from typing import Dict


class Solution:
    INT_MAX = 0x7ffffffff

    def dijkstra(self, graph: Dict[str, Dict[str, int]], vertex: str) -> Dict[str, int]:
        if vertex not in graph:
            return dict()
        result = {vertex: 0}
        # TODO: use priority queue for this
        not_visited = {n: graph[vertex][n] if n in graph[vertex] else self.INT_MAX for n in graph.keys()}
        del not_visited[vertex]

        while len(not_visited) > 0:
            # get the shortest distance
            min_dis = self.INT_MAX
            picked = None
            for vertex, dis in not_visited.items():
                if dis <= min_dis:
                    min_dis = dis
                    picked = vertex

            result[picked] = min_dis
            del not_visited[picked]
            # update result
            for vertex, dis in graph[picked].items():
                if vertex in not_visited and not_visited[vertex] > min_dis + dis:
                    not_visited[vertex] = min_dis + dis

        return result

    def dijkstra_by_heap(self, graph: Dict[str, Dict[str, int]], target: str) -> Dict[str, int]:
        if target not in graph:
            return dict()
        result = {target: 0}
        # every element in heap is [distance_from_target, vertex_name]
        heap = [[graph[target][v] if v in graph[target] else self.INT_MAX, v] for v in graph.keys() if v != target]
        # {vertex_name: element_in_heap}
        not_visited = {entry[1]: entry for entry in heap}
        heapq.heapify(heap)

        while not_visited:
            # get the shortest distance
            entry = heapq.heappop(heap)
            min_dis, picked = entry[0], entry[1]

            result[picked] = min_dis
            del not_visited[picked]
            # update result
            updated = False
            for vertex, dis in graph[picked].items():
                if vertex in not_visited and not_visited[vertex][0] > min_dis + dis:
                    not_visited[vertex][0] = min_dis + dis
                    updated = True
            if updated:
                heapq.heapify(heap)

        return result
