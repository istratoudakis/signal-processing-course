import numpy as np
from typing import Dict, Any

def compute_matrix_diagnostics(X: np.ndarray, tol: float = None) -> Dict[str, Any]:
    """
    Computes core numerical linear algebra diagnostics for a design matrix X 
    using Singular Value Decomposition (SVD) without forming X.T @ X.
    """
    u, s, vt = np.linalg.svd(X, full_matrices=False)
    rank = np.linalg.matrix_rank(X, tol=tol)
    cond_x = s[0] / s[-1] if s[-1] > 0 else np.inf
    
    return {
        "singular_values": s,
        "rank": int(rank),
        "cond_X": float(cond_x),
        "cond_normal": float(cond_x ** 2),
        "null_space_basis": vt[rank:].T
    }