from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from rank_bm25 import BM25Okapi
import os
import re
import string
import torch
from transformers import BertTokenizer, BertForSequenceClassification

app = Flask(__name__)

# Connect to Elasticsearch
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
INDEX_NAME = "surch_index"

es = Elasticsearch([ELASTICSEARCH_HOST])

# Load BERT Model for Query Relevance Scoring
bert_model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
bert_model = BertForSequenceClassification.from_pretrained(bert_model_name, num_labels=1)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bert_model.to(device)

def preprocess_text(text):
    """ Clean and tokenize text for BM25 ranking """
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    return text.split()

@app.route('/search', methods=['GET'])
def search():
    """ Process query and return ranked results """
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Fetch documents from Elasticsearch
    es_results = es.search(index=INDEX_NAME, body={"query": {"match": {"content": query}}}, size=20)
    docs = [hit["_source"]["content"] for hit in es_results["hits"]["hits"]]
    
    if not docs:
        return jsonify({"results": []})

    # Apply BM25 ranking
    bm25 = BM25Okapi([preprocess_text(doc) for doc in docs])
    query_tokens = preprocess_text(query)
    bm25_scores = bm25.get_scores(query_tokens)

    # Apply BERT ranking
    bert_inputs = tokenizer([query] * len(docs), docs, padding=True, truncation=True, return_tensors="pt").to(device)
    with torch.no_grad():
        bert_scores = bert_model(**bert_inputs).logits.squeeze().cpu().tolist()

    # Combine BM25 and BERT scores (weighted sum)
    combined_scores = [(docs[i], 0.5 * bm25_scores[i] + 0.5 * bert_scores[i]) for i in range(len(docs))]
    ranked_results = sorted(combined_scores, key=lambda x: x[1], reverse=True)

    return jsonify({"results": [{"content": doc, "score": score} for doc, score in ranked_results]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
