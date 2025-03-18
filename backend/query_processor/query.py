from backend.indexer.indexer import Indexer
from backend.ranking_engine.ranker import Ranker
from backend.personalization.personalizer import Personalizer

class QueryProcessor:
    def __init__(self):
        self.indexer = Indexer()
        self.ranker = Ranker()
        self.personalizer = Personalizer()

    def process_query(self, query, user_id=None):
        """Fetch and rank results, then personalize"""
        
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title^2", "content"],
                    "fuzziness": "AUTO"
                }
            }
        }

        response = self.indexer.es.search(index="surch_index", body=search_body)
        results = [
            {
                "title": hit["_source"]["title"],
                "snippet": hit["_source"]["content"][:200] + "...",
                "url": hit["_source"]["url"]
            }
            for hit in response["hits"]["hits"]
        ]

        # Rank results
        ranked_results = self.ranker.rank_results(query, results)

        # Personalize if user_id is given
        if user_id:
            ranked_results = self.personalizer.personalize_results(user_id, ranked_results)

        return ranked_results
