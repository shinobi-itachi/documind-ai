def confidence_score(results):
    if not results:
        return 0

    avg_score = sum(r["score"] for r in results) / len(results)

    confidence = round(avg_score * 100, 2)

    if confidence > 100:
        confidence = 100

    return confidence