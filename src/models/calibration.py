import numpy as np
from typing import Optional, Tuple

def solve_wls(X: np.ndarray, y: np.ndarray, sigma: np.ndarray) -> Tuple[np.ndarray, float]:
    # w_i = 1 / sigma_i^2
    w = 1.0 / (sigma**2)
    sqrt_w = np.sqrt(w)

    # Transform the design matrix and observations
    X_weighted = sqrt_w[:, None] * X # row-wise scaling via broadcasting (avoids N x N matrix)
    y_weighted = sqrt_w * y

    # Solve the equivalent OLS problem on the transformed data
    theta_weighted, *_ = np.linalg.lstsq(X_weighted, y_weighted, rcond=None)

    # Compute the original residuals using the optimal parameters
    r_weighted = y - (X @ theta_weighted)

    # Calculate the final weighted cost criterion J_W
    J_opt = np.sum(w * (r_weighted**2))

    return theta_weighted, float(J_opt)

def solve_tikhonov_augmented(X: np.ndarray, y: np.ndarray, lam: float, L: Optional[np.ndarray]) -> np.ndarray:

    n_features = X.shape[1]

    # If penalty matrix L is not explicitly provided, default to penalizing 
    # all coefficients while leaving the constant term (first column) unpenalized.
    if L is None:
        L = np.eye(n_features)
        L[0, 0] = 0.0  # Zero penalty for the constant offset \theta_0

    # Construct the augmented design matrix 
    X_aug = np.vstack((X, np.sqrt(lam) * L))

    # Construct the augmented observation vector
    p = L.shape[0]  # Number of penalty constraints
    y_aug = np.concatenate((y, np.zeros(p)))

    # Solve using a numerically stable method (QR/SVD)
    theta, *_ = np.linalg.lstsq(X_aug, y_aug, rcond=None)
    
    return theta