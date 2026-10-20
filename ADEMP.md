# ADEMP Framework: Logistic Misspecification Simulation

This document outlines the ADEMP (Aims, Data-generating mechanisms, Estimands, Methods, Performance measures) framework for the simulation replicating and extending Freedman (2008), *Randomization Does Not Justify Logistic Regression*.

## Aims
The goal of the paper is to evaluate the behavior, bias, and consistency of the standard logistic regression maximum likelihood estimator (MLE) when applied to randomized experimental data where the true data-generating mechanism is explicitly non-logistic.
To contrast the MLE's performance against the proposed plug-in estimator and the simple intention-to-treat (ITT) estimator under two distinct severity levels of model misspecification: a baseline threshold model and a heavily confounded non-linear model. 
Note that the baseline model was proposed in Freedman and we extended the similar simulation to a non linear model to see how it performs. 

## Data-Generating Mechanisms (DGM)
*   **Shared Design:** For both DGMs, the finite study populations are of size $n \in \{100, 500, 1000, 5000\}$. Treatment assignment is purely stochastic and independent of potential outcomes, with each subject having a 75% probability of being assigned to treatment
($ X_i \sim \text{Bernoulli}(0.75)$). 
           This assignment is randomized across 1,000 simulation replicates for each $n$.
*   **Freedman DGP (Baseline Misspecification):** 
    *   Latent variables: $U_i, V_i \sim \text{Uniform}(0, 1)$.
    *   Observable covariate: $Z_i = V_i$.
    *   Potential outcomes: Deterministic step-functions where $Y_i^C = \mathbf{1}(U_i > 0.5)$ and $Y_i^T = \mathbf{1}(U_i + V_i > 0.75)$.
*   **Nonlinear DGP (Severe Misspecification):** 
    *   Latent variables: $U_i \sim \mathcal{N}(0, 1)$ and observable covariate $Z_i \sim \mathcal{N}(0, 1)$.
    *   Potential outcomes: Deterministic thresholding with a quadratic covariate interaction, where $Y_i^C = \mathbf{1}(U_i + 0.5Z_i^2 > 1)$ and $Y_i^T = \mathbf{1}(U_i + 0.5Z_i^2 + Z_i > 1.5)$.

## Estimands
 The target parameter is the true finite-population differential log odds of success, defined non-parametrically as $\Delta = \log\frac{\alpha^T}{1-\alpha^T} - \log\frac{\alpha^C}{1-\alpha^C}$. 
 Here, $\alpha^T$ and $\alpha^C$ represent the fixed fraction of successes if the entire study population of size $n$ were assigned to treatment or control, respectively.

## Methods
  **Logit MLE ($\hat{\beta}_2$):** The coefficient for the treatment indicator obtained by fitting a standard logistic regression model with the assignment variable and the linear covariate $Z_i$.
  
  **Plug-in Estimator ($\tilde{\Delta}$):** The differential log odds calculated by plugging the MLE coefficients back into the logistic CDF to compute the average predicted probabilities for the population under both treatment counterfactuals.
  
  **ITT Estimator ($\hat{\Delta}$):** The simple empirical difference in log odds calculated directly from the observed success rates in the randomized treatment and control groups.

## Performance Measures
      The empirical mean of the estimates across the 1,000 replicates is compared against the true finite-population parameter $\Delta$ (which is held constant for a given $n$) to assess bias and asymptotic consistency.
      Also, the empirical standard deviation (SD) of the estimates is calculated across the 1,000 replicates to measure the variability and stability of each estimator.



