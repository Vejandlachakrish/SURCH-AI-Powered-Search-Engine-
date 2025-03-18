from flask import Flask, request, jsonify
import faiss
import numpy as np
import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.preprocessing import MinMaxScaler
from rank_bm25 import BM25Okapi

app = Flask(__name__)

# Load BERT for embedding generation
bert_model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
bert_model = BertModel.from_pretrained(bert_model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)

# Initialize FAISS index
dimension = 768
faiss_index = faiss.IndexFlatL2(dimension)

# BM25 model initialization
bm25_corpus = []  # Placeholder for corpus
bm25 = None

def preprocess_text(text):
    """ Tokenizes text for BM25 processing """
    return text.lower().split()

def encode_text(text):
    """ Generate BERT embeddings for FAISS ranking """
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        embeddings = bert_model(**tokens).last_hidden_state[:, 0, :].cpu().numpy()
    return embeddings

def initialize_faiss_index(docs):
    """ Initialize FAISS index with document embeddings """
    global faiss_index
    embeddings = np.vstack([encode_text(doc) for doc in docs])
    faiss_index.add(embeddings)

def initialize_bm25(docs):
    """ Initialize BM25 model """
    global bm25, bm25_corpus
    bm25_corpus = [preprocess_text(doc) for doc in docs]
    bm25 = BM25Okapi(bm25_corpus)

@app.route('/rank', methods=['POST'])
def rank_results():
    """ Rank results using BM25, BERT, FAISS, and LTR """
    data = request.json
    query = data.get("query", "")
    results = data.get("results", [])

    if not query or not results:
        return jsonify({"error": "Query or results missing"}), 400

    # Compute BM25 scores
    query_tokens = preprocess_text(query)
    bm25_scores = bm25.get_scores(query_tokens) if bm25 else [0] * len(results)

    # Compute FAISS similarity scores
    query_embedding = encode_text(query)
    _, faiss_scores = faiss_index.search(query_embedding, len(results))
    faiss_scores = faiss_scores[0]

    # Normalize scores
    scaler = MinMaxScaler()
    bm25_scores = scaler.fit_transform(np.array(bm25_scores).reshape(-1, 1)).flatten()
    faiss_scores = scaler.fit_transform(np.array(faiss_scores).reshape(-1, 1)).flatten()

    # Combine scores
    final_scores = 0.5 * bm25_scores + 0.5 * faiss_scores
    ranked_results = sorted(zip(results, final_scores), key=lambda x: x[1], reverse=True)

    return jsonify({"ranked_results": [{"content": doc, "score": score} for doc, score in ranked_results]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
