import networkx as nx
import logging

# הגדרת מערכת הלוגים
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class GraphicalCakeDivider:
    def __init__(self, graph, valuations):
        self.graph = graph
        self.valuations = valuations

    def divide(self):
        logger.info("Starting division on graph with %d nodes and %d edges",
                    self.graph.number_of_nodes(), self.graph.number_of_edges())

        if nx.is_connected(self.graph) and len(list(nx.bridges(self.graph))) == 0:
            logger.info("Graph has no bridges – using proportional division")
            return self._proportional_division()

        logger.info("Graph has bridges – using guaranteed third division")
        return self._guaranteed_third_division()

    def _proportional_division(self):
        edges = list(self.graph.edges())
        assignment = [[], []]
        Gs = [nx.Graph(), nx.Graph()]
        for G in Gs:
            G.add_nodes_from(self.graph.nodes())

        turn = 0
        for e in edges:
            logger.info("Trying to assign edge %s to agent %d", e, turn)
            Gs[turn].add_edge(*e)
            if nx.is_connected(Gs[turn]):
                assignment[turn].append(e)
                logger.info("Edge %s assigned to agent %d", e, turn)
            else:
                Gs[turn].remove_edge(*e)
                other = 1 - turn
                Gs[other].add_edge(*e)
                assignment[other].append(e)
                logger.info("Edge %s reassigned to agent %d to preserve connectivity", e, other)
            turn = 1 - turn

        for i in range(2):
            if len(assignment[i]) == 0 and len(assignment[1 - i]) > 1:
                moved_edge = assignment[1 - i].pop()
                assignment[i].append(moved_edge)
                logger.info("Moved edge %s to agent %d to prevent empty assignment", moved_edge, i)

        logger.info("Final assignment: %d edges to agent 0, %d edges to agent 1",
                    len(assignment[0]), len(assignment[1]))
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
            logger.info("Evaluating edge %s with val1=%.2f, val2=%.2f", e, val1, val2)

            if val1 >= val2:
                G1.add_edge(*e)
                if nx.is_connected(G1):
                    assignment[0].add(e)
                    logger.info("Assigned edge %s to agent 0", e)
                else:
                    G1.remove_edge(*e)
                    G2.add_edge(*e)
                    assignment[1].add(e)
                    logger.info("Edge %s reassigned to agent 1 to preserve connectivity", e)
            else:
                G2.add_edge(*e)
                if nx.is_connected(G2):
                    assignment[1].add(e)
                    logger.info("Assigned edge %s to agent 1", e)
                else:
                    G2.remove_edge(*e)
                    G1.add_edge(*e)
                    assignment[0].add(e)
                    logger.info("Edge %s reassigned to agent 0 to preserve connectivity", e)

        logger.info("Final assignment: %d edges to agent 0, %d edges to agent 1",
                    len(assignment[0]), len(assignment[1]))

        return [list(assignment[0]), list(assignment[1])]
