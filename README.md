# 🛡️ AI-Powered Trust & Safety Routing Engine

An end-to-end intelligent moderation system that classifies user-generated content and applies operational routing logic to manage platform safety at scale.

---

## 📌 Project Vision
In modern social platforms, the volume of content makes 100% human moderation impossible. This project creates a "Triaging Layer" that:
1.  **Reduces Moderator Burnout** by auto-approving safe content.
2.  **Prioritizes High-Risk Harm** by routing threats to Subject Matter Experts (SMEs).
3.  **Ensures Accuracy** through a Human-in-the-Loop (HITL) triage system.

---

## 📊 1. Data Architecture & DNA
The engine is trained on the **Jigsaw Toxic Comment Dataset** (~160,000 comments).

### The Engineering Challenge: Class Imbalance
The dataset is naturally skewed (90% Safe vs. 10% Toxic). To make the model "safety-ready," I implemented:
* **The 7th Class (`is_safe`):** Unlike standard models that only look for toxicity, I engineered a dedicated "Safe" class. This allows the model to learn the specific vocabulary of healthy conversation.
* **Balanced Undersampling:** I reduced the "Safe" class to a 1:1 ratio with the collective "Toxic" classes during training. This prevents the model from being "blinded" by the sheer volume of safe data.
* **Feature Engineering:** Used **TF-IDF Vectorization** (top 10,000 words) to convert text into numerical signals that prioritize unique, high-impact words over common stop-words.

[Image of a bar chart showing class distribution in a toxic comment dataset]

---

## 🏗️ 2. Technical Architecture
The system follows a decoupled Full-Stack ML architecture:

### **The Backend (AI Brain)**
* **Algorithm:** Multi-label **Logistic Regression** (OneVsRest). 
* **Why this choice?** It offers high **interpretability**. In T&S, we must be able to explain *why* a comment was flagged.
* **API:** A Flask-based REST service that processes text and returns probability scores for 7 distinct categories.

### **The Routing Engine (Operational Logic)**
The system applies "Business Rules" to the raw AI scores to determine the next step in the moderation workflow:
* **✅ Auto-Approve:** If `is_safe` probability is > 0.85.
* **🚨 SME Route:** If high-harm labels (`threat` or `identity_hate`) are detected with > 0.80 confidence.
* **🔍 General Triage:** If confidence is "Medium" (0.50 - 0.80), the content is sent to a human queue for a final decision.

[Image of a trust and safety human-in-the-loop workflow diagram]

---

## 📈 3. Performance Metrics
In Trust & Safety, **Recall** (not missing a violation) is often more important than **Precision**.

| Category | Priority | Result | Strategic Insight |
| :--- | :--- | :--- | :--- |
| **is_safe** | Automation | **93% Recall** | Successfully automates the vast majority of harmless traffic. |
| **threat** | Safety | **71% Recall** | High-sensitivity setting to ensure physical safety. |
| **Latency** | Speed | **~85ms** | Fast enough for real-time, "at-the-edge" moderation. |

[Image of a precision-recall curve for multi-label classification]

---

## 🚀 4. Installation & Usage

### 1. Clone & Install
```bash
git clone [https://github.com/sasimula/Trust-Safety-Routing-Engine.git](https://github.com/sasimula/Trust-Safety-Routing-Engine.git)
cd Trust-Safety-Routing-Engine
pip install -r requirements.txt
