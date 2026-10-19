import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "simulated"

def generate_summary_table(csv_path):
    """
    Generates average and SD tables.
    """
    df = pd.read_csv(csv_path).dropna()
    
    summary = df.groupby('n').agg({
        'MLE_Beta2': ['mean', 'std'],
        'Plugin_Delta': ['mean', 'std'],
        'ITT_Delta': ['mean', 'std'],
        'True_Delta': 'mean' # Constant across reps for a given n[cite: 4]
    }).round(3)
    
    return summary

def plot_asymptotics(csv_path, output_name):
    """
    Plots the convergence of the estimators as n increases.
    """
    df = pd.read_csv(csv_path).dropna()
    df_melted = df.melt(id_vars=['n', 'rep'], 
                        value_vars=['MLE_Beta2', 'Plugin_Delta', 'ITT_Delta', 'True_Delta'],
                        var_name='Estimator', value_name='Estimate')
    
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='n', y='Estimate', hue='Estimator', data=df_melted, 
                palette=['#e74c3c', '#2ecc71', '#3498db', '#2c3e50'], showfliers=False)
    
    # Add true parameter lines
    true_means = df.groupby('n')['True_Delta'].mean()
    for i, n in enumerate(sorted(df['n'].unique())):
        plt.hlines(true_means[n], i-0.4, i+0.4, color='black', linestyles='dashed', alpha=0.7)

    plt.title("Estimator Convergence: Logit Misspecification")
    plt.xlabel("Study Population Size (n)")
    plt.ylabel("Differential Log Odds")
    plt.legend(title="Method")
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"simulated/{output_name}.pdf", format='pdf', bbox_inches='tight')

if __name__ == "__main__":
    # Process the Freedman DGP
    freedman_csv = "sim_results_freedman.csv"
    summary_f = generate_summary_table(freedman_csv)
    print("Freedman DGP Summary:\n", summary_f)
    plot_asymptotics(freedman_csv, "freedman_convergence")
    
    # Process the Nonlinear DGP
    nonlinear_csv = "sim_results_nonlinear.csv"
    summary_nl = generate_summary_table(nonlinear_csv)
    print("\nNonlinear DGP Summary:\n", summary_nl)
    plot_asymptotics(nonlinear_csv, "nonlinear_convergence")