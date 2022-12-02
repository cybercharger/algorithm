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
