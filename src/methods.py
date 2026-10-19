import numpy as np
import statsmodels.api as sm
import warnings

def calc_true_delta(Y_C, Y_T):
    """Calculates the true population-level differential log odds."""
    alpha_T = np.mean(Y_T)
    alpha_C = np.mean(Y_C)
    
    # Handle perfect separation or zero probabilities
    if alpha_T == 0 or alpha_T == 1 or alpha_C == 0 or alpha_C == 1:
        return np.nan
        
    log_odds_T = np.log(alpha_T / (1 - alpha_T))
    log_odds_C = np.log(alpha_C / (1 - alpha_C))
    return log_odds_T - log_odds_C

def estimate_effects(X, Z, Y_obs):
    """
    Computes the standard MLE logit coefficient, the plug-in estimator,
    and the ITT estimator.
    """
    n = len(Y_obs)
    n_T = np.sum(X == 1)
    n_C = n - n_T
    
    # 1. ITT Estimator
    alpha_T_hat = np.sum(Y_obs[X == 1]) / n_T if n_T > 0 else np.nan
    alpha_C_hat = np.sum(Y_obs[X == 0]) / n_C if n_C > 0 else np.nan
    
    itt_delta = np.nan
    if 0 < alpha_T_hat < 1 and 0 < alpha_C_hat < 1:
        itt_delta = np.log(alpha_T_hat / (1 - alpha_T_hat)) - np.log(alpha_C_hat / (1 - alpha_C_hat))
    
    # 2. Logit MLE and Plug-in
    exog = sm.add_constant(np.column_stack((X, Z)))
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        try:
            model = sm.Logit(Y_obs, exog).fit(disp=0, method='newton')
            beta_hat_2 = model.params[1] # Treatment coefficient
            
            # Construct counterfactual design matrices
            exog_T = sm.add_constant(np.column_stack((np.ones_like(X), Z)), has_constant='add')
            exog_C = sm.add_constant(np.column_stack((np.zeros_like(X), Z)), has_constant='add')
            
            p_T = model.predict(exog_T)
            p_C = model.predict(exog_C)
            
            alpha_T_tilde = np.mean(p_T)
            alpha_C_tilde = np.mean(p_C)
            
            plugin_delta = np.log(alpha_T_tilde / (1 - alpha_T_tilde)) - np.log(alpha_C_tilde / (1 - alpha_C_tilde))
            
        except Exception:
            beta_hat_2 = np.nan
            plugin_delta = np.nan
            
    return beta_hat_2, plugin_delta, itt_delta