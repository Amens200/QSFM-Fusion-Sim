import json, os, numpy as np
import matplotlib.pyplot as plt

os.makedirs('results', exist_ok=True)
rng = np.random.default_rng(42)
n = 200
signal = rng.normal(0.0, 1.0, n)
anomaly = (np.abs(signal) > 2.0).astype(int)
score = (np.abs(signal) / 3.0).clip(0, 1)
metrics = { 'seed': 42, 'n': int(n), 'anomaly_rate': float(anomaly.mean()), 'mean_score': float(score.mean()) }
with open('results/demo_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)
plt.figure(figsize=(6,3))
plt.plot(score)
plt.title('QSFM-Fusion-Sim demo score (seed=42)')
plt.xlabel('index'); plt.ylabel('score')
plt.tight_layout(); plt.savefig('results/demo_plot.png', dpi=160)
print('Wrote results/demo_metrics.json and results/demo_plot.png')
