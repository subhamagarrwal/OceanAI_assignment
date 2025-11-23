import chromadb
from pathlib import Path

CHROMA_DB_PATH = Path("chroma_data")
CHROMA_DB_PATH.mkdir(exist_ok=True)

client = chromadb.PersistentClient(path=str(CHROMA_DB_PATH))

def get_vector_store():
    return client.get_or_create_collection(
        name="rag_documents",
        metadata={"hnsw:space": "cosine"}
    )
