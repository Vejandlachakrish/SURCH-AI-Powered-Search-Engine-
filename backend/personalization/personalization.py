from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import random
import os
from collections import defaultdict
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from contextualbandits.online import LinUCB

app = Flask(__name__)

# User history storage (simulated database)
user_click_data = defaultdict(list)  # {user_id: [(query, clicked_doc)]}

# Collaborative Filtering Model
reader = Reader(rating_scale=(0, 1))
svd_model = SVD()

# Contextual Bandit Model
num_arms = 10  # Number of recommendation choices
lin_ucb = LinUCB(num_arms)

def train_collaborative_filtering():
    """ Train a collaborative filtering model using user history """
    if not user_click_data:
        return
    data = []
    for user, interactions in user_click_data.items():
        for query, doc in interactions:
            data.append((user, doc, 1))  # Assume all clicks are positive interactions
    df = pd.DataFrame(data, columns=["user", "doc", "rating"])
    surprise_data = Dataset.load_from_df(df, reader)
    trainset = surprise_data.build_full_trainset()
    svd_model.fit(trainset)

def recommend_cf(user_id):
    """ Recommend documents using collaborative filtering """
    if not user_click_data.get(user_id):
        return []
    known_docs = [doc for _, doc in user_click_data[user_id]]
    predictions = [(doc, svd_model.predict(user_id, doc).est) for doc in known_docs]
    return sorted(predictions, key=lambda x: x[1], reverse=True)[:5]

def recommend_bandit(user_id, query, available_docs):
    """ Use a contextual bandit model to personalize recommendations """
    user_context = np.random.rand(num_arms)  # Simulating user context as a random vector
    action = lin_ucb.predict(user_context.reshape(1, -1))[0]
    return available_docs[min(action, len(available_docs) - 1)]  # Choose best-ranked doc

@app.route('/personalize', methods=['POST'])
def personalize_results():
    """ Personalize search results using collaborative filtering & bandits """
    data = request.json
    user_id = data.get("user_id", "")
    query = data.get("query", "")
    results = data.get("results", [])

    if not user_id or not query or not results:
        return jsonify({"error": "Missing parameters"}), 400

    # Train models if data exists
    train_collaborative_filtering()

    # Get CF recommendations
    cf_recommendations = recommend_cf(user_id)
    cf_docs = [doc for doc, _ in cf_recommendations]

    # Apply contextual bandit model for final personalization
    final_results = [recommend_bandit(user_id, query, results)] + [doc for doc in results if doc not in cf_docs]
    
    return jsonify({"personalized_results": final_results[:5]})

@app.route('/log_click', methods=['POST'])
def log_user_click():
    """ Log user clicks to improve personalization """
    data = request.json
    user_id = data.get("user_id", "")
    query = data.get("query", "")
    clicked_doc = data.get("clicked_doc", "")

    if not user_id or not query or not clicked_doc:
        return jsonify({"error": "Missing parameters"}), 400

    user_click_data[user_id].append((query, clicked_doc))
    return jsonify({"message": "Click logged successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
