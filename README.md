# QSFM-Fusion (Simulation-Only)

**Quantum Sensor Fusion (QSFM)** — a public, non-export-controlled, **simulation** repository demonstrating anomaly detection and fusion across heterogeneous signals with entropy/coherence features and learning-based policy shaping.

> ⚠️ **Safety & Scope:** This repo is simulation-only, no operational deployment code, no vendor data, and no export-controlled content. It is intended for research discussion and portfolio review.

## Why it matters (mission fit)
- **Critical infrastructure & border security:** Detect and triage anomalous patterns across simulated sensor streams.
- **Supply-chain integrity:** Flag manifest/routing anomalies in a controlled sandbox.
- **Hardware-aware ideas:** Entropy/coherence features and neuromorphic/learning hooks align with modern quantum-inspired sensing research.
- **Reproducibility:** Seeded runs, deterministic pipelines, and simple artifacts for evaluation.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # create if not present; see minimal list below
python QSFM_FusionSimulation.py  # runs a short seeded simulation
```

### Minimal requirements
```
numpy
scipy
pandas
matplotlib
```

## What’s included
- **QSFM_FusionSimulation.py** — main simulation harness (seeded).
- **QSFM_Fusion.py / QSFM_Main.py** — fusion and orchestration helpers.
- **QSFM TestSuite.py** — smoke tests / assertions (rename to `QSFM_TestSuite.py` for consistent naming).
- **QSFM Entropy Demo.py** — small demo of entropy/coherence features (rename to `QSFM_Entropy_Demo.py`).
- **QSFM_ASIC_Fusion.v** — *verilog sketch (illustrative only)*.
- **QSFM_Integration.cpp / QSFM_Scanner.cpp** — C++ stubs for future acceleration.
- **build_script.sh** — helper script for local builds.
- **SimulationResults.txt** — sample output.

## Suggested structure (next pass)
```
src/qsfm_fusion/
  __init__.py
  fusion_sim.py
scripts/
  demo.py
tests/
  test_smoke.py
.github/workflows/
  ci.yml
results/  (generated)
```

## Reproducing a simple plot
Add a tiny demo script (example):
```python
# scripts/demo.py
import numpy as np, json, os
import matplotlib.pyplot as plt

os.makedirs("results", exist_ok=True)
rng = np.random.default_rng(42)
x = rng.normal(0, 1, 200)
score = np.clip(np.abs(x)/3, 0, 1)
json.dump({"seed":42,"mean_score":float(score.mean())}, open("results/demo_metrics.json","w"))
plt.plot(score); plt.title("QSFM demo score (seed=42)"); plt.savefig("results/demo_plot.png", dpi=160)
print("Wrote results/demo_metrics.json & results/demo_plot.png")
```

## Repo tree (current snapshot)
```
.
├── QSFM_FusionSimulation.py
├── QSFM_Fusion.py
├── QSFM_Main.py
├── QSFM TestSuite.py
├── QSFM Entropy Demo.py
├── QSFM_ASIC_Fusion.v
├── QSFM_Integration.cpp
├── QSFM_Scanner.cpp
├── build_script.sh
├── SimulationResults.txt
└── README.md
```

## License
MIT (recommended for public research code). Add a `LICENSE` file if not already present.

## Topics (for GitHub discovery)
`quantum-computing` · `sensor-fusion` · `anomaly-detection` · `critical-infrastructure` · `python` · `research`

## Contact
Issues and PRs welcome. For introductions/collaboration, connect on LinkedIn.

---

*Tip: rename files to avoid spaces (e.g., `QSFM_Entropy_Demo.py`), standardize to `snake_case` in future updates, and add CI (ruff/black/pytest) for a professional touch.*
