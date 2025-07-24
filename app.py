from flask import Flask, render_template, request, redirect, url_for
import networkx as nx
import random
import logging
from algorithm import GraphicalCakeDivider

# הגדרת לוגים לקובץ
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

def parse_edges(text):
    edges = []
    for line in text.strip().splitlines():
        parts = line.strip().split()
        if len(parts) == 2:
            u, v = map(int, parts)
            edges.append((u, v))
    return edges

def parse_valuation(text):
    val = {}
    for line in text.strip().splitlines():
        parts = line.strip().split()
        if len(parts) == 3:
            u, v, w = parts
            u, v = int(u), int(v)
            w = float(w)
            val[(min(u, v), max(u, v))] = w
    return val

def format_result(division, valuations):
    output = "חלוקת הקשתות בין הסוכנים\n"
    for i, edges in enumerate(division):
        output += f"\nסוכן {i + 1}\n"
        for e in edges:
            u, v = e
            value = valuations[i].get((min(u, v), max(u, v)), 0.0)
            output += f"קשת ({u}, {v}) – ערך: {value}\n"
    return output

def generate_random_graph(num_nodes=4, prob=0.5):
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

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        mode = request.form.get("mode")

        if mode == "manual":
            edges_text = request.form.get("edges", "")
            val1_text = request.form.get("val1", "")
            val2_text = request.form.get("val2", "")

            try:
                edges = parse_edges(edges_text)
                val1 = parse_valuation(val1_text)
                val2 = parse_valuation(val2_text)
                G = nx.Graph()
                G.add_edges_from(edges)
                divider = GraphicalCakeDivider(G, [val1, val2])
                division = divider.divide()
                result = format_result(division, [val1, val2])
                logger.info("Manual input processed successfully")
                return render_template("result.html", result=result)
            except Exception as e:
                logger.error("Error during manual input: %s", str(e))
                return render_template("index.html", error=f"שגיאה: {str(e)}")

        elif mode == "random":
            try:
                G = generate_random_graph()
                val1, val2 = generate_random_valuations(G)
                divider = GraphicalCakeDivider(G, [val1, val2])
                division = divider.divide()
                result = format_result(division, [val1, val2])
                logger.info("Random input processed successfully")
                return render_template("result.html", result=result)
            except Exception as e:
                logger.error("Error during random input: %s", str(e))
                return render_template("index.html", error=f"שגיאה: {str(e)}")

    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
        app.run(debug=True, host="0.0.0.0", port=5000)

