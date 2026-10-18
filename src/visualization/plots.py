import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Callable

from src.utils.diagnostics import compute_matrix_diagnostics

def set_academic_style():
    """Applies academic styling for Matplotlib figures."""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams['figure.dpi'] = 150

# EXERCISE 01

def plot_component_decomposition(T: np.ndarray, offset_comp: np.ndarray, 
                                 linear_comp: np.ndarray, total_voltage: np.ndarray, 
                                 theta_0: float):
    """
    Plots the breakdown of the nonlinear sensor calibration model into its affine 
    and quadratic components.
    """
    set_academic_style()
    plt.figure(figsize=(10, 6))

    # Fill between to show accumulation (Superposition effect)
    plt.plot(T, offset_comp, ':', color='gray', lw=2, 
             label=r'Constant Offset: $\theta_0$ (Column $\mathbf{x_0}$)')
    plt.plot(T, offset_comp + linear_comp, '--', color='steelblue', lw=2, 
             label=r'Baseline + Linear: $\theta_0 + \theta_1 T$')
    
    # Notice the bold math fonts for vectors/matrices
    plt.plot(T, total_voltage, '-', color='navy', lw=3, 
             label=r'Total Output Voltage: $\mathbf{y} = \mathbf{X}\boldsymbol{\theta}$')

    # Highlight the Quadratic effect
    plt.fill_between(T, offset_comp + linear_comp, total_voltage, color='darkorange', alpha=0.2,
                     label=r'Quadratic Contribution: $\theta_2 T^2$')

    # Plot aesthetics and labeling
    plt.title("Sensor Calibration Model: Component Decomposition", fontsize=14, fontweight='bold', pad=15)
    plt.xlabel(r"Reference Temperature $T$ ($^\circ\text{C}$)", fontsize=12)
    plt.ylabel(r"Output Voltage $y$ ($\text{V}$)", fontsize=12)
    plt.xlim(0, 100)
    plt.ylim(0, 9)

    # Origin point to emphasize offset (positioned below the line for visual clarity)
    plt.scatter(0, theta_0, color='black', zorder=5)
    plt.annotate(r'$\theta_0$ Offset', xy=(0, theta_0), xytext=(8, 0.25), 
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color='black', lw=1.5), 
                 fontsize=12, fontweight='bold')

    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=11)
    plt.tight_layout()
    plt.show()

def plot_wls_diagnostics(scenarios: List[Tuple[str, np.ndarray, np.ndarray]], 
                         T: np.ndarray, X: np.ndarray, theta_true: np.ndarray, 
                         T_dense: np.ndarray, X_dense: np.ndarray, y_true_dense: np.ndarray, 
                         solve_wls_fn: Callable):
    """
    Plots the 3 WLS vs OLS scenarios, computes SVD diagnostics, and prints the estimation errors.
    """
    # Apply academic styling
    set_academic_style()
    fig, axes = plt.subplots(2, 3, figsize=(16, 9), dpi=150)

    print(f"{'Scenario':<32} | {'rank':<4} | {'cond(X_w)':<10} | {'cond(Normal)':<12} | {'||X.T W r||':<11} | {'J_opt':<8} | {'Err OLS':<8} | {'Err WLS':<8}")
    print("-" * 112)

    for idx, (title, y_meas, sig) in enumerate(scenarios):
        # 1. Solve WLS & OLS
        theta_wls, J_opt = solve_wls_fn(X, y_meas, sig)
        theta_ols, *_ = np.linalg.lstsq(X, y_meas, rcond=None)
        
        # 2. Compute Whitened Design Matrix
        w = 1.0 / (sig**2)
        sqrt_w = np.sqrt(w)
        X_weighted = sqrt_w[:, None] * X
        
        # 3. Numerical Diagnostics (Using our new utility)
        diag = compute_matrix_diagnostics(X_weighted)
        rank_w = diag['rank']
        cond_w = diag['cond_X']
        cond_normal = diag['cond_normal']
        singular_values = diag['singular_values']
        
        # 4. Orthogonality check and estimation errors
        r_wls = y_meas - (X @ theta_wls)
        orth_check = np.linalg.norm(X.T @ (w * r_wls))
        err_ols = np.linalg.norm(theta_ols - theta_true)
        err_wls = np.linalg.norm(theta_wls - theta_true)
        
        clean_name = title.splitlines()[0]
        print(f"{clean_name:<32} | {rank_w:<4d} | {cond_w:<10.2e} | {cond_normal:<12.2e} | {orth_check:<11.2e} | {J_opt:<8.4f} | {err_ols:<8.4f} | {err_wls:<8.4f}")
        
        # --- Top Row: Calibration Curve Fits ---
        ax_top = axes[0, idx]
        vis_err = np.minimum(sig, 4.0) # Clip visual error bars
        ax_top.errorbar(T, y_meas, yerr=vis_err, fmt='ko', ecolor='gray', elinewidth=1.2, 
                        capsize=3, label=r'Measurements $y_i \pm \sigma_i$')
        ax_top.plot(T_dense, y_true_dense, 'g:', lw=2, label='True Model')
        ax_top.plot(T_dense, X_dense @ theta_ols, 'r--', lw=2, label='OLS Fit')
        ax_top.plot(T_dense, X_dense @ theta_wls, 'b-', lw=2.5, label='WLS Fit')
        
        ax_top.set_title(title, fontsize=11, pad=8)
        ax_top.set_xlabel(r"Reference Temperature $T$ ($^\circ\text{C}$)", fontsize=10)
        ax_top.set_ylabel(r"Sensor Voltage $y$ ($\text{V}$)", fontsize=10)
        ax_top.set_ylim(-1.0, 12.0)
        ax_top.grid(True, linestyle='--', alpha=0.5)
        ax_top.legend(loc='upper left', fontsize=8.5, framealpha=0.9)
        
        # --- Bottom Row: Singular Value Spectrum ---
        ax_bot = axes[1, idx]
        sv_indices = np.arange(1, len(singular_values) + 1)
        ax_bot.bar(sv_indices, singular_values, color=['navy', 'steelblue', 'darkorange'], width=0.5)
        ax_bot.set_yscale('log')
        ax_bot.set_xticks(sv_indices)
        ax_bot.set_xticklabels([r'$\sigma_1(\tilde{\mathbf{X}})$', r'$\sigma_2(\tilde{\mathbf{X}})$', r'$\sigma_3(\tilde{\mathbf{X}})$'], fontsize=10)
        ax_bot.set_ylabel("Singular Value Magnitude", fontsize=10)
        ax_bot.set_title(
            f"SVD Spectrum: $\\kappa_2(\\tilde{{\\mathbf{{X}}}}) = {cond_w:.2e}\n$"
            f"$\\|\\hat{{\\boldsymbol{{\\theta}}}}_{{OLS}}-\\boldsymbol{{\\theta}}\\|_2={err_ols:.3f}$ vs $\\|\\hat{{\\boldsymbol{{\\theta}}}}_{{WLS}}-\\boldsymbol{{\\theta}}\\|_2={err_wls:.3f}$",
            fontsize=10, pad=8
        )
        ax_bot.set_ylim(1e-3, 1e6)
        ax_bot.grid(True, which='both', linestyle='--', alpha=0.5)

    plt.suptitle("WLS Estimation: Impact of Sensor Reliability on Fit Accuracy, SVD Geometry, and Conditioning", fontsize=13, y=1.02, fontweight='bold')
    plt.tight_layout()
    plt.show()

