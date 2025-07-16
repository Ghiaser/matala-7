from flask import Flask, render_template, request
import networkx as nx
import random
from algorithm import GraphicalCakeDivider

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/run", methods=["POST"])
def run():
    mode = request.form.get("mode")

    if mode == "random":
        G = nx.erdos_renyi_graph(6, 0.5)
        val0 = {}
        val1 = {}
        for e in G.edges():
            e = (min(e), max(e))
            val0[e] = round(random.uniform(0, 1), 2)
            val1[e] = round(random.uniform(0, 1), 2)
    else:
        G = nx.cycle_graph(4)
        val0 = {(0, 1): 0.3, (1, 2): 0.3, (2, 3): 0.2, (3, 0): 0.2}
        val1 = {(0, 1): 0.2, (1, 2): 0.2, (2, 3): 0.3, (3, 0): 0.3}

    divider = GraphicalCakeDivider(G, [val0, val1])
    result = divider.divide()
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
