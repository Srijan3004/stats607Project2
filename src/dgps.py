import numpy as np

SEED = 1234567891

def generate_freedman_population(n, seed=None):
    """
    Replicates the DGP from Freedman (2008), Section 5.
    """
        
    U = np.random.uniform(0, 1, n)
    V = np.random.uniform(0, 1, n)
    Z = V  # Observable covariate
    
    # Potential outcomes are fixed deterministic values given U, V
    Y_C = (U > 0.5).astype(int)
    Y_T = ((U + V) > 0.75).astype(int)
    
    return Z, Y_C, Y_T

def generate_nonlinear_population(n, seed=None):
    """
    Extended simulation: Introduces a non-linear specification error.
    """
        
    Z = np.random.normal(0, 1, n)
    U = np.random.normal(0, 1, n)
    
    # Non-linear thresholding
    Y_C = (U + 0.5 * Z**2 > 1).astype(int)
    Y_T = (U + 0.5 * Z**2 + Z > 1.5).astype(int)
    
    return Z, Y_C, Y_T

def randomize_treatment(Y_C, Y_T, p_treat=0.75, seed=None):
    """
    Assigns treatment based on a (un)biased coin.
    """
        
    n = len(Y_C)
    X = np.random.binomial(1, p_treat, n)
    Y_obs = X * Y_T + (1 - X) * Y_C
    
    return X, Y_obs