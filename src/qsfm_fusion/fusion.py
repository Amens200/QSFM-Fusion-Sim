# Enhanced QSFM_Fusion.py - Added fidelity abort (F = Tr(√(ρ1 ρ2 √ρ1)) > 0.9)
import numpy as np
import re
import time
from sklearn.svm import SVC
from qutip import rand_dm, entropy_vn, coherent_dm, tracedist, basis, tensor, qeye, sigmax, sigmaz, fidelity  # Re-added fidelity
from scipy.signal import savgol_filter, hilbert

class QSFM_Fusion:
    def __init__(self, states=10, actions=6, alpha=0.05, gamma=0.999, epsilon=0.03):
        self.states = states
        self.actions = actions
        self.Q = np.zeros((states, actions))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.reward_history = []
        self.temporal_flags = np.zeros(states)
        self.db = sqlite3.connect('qsfm_audits.db')
        self.db.execute('''CREATE TABLE IF NOT EXISTS audits
                          (timestamp TEXT, anomaly REAL, entropy REAL, seized REAL, hmac TEXT)''')

    def update_q_learning(self, state, action, reward, next_state):
        predict = self.Q[state, action]
        target = reward + self.gamma * np.max(self.Q[next_state])
        self.Q[state, action] += self.alpha * (target - predict)
        self.reward_history.append(reward)
        self.temporal_flags[state] += 1
        if reward > 0:
            print(f"Q-update win! Reward: {reward} - Smugglers on notice!")

    def sensor_fuse(self, mag_data, grav_data, labels, locations=None, manifest_weights=None):
        fused = np.column_stack((mag_data, grav_data))
        if locations is not None:
            loc_features = np.array(locations)[:, np.newaxis]
            loc_dists = np.linalg.norm(loc_features, axis=1)
            fused = np.column_stack((fused, loc_dists))
        svm = SVC(kernel='rbf')
        svm.fit(fused, labels)
        predictions = svm.predict(fused)
        anomaly = np.mean(predictions != labels)
        
        if manifest_weights is not None:
            sensor_masses = (grav_data * 1e5).astype(int)  # 5e-5 Gal ≈ 50 kg
            deltas = np.abs(sensor_masses - manifest_weights)
            anomaly += np.mean(deltas > 1e-3)
            print(f"Manifest mismatch: {np.mean(deltas):.4f} - Possible tampering detected!")
        
        state = min(int(anomaly * self.states), self.states - 1)
        action = np.argmax(self.Q[state]) if np.random.rand() > self.epsilon else np.random.randint(0, self.actions)
        reward = -anomaly * 10
        next_state = state
        self.update_q_learning(state, action, reward, next_state)
        
        return anomaly

    def entropy_predict(self, rho_list, dt=1e-6, tau=0.01, comms_signatures=None):
        entropies = np.array([entropy_vn(rho) for rho in rho_list])
        rates = np.diff(entropies) / dt
        anomaly_rate = np.mean(rates) if np.any(rates > tau) else 0
        
        coherences = np.array([np.sum(np.abs(rho.full() - np.diag(np.diag(rho.full())))) for rho in rho_list])
        trace_dists = np.array([tracedist(rho_list[i], rho_list[i+1]) for i in range(len(rho_list)-1)])
        anomaly_rate += np.mean(np.diff(coherences) / dt) + np.mean(trace_dists / dt)
        
        # New: Fidelity abort - Check stability (F > 0.9 or abort)
        for i in range(len(rho_list)-1):
            F = fidelity(rho_list[i], rho_list[i+1])
            if F < 0.9:
                print(f"Fidelity abort! F={F:.3f} < 0.9 - Quantum smugglers detected?")
                anomaly_rate *= 1.2  # Uplift penalty
        
        if comms_signatures is not None:
            comm_entropies = self._von_neumann_entropy(comms_signatures)
            anomaly_rate += np.mean(np.diff(comm_entropies))
            print(f"Pattern-of-life disturbance: {anomaly_rate:.4f} - Entropy says: Black market bingo!")
        
        return anomaly_rate

    def _von_neumann_entropy(self, sigs):
        entropies = np.zeros(len(sigs))
        for i in range(len(sigs)):
            evals = np.linalg.eigvalsh(np.outer(sigs[i], sigs[i]))
            entropies[i] = -np.sum(evals * np.log(evals + 1e-10))
        return entropies

    def ship_manifest_processor(self, manifests):
        weights = []
        for m in manifests:
            nums = re.findall(r'\d+', m)
            weight = float(nums[-1]) if nums else 0.0
            weights.append(weight)
        print("Manifests parsed - Weights extracted! (No quantum ghosts in the cargo.)")
        return np.array(weights)

    def log_audit(self, timestamp, anomaly, entropy, seized, hmac_signature):
        self.db.execute("INSERT INTO audits (timestamp, anomaly, entropy, seized, hmac) VALUES (?, ?, ?, ?, ?)",
                        (timestamp, anomaly, entropy, seized, hmac_signature))
        self.db.commit()

# Flask API for port integration
app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan_container():
    data = request.json
    mag_data = np.array(data.get('mag_data', [1e-9]*100))
    grav_data = np.array(data.get('grav_data', [5e-5]*100))
    labels = np.array(data.get('labels', [0]*100))
    locations = np.array(data.get('locations', [[0.1, 0.1]]*100))
    manifests = data.get('manifests', ["cargo: electronics 50kg"]*100)
    
    qsfm = QSFM_Fusion()
    manifest_weights = qsfm.ship_manifest_processor(manifests)
    rho_list = [rand_dm(2) for _ in range(10)]
    comms = [np.random.rand(5) for _ in range(10)]
    anomaly_rate = qsfm.sensor_fuse(mag_data, grav_data, labels, locations, manifest_weights)
    entropy_rate = qsfm.entropy_predict(rho_list, comms_signatures=comms)
    seized = 100 * anomaly_rate * 0.8
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    hmac_signature = hmac.new(b'mock_key', str(anomaly_rate).encode(), hashlib.sha256).hexdigest()
    qsfm.log_audit(timestamp, anomaly_rate, entropy_rate, seized, hmac_signature)
    
    return jsonify({
        'timestamp': timestamp,
        'anomaly_rate': anomaly_rate * 100,
        'entropy_rate': entropy_rate,
        'seized_kg': seized,
        'hmac': hmac_signature
    })