import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b)


def mmr(query_emb, doc_embs, docs, top_k=5, lambda_param=0.7):
    """
    Maximal Marginal Relevance (MMR)

    Balances:
    - Relevance (similarity to query)
    - Diversity (difference from already selected docs)
    """

    selected = []
    selected_indices = []

    if len(docs) == 0:
        return []

    # Step 1: pick most relevant doc
    similarities = [cosine_similarity(query_emb, emb) for emb in doc_embs]
    first_idx = int(np.argmax(similarities))

    selected.append(docs[first_idx])
    selected_indices.append(first_idx)

    # Step 2: iteratively select remaining docs
    while len(selected) < min(top_k, len(docs)):
        mmr_scores = []

        for i, emb in enumerate(doc_embs):
            if i in selected_indices:
                mmr_scores.append(-np.inf)
                continue

            relevance = cosine_similarity(query_emb, emb)

            diversity = max(
                [cosine_similarity(emb, doc_embs[j]) for j in selected_indices],
                default=0
            )

            score = lambda_param * relevance - (1 - lambda_param) * diversity
            mmr_scores.append(score)

        next_idx = int(np.argmax(mmr_scores))

        selected.append(docs[next_idx])
        selected_indices.append(next_idx)

    return selected