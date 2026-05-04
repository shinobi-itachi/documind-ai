# 📄 DocuMind AI – Enterprise RAG Document Intelligence System

DocuMind AI is an end-to-end Retrieval-Augmented Generation (RAG) system that allows users to upload documents and ask questions with context-aware, intelligent answers.

🚀 Live API: https://your-render-url.onrender.com/docs

---

## 🚀 Features

- 📂 Upload multiple documents (PDF, DOCX, TXT)
- ✂️ Intelligent text chunking
- 🔍 Semantic search using embeddings
- 🧠 Multi-query retrieval for better recall
- ⚖️ MMR (Maximal Marginal Relevance) for diversity
- 🤖 LLM-based answer generation
- 📊 Confidence scoring for answers
- 🌐 FastAPI backend (deployed)
- 🖥️ Streamlit UI for interaction

---

## 🏗️ How It Works

1. Documents are uploaded
2. Text is cleaned and chunked
3. Chunks are converted into embeddings
4. Stored in a vector database
5. User query is expanded into multiple queries
6. Relevant chunks are retrieved
7. MMR selects diverse + relevant chunks
8. LLM generates final answer
9. Confidence score is calculated

---

## 📁 Project Structure
documind_ai/
│
├── app/ # Streamlit UI
├── src/
│ ├── ingestion/ # Load, clean, chunk documents
│ ├── embeddings/ # Embedding model
│ ├── retrieval/ # Multi-query + MMR
│ ├── vectorstore/ # Vector DB
│ ├── llm/ # Prompt + generator
│ ├── pipeline/ # RAG pipeline
│ ├── evaluation/ # Metrics & RAGAS
│ ├── confidence/ # Confidence scoring
│ ├── compression/ # Context compression
│
├── api.py # FastAPI backend
├── main.py # CLI pipeline
├── requirements.txt
└── README.md

⚠️ Note
If LLM API quota is exceeded, system returns fallback answers using retrieved documents.
Accuracy depends on document quality and chunking.

🧠 Key Learnings
Built full RAG pipeline from scratch
Implemented retrieval optimization (multi-query + MMR)
Handled real-world LLM failures (quota, latency)
Designed scalable backend using FastAPI

👨‍💻 Author
Rohit Kamble
