from backend.app.algorithms.base import ColoringAlgorithm, ColoringResult
from backend.app.domain.graph import Graph


class WelshPowellColoring(ColoringAlgorithm):
    def run(self, graph: Graph) -> ColoringResult:
        node_ids = graph.node_ids()
        if not node_ids:
            return ColoringResult({})

        ordered = sorted(
            node_ids,
            key=lambda node_id: (
                -graph.weighted_degree(node_id),
                -graph.degree(node_id),
                node_id,
            ),
        )
        colors = {}

        for node_id in ordered:
            used = {colors[nbr] for nbr in graph.neighbors(node_id) if nbr in colors}
            color = 0
            while color in used:
                color += 1
            colors[node_id] = color

        return ColoringResult(colors)