def plot_ridge_trace(X: np.ndarray, y_noisy: np.ndarray, L: np.ndarray, 
                     lams: np.ndarray, solve_tikhonov_fn: Callable):
    """
    Plots the Ridge Trace (parameter shrinkage) and the Condition Number drop
    for various regularization parameters (lambdas) using an augmented system.
    """
    set_academic_style()
    
    thetas = []
    conds = []

    for lam in lams:
        # Track Condition Number of the augmented matrix X_aug using our new utility
        X_aug = np.vstack([X, np.sqrt(lam) * L])
        diag = compute_matrix_diagnostics(X_aug)
        conds.append(diag['cond_X'])
        
        # Solve the augmented system using the modular function
        theta = solve_tikhonov_fn(X, y_noisy, lam, L)
        thetas.append(theta)

    thetas = np.array(thetas)

    # Plotting the Ridge Trace and Condition Number
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True, dpi=150)

    # Subplot 1: Parameter Shrinkage (Ridge Trace)
    ax1.plot(lams, thetas[:, 0], label=r'$\theta_0$ (Unpenalized Offset)', color='black', linewidth=2)
    ax1.plot(lams, thetas[:, 1], label=r'$\theta_1$ (Linear)', color='blue', linewidth=2)
    ax1.plot(lams, thetas[:, 2], label=r'$\theta_2$ (Quadratic)', color='red', linewidth=2)
    ax1.set_ylabel("Parameter Value", fontsize=12)
    ax1.set_title("Ridge Trace: Stabilization of Parameters via Augmented System", fontsize=14, fontweight='bold')
    ax1.set_xscale('log')
    ax1.axvline(x=1e-4, color='green', linestyle=':', linewidth=1.5, alpha=0.8)
    ax1.legend(loc='best', fontsize=11)
    ax1.grid(True, which="both", ls="--", alpha=0.5)

    # Subplot 2: Condition Number Drop
    ax2.plot(lams, conds, color='purple', linewidth=2)
    ax2.set_ylabel(r"Condition Number $\kappa(\tilde{\mathbf{X}}_{\text{aug}})$", fontsize=12)
    ax2.set_xlabel(r"Trade-off Parameter $\lambda$ (Log Scale)", fontsize=12)
    ax2.set_yscale('log')
    ax2.set_xscale('log')
    ax2.grid(True, which="both", ls="--", alpha=0.5)
    ax2.axvline(x=1e-4, color='green', linestyle=':', label='Optimal Stabilization Region')
    ax2.legend(loc='upper right', fontsize=11)

    plt.tight_layout()
    plt.show()