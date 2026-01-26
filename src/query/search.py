import json

from src.query.query_parser import parse_query
from src.storage.index_reader import IndexReader
from src.storage.document_store import DocumentStore
from src.ranking.tfidf import TFIDFRanker
from src.ranking.bm25 import BM25Ranker
from src.utils.config import METADATA_PATH, RANKER
from src.utils.config import METADATA_PATH, RANKER, TITLE_INDEX_PATH


class SearchEngine:
    def __init__(self, index_path, doc_store_path, total_docs=None):
        self.index_reader = IndexReader(index_path)
        self.doc_store = DocumentStore()
        self.doc_store.load(doc_store_path)
        self.title_index_reader = IndexReader(TITLE_INDEX_PATH)

        # load metadata
        with open(METADATA_PATH, "r") as f:
            metadata = json.load(f)

        # choose ranker
        if RANKER == "bm25":
            self.ranker = BM25Ranker(
                                    body_index = self.index_reader,
                                    title_index = self.title_index_reader,
                                    metadata = metadata
                                    )

        else:
            self.ranker = TFIDFRanker(self.index_reader, metadata["total_docs"])

    def search(self, query, top_k=10):
        tokens = parse_query(query)
        scores = self.ranker.score(tokens)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for doc_id, score in ranked:
            title = self.doc_store.get(doc_id)
            results.append((doc_id, title, round(score, 4)))

        return results
