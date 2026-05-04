from src.ingestion.load_documents import load_documents
from src.ingestion.clean_text import clean_text
from src.ingestion.chunking import chunk_documents

from src.embeddings.embedding_model import EmbeddingModel
from src.vectorstore.vectordb import VectorDB

from src.retrieval.multi_query import generate_multi_queries
from src.retrieval.mmr import mmr

from src.llm.prompt_template import build_prompt
from src.llm.generator import generate_answer


def build_index():
    docs = load_documents("data/raw")

    for d in docs:
        d["text"] = clean_text(d["text"])

    chunks = chunk_documents(docs)

    embedder = EmbeddingModel()
    texts = [c["text"] for c in chunks]
    embeddings = embedder.encode(texts)

    vectordb = VectorDB(dim=len(embeddings[0]))
    vectordb.add(embeddings, chunks)

    return {
        "num_documents": len(docs),
        "num_chunks": len(chunks),
        "vectordb": vectordb,
        "embedder": embedder
    }


def run_pipeline(query):
    data = build_index()

    vectordb = data["vectordb"]
    embedder = data["embedder"]

    queries = generate_multi_queries(query)

    all_results = []

    for q in queries:
        q_emb = embedder.encode([q])[0]
        results = vectordb.search(q_emb, top_k=3)
        all_results.extend(results)

    unique_results = {}
    for r in all_results:
        key = r["text"]
        if key not in unique_results or r["score"] > unique_results[key]["score"]:
            unique_results[key] = r

    candidate_docs = list(unique_results.values())

    candidate_texts = [doc["text"] for doc in candidate_docs]
    candidate_embs = embedder.encode(candidate_texts)

    query_emb = embedder.encode([query])[0]

    final_results = mmr(query_emb, candidate_embs, candidate_docs, top_k=5)

    prompt = build_prompt(query, final_results)
    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "confidence": "Medium",
        "sources": [
            {
                "source": doc["source"],
                "page": doc["page"]
            }
            for doc in final_results
        ]
    }