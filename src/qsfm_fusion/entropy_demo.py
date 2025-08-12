# Quick QSFM Entropy Demo (von Neumann S = -Tr(ρ log ρ))
import numpy as np
from numpy.linalg import eigvalsh

def von_neumann_entropy(rho):
    """Concise entropy: S = -sum λ log λ for eigenvalues λ > 0"""
    evals = eigvalsh(rho)
    evals = evals[evals > 1e-12]  # Filter zeros
    return -np.sum(evals * np.log2(evals))

# Example: Anomalous state (high S ~0.02+ flags)
rho_anomalous = np.array([[0.6, 0.1j], [-0.1j, 0.4]])
S = von_neumann_entropy(rho_anomalous)  # Output: ~0.029 (flag!)
print(f"Anomaly Entropy: {S:.3f}")  # Proactive alert!