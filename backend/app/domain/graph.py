from typing import Dict, List, Optional, Set, Tuple

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
        self._edge_map: Dict[Tuple[str, str], Edge] = {}

    def add_node(self, node: Node) -> None:
        node_id = node.id
        if node_id not in self.nodes:
            self.nodes[node_id] = node
            self.adj[node_id] = set()
            return
        existing = self.nodes[node_id]
        label = existing.label or node.label
        activity = node.activity if node.activity is not None else existing.activity
        interaction = node.interaction if node.interaction is not None else existing.interaction
        connection_count = (
            node.connection_count
            if node.connection_count is not None
            else existing.connection_count
        )
        self.nodes[node_id] = Node(
            node_id,
            label,
            activity=activity,
            interaction=interaction,
            connection_count=connection_count,
        )

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
        self._edge_map[key] = edge
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

    def edge_weight(self, source_id: str, target_id: str) -> Optional[float]:
        edge = self._edge_map.get(tuple(sorted((source_id, target_id))))
        if not edge:
            return None
        return edge.relation_degree

    def neighbors_sorted_by_weight(self, node_id: str, descending: bool = True) -> List[str]:
        neighbors = list(self.neighbors(node_id))
        if not neighbors:
            return []

        def sort_key(neighbor: str) -> Tuple[float, str]:
            weight = self.edge_weight(node_id, neighbor)
            weight_value = weight if weight is not None else 0.0
            weight_key = -weight_value if descending else weight_value
            return (weight_key, neighbor)

        ordered = sorted(neighbors, key=sort_key)
        return ordered

    def weighted_degree(self, node_id: str) -> float:
        total = 0.0
        for neighbor in self.neighbors(node_id):
            weight = self.edge_weight(node_id, neighbor)
            if weight is not None:
                total += weight
        return total

    def apply_weight_calculator(self, calculator) -> None:
        new_edges: List[Edge] = []
        new_edge_map: Dict[Tuple[str, str], Edge] = {}
        for edge in self.edges:
            weight = calculator.calculate(self, edge.source_id, edge.target_id)
            updated = Edge(
                edge.source_id,
                edge.target_id,
                relation_type=edge.relation_type,
                relation_degree=weight,
            )
            new_edges.append(updated)
            new_edge_map[updated.key()] = updated
        self.edges = new_edges
        self._edge_map = new_edge_map
        self._edge_keys = set(new_edge_map.keys())
