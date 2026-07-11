# 🚀 EdgeGuard: Real-Time Threat & Anomaly Detection System

## 📌 Overview

EdgeGuard is a real-time anomaly detection system designed to identify suspicious patterns using lightweight machine learning models running on edge devices.

## 🧠 Features

* Real-time anomaly detection
* Lightweight ML model (Isolation Forest)
* ONNX-based fast inference (C++)
* Python-based model training
* Scalable and efficient

## 🛠️ Tech Stack

* C++ (Inference Engine)
* Python (Model Training)
* ONNX Runtime
* Scikit-learn

## 📂 Project Structure

```
EdgeGuard/
│
├── cpp_engine/      # C++ inference engine
├── python_ai/       # Model training scripts
├── models/          # Trained ONNX models
├── data/            # Dataset
```

## ⚙️ Setup Instructions

### 1. Train Model (Python)

```bash
cd python_ai
python train_and_export.py
```

### 2. Run Inference Engine (C++)

```bash
cd cpp_engine
mkdir build
cd build
cmake ..
make
./edge_guard_engine
```

## 📈 Future Improvements

* Add real-time dashboard
* Integrate live data streams
* Improve model accuracy

## 🌐 Live Demo
[Click here to try EdgeGuard](https://myedgeguard.streamlit.app/)

## 👨‍💻 Author

Krish Kumar Vishwakarma
B.Tech CSE 
