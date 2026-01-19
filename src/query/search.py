from src.ranking.tfidf import TFIDFRanker
from src.query.query_parser import parse_query
from src.storage.index_reader import IndexReader
from src.storage.document_store import DocumentStore
from src.utils.config import INVERTED_INDEX_PATH, DOCUMENT_STORE_PATH


class SearchEngine:
    def __init__(self, index_path, doc_store_path, total_docs: int):
        self.index_reader = IndexReader(index_path)
        self.doc_store = DocumentStore.load(doc_store_path)
        self.ranker = TFIDFRanker(self.index_reader, total_docs)

    def search(self, query, top_k=10):
        tokens = parse_query(query)

        scores = self.ranker.score(tokens)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []
        for doc_id, score in ranked[:top_k]:
            title = self.doc_store.get_title(doc_id)
            results.append((doc_id, title, round(score, 3)))
        print("Query tokens:", tokens)
        print("Scores:", scores)

        return results
