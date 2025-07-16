import networkx as nx
from typing import Dict, List, Tuple

class GraphicalCakeDivider:
    def __init__(self, graph: nx.Graph, valuations: List[Dict[Tuple[int, int], float]]):
        self.graph = graph.copy()
        self.valuations = valuations  # List of dictionaries per agent
        self.num_agents = len(valuations)

    def divide(self) -> Dict[int, List[Tuple[int, int, float]]]:
        if not nx.is_connected(self.graph):
            raise ValueError("Graph must be connected")

        if not nx.has_bridges(self.graph):
            return self._proportional_division()
        else:
            return self._guaranteed_third_division()

    def _proportional_division(self) -> Dict[int, List[Tuple[int, int, float]]]:
        edges = list(self.graph.edges())
        allocation = {i: [] for i in range(self.num_agents)}
        for i, e in enumerate(edges):
            u, v = e
            e = (min(u, v), max(u, v))
            for a in range(self.num_agents):
                if e not in self.valuations[a]:
                    self.valuations[a][e] = 0.0
            agent = i % self.num_agents
            val = self.valuations[agent][e]
            allocation[agent].append((e[0], e[1], val))
        return allocation

    def _guaranteed_third_division(self) -> Dict[int, List[Tuple[int, int, float]]]:
        edges = list(self.graph.edges())
        sorted_edges = sorted(edges, key=lambda e: (self.valuations[0].get((min(e), max(e)), 0) +
                                                       self.valuations[1].get((min(e), max(e)), 0)), reverse=True)

        allocation = {0: [], 1: []}
        assigned = set()
        G0, G1 = nx.Graph(), nx.Graph()
        G0.add_nodes_from(self.graph.nodes())
        G1.add_nodes_from(self.graph.nodes())

        for e in sorted_edges:
            u, v = e
            e = (min(u, v), max(u, v))
            if e in assigned:
                continue
            val0 = self.valuations[0].get(e, 0)
            val1 = self.valuations[1].get(e, 0)
            agent = 0 if val0 >= val1 else 1
            assigned.add(e)
            (G0 if agent == 0 else G1).add_edge(*e)
            allocation[agent].append((e[0], e[1], self.valuations[agent][e]))

        return allocation
