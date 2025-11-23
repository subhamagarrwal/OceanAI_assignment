from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
import shutil
import os
from pathlib import Path

# Import modules
from sentence_transformers import SentenceTransformer
from rag.database import get_vector_store
from rag.retriever import ChromaRetriever
from rag.engine import RAGQueryEngine
from core.agent import AutonomousQAAgent
from rag.ingestion import ingest_documents

app = FastAPI(title="Autonomous QA Agent API")

# --- Global State ---
agent = None
embed_model = None
collection = None


@app.get("/")
async def root():
    return {"status": "ok", "message": "Autonomous QA Agent Backend is running"}


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "agent_initialized": agent is not None,
        "vector_store_initialized": collection is not None
    }


class PlanRequest(BaseModel):
    requirement: str


class CodeRequest(BaseModel):
    test_case: dict


@app.on_event("startup")
async def startup_event():
    global agent, embed_model, collection
    try:
        print("🚀 Initializing RAG & Agent with ChromaDB...")
        
        embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Embedding model loaded")
        
        collection = get_vector_store()
        print("✅ ChromaDB collection initialized")
        
        retriever = ChromaRetriever(collection, embed_model)
        rag_engine = RAGQueryEngine(retriever)
        
        agent = AutonomousQAAgent(rag_engine, output_dir="generated_tests")
        print("✅ Backend Ready!")
    except Exception as e:
        print(f"❌ Startup error: {e}")
        import traceback
        traceback.print_exc()
        print("⚠️ Server will start but some features may be unavailable")
        agent = None
        collection = None


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    if not collection:
        raise HTTPException(status_code=503, detail="Vector store not initialized")
    
    if not embed_model:
        raise HTTPException(status_code=503, detail="Embedding model not initialized")
    
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    
    ingested_count = 0
    for file in files:
        file_path = temp_dir / file.filename
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            ingest_documents(str(file_path), embed_model, collection)
            ingested_count += 1
        except Exception as e:
            print(f"Error processing {file.filename}: {e}")
    
    return {
        "message": f"Successfully processed {ingested_count} out of {len(files)} files",
        "total_documents_in_store": collection.count()
    }


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
