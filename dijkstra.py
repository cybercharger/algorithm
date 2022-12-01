from typing import Dict


class Solution:
    INT_MAX = 0x7ffffffff

    def dijkstra(self, graph: Dict[str, Dict[str, int]], node: str) -> Dict[str, int]:
        if node not in graph:
            return dict()
        result = {node: 0}
        # TODO: use priority queue for this
        to_visit = {n: graph[node][n] if n in graph[node] else self.INT_MAX for n in graph.keys()}
        del to_visit[node]

        while len(to_visit) > 0:
            # get the shortest distance
            min_dis = self.INT_MAX
            picked = None
            for node, dis in to_visit.items():
                if dis <= min_dis:
                    min_dis = dis
                    picked = node

            result[picked] = min_dis
            del to_visit[picked]
            # update result
            for node, dis in graph[picked].items():
                if node in to_visit and to_visit[node] > min_dis + dis:
                    to_visit[node] = min_dis + dis

        return result
