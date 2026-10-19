import os
import numpy as np
import pandas as pd
from pathlib import Path
from dgps import generate_freedman_population, generate_nonlinear_population, randomize_treatment
from methods import calc_true_delta, estimate_effects

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "simulated"

def run_simulation(n_values=[100, 500, 1000, 5000], replicates=1000, dgp='freedman'):
    """
    Executes the Monte Carlo loops and caches output.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    
    for n in n_values:
        print(f"Running n={n} for DGP={dgp}...")
        
        # Freeze potential outcomes for the population[cite: 4]
        if dgp == 'freedman':
            Z, Y_C, Y_T = generate_freedman_population(n)
        else:
            Z, Y_C, Y_T = generate_nonlinear_population(n)
            
        true_delta = calc_true_delta(Y_C, Y_T)
        
        for rep in range(replicates):
            X, Y_obs = randomize_treatment(Y_C, Y_T, p_treat=0.75)
            beta_hat, plugin_delta, itt_delta = estimate_effects(X, Z, Y_obs)
            
            results.append({
                'n': n,
                'rep': rep,
                'True_Delta': true_delta,
                'MLE_Beta2': beta_hat,
                'Plugin_Delta': plugin_delta,
                'ITT_Delta': itt_delta
            })
            
    df = pd.DataFrame(results)
    output_file = OUTPUT_DIR / f"sim_results_{dgp}.csv"
    df.to_csv(output_file, index=False)
    print(f"Cached results to {output_file}")
    return df

if __name__ == "__main__":
    df_freedman = run_simulation(dgp='freedman')
    df_nonlinear = run_simulation(dgp='nonlinear')