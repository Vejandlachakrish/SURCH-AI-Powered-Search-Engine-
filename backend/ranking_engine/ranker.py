from backend.indexer.indexer import Indexer
from rank_bm25 import BM25Okapi
from transformers import BertTokenizer, BertForSequenceClassification
import torch

class Ranker:
    def __init__(self):
        self.indexer = Indexer()
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased")

    def rank_results(self, query, results):
        """Ranks results using BM25 & BERT"""

        # BM25 Ranking
        tokenized_corpus = [doc["content"].split() for doc in results]
        bm25 = BM25Okapi(tokenized_corpus)
        query_tokens = query.split()
        bm25_scores = bm25.get_scores(query_tokens)

        # BERT Re-ranking
        bert_scores = []
        for doc in results:
            inputs = self.tokenizer(query, doc["content"], return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():
                logits = self.model(**inputs).logits
            bert_scores.append(logits.item())

        # Combine BM25 & BERT scores
        for i, doc in enumerate(results):
            doc["bm25_score"] = bm25_scores[i]
            doc["bert_score"] = bert_scores[i]
            doc["final_score"] = 0.5 * bm25_scores[i] + 0.5 * bert_scores[i]

        results = sorted(results, key=lambda x: x["final_score"], reverse=True)
        return results
