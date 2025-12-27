import math
from typing import Optional

from backend.app.domain.graph import Graph


class WeightCalculator:
    @staticmethod
    def _metric(value: Optional[float], fallback: float = 0.0) -> float:
        if value is None:
            return fallback
        try:
            return float(value)
        except (TypeError, ValueError):
            return fallback

    @classmethod
    def calculate(cls, graph: Graph, source_id: str, target_id: str) -> float:
        source = graph.nodes.get(source_id)
        target = graph.nodes.get(target_id)
        if not source or not target:
            raise ValueError("Weight calculation requires existing nodes")

        source_activity = cls._metric(source.activity)
        target_activity = cls._metric(target.activity)
        source_interaction = cls._metric(source.interaction)
        target_interaction = cls._metric(target.interaction)

        source_connection = (
            cls._metric(source.connection_count)
            if source.connection_count is not None
            else float(graph.degree(source_id))
        )
        target_connection = (
            cls._metric(target.connection_count)
            if target.connection_count is not None
            else float(graph.degree(target_id))
        )

        diff_activity = source_activity - target_activity
        diff_interaction = source_interaction - target_interaction
        diff_connection = source_connection - target_connection

        distance = math.sqrt(
            diff_activity * diff_activity
            + diff_interaction * diff_interaction
            + diff_connection * diff_connection
        )
        return 1.0 / (1.0 + distance)
