from src.ingestion.load_documents import load_documents
from src.ingestion.clean_text import clean_text
from src.ingestion.chunking import chunk_documents

from src.embeddings.embedding_model import EmbeddingModel
from src.vectorstore.vectordb import VectorDB

from src.retrieval.multi_query import generate_multi_queries
from src.retrieval.mmr import mmr

from src.llm.prompt_template import build_prompt
from src.llm.generator import generate_answer


# ======================
# 1. LOAD + PREPROCESS
# ======================
docs = load_documents("data/raw")
print("Loaded docs:", len(docs))

for d in docs:
    d["text"] = clean_text(d["text"])

chunks = chunk_documents(docs)
print("Total chunks:", len(chunks))


# ======================
# 2. EMBEDDINGS
# ======================
embedder = EmbeddingModel()

texts = [c["text"] for c in chunks]

print("Creating embeddings...")
embeddings = embedder.encode(texts)


# ======================
# 3. VECTOR DB
# ======================
vectordb = VectorDB(dim=len(embeddings[0]))
vectordb.add(embeddings, chunks)

print("Vector DB created!")


# ======================
# 4. QUERY + RETRIEVAL
# ======================
query = "What is maternity leave policy?"

queries = generate_multi_queries(query)

all_results = []

for q in queries:
    q_emb = embedder.encode([q])[0]
    results = vectordb.search(q_emb, top_k=3)
    all_results.extend(results)


# ======================
# 5. REMOVE DUPLICATES
# ======================
unique_results = {}

for r in all_results:
    key = r["text"]
    if key not in unique_results or r["score"] > unique_results[key]["score"]:
        unique_results[key] = r

candidate_docs = list(unique_results.values())


# ======================
# 6. MMR RERANKING
# ======================
candidate_texts = [doc["text"] for doc in candidate_docs]
candidate_embs = embedder.encode(candidate_texts)

query_emb = embedder.encode([query])[0]

final_results = mmr(
    query_emb=query_emb,
    doc_embs=candidate_embs,
    docs=candidate_docs,
    top_k=5
)


# ======================
# 7. PRINT RETRIEVAL
# ======================
print("\nTop Results:\n")

for r in final_results:
    print(f"Score: {r['score']:.3f}")
    print(f"Source: {r['source']} | Page: {r['page']}")
    print(r["text"][:200])
    print("-" * 50)


# ======================
# 8. RAG (LLM GENERATION)
# ======================
prompt = build_prompt(query, final_results)

answer = generate_answer(prompt)

print("\nFINAL ANSWER:\n")
print(answer)