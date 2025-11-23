from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import shutil
import os
from pathlib import Path

# RAG imports
from rag.ingestion import ingest_documents
from rag.engine import RAGQueryEngine
from rag.retriever import ChromaRetriever
from rag.database import get_vector_store
from core.agent import AutonomousQAAgent

app = FastAPI(title="Autonomous QA Agent API")

# global variables 
agent = None
rag_engine = None
vector_store = None


@app.get("/")
async def root():
    return {"status": "ok", "message": "Autonomous QA Agent Backend is running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "rag_engine_initialized": rag_engine is not None,
        "vector_store_initialized": vector_store is not None
    }


class PlanRequest(BaseModel):
    requirement: str


class CodeRequest(BaseModel):
    test_case: dict


@app.on_event("startup")
async def startup_event():
    global agent, rag_engine, vector_store
    try:
        print("1.Initializing RAG Engine...")
        
        # Initialize vector store (ChromaDB with built-in embeddings)
        print("Connecting to vector store...")
        vector_store = get_vector_store()
        print("2.Vector store connected")
        
        # Initialize retriever (no external embedding model needed)
        print("Initializing retriever...")
        retriever = ChromaRetriever(vector_store, k=5)
        print("3.Retriever initialized")
        
        # Initialize RAG engine
        print("Initializing RAG engine...")
        rag_engine = RAGQueryEngine(retriever)
        print("4.RAG Engine ready")
        
        # Initialize Agent
        print("Initializing QA Agent...")
        agent = AutonomousQAAgent(rag_engine, output_dir="generated_tests")
        print("5.Autonomous QA Agent Ready!")
    except Exception as e:
        import traceback
        print(f"Error: Startup error: {e}")
        print(f"❌ Traceback:\n{traceback.format_exc()}")
        print("⚠️ Server will start but some features may be unavailable")
        agent = None
        rag_engine = None
        vector_store = None


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    Upload and ingest documents into ChromaDB database.
    """
    if not vector_store:
        raise HTTPException(
            status_code=503,
            detail="RAG system not initialized"
        )
    
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    
    file_paths = []
    for file in files:
        file_path = temp_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_paths.append(str(file_path))
    
    # Ingest into ChromaDB
    try:
        for file_path in file_paths:
            ingest_documents(file_path, vector_store)
        
        return {
            "message": f"Successfully processed {len(files)} files",
            "files": [f.filename for f in files]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )


@app.post("/plan")
async def generate_plan(request: PlanRequest):
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    plan = agent.generate_test_plan(request.requirement)
    return plan


@app.post("/code")
async def generate_code(request: CodeRequest):
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    code = agent.generate_selenium_code(request.test_case)
    return {"code": code}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
