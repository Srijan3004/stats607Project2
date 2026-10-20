import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from dgps import generate_freedman_population, generate_nonlinear_population, randomize_treatment
from methods import calc_true_delta, estimate_effects
from simulation import run_simulation

def test_dgp_expected_properties():
    """
    Check 1: DGP verification.
    Validates that the generated data matches the theoretical probabilities 
    stated in Freedman Section 5.
    """
    n_large = 100000 
    Z, Y_C, Y_T = generate_freedman_population(n_large, seed=123)
    
    # 1. P(U_i > 1/2) = 0.5. So expected success in control is ~0.5
    assert np.isclose(np.mean(Y_C), 0.5, atol=0.01), "Control success rate deviates from 0.5"
    
    # 2. P(U_i + V_i > 3/4) = 1 - P(U_i+V_i < 0.75) = 1 - (0.5 * 0.75^2) = 23/32 = 0.71875
    assert np.isclose(np.mean(Y_T), 23/32, atol=0.01), "Treatment success rate deviates from 23/32"

def test_method_correctness():
    """
    Check 2: Method correctness.
    Recovers true values in a simple case where we can calculate ITT by hand.
    """
    # Create a dummy dataset: 4 assigned to Treatment, 4 to Control
    X = np.array([1, 1, 1, 1, 0, 0, 0, 0])
    
    # Treatment has 2 successes (50% rate). Control has 1 success (25% rate).
    Y_obs = np.array([1, 1, 0, 0, 1, 0, 0, 0])
    
    # Covariate Z (set to 0 to neutralize for ITT check)
    Z = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    
    beta_hat_2, plugin_delta, itt_delta = estimate_effects(X, Z, Y_obs)
    
    # Manual ITT calculation: log(0.5 / 0.5) - log(0.25 / 0.75)
    # 0 - (-1.098612) = 1.098612
    expected_itt = np.log(0.5 / (1 - 0.5)) - np.log(0.25 / (1 - 0.25))
    
    assert np.isclose(itt_delta, expected_itt), f"Expected ITT {expected_itt}, got {itt_delta}"

def test_reproducibility():
    """
    Check 3: Reproducibility check.
    Ensures that identical seeds yield strictly identical DGP arrays and random assignments.
    """
    # 1. Check DGP reproducibility
    Z1, Y_C1, Y_T1 = generate_freedman_population(500, seed=42)
    Z2, Y_C2, Y_T2 = generate_freedman_population(500, seed=42)
    
    np.testing.assert_array_equal(Z1, Z2, err_msg="Covariates Z differ despite same seed")
    np.testing.assert_array_equal(Y_C1, Y_C2, err_msg="Y_C differs despite same seed")
    np.testing.assert_array_equal(Y_T1, Y_T2, err_msg="Y_T differs despite same seed")
    
    # 2. Check Treatment Assignment reproducibility
    X1, Y_obs1 = randomize_treatment(Y_C1, Y_T1, p_treat=0.75, seed=99)
    X2, Y_obs2 = randomize_treatment(Y_C2, Y_T2, p_treat=0.75, seed=99)
    
    np.testing.assert_array_equal(X1, X2, err_msg="Treatment assignments differ despite same seed")
    np.testing.assert_array_equal(Y_obs1, Y_obs2, err_msg="Observed Y differs despite same seed")
if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main(["-v", __file__]))
