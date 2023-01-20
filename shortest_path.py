import heapq
from typing import Dict, Tuple


class Solution:
    MAX_DISTANCE = 0x7ffffffff

    def dijkstra(self, graph: Dict[str, Dict[str, int]], source: str) -> Dict[str, Tuple[int, str]]:
        if source not in graph:
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
        if source not in graph:
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
        if source not in graph:
            return dict()
        result = {v: (self.MAX_DISTANCE, source) for v in graph}
        result[source] = (0, source)
        to_visit = {v: (graph[source].get(v, self.MAX_DISTANCE), source) for v in graph if v != source}
        heap = []
        for v, d in graph[source].items():
            heapq.heappush(heap, (d, v, source))

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
