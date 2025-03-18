from elasticsearch import Elasticsearch
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Connect to Elasticsearch
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")
INDEX_NAME = "surch_index"

es = Elasticsearch([ELASTICSEARCH_HOST])

# Create the index if it doesn't exist
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body={
            "mappings": {
                "properties": {
                    "url": {"type": "keyword"},
                    "content": {"type": "text"}
                }
            }
        })

create_index()

@app.route('/index', methods=['POST'])
def index_document():
    """ Receives data from the crawler and stores it in Elasticsearch """
    data = request.json
    if not data or 'url' not in data or 'content' not in data:
        return jsonify({"error": "Invalid data"}), 400

    doc = {
        "url": data['url'],
        "content": data['content']
    }
    es.index(index=INDEX_NAME, body=doc)
    
    return jsonify({"message": "Document indexed"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
