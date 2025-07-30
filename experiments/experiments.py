import time
import csv
import random
import networkx as nx
import matplotlib.pyplot as plt
from contiguous_labeling import contiguous_oriented_labeling

def generate_random_connected_graph(n, p=0.5):
    while True:
        G = nx.erdos_renyi_graph(n, p)
        if nx.is_connected(G):
            return G

def generate_random_vertex_valuations(G):
    val1 = {}
    val2 = {}
    for v in G.nodes:
        val1[v] = round(random.uniform(0, 1), 2)
        val2[v] = round(random.uniform(0, 1), 2)
    return val1, val2

def edge_value(u, v, val):
    return val.get(u, 0) + val.get(v, 0)

def compute_agent_value(edges, val):
    return sum(edge_value(u, v, val) for u, v in edges)

def random_edge_partition(G):
    edges = list(G.edges())
    random.shuffle(edges)
    mid = len(edges) // 2
    return [edges[:mid], edges[mid:]]

def run_experiments(output_csv="experiments/results.csv", sizes=[10, 20, 30, 40, 50], samples=5):
    with open(output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "method", "runtime", "agent0_value", "agent1_value", "min_fairness"])

        for n in sizes:
            for _ in range(samples):
                G = generate_random_connected_graph(n)
                val1, val2 = generate_random_vertex_valuations(G)
                agents = [val1, val2]

                # Run contiguous_oriented_labeling algorithm
                start = time.time()
                labeling = contiguous_oriented_labeling(G)
                runtime = time.time() - start

                if labeling is None:
                    print(f"⚠️ Skipping graph with n={n} due to labeling failure")
                    continue

                # Convert labeling to list of edges
                edges = [(src, dst) for (_, src, dst) in labeling]
                half = len(edges) // 2
                division = [edges[:half], edges[half:]]

                val0 = compute_agent_value(division[0], val1)
                val1_val = compute_agent_value(division[1], val2)
                writer.writerow([n, "original", runtime, val0, val1_val, min(val0, val1_val)])

                # Run baseline: random partition
                start = time.time()
                rand_div = random_edge_partition(G)
                runtime_rand = time.time() - start

                val0_rand = compute_agent_value(rand_div[0], val1)
                val1_rand = compute_agent_value(rand_div[1], val2)
                writer.writerow([n, "random", runtime_rand, val0_rand, val1_rand, min(val0_rand, val1_rand)])

def plot_results(csv_file="experiments/results.csv"):
    import pandas as pd

    df = pd.read_csv(csv_file)
    grouped = df.groupby(["n", "method"]).mean().reset_index()

    for metric in ["runtime", "min_fairness"]:
        plt.figure()
        for method in grouped["method"].unique():
            sub = grouped[grouped["method"] == method]
            plt.plot(sub["n"], sub[metric], label=method)
        plt.xlabel("Number of Nodes (n)")
        plt.ylabel(metric)
        plt.title(f"{metric} vs n")
        plt.legend()
        plt.grid()
        plt.savefig(f"experiments/plot_{metric}.png")
        plt.close()

if __name__ == "__main__":
    run_experiments()
    plot_results()
    print(" Experiments completed.")
