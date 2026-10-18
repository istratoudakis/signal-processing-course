# Signal Processing — Computational Labs & Interactive Companion

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Package: Editable src](https://img.shields.io/badge/Architecture-Modular%20src%20Package-success.svg)](#modular-python-package-architecture)
[![Visualizations: Matplotlib & Manim](https://img.shields.io/badge/Visualizations-Matplotlib%20%7C%20Manim-orange.svg)](#overview--pedagogical-philosophy)
[![Status: Active Development](https://img.shields.io/badge/Roadmap-Active%20(Completion%3A%20Jan%202027)-informational.svg)](#laboratory-roadmap--release-schedule)

> **Academic & Open Educational Resource:** Inspired by the undergraduate curriculum of the **Department of Electrical and Computer Engineering (ECE) at the University of Patras**, this repository is structured as a comprehensive, self-contained computational companion for **any student, researcher, or engineer** seeking a rigorous, from-scratch mastery of Statistical Signal Processing, Estimation Theory, and Numerical Linear Algebra.

---

## Overview & Pedagogical Philosophy

Modern signal processing lies at the intersection of linear algebra, probability theory, numerical optimization, and physical system modeling. This repository bridges the gap between theoretical derivations on the lecture board and production-grade numerical implementations in Python.

Rather than treating algorithms as black-box library calls, every module in this repository builds estimators and signal processing pipelines from **first principles**, supported by three core pillars:

1. **Rigorous Mathematical Derivations:** Step-by-step $\LaTeX$ formulations connecting subspace geometry, statistical estimation, and physical measurement models.
2. **Modular, Production-Grade Python Package:** Configured via `pyproject.toml` as an editable local package (`src/`), enforcing a strict separation of concerns between mathematical solvers (`src/models/`), numerical diagnostics (`src/utils/`), and visualization engines (`src/visualization/`).
3. **Geometric Intuition via Manim:** Embedded high-definition animations (1080p60) that translate abstract mathematical operations—such as column-space projections, covariance whitening, and ill-conditioned objective surfaces—into clear geometric visuals.

---

## Comprehensive Course Curriculum

The syllabus is organized into **four progressive parts**, transitioning from deterministic linear algebra and subspace methods to Bayesian inference, nonlinear optimization, and dynamic state-space tracking.

### Part I — Numerical Linear Algebra & Multidimensional Signals
*Focus: Linear Least Squares, Numerical Conditioning, Multidimensional Signal Processing, and Second-Order Random Vectors.*
* **Linear Least Squares (LLS):** Residual vectors, design matrices, overdetermined linear systems, and orthogonal subspace projections.
* **Subspace Geometry:** Orthogonality, vector/matrix norms, inner products, and column-space geometry.
* **Conditioning & Regularization:** Rank deficiency, Vandermonde collinearity, matrix condition number ($\kappa(\mathbf{X})$), and Tikhonov regularization (Ridge regression).
* **Matrix Factorizations:** QR decomposition, Singular Value Decomposition (SVD), Moore–Penrose pseudoinverse, and spectral analysis via singular values.
* **Multidimensional & Multichannel Signals:** 2-D discrete convolution, separable filtering kernels, and matrix vectorization (`vec` operator).
* **Random Vectors & Whitening:** Covariance matrices, correlated and heteroscedastic noise, quadratic forms, symmetric Positive Semi-Definite (PSD) matrices, eigendecomposition, Cholesky factorization, and the Whitening Transformation.

### Part II — Statistical & Bayesian Estimation
*Focus: Maximum Likelihood (MLE), Maximum A Posteriori (MAP), Bayesian Inference, and Basis Function Regression.*
* **Maximum Likelihood Estimation (MLE):** Likelihood formulation under Gaussian noise, equivalence between Weighted Least Squares and Gaussian MLE, and estimation of sample mean, variance, and linear model parameters.
* **MAP Estimation & Regularization:** Prior distributions, likelihood functions, and interpreting deterministic regularization ($L_2$ / Tikhonov) as Bayesian prior information.
* **Multivariate Gaussian Models:** Joint probability density geometry, Mahalanobis distance, covariance structures, and precision matrices ($\mathbf{\Lambda} = \mathbf{C}^{-1}$).
* **Bayesian Parameter Estimation:** Posterior distributions, posterior mean (MMSE) vs. MAP estimators, parameter uncertainty quantification, credible regions, and sequential (recursive) Bayesian updates.
* **Bayesian Linear Regression:** Posterior distributions over model weights, posterior predictive distributions, and the decomposition of **epistemic (model)** vs. **aleatoric (measurement)** uncertainty.
* **Basis Expansions & Model Complexity:** Polynomial, Fourier, and Radial Basis Function (RBF) regression, hyperparameter tuning, and sequential Bayesian learning.

### Part III — Nonlinear Estimation & Optimal Filtering
*Focus: Nonlinear Least Squares, Iterative Numerical Optimization, and Time/Frequency-Domain Wiener Filtering.*
* **Nonlinear Measurement Models:** Residual vectors for nonlinear systems, multivariate functions, partial derivatives, and Jacobian matrices ($\mathbf{J}$).
* **Local Approximations & Optimization:** Multidimensional Taylor series expansions, gradient vectors ($\nabla$), Hessian matrices ($\mathbf{H}$), and local linearization.
* **Iterative Solvers:** Steepest Gradient Descent, Gauss–Newton algorithm, and Levenberg–Marquardt damped optimization; sensitivity to initialization, local minima, and weighted/robust loss functions.
* **Optimal Linear Estimation (LMMSE):** Linear Minimum Mean Square Error estimation and the **Orthogonality Principle** in Hilbert spaces.
* **Time-Domain Wiener Filtering:** Finite Impulse Response (FIR) Wiener filters, autocorrelation/cross-correlation matrices, Wiener–Hopf equations, and optimal linear prediction.
* **Frequency-Domain Wiener Filtering:** Power Spectral Densities (PSDs) of signal and noise, optimal frequency-domain smoothing, deconvolution, and regularized spectral inversion.

### Part IV — Dynamic Estimation & Sensor Fusion
*Focus: State-Space Modeling, Kalman Filtering, Multi-Sensor Fusion, and Real-Time Tracking.*
* **State-Space Formulations:** Latent state vectors, discrete-time system dynamics, observation models, process noise, and measurement noise statistics.
* **Uncertainty Propagation:** Affine transformations of Gaussian random variables and open-loop covariance propagation.
* **The Kalman Filter:** Two-step recursive estimation (Prediction & Measurement Update/Correction), innovation sequence, optimal Kalman Gain ($\mathbf{K}_k$), and closed-loop covariance update.
* **Multidimensional Tracking & Sensor Fusion:** Fusing measurements from heterogeneous sensors with distinct uncertainty profiles, and handling missing or asynchronous observations.
* **Filter Tuning & Diagnostics:** Selection and practical tuning of process ($\mathbf{Q}$) and measurement ($\mathbf{R}$) noise covariance matrices, innovation whiteness analysis, and numerically stable implementations (e.g., Joseph-form covariance update).

---


## Modular Python Package Architecture

To keep the Jupyter Notebooks clean, readable, and strictly focused on mathematical pedagogy, all core numerical solvers, diagnostic routines, and plotting pipelines are abstracted into an installable Python package located in `src/`.

By configuring the project via `pyproject.toml` and installing it in **editable mode** (`pip install -e .`), the `src` package is registered directly in your Python environment. Combined with Jupyter's `%autoreload 2` magic command, any modifications you make to the underlying `.py` modules in VS Code are instantaneously reflected inside the active notebook kernel without restarting.

```text
signal-processing-course/
├── docs/                                             # Course handouts, notes, and reference PDFs
├── notebooks/                                        # Interactive Jupyter Notebooks for each lab
|   └── part-1                                        
│       └── 01-temperature-sensor-calibration.ipynb   # Lab 01: WLS Estimation & Tikhonov Regularization
├── src/                                              # Core installable Python package
│   ├── __init__.py
│   ├── models/                                       # Mathematical solvers & estimation algorithms
│   │   ├── __init__.py
│   │   └── calibration.py                            # WLS, QR/SVD solvers & Tikhonov augmented systems
│   ├── utils/                                        # Helper routines & numerical diagnostics
│   │   ├── __init__.py
│   │   ├── diagnostics.py                            # Matrix conditioning, SVD spectrum & statistical metrics
│   │   └── notebook_helpers.py                       # Automated Manim caching & HTML5 video embedding
│   └── visualization/                                # Visual engines
│       ├── __init__.py
│       ├── animations.py                             # Manim scenes for geometric intuition (Projections, Whitening)
│       └── plots.py                                  # Publication-quality Matplotlib figures & diagnostics
├── .gitignore                                        # Git exclusions for caches, virtualenvs, and build artifacts
├── pyproject.toml                                   # Modern PEP 621 package configuration for editable install
├── requirements.txt                                 # Pinned scientific Python dependencies
└── README.md                                        # Course guide, syllabus, and documentation
```

---

## Getting Started (Installation & Setup)

Follow these steps to set up a reproducible local environment on your machine and run the interactive notebooks without pathing or import errors.

### 1. Clone the Repository
```bash
git clone https://github.com/istratoudakis/signal-processing-course.git
cd signal-processing-course
```

### 2. Create and Activate an Isolated Virtual Environment
Using an isolated environment (`Python 3.10+`) is strongly recommended to prevent dependency conflicts:

* **Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
* **Linux / macOS (Bash/Zsh):**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Install Dependencies & Register the Local `src` Package
Install the scientific computing stack and register `src/` as an editable package:
```bash
pip install -r requirements.txt
pip install -e .
```

> **Note on Manim Animations:** Pre-rendered `1080p60` videos are managed by the helper function `render_and_display_scene()` inside `src/utils/notebook_helpers.py`. If cached videos exist in `notebooks/media/`, they are embedded automatically. If you wish to render the scenes locally or modify `src/visualization/animations.py` and re-render (`force_render=True`), ensure that **FFmpeg** and a working **LaTeX distribution** (e.g., MiKTeX or TeX Live) are installed on your system.

---

> **Important Note on Video Playback in GitHub Preview:**  
> GitHub's built-in web renderer enforces strict Content Security Policies (CSP) and does not play embedded HTML5 `.mp4` videos directly inside the notebook preview.  
> To experience the full `1080p60` Manim animations:
> * **Run locally (Recommended):** Clone the repository and execute the notebooks in **VS Code** or **Jupyter Lab**.
> * **Interactive Web Viewer:** Paste the notebook link into [nbviewer.org](https://nbviewer.org/) for complete rendering.

--- 

## How to Study with This Repository

1. **Master the Theory First:** Every notebook section begins with the rigorous mathematical formulation of the physical system. Verify the matrix dimensions, subspace assumptions, and noise covariance structures before executing the code cell.
2. **Stress-Test the Estimators:** Actively experiment with the simulation parameters in the notebooks. Increase the noise variance, narrow the observation window to induce collinearity, or sweep the regularization hyperparameter $\lambda$ across orders of magnitude to observe how estimators behave in extreme regimes.
3. **Inspect the Underlying Numerical Linear Algebra:** Open `src/models/` side-by-side with the Jupyter Notebook in VS Code. Compare how direct Normal Equations ($\mathbf{X}^T\mathbf{W}\mathbf{X}$) behave versus numerically stable **QR** or **SVD** factorizations on ill-conditioned Vandermonde matrices, tweak the code, save, and re-run the cell immediately.

---

## Notes & Usage

Feel free to clone, study, and play around with the code. It's meant as a personal study project and open learning companion—break things, tweak the parameters, and see how the math actually works under the hood.