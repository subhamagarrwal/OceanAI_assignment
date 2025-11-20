from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Optional
import shutil
import os
from pathlib import Path

# Import your existing modules
from sentence_transformers import SentenceTransformer
from rag.database import vector_store
from rag.retriever import PGVectorRetriever
from rag.engine import RAGQueryEngine
from core.agent import AutonomousQAAgent
from rag.ingestion import ingest_documents

app = FastAPI(title="Autonomous QA Agent API")

# --- Global State ---
agent = None
embed_model = None

class PlanRequest(BaseModel):
    requirement: str

class CodeRequest(BaseModel):
    test_case: dict

@app.on_event("startup")
async def startup_event():
    global agent, embed_model
    print("🚀 Initializing RAG & Agent...")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    retriever = PGVectorRetriever(vector_store, embed_model)
    rag_engine = RAGQueryEngine(retriever)
    agent = AutonomousQAAgent(rag_engine, output_dir="generated_tests")
    print("✅ Backend Ready!")

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    # Save to temp dir then ingest
    temp_dir = Path("temp_uploads")
    temp_dir.mkdir(exist_ok=True)
    
    saved_paths = []
    for file in files:
        file_path = temp_dir / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(str(file_path))
        
        # Ingest immediately
        try:
            ingest_documents(str(file_path), embed_model)
        except Exception as e:
            print(f"Error ingesting {file.filename}: {e}")
            # We continue even if one fails, or you might want to return error
    
    return {"message": f"Successfully processed {len(files)} files"}

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
    
    # We return the code string directly to the frontend
    code = agent.generate_selenium_code(request.test_case)
    return {"code": code}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
