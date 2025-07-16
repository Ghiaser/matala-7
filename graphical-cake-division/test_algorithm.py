import networkx as nx
from algorithm import GraphicalCakeDivider

def test_cycle_graph():
    G = nx.cycle_graph(4)
    val0 = {(0, 1): 0.3, (1, 2): 0.3, (2, 3): 0.2, (3, 0): 0.2}
    val1 = {(0, 1): 0.2, (1, 2): 0.2, (2, 3): 0.3, (3, 0): 0.3}
    divider = GraphicalCakeDivider(G, [val0, val1])
    result = divider.divide()
    assert 0 in result and 1 in result
    assert len(result[0]) + len(result[1]) == len(G.edges())

def test_path_graph():
    G = nx.path_graph(4)
    val0 = {(0, 1): 0.3, (1, 2): 0.3, (2, 3): 0.4}
    val1 = {(0, 1): 0.4, (1, 2): 0.3, (2, 3): 0.3}
    divider = GraphicalCakeDivider(G, [val0, val1])
    result = divider.divide()
    assert 0 in result and 1 in result
    assert len(result[0]) + len(result[1]) == len(G.edges())

def test_single_edge_graph():
    G = nx.Graph()
    G.add_edge(0, 1)
    val0 = {(0, 1): 1.0}
    val1 = {(0, 1): 0.0}
    divider = GraphicalCakeDivider(G, [val0, val1])
    result = divider.divide()
    assert 0 in result or 1 in result
    total_edges = sum(len(edges) for edges in result.values())
    assert total_edges == 1
