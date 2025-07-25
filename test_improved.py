import networkx as nx
import random
from performance_improvement.improved_algorithm import FastGraphicalCakeDivider

def generate_connected_graph(n):
    while True:
        G = nx.erdos_renyi_graph(n, 0.5)
        if nx.is_connected(G):
            return G

def generate_vertex_valuations(G):
    val1 = {v: round(random.uniform(0, 1), 2) for v in G.nodes()}
    val2 = {v: round(random.uniform(0, 1), 2) for v in G.nodes()}
    return [val1, val2]

def test_fast_divider_valid_partition():
    G = generate_connected_graph(10)
    agents = generate_vertex_valuations(G)
    divider = FastGraphicalCakeDivider(G, agents)
    division = divider.divide()

    # בדיקה: פלט הוא רשימה של שתי קבוצות קשתות
    assert isinstance(division, list)
    assert len(division) == 2

    # בדיקה: כל קשת מחולקת בדיוק פעם אחת
    all_edges = set(G.edges())
    div_edges = set(division[0] + division[1])
    assert all_edges == div_edges
    assert len(set(division[0]).intersection(division[1])) == 0

    print(" test_fast_divider_valid_partition passed.")

if __name__ == "__main__":
    test_fast_divider_valid_partition()
