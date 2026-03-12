from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import warnings

warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app) 

print("Loading 7-Class AI Model...")
vectorizer = joblib.load('tfidf_vectorizer.pkl')
classifier = joblib.load('ts_routing_model.pkl')

# IMPORTANT: We added 'is_safe' to the end of the list!
POLICIES = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate', 'is_safe']

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('comment_text', '')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Convert text to math and get probabilities
    vectorized_text = vectorizer.transform([text])
    probs = classifier.predict_proba(vectorized_text)[0]
    
    max_prob = np.max(probs)
    max_index = np.argmax(probs)
    predicted_policy = POLICIES[max_index]
    
    # --- UPDATED ROUTING LOGIC ---
    if predicted_policy == 'is_safe':
        assigned_queue = "✅ SAFE_AUTO_APPROVE"
    elif max_prob >= 0.80:
        assigned_queue = f"🚨 {predicted_policy.upper()}_SME_QUEUE"
    elif max_prob >= 0.50:
        assigned_queue = "⚠️ GENERAL_TRIAGE_QUEUE"
    else:
        assigned_queue = "✅ SAFE_AUTO_APPROVE"
        
    return jsonify({
        "original_text": text,
        "predicted_policy": predicted_policy,
        "confidence_score": round(max_prob * 100, 2),
        "assigned_queue": assigned_queue
    })

if __name__ == '__main__':
    print("API is LIVE on port 5000!")
    app.run(port=5000, debug=True)