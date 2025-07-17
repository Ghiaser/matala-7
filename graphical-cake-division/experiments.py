import networkx as nx
import csv
import time
from algorithm import GraphicalCakeDivider
import random


def generate_random_graph(num_nodes=6, prob=0.5):
    G = nx.erdos_renyi_graph(num_nodes, prob)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(num_nodes, prob)
    return G


def generate_random_valuations(G):
    val1 = {}
    val2 = {}
    for u, v in G.edges():
        key = (min(u, v), max(u, v))
        val1[key] = round(random.uniform(0, 1), 2)
        val2[key] = round(1.0 - val1[key], 2)
    return val1, val2


def run_experiments(num_runs=100, num_nodes=6, prob=0.5, output_file="results.csv"):
    with open(output_file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Run", "NumNodes", "NumEdges", "BridgeFree",
            "TimeSeconds", "ValueAgent1", "ValueAgent2"
        ])

        for i in range(num_runs):
            G = generate_random_graph(num_nodes, prob)
            val1, val2 = generate_random_valuations(G)
            divider = GraphicalCakeDivider(G, [val1, val2])

            start = time.time()
            division = divider.divide()
            end = time.time()
            elapsed = round(end - start, 4)

            total1 = sum(val1.get((min(u, v), max(u, v)), 0) for u, v in division[0])
            total2 = sum(val2.get((min(u, v), max(u, v)), 0) for u, v in division[1])

            bridge_free = int(nx.is_connected(G) and len(list(nx.bridges(G))) == 0)

            writer.writerow([
                i + 1, len(G.nodes()), len(G.edges()), bridge_free,
                elapsed, round(total1, 3), round(total2, 3)
            ])

    print(f" {num_runs} runs completed. Results saved to {output_file}")


if __name__ == "__main__":
    run_experiments(num_runs=100, num_nodes=8, prob=0.5)
