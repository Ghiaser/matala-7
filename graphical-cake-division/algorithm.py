import networkx as nx

class GraphicalCakeDivider:
    def __init__(self, graph, valuations):
        self.graph = graph
        self.valuations = valuations

    def divide(self):
        is_bridge_free = nx.is_connected(self.graph) and len(list(nx.bridges(self.graph))) == 0
        return self._proportional_division() if is_bridge_free else self._guaranteed_third_division()

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

        # דואגים שלא יהיה חלק ריק
        for i in range(2):
            if not assignment[i] and len(assignment[1 - i]) > 1:
                assignment[i].append(assignment[1 - i].pop())

        return assignment

    def _guaranteed_third_division(self):
        edges = list(self.graph.edges())
        sorted_edges = sorted(
            edges,
            key=lambda e: self.valuations[0].get(tuple(sorted(e)), 0) +
                          self.valuations[1].get(tuple(sorted(e)), 0),
            reverse=True
        )

        assignment = [set(), set()]
        Gs = [nx.Graph(), nx.Graph()]
        for G in Gs:
            G.add_nodes_from(self.graph.nodes())

        for e in sorted_edges:
            key = tuple(sorted(e))
            val1 = self.valuations[0].get(key, 0)
            val2 = self.valuations[1].get(key, 0)
            preferred = 0 if val1 >= val2 else 1
            other = 1 - preferred

            Gs[preferred].add_edge(*e)
            if nx.is_connected(Gs[preferred]):
                assignment[preferred].add(e)
            else:
                Gs[preferred].remove_edge(*e)
                Gs[other].add_edge(*e)
                assignment[other].add(e)

        return [list(assignment[0]), list(assignment[1])]
