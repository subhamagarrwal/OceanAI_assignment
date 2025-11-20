from pathlib import Path
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TextNode
from rag.database import vector_store
from sentence_transformers import SentenceTransformer

def clean_text_block(text: str):
    text = " ".join(text.split())
    if len(text) < 5:
        return None
    return text

def ingest_documents(file_path: str, embed_model: SentenceTransformer):
    print(f"Loading documents from {file_path}...")
    input_path = Path(file_path)
    
    if not input_path.exists():
        print(f"File {file_path} not found.")
        return

    raw = input_path.read_text(encoding="utf-8")
    documents = []

    for block in raw.split("\n\n"):
        cleaned = clean_text_block(block)
        if cleaned:
            documents.append(cleaned)

    print(f"Loaded {len(documents)} clean doc blocks.")

    splitter = SentenceSplitter(chunk_size=512)
    nodes = []

    for doc in documents:
        chunks = splitter.split_text(doc)
        for ch in chunks:
            nodes.append(TextNode(text=ch))

    print(f"Total chunks: {len(nodes)}")

    print("Generating embeddings...")
    for node in nodes:
        node.embedding = embed_model.encode(node.text).tolist()

    print("Inserting into PGVector...")
    vector_store.add(nodes)
    print("Nodes added to PGVectorStore.")
