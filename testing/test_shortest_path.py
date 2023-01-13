from typing import Tuple, List, Dict
from unittest import TestCase
from shortest_path import Solution


class TestSolution(TestCase):
    edges = [
        ('A', 'B', 12), ('A', 'F', 16), ('A', 'G', 14),
        ('B', 'C', 10), ('B', 'F', 7),
        ('G', 'F', 9), ('G', 'E', 8),
        ('F', 'C', 6), ('F', 'E', 2),
        ('C', 'D', 3),
        ('C', 'E', 5),
        ('E', 'D', 4),
        ('X', 'Y', 5),
    ]

    @staticmethod
    def gen_graph(edges: List[Tuple[str, str, int]]) -> Dict[str, Dict[str, int]]:
        graph: Dict[str, Dict[str, int]] = {}
        for n1, n2, distance in edges:
            if n1 not in graph:
                graph[n1] = {n2: distance}
            if n2 not in graph:
                graph[n2] = {}
            graph[n1].update({n2: distance})
            graph[n2].update({n1: distance})
        return graph

    def test_dijkstra(self):
        graph = self.gen_graph(self.edges)
        print(graph)
        solution = Solution()
        result = solution.dijkstra(graph, 'A')
        print(result)
        result = solution.dijkstra(graph, 'D')
        print(result)
        # self.fail()
