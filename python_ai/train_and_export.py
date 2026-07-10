import numpy as np
from sklearn.ensemble import IsolationForest
from skl2onnx import to_onnx
from skl2onnx.common.data_types import FloatTensorType
import os

np.random.seed(42)

print("Step 1: Generating synthetic security log data... ")

# Normal Data
normal_freq = np.random.normal(loc=15, scale=5, size=2000)
normal_size = np.random.normal(loc=4.0, scale=1.0, size=2000)
normal_failed = np.random.poisson(lam=0.2, size=2000)

X_normal = np.column_stack((normal_freq, normal_size, normal_failed))

# Attack Data
attack_freq = np.random.normal(loc=180, scale=30, size=100)
attack_size = np.random.normal(loc=25.0, scale=5.0, size=100)
attack_failed = np.random.randint(5, 20, size=100)

X_attack = np.column_stack((attack_freq, attack_size, attack_failed))

# Combine
X_train = np.vstack((X_normal, X_attack)).astype(np.float32)

print("Step 2: Training the Isolation Forest model...")

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X_train)

print("Step 3: Converting Python ML model to ONNX format...")

initial_type = [('float_input', FloatTensorType([None, 3]))]
onnx_model = to_onnx(
    model,
    initial_types=initial_type,
    target_opset={'': 12, 'ai.onnx.ml': 3}
)

# Save model safely
base_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(base_dir, "../models")
os.makedirs(models_dir, exist_ok=True)

model_path = os.path.join(models_dir, "anomaly_model.onnx")

with open(model_path, "wb") as f:
    f.write(onnx_model.SerializeToString())

print(f"Success! AI Model saved at: {model_path}")