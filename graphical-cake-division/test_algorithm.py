import networkx as nx
from algorithm import GraphicalCakeDivider

def test_cycle_graph():
    G = nx.cycle_graph(4)
    val0 = {(min(i, (i+1)%4), max(i, (i+1)%4)): 0.25 for i in range(4)}
    val1 = val0.copy()
    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()
    assert all(len(part) > 0 for part in division)
    for part in division:
        subgraph = G.edge_subgraph(part)
        assert subgraph.number_of_edges() > 0
        assert nx.is_connected(subgraph)

def test_path_graph():
    G = nx.path_graph(4)
    val0 = {(min(u, v), max(u, v)): 1 for u, v in G.edges()}
    val1 = val0.copy()
    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()
    for part in division:
        if len(part) > 0:
            subgraph = G.edge_subgraph(part)
            assert nx.is_connected(subgraph)

def test_single_edge_graph():
    G = nx.Graph()
    G.add_edge(0, 1)
    val0 = {(0, 1): 1}
    val1 = {(0, 1): 1}
    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()
    assert sum(len(part) for part in division) == 1
