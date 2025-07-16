import networkx as nx

class GraphicalCakeDivider:
    def __init__(self, graph, valuations):
        self.graph = graph
        self.valuations = valuations

    def divide(self):
        if nx.is_connected(self.graph) and len(list(nx.bridges(self.graph))) == 0:
            return self._proportional_division()
        return self._guaranteed_third_division()

    def _proportional_division(self):
        edges = list(self.graph.edges())
        assignment = [[], []]
        Gs = [nx.Graph(), nx.Graph()]
        for G in Gs:
            G.add_nodes_from(self.graph.nodes())

        turn = 0
        for e in edges:
            Gs[turn].add_edge(*e)
            if nx.is_connected(Gs[turn]):
                assignment[turn].append(e)
            else:
                Gs[turn].remove_edge(*e)
                other = 1 - turn
                Gs[other].add_edge(*e)
                assignment[other].append(e)
            turn = 1 - turn

        # Ensure no agent gets empty set
        for i in range(2):
            if len(assignment[i]) == 0 and len(assignment[1 - i]) > 1:
                assignment[i].append(assignment[1 - i].pop())

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
