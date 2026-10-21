# Freedman (2008) Simulation: Logit Misspecification

A lightweight, modular Python framework demonstrating the impact of specification error when applying logistic regression to randomized experimental data, 
based on David A. Freedman's 2008 paper. The simulation contrasts the biased standard Logit MLE against the asymptotically consistent Plug-in and 
Intention-to-Treat (ITT) estimators under both baseline and severe non-linear confounding.

## Project Structure

*   `src/`: Core logic (`dgps.py`, `methods.py`, `simulation.py`, `metrics.py`).
*   `tests/`: `pytest` suite for theoretical DGP check, method check, and strict reproducibility.
*   `data/`: Cached raw Monte Carlo outputs (`sim_results_*.csv`).
*   `results/`: Generated summary tables (`raw/`) and convergence plots (`figures/`).
*   `ADEMP.md`: Rewriting the full scenario in ADEMP framework

## At a glance

Ensure you have Python 3 installed, then install the dependencies:

```bash
pip install -r requirements.txt
```

Use the included `Makefile` to drive the workflow:

*   **`make all`**: Run the entire pipeline (simulations + metrics).
*   **`make simulate`**: Execute the Monte Carlo loops and cache results to `data/`.
*   **`make metrics`**: Generate summary tables and PDF convergence plots in `results/`.
*   **`make test`**: Run the unit testing suite to verify DGP math and seed reproducibility.
*   **`make clean`**: Purge all generated cache and result files.

