import math
from collections import defaultdict


class BM25Ranker:
    def __init__(self, index_reader, metadata, k1=1.5, b=0.75):
        self.index_reader = index_reader
        self.total_docs = metadata["total_docs"]
        self.avg_doc_length = metadata["avg_doc_length"]
        self.doc_lengths = metadata["doc_lengths"]


        # k1: term saturation (1.2–2.0)
        # b: length normalization (0.75 standard)
        self.k1 = k1
        self.b = b

    def score(self, query_tokens):
        scores = defaultdict(float)

        for term in query_tokens:
            postings = self.index_reader.get_postings(term)
            if not postings:
                continue

            df = len(postings)
            idf = math.log((self.total_docs - df + 0.5) / (df + 0.5) + 1)

            for doc_id, tf in postings.items():
                dl = self.doc_lengths.get(str(doc_id), 0)

                denom = tf + self.k1 * (1 - self.b + self.b * (dl / self.avg_doc_length))
                score = idf * (tf * (self.k1 + 1)) / denom

                scores[doc_id] += score

        return scores
