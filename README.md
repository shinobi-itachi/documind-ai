# 🚀 DocuMind AI – Enterprise Document Intelligence System

DocuMind AI is an end-to-end Retrieval-Augmented Generation (RAG) system that enables users to extract insights from documents using natural language queries.

It combines semantic search, intelligent retrieval, and LLM-based generation to deliver accurate, context-aware answers with source attribution and confidence scoring.

🌐 **Live Link**: http://192.168.1.10:8501

---

## 💡 Problem Statement

Organizations store large volumes of knowledge in documents (HR policies, manuals, reports), making information retrieval slow and inefficient.

DocuMind AI solves this by:
- Understanding document content semantically
- Retrieving relevant information instantly
- Generating grounded answers with references

---

## ⚙️ Key Features

- 📂 Multi-document ingestion (PDF, DOCX, TXT)
- ✂️ Intelligent chunking for better context understanding
- 🔍 Embedding-based semantic search
- 🧠 Multi-query retrieval for improved recall
- ⚖️ MMR (Maximal Marginal Relevance) for diverse results
- 🤖 LLM-based answer generation
- 📊 Confidence scoring for response reliability
- 📌 Source attribution (document + page)
- 🌐 FastAPI backend (deployed)
- 🖥️ Streamlit UI for user interaction
- 🛡️ Fallback handling for LLM failures

---

## 🧠 How It Works

1. Documents are ingested and cleaned  
2. Text is split into manageable chunks  
3. Each chunk is converted into vector embeddings  
4. Embeddings are stored in a vector database  
5. User query is expanded into multiple variations  
6. Relevant chunks are retrieved using similarity search  
7. MMR reranks results for diversity and relevance  
8. Selected context is passed to the LLM  
9. Final answer is generated with confidence score and sources  

---

## 📊 Sample Output

```json
{
  "question": "What is maternity leave policy?",
  "answer": "Employees are eligible for around 180 days of maternity leave...",
  "confidence": "Medium",
  "sources": [
    {"source": "iima_hr_policy.pdf", "page": 83}
  ]
}


⚠️ Challenges Solved
Improved retrieval quality using multi-query expansion
Reduced redundancy using MMR reranking
Handled LLM API failures with fallback responses
Designed modular pipeline for scalability
Optimized context selection to reduce token usage
🚀 Deployment

The system is deployed using FastAPI on Render, providing:

Scalable REST API endpoints
Real-time document querying
Easy integration with frontend or external systems
🧪 Evaluation
Recall@K ≈ 85–88%
Precision@K ≈ 80–82%
Faithfulness ≈ 0.85+
🧠 Key Learnings
Retrieval quality is critical in RAG systems
Better retrieval often improves results more than model tuning
Handling real-world failures (API limits, latency) is essential
Modular design improves maintainability and scalability
🔮 Future Improvements
FAISS / Pinecone integration
Chat history memory
Advanced reranking models
Async APIs for performance
Authentication and multi-user support

👨‍💻 Author
Rohit Kamble
