from typing import Dict, List, Set, Tuple

from backend.app.domain.edge import Edge
from backend.app.domain.node import Node


class Graph:
    """
    Simple undirected graph with adjacency list.
    Nodes are identified by string ids.
    """

    def __init__(self) -> None:
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.adj: Dict[str, Set[str]] = {}
        self._edge_keys: Set[Tuple[str, str]] = set()

    def add_node(self, node: Node) -> None:
        node_id = node.id
        if node_id not in self.nodes:
            self.nodes[node_id] = node
            self.adj[node_id] = set()
            return
        existing = self.nodes[node_id]
        if (existing.label is None or existing.label == "") and node.label:
            self.nodes[node_id] = Node(node_id, node.label)

    def add_edge(self, edge: Edge) -> None:
        if edge.source_id == edge.target_id:
            return
        key = edge.key()
        if key in self._edge_keys:
            return
        self._edge_keys.add(key)
        self.add_node(Node(edge.source_id))
        self.add_node(Node(edge.target_id))
        self.edges.append(edge)
        self.adj[edge.source_id].add(edge.target_id)
        self.adj[edge.target_id].add(edge.source_id)

    def has_node(self, node_id: str) -> bool:
        return node_id in self.nodes

    def neighbors(self, node_id: str) -> Set[str]:
        return self.adj.get(node_id, set())

    def degree(self, node_id: str) -> int:
        return len(self.adj.get(node_id, set()))

    def node_ids(self) -> List[str]:
        return list(self.nodes.keys())
