from flask import Flask, render_template, request
import networkx as nx
import random
import logging
from contiguous_labeling import contiguous_oriented_labeling

# Configure logging
logging.basicConfig(filename='logs.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def parse_edges(text):
    edges = []
    for line in text.strip().splitlines():
        parts = line.strip().split()
        if len(parts) == 2:
            u, v = parts
            edges.append((u, v))
    return edges

def parse_vertex_valuation(text):
    val = {}
    for line in text.strip().splitlines():
        parts = line.strip().split()
        if len(parts) == 2:
            node, value = parts
            val[node] = float(value)
    return val

def generate_random_graph(num_nodes=5, prob=0.5):
    G = nx.erdos_renyi_graph(num_nodes, prob)
    while not nx.is_connected(G):
        G = nx.erdos_renyi_graph(num_nodes, prob)
    G = nx.relabel_nodes(G, lambda x: str(x))
    return G

def generate_random_vertex_valuations(G):
    val1 = {}
    val2 = {}
    for v in G.nodes():
        val1[v] = round(random.uniform(0, 1), 2)
        val2[v] = round(random.uniform(0, 1), 2)
    return val1, val2

def divide_by_vertex_valuation(G, val1, val2):
    labeling = contiguous_oriented_labeling(G)
    if labeling is None:
        return None

    ordered_edges = [(u, v) for _, u, v in labeling]
    total1 = sum(val1.get(u, 0) + val1.get(v, 0) for u, v in ordered_edges)
    total2 = sum(val2.get(u, 0) + val2.get(v, 0) for u, v in ordered_edges)

    sum1 = sum2 = 0
    part1 = []

    for u, v in ordered_edges:
        part1.append((u, v))
        sum1 += val1.get(u, 0) + val1.get(v, 0)
        sum2 += val2.get(u, 0) + val2.get(v, 0)
        if sum1 >= total1 / 2 or sum2 >= total2 / 2:
            break

    part2 = [e for e in ordered_edges if e not in part1]

    # Visualize the ordering of the edges
    return part1, part2, ordered_edges  # Add ordered_edges for visualization

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    edges_text = ''
    val1_text = ''
    val2_text = ''
    ordered_edges = []

    if request.method == "POST":
        mode = request.form.get("mode")

        try:
            if mode == "manual":
                edges_text = request.form.get("edges", "")
                val1_text = request.form.get("val1", "")
                val2_text = request.form.get("val2", "")
                edges = parse_edges(edges_text)
                val1 = parse_vertex_valuation(val1_text)
                val2 = parse_vertex_valuation(val2_text)
                G = nx.Graph()
                G.add_edges_from(edges)

            elif mode == "random":
                G = generate_random_graph()
                val1, val2 = generate_random_vertex_valuations(G)
                edges = list(G.edges())
                edges_text = "\n".join(f"{u} {v}" for u, v in edges)
                val1_text = "\n".join(f"{v} {val1[v]}" for v in G.nodes())
                val2_text = "\n".join(f"{v} {val2[v]}" for v in G.nodes())

            else:
                raise ValueError("מצב לא חוקי.")

            # ✅ קודם נבדוק אם הפונקציה לא החזירה None
            result_tuple = divide_by_vertex_valuation(G, val1, val2)
            if result_tuple is None:
                raise ValueError("לא ניתן לתייג את הגרף או לבצע חלוקה הוגנת.")

            group1, group2, ordered_edges = result_tuple

            result = "תוצאה:\n"
            result += "\nסוכן 1:\n" + "\n".join(
                f"{u} - {v} (ערך: {val1.get(u, 0)+val1.get(v, 0):.2f})" for u, v in group1)
            result += "\n\nסוכן 2:\n" + "\n".join(
                f"{u} - {v} (ערך: {val2.get(u, 0)+val2.get(v, 0):.2f})" for u, v in group2)

        except Exception as e:
            error = f"שגיאה: {str(e)}"
            logger.error("Error during processing: %s", str(e))

    return render_template(
        "index.html",
        result=result,
        error=error,
        edges_text=edges_text,
        val1_text=val1_text,
        val2_text=val2_text,
        ordered_edges=ordered_edges
    )


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5050)
