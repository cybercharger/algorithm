import heapq
from typing import Dict


class Solution:
    INT_MAX = 0x7ffffffff

    def dijkstra(self, graph: Dict[str, Dict[str, int]], vertex: str) -> Dict[str, int]:
        if vertex not in graph:
            return dict()
        result = {vertex: 0}
        # TODO: use priority queue for this
        not_visited = {n: graph[vertex][n] if n in graph[vertex] else self.INT_MAX for n in graph}
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
        # every element in heap is [distance_from_target, vertex_name],
        # TC: O(V)
        heap = [[graph[target][v] if v in graph[target] else self.INT_MAX, v, 0] for v in graph if v != target]
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
            # tail element will be moved to head after popping up, and flipped down to make the heap valid again
            # all other elements will be flipped only once except the tail elm, hence,
            # the index of flipped elm is the original index of it,
            # just following the index down until a non-flipped elm found or reaching the leaf elm
            idx = 0
            # TC: V * logV
            while len(heap) > idx != heap[idx][2]:
                heap[idx][2], idx = idx, heap[idx][2]

            min_dis, picked = entry[0], entry[1]

            result[picked] = min_dis
            del to_visit[picked]
            # update result

            # TC: E * logV
            for vertex, dis in graph[picked].items():
                if vertex in to_visit and to_visit[vertex][0] > min_dis + dis:
                    entry = to_visit[vertex]
                    entry[0] = min_dis + dis

                    # since heap is maintained, just bubbling up the changed value to proper position will keep the heap valid
                    cur = entry[2]
                    while cur > 0:
                        parent = (cur - 1) // 2
                        if heap[cur][0] >= heap[parent][0]:
                            break
                        heap[cur], heap[parent] = heap[parent], heap[cur]
                        heap[cur][2], heap[parent][2] = cur, parent
                        cur = parent

        return result
