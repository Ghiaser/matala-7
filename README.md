# FairGraphDivider — Performance Evaluation

This project extends the FairGraphDivider algorithm by adding a performance benchmark and an optimized implementation, as required by the final assignment: "שיפור ביצועים – מטלת פייתון".


##  Experiment Description

The file `experiments.py` benchmarks two methods:

1. `GraphicalCakeDivider` — the original algorithm from algorithm.py  
2. `FastGraphicalCakeDivider` — an improved version with precomputed edge values

Each algorithm is evaluated on:

- Varying graph sizes (n = 10 to 50)  
- Average runtime  
- Value per agent  
- Minimum fairness (min value between agents)

Results are saved in CSV and shown in graphs.

##  Running the Benchmark

1. Install required libraries:
pip install matplotlib pandas networkx

2. Run the experiment script:
 python experiments/experiments.py   

3. This generates:
- results.csv  
- plot_runtime.png  
- plot_min_fairness.png

  
 4.run test
  python test_improved.py


## ⚙️ Improvements Made

The optimized algorithm (`FastGraphicalCakeDivider`) improves performance by:

- Precomputing edge values for each agent  
- Avoiding redundant value calculations during division  

The division strategy remains identical to the original (based on Section 4 of the paper).


