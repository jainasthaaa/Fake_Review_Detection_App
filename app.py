import pandas as pd
import re
import string
import os
import json
import time
import hashlib
import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sample dataset with real & fake reviews
data = {
    "review": [
        "Great quality! Love it!", 
        "Amazing fit, highly recommended!", 
        "Best deal ever! Buy now!", 
        "Totally fake product, scam!", 
        "Horrible quality, not worth it!", 
        "This is a spam review, avoid!",
        "BUY NOW! Best deal ever!!",
        "Fits well, comfortable!",
        "Worst product ever, don't buy!",
        "Scam product, totally fake!"
    ],
    "label": [1, 1, 0, 0, 0, 0, 0, 1, 1, 0]  # 1 = Genuine, 0 = Fake
}

df = pd.DataFrame(data)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df["cleaned_review"] = df["review"].apply(preprocess_text)

# Train model using TF-IDF and Naïve Bayes
vectorizer = TfidfVectorizer()
classifier = MultinomialNB()
pipeline = Pipeline([("tfidf", vectorizer), ("classifier", classifier)])

X_train = df["cleaned_review"]
y_train = df["label"]
pipeline.fit(X_train, y_train)

# Fake Review Detection Function
def predict_review(review_text):
    review_text = preprocess_text(review_text)
    prediction = pipeline.predict([review_text])[0]
    return "Genuine Review" if prediction == 1 else "Fake Review"

# User purchase verification dataset
verified_users = {
    "user123": ["productA", "productB"],
    "user456": ["productC"],
    "user789": ["productZ"],
    "user999": ["productX"],
    "user111": ["productB"]
}

@app.route('/')
def index():
    return redirect(url_for('serve_html'))

@app.route('/c')
def serve_html():
    return render_template('c.html')

review_chain = []

# Review Prediction API
@app.route('/predict', methods=['POST'])
def predict():
    data = request.form
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    review_text = data.get("review")
    file = request.files.get("file")

    if not user_id or not product_id or not review_text:
        return render_template('c.html', error="Missing fields")

    # Verify purchase
    is_verified = user_id in verified_users and product_id in verified_users[user_id]

    # Predict review authenticity
    prediction = predict_review(review_text)
    proof_filename = None
    if file:
        proof_filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], proof_filename))

    if not is_verified:
        if proof_filename:
            prediction = "Pending Verification"
        else:
            prediction = "Fake Review"

    # Save review
    review_data = {
        "user_id": user_id,
        "product_id": product_id,
        "review": review_text,
        "purchase_verified": is_verified,
        "prediction": prediction,
        "proof": proof_filename,
        "timestamp": time.time()
    }
    review_hash = hashlib.sha256(json.dumps(review_data).encode()).hexdigest()
    review_data["hash"] = review_hash

    # Update review chain
    if review_chain:
        review_data["previous_hash"] = review_chain[-1]["hash"]
    else:
        review_data["previous_hash"] = None

    review_chain.append(review_data)

    return jsonify(review_data)

# Endpoint to get the review chain
@app.route('/review-chain', methods=['GET'])
def get_review_chain():
    return jsonify(review_chain)

# Run Flask App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)