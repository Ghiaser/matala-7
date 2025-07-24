import pytest
import networkx as nx
from algorithm import GraphicalCakeDivider
import logging

# הגדרת לוגים לבדיקה
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_cycle_graph():
    logger.info("Running test_cycle_graph")
    G = nx.cycle_graph(4)  # גרף עם 4 קודקודים בצורת מעגל
    val0 = {(i, (i + 1) % 4): 0.25 for i in range(4)}
    val1 = {(i, (i + 1) % 4): 0.25 for i in range(4)}
    # התאמת המפתחות לפורמט מסודר
    val0 = {tuple(sorted(k)): v for k, v in val0.items()}
    val1 = {tuple(sorted(k)): v for k, v in val1.items()}

    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()

    assert all(len(part) > 0 for part in division), "Each agent should receive at least one edge"
    logger.info("test_cycle_graph passed")


def test_single_edge_graph():
    logger.info("Running test_single_edge_graph")
    G = nx.Graph()
    G.add_edge(0, 1)
    val0 = {(0, 1): 1.0}
    val1 = {(0, 1): 0.5}

    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()

    total_edges = sum(len(part) for part in division)
    assert total_edges == 1
    logger.info("test_single_edge_graph passed")


def test_path_graph():
    logger.info("Running test_path_graph")
    G = nx.path_graph(3)  # קודקודים: 0-1-2
    val0 = {(0, 1): 0.4, (1, 2): 0.6}
    val1 = {(0, 1): 0.6, (1, 2): 0.4}
    val0 = {tuple(sorted(k)): v for k, v in val0.items()}
    val1 = {tuple(sorted(k)): v for k, v in val1.items()}

    divider = GraphicalCakeDivider(G, [val0, val1])
    division = divider.divide()

    total_edges = sum(len(part) for part in division)
    assert total_edges == 2
    logger.info("test_path_graph passed")
