from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path

from src.pipeline.rag_pipeline import build_index, run_pipeline

app = FastAPI(
    title="DocuMind AI API",
    description="Enterprise RAG Powered Document Intelligence System",
    version="1.0.0"
)

# =========================
# Enable CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Request Schema
# =========================
class QueryRequest(BaseModel):
    query: str

# =========================
# File Upload
# =========================
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload a PDF, DOCX, or image file for processing"""
    
    allowed_extensions = ['.pdf', '.docx', '.png', '.jpg', '.jpeg']
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in allowed_extensions:
        return {
            "error": f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        }
    
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "size": file_path.stat().st_size,
        "path": str(file_path)
    }

# =========================
# Health Check
# =========================
@app.get("/")
def root():
    return {
        "message": "DocuMind AI API Running"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# =========================
# Build Vector Index
# =========================
@app.get("/build-index")
def build_vector_index():
    data = build_index()
    
    return {
        "message": "Index built successfully",
        "documents": data["num_documents"],
        "chunks": data["num_chunks"]
    }

# =========================
# Ask Question
# =========================
@app.post("/ask")
def ask_question(request: QueryRequest):
    result = run_pipeline(request.query)
    
    return {
        "query": request.query,
        "answer": result["answer"],
        "confidence": result["confidence"],
        "sources": result["sources"]
    }