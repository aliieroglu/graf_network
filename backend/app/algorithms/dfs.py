from typing import List

from backend.app.algorithms.base import Algorithm, AlgorithmResult
from backend.app.domain.graph import Graph


class DFSAlgorithm(Algorithm):
    def run(self, graph: Graph, start_id: str) -> AlgorithmResult:
        if not graph.has_node(start_id):
            raise ValueError("Start node not found")

        visited = set()
        order: List[str] = []
        stack = [start_id]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            order.append(current)
            neighbors = graph.neighbors_sorted_by_weight(current, descending=True)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)

        return AlgorithmResult(order=order)
