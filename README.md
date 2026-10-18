Signal Processing — Computational Labs & Interactive CompanionDepartment of Electrical and Computer Engineering (ECE) | University of Patras   


Overview  
Welcome to the computational companion repository for the Signal Processing course at the Department of Electrical and Computer Engineering, University of Patras.This repository is designed specifically for students taking the course who want to bridge the gap between theoretical derivations on the board and practical, numerical implementations in Python. Rather than treating algorithms as black-box library calls, each module builds the estimators and signal processing pipelines from first principles, supported by:  
Rigorous Mathematical Derivations: Step-by-step $\LaTeX$ formulations connecting linear algebra, statistical estimation, and physical system modeling.   
Modular, Production-Grade Python Code: Clean separation between core mathematical solvers (src/models/), diagnostic utilities (src/utils/), and plotting engines (src/visualization/).  
Geometric Intuition via Manim: Embedded animations that visualize abstract concepts—such as vector space projections, covariance whitening, and ill-conditioned surfaces—in an intuitive, geometric way.Course Modules & Laboratories01. Nonlinear Temperature Sensor Calibration under Heterogeneous NoiseNotebook: notebooks/01-temperature-sensor-calibration.ipynbCore Concepts:Polynomial system modeling: $y_i = \theta_0 + \theta_1 T_i + \theta_2 T_i^2 + n_i$Ordinary Least Squares (OLS) vs. Weighted Least Squares (WLS) under heteroscedastic noise ($\mathbf{C}_n = \text{diag}(\sigma_1^2, \dots, \sigma_N^2)$).Geometric interpretation of the Whitening Transformation ($\mathbf{W} = \mathbf{C}_n^{-1}$) and Mahalanobis distance minimization.Numerical instability, Vandermonde matrix collinearity, and condition number ($\kappa(\mathbf{X})$) analysis over narrow measurement ranges.Tikhonov Regularization (Ridge Regression): Stabilizing ill-conditioned inverse problems via augmented linear systems and the Bias-Variance tradeoff (Ridge trace analysis).02. Spectral Analysis & Frequency Estimation (Upcoming)Notebook: notebooks/02-spectral-analysis.ipynbCore Concepts: Non-parametric and parametric power spectral density (PSD) estimation, windowing, spectral leakage, and resolution tradeoffs.Repository ArchitectureTo keep the Jupyter Notebooks clean, readable, and focused on pedagogy, all heavy numerical computations and plotting routines are organized into a local Python package (src):signal-processing-course/
├── docs/                                         # Course handouts, notes, and reference PDFs
├── notebooks/                                    # Interactive Jupyter Notebooks for each lab
│   ├── media/                                    # Cached Manim video renders (1080p60)
│   └── 01-temperature-sensor-calibration.ipynb   # Lab 1: Estimation & Regularization
├── src/                                          # Core Python package
│   ├── models/                                   # Mathematical solvers & DSP algorithms
│   │   ├── __init__.py
│   │   └── calibration.py                        # WLS and Tikhonov augmented solvers
│   ├── utils/                                    # Helper routines & numerical diagnostics
│   │   ├── __init__.py
│   │   ├── diagnostics.py                        # Matrix conditioning & statistical metrics
│   │   └── notebook_helpers.py                   # Manim rendering & notebook display tools
│   └── visualization/                            # Visual engines
│       ├── __init__.py
│       ├── animations.py                         # Manim scenes for geometric intuition
│       └── plots.py                              # Publication-quality Matplotlib figures
├── .gitignore                                    # Git exclusions for caches and build artifacts
├── pyproject.toml                                # Package configuration for editable install
├── requirements.txt                              # Pinned Python dependencies
└── README.md                                     # Course guide and documentation
Getting Started (For Students)Follow these steps to set up the local environment on your machine and run the interactive notebooks without import errors.1. Clone the Repositorygit clone <repository-url>
cd signal-processing-course
2. Create and Activate a Virtual EnvironmentIt is strongly recommended to use an isolated Python environment (Python $3.10+$):On Windows (PowerShell):python -m venv .venv
.\.venv\Scripts\Activate.ps1
On Linux / macOS:python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies & Local PackageInstall the required scientific libraries and register the src folder as an editable package so Jupyter can resolve all imports automatically:pip install -r requirements.txt
pip install -e .
Note on Manim Animations: Pre-rendered 1080p60 videos are cached inside notebooks/media/. The helper function render_and_display_scene() will play them automatically without requiring you to re-render them. If you wish to modify the animations in src/visualization/animations.py and re-render them from scratch (force_render=True), make sure you have FFmpeg and a working LaTeX distribution installed on your system.How to Study with This RepositoryRead the Theory First: Each notebook section starts with the mathematical formulation of the physical problem. Make sure you follow the matrix dimensions and statistical assumptions before running the code cell.Experiment with the Parameters: Try changing the noise variance, narrowing the temperature window, or varying the regularization hyperparameter $\lambda$ to see how the estimators behave in extreme regimes.Inspect the Source Code: Because the notebooks use %autoreload 2, you can open src/models/calibration.py side-by-side in VS Code, inspect or tweak the underlying linear algebra routines (e.g., QR decomposition vs. Normal Equations), save the file, and immediately re-run the notebook cell to see the effect.License & Academic IntegrityThis repository is intended as an educational resource for students of the ECE Department at the University of Patras. Feel free to use, modify, and experiment with the code for your study and deeper understanding of Signal Processing.