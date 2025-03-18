from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# ✅ Ensure Elasticsearch is correctly connected
ES_HOST = "http://elasticsearch:9200"  # Use "elasticsearch" when running in Docker
ES_USER = "elastic"
ES_PASS = "changeme"

def connect_to_elasticsearch():
    """Attempts to connect to Elasticsearch and returns the client."""
    try:
        es_client = Elasticsearch(ES_HOST, basic_auth=(ES_USER, ES_PASS))
        if es_client.ping():
            print("✅ Successfully connected to Elasticsearch!")
            return es_client
        else:
            raise ValueError("❌ Elasticsearch is running but NOT responding to pings!")
    except Exception as e:
        print(f"❌ Error connecting to Elasticsearch: {e}")
        return None

es = connect_to_elasticsearch()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "SURCH Search Engine Backend Running"}), 200

@app.route("/search", methods=["GET"])
def search():
    if es is None:
        return jsonify({"error": "❌ Elasticsearch is not connected"}), 500

    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "No search query provided", "results": []}), 400

    search_results = perform_search(query)

    if isinstance(search_results, dict) and "error" in search_results:
        return jsonify(search_results), 500  # Return error response if search failed

    return jsonify({"results": search_results})  # Return actual results

def perform_search(query):
    """Fetch search results from Elasticsearch"""
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^2", "content"],  # Boost title importance
                "fuzziness": "AUTO"  # Allow typo tolerance
            }
        }
    }

    try:
        response = es.search(index="surch_index", body=search_body)

        if response["hits"]["total"]["value"] == 0:
            return []  # Return empty list if no results found

        results = [
            {
                "title": hit["_source"].get("title", "No Title"),
                "snippet": hit["_source"].get("content", "")[:200] + "...",  # Short preview
                "url": hit["_source"].get("url", "#"),
                "score": hit["_score"]  # Relevance score
            }
            for hit in response["hits"]["hits"]
        ]

        print(f"🔍 Search Results: {results}")  # Debugging output
        return results

    except Exception as e:
        print(f"❌ Elasticsearch search error: {e}")
        return {"error": f"Search failed: {str(e)}"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
