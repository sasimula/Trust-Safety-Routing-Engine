# 🛡️ AI-Powered Trust & Safety Routing Engine

An end-to-end Machine Learning pipeline and web application designed to classify online comments and intelligently route them to specialized moderation queues.

## 📌 Project Overview
In a platform with millions of users, human moderators cannot review every comment. This project solves two major problems:
1. **Moderator Burnout:** By auto-approving clearly safe content.
2. **Specialized Handling:** By routing high-risk content (Threats, Identity Hate) to Subject Matter Experts (SMEs).

## 📊 The Dataset & Engineering Challenge
The project uses the **Jigsaw Toxic Comment Classification** dataset (approx. 160k rows).

### 1. The Imbalance Problem
The dataset is highly imbalanced:
* **~90% Safe:** General conversation.
* **~10% Toxic:** Breaking at least one policy.
* **<1% Threats/Hate:** Extremely rare but high-risk.



### 2. Data Engineering Strategy
To ensure the AI could "see" the rare classes without being overwhelmed by safe data, I implemented:
* **Undersampling:** Reduced the 'Safe' class to match the total volume of 'Toxic' classes (1:1 ratio).
* **7-Class Architecture:** Added `is_safe` as an explicit target class to reduce False Positives (like "I like gemini").
* **Weighted Loss:** Used `class_weight='balanced'` in the Logistic Regression model to penalize the misclassification of rare labels like 'Threat'.

## ⚙️ Technical Stack
* **ML Core:** Python, Scikit-Learn (Logistic Regression, OneVsRestClassifier).
* **NLP:** TF-IDF Vectorization (Top 10,000 features).
* **Backend:** Flask API (Handles real-time classification and routing logic).
* **Frontend:** React + Tailwind CSS (Operational Dashboard for testing).

## 📈 Model Performance
Based on the final training run:

| Category | Precision | Recall | F1-Score | Insight |
| :--- | :--- | :--- | :--- | :--- |
| **is_safe** | 0.86 | **0.93** | 0.89 | High Recall means 93% of safe traffic is auto-approved. |
| **threat** | 0.34 | **0.71** | 0.46 | Jumped from 12% to 71% recall through class weighting. |
| **toxic** | 0.89 | 0.84 | 0.86 | Strong general performance. |



## 🛠️ Operational Logic (The "Routing Engine")
The system doesn't just predict a label; it makes a business decision:
* **Confidence > 80%:** Routes to a specific **SME Queue** (e.g., `🚨 THREAT_SME_QUEUE`).
* **Confidence 50-80%:** Routes to **General Triage**.
* **Predicted 'is_safe':** Routes to **✅ SAFE_AUTO_APPROVE**.

## 🚀 How to Run
1. **Install Dependencies:** `pip install -r requirements.txt`
2. **Start Backend:** `python app.py`
3. **Launch Frontend:** Open `index.html` in a browser.
