import networkx as nx

class GraphicalCakeDivider:
    def __init__(self, graph, valuations):
        self.graph = graph
        self.valuations = valuations

    def divide(self):
        if nx.is_connected(self.graph) and nx.bridges(self.graph) == []:
            return self._proportional_division()
        return self._guaranteed_third_division()

    def _proportional_division(self):
        edges = list(self.graph.edges())
        assignment = [[], []]
        turn = 0
        for e in edges:
            assignment[turn].append(e)
            turn = 1 - turn
        return assignment

    def _guaranteed_third_division(self):
        edges = list(self.graph.edges())
        sorted_edges = sorted(
            edges,
            key=lambda e: self.valuations[0].get((min(e), max(e)), 0) +
                          self.valuations[1].get((min(e), max(e)), 0),
            reverse=True
        )
        assignment = [set(), set()]
        G1 = nx.Graph()
        G2 = nx.Graph()
        G1.add_nodes_from(self.graph.nodes())
        G2.add_nodes_from(self.graph.nodes())

        for e in sorted_edges:
            val1 = self.valuations[0].get((min(e), max(e)), 0)
            val2 = self.valuations[1].get((min(e), max(e)), 0)
            if val1 >= val2:
                G1.add_edge(*e)
                if nx.is_connected(G1):
                    assignment[0].add(e)
                else:
                    G1.remove_edge(*e)
                    G2.add_edge(*e)
                    assignment[1].add(e)
            else:
                G2.add_edge(*e)
                if nx.is_connected(G2):
                    assignment[1].add(e)
                else:
                    G2.remove_edge(*e)
                    G1.add_edge(*e)
                    assignment[0].add(e)

        return [list(assignment[0]), list(assignment[1])]
