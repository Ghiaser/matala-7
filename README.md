
# Graphical Cake Division 🍰

This repository hosts the **Graphical Cake Division** algorithm and a web-based interface to interact with it.

## 📚 About the Algorithm

The **Graphical Cake Division algorithm** implements a fair division protocol based on the paper:
[file:///C:/Users/ghias/Downloads/1910.14129v1%20(1)%20(1).pdf)
by Avinatan Hassidim, Shahar Dobzinski, et al.

It is designed to divide edges of a graph between two agents with individual valuations while ensuring:

- 🟢 Fairness: If the graph has no bridges, each agent gets at least ½ of their total value; otherwise, at least ⅓.
- 🔗 Connectivity: Each agent receives a connected subgraph.
- ⚙️ Efficiency: Edge values are allocated greedily based on total valuation.

## 🧠 About the Code

This project is written in Python and includes:

- `algorithm.py`: The core implementation with the `GraphicalCakeDivider` class.
- `test_algorithm.py`: A set of unit tests using `pytest` for verifying correctness.
- `app.py`: A simple Flask web server with a form-based UI.
- `templates/`: HTML templates for the web interface (index, result, about).
- `requirements.txt`: Lists required Python packages.

### Dependencies:

- Python 3.10+
- Flask
- NetworkX
- Pytest

## 🌐 Website Structure

The website includes the following features:

- Input form for a custom graph and agent valuations.
- Option to generate random connected graphs with random values.
- Clear explanation of the algorithm and its guarantees.
- Result page displaying the allocation in a readable format.

### Pages:

- `/` (index): Input form + algorithm explanation.
- `/about`: Detailed information about the paper and algorithm.
- `result.html`: Shown after submitting input.

## 🚀 Getting Started

```bash
cd graphical-cake-division
pip install -r requirements.txt
python app.py
```

Then open your browser and visit:

```
http://127.0.0.1:5000
```

## 🧪 Running Tests

```bash

 python -m pytest --verbose test_algorithm.py

```
