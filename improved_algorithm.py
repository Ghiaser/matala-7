import logging
from collections import defaultdict

class FastGraphicalCakeDivider:
    def __init__(self, graph, vertex_valuations):
        self.graph = graph
        self.vertex_valuations = vertex_valuations
        self.edge_values = self._precompute_edge_values()

    def _precompute_edge_values(self):
        edge_values = [defaultdict(float) for _ in range(2)]
        for u, v in self.graph.edges():
            for agent_id in range(2):
                val_u = self.vertex_valuations[agent_id].get(u, 0.0)
                val_v = self.vertex_valuations[agent_id].get(v, 0.0)
                edge_values[agent_id][(min(u, v), max(u, v))] = val_u + val_v
        return edge_values

    def divide(self):
        # Get contiguous oriented labeling from the original implementation
        from algorithm import contiguous_oriented_labeling
        directed_edges = contiguous_oriented_labeling(self.graph)

        A, B = [], []
        value_A, value_B = 0.0, 0.0

        for (u, v) in directed_edges:
            edge = (min(u, v), max(u, v))
            val0 = self.edge_values[0][edge]
            val1 = self.edge_values[1][edge]

            if value_A <= value_B:
                A.append(edge)
                value_A += val0
            else:
                B.append(edge)
                value_B += val1

        return [A, B]
