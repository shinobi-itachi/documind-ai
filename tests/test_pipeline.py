from src.evaluation.metrics import recall_at_k, precision_at_k


def test_metrics():
    retrieved = ["a", "b", "c", "d", "e"]
    relevant = ["a", "c"]

    assert recall_at_k(retrieved, relevant, 5) == 1.0
    assert precision_at_k(retrieved, relevant, 5) == 0.4