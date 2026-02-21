# Deep-Learning-Intrusion-Detection-System-
# SECURE_IDS | Deep Learning Intrusion Detection System

A modern, full-stack Network Intrusion Detection System (IDS) that leverages Deep Learning to identify malicious network traffic in real-time or via bulk CSV uploads.



## ✨ Features
* **Real-time Analysis:** Input single CSV rows for instant binary classification.
* **Bulk CSV Upload:** Process entire datasets to calculate attack/benign distribution percentages.
* **Modern Dashboard:** A clean, minimalist UI with high-contrast visual indicators.
* **Automated Normalization:** Built-in L2 normalization logic to ensure data matches training standards.
* **Apache Integration:** Configuration files included for professional deployment on Linux/Ubuntu.

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3 (Modern UI), JavaScript (ES6+).
* **Backend:** Python 3.x, Flask, SQLAlchemy.
* **AI/ML:** TensorFlow 2.x, Keras (.keras format), Scikit-learn.
* **Deployment:** Apache2, mod_wsgi.

## 📂 Project Structure
```text
.
├── app.py              # Flask Backend & Prediction Logic
├── ids_app.wsgi        # Apache Entry Point
├── static/
│   └── style.css       # Modern UI Styling
├── templates/
│   └── index.html      # Dashboard Interface
├── ids_model.keras     # Trained Model (Local only, not uploaded)
└── .gitignore          # Excludes large files and datasets
