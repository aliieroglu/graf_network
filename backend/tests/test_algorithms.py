from backend.app.algorithms.bfs import BFSAlgorithm
from backend.app.algorithms.dfs import DFSAlgorithm
from backend.app.domain.edge import Edge
from backend.app.domain.graph import Graph
from backend.app.domain.node import Node
from backend.app.domain.weight_calculator import WeightCalculator


def _build_weighted_graph() -> Graph:
    graph = Graph()
    graph.add_node(Node("A", activity=0.0, interaction=0.0, connection_count=0))
    graph.add_node(Node("B", activity=0.0, interaction=0.0, connection_count=0))
    graph.add_node(Node("C", activity=1.0, interaction=0.0, connection_count=0))
    graph.add_edge(Edge("A", "B"))
    graph.add_edge(Edge("A", "C"))
    graph.apply_weight_calculator(WeightCalculator)
    return graph


def test_bfs_prefers_higher_weight_neighbor():
    graph = _build_weighted_graph()
    result = BFSAlgorithm().run(graph, "A")
    assert result.order == ["A", "B", "C"]


def test_dfs_prefers_higher_weight_neighbor():
    graph = _build_weighted_graph()
    result = DFSAlgorithm().run(graph, "A")
    assert result.order == ["A", "B", "C"]
