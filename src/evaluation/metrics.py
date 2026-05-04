def recall_at_k(retrieved, relevant, k=5):
    retrieved_k = retrieved[:k]

    hit = sum(1 for r in retrieved_k if r in relevant)

    return hit / len(relevant) if relevant else 0


def precision_at_k(retrieved, relevant, k=5):
    retrieved_k = retrieved[:k]

    hit = sum(1 for r in retrieved_k if r in relevant)

    return hit / k