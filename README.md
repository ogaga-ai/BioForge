# BioForge

**Integrated DOE + ML Bioprocess Optimization Framework**

> *"Any U.S. research institution or manufacturer can run their own waste stream through BioForge and receive actionable optimization results — independently, without requiring access to the developer or laboratory."*

---

## Overview

BioForge is an open-source computational platform that bridges the gap between laboratory-scale waste-to-value research and industrial-scale domestic manufacturing. It combines **Design of Experiments (DOE)** with advanced **Machine Learning** to identify and optimize the process conditions under which U.S. agricultural and industrial waste streams can be converted into high-value biochemicals, biofuels, and critical industrial inputs at commercially viable yields.

The platform is:
- **Substrate-agnostic** — applicable to corn stover, sugarcane bagasse, food waste, and any domestic waste stream
- **Product-agnostic** — applicable to citric acid, succinic acid, lactic acid, biodiesel, industrial enzymes, and more
- **Open-source** — permanently available to any U.S. university, national lab, or manufacturer

---

## Current Status

**v0.1 — Optimization Engine Module (Active Development)**

| Module | Status |
|--------|--------|
| DOE Engine (Box-Behnken, CCD) | ✅ Implemented |
| ML Optimizer (ANN, RF, GBR, SVR) | ✅ Implemented |
| Sensitivity Analysis (Permutation/Sobol) | ✅ Implemented |
| Optimization Protocol Card Generator | ✅ Implemented |
| Hollow-Fiber Separation Module | 🔄 In progress |
| Process Simulation Engine | 📋 Planned (Stage 2) |
| Scale-up Feasibility Assessment | 📋 Planned (Stage 2) |
| Web Interface (FastAPI + frontend) | 📋 Planned (Stage 2) |

---

## Validated On

The optimization engine has been prototyped and validated using experimental data from the following peer-reviewed publication:

> **Okedi, O.M.** et al. (2024). *Biotechnological Conversion of Yam Peels for Enhanced Citric Acid Production.* **Industrial Crops and Products**, Impact Factor 6.2.
> - DOE: Box-Behnken Design (17 runs, 3 factors)
> - Models: ANN (R² = 0.99883), ANFIS (R² = 0.99880)
> - Result: **49.1% yield improvement** (28.90 → 43.08 g/l citric acid)
> - Key finding: Sodium fluoride is the most influential factor (67.5% variance)

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/ogaga-ai/BioForge.git
cd BioForge

# Install dependencies
pip install -r requirements.txt

# Launch the demonstration notebook
cd notebooks
jupyter notebook BioForge_CitricAcid_Optimization.ipynb
```

---

## Repository Structure

```
BioForge/
├── bioforge/
│   ├── optimization/
│   │   ├── doe_engine.py          # DOE matrix generation (BBD, CCD)
│   │   └── ml_optimizer.py        # ANN, RF, GBR, SVR model training + sensitivity
│   ├── separation/                # Hollow-fiber contactor module (in progress)
│   ├── simulation/                # Process simulation engine (planned)
│   ├── reporting/
│   │   └── protocol_card.py       # Optimization protocol card generator
│   └── utils/
├── notebooks/
│   └── BioForge_CitricAcid_Optimization.ipynb   # Full demonstration notebook
├── data/
│   └── raw/
│       └── citric_acid_doe_matrix.csv            # Published experimental data
├── outputs/
│   ├── figures/                   # Generated plots and architecture diagrams
│   └── reports/                   # Protocol cards (text output)
├── docs/
│   ├── BioForge_Project_Overview.html
│   └── generate_architecture_diagram.py
├── tests/
├── requirements.txt
└── README.md
```

---

## Technical Stack

- **Python 3.11**
- **NumPy / Pandas** — data manipulation
- **Scikit-learn** — Random Forest, SVR, ANN (MLPRegressor), permutation importance
- **SciPy** — statistical analysis, curve fitting
- **Matplotlib / Seaborn** — visualization
- **Jupyter Notebook** — interactive workflow

---

## Roadmap

### Stage 1: Protocol Database (2026–2028)
Systematic DOE + ML optimization across U.S. priority waste streams:
- Corn stover → succinic acid
- Sugarcane bagasse → lactic acid
- Food processing residues → citric acid

### Stage 2: BioForge Platform (2027–2029)
Full deployable platform with web interface, separation module, and process simulation.

### Stage 3: Pilot Validation (2029–2031)
Multi-institutional partnerships with NREL, Argonne National Lab, and industry partners.

---

## Developer

**Ogaga Maxwell Okedi**
M.S. Chemical Engineering — Florida A&M University
M.S. Computer Science (incoming) — University of Texas at Dallas

*Google Scholar: 6 publications | 112 citations | h-index 5*

---

## License

MIT License — open for use by any U.S. research institution, national laboratory, or manufacturer.
