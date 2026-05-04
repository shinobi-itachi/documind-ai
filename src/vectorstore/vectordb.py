import faiss
import numpy as np

class VectorDB:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)
        self.metadata = []

    def add(self, embeddings, metadata):
        self.index.add(np.array(embeddings, dtype="float32"))
        self.metadata.extend(metadata)

    def search(self, query_embedding, top_k=5):
        scores, indices = self.index.search(
            np.array([query_embedding], dtype="float32"),
            top_k
        )

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            item = self.metadata[idx]
            item["score"] = float(score)
            results.append(item)

        return results