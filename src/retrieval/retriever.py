from src.retrieval.multi_query import generate_multi_queries
from src.retrieval.mmr import mmr


def retrieve_documents(query, embedder, vectordb, top_k=5):
    queries = generate_multi_queries(query)

    all_results = []

    for q in queries:
        q_emb = embedder.encode([q])[0]
        results = vectordb.search(q_emb, top_k=top_k)
        all_results.extend(results)

    # remove duplicates
    unique = []
    seen = set()

    for r in all_results:
        key = (r["source"], r["page"], r["text"][:100])

        if key not in seen:
            seen.add(key)
            unique.append(r)

    doc_embs = [embedder.encode([r["text"]])[0] for r in unique]
    query_emb = embedder.encode([query])[0]

    final_results = mmr(query_emb, doc_embs, unique, top_k=top_k)

    return final_results