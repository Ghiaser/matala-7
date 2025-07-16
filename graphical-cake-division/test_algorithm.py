import networkx as nx
from algorithm import GraphicalCakeDivider

def test_cycle_graph():
    G = nx.cycle_graph(4)
    val0 = {(i, (i+1)%4): 0.25 for i in range(4)}
    val1 = {(i, (i+1)%4): 0.25 for i in range(4)}
    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()
    assert all(len(part) > 0 for part in division)

def test_single_edge_graph():
    G = nx.Graph()
    G.add_edge(0, 1)
    val0 = {(0, 1): 1.0}
    val1 = {(0, 1): 0.0}
    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()
    assert sum(len(part) for part in division) == 1

def test_path_graph():
    G = nx.path_graph(4)
    val0 = {(0, 1): 0.3, (1, 2): 0.3, (2, 3): 0.4}
    val1 = {(0, 1): 0.4, (1, 2): 0.3, (2, 3): 0.3}
    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()
    assert all(len(part) > 0 for part in division)
