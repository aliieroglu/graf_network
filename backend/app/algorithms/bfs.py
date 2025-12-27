from collections import deque
from typing import List

from backend.app.algorithms.base import Algorithm, AlgorithmResult
from backend.app.domain.graph import Graph


class BFSAlgorithm(Algorithm):
    def run(self, graph: Graph, start_id: str) -> AlgorithmResult:
        if not graph.has_node(start_id):
            raise ValueError("Start node not found")

        visited = set()
        order: List[str] = []
        queue: deque[str] = deque([start_id])
        visited.add(start_id)

        while queue:
            current = queue.popleft()
            order.append(current)
            for neighbor in graph.neighbors_sorted_by_weight(current, descending=True):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return AlgorithmResult(order=order)
