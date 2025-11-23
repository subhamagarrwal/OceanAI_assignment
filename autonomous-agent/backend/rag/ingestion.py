from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from sentence_transformers import SentenceTransformer
import uuid

def ingest_documents(file_path: str, embed_model: SentenceTransformer, collection):
    print(f"Loading documents from {file_path}...")
    
    try:
        # Use SimpleDirectoryReader to handle various file formats (txt, md, pdf, etc.)
        reader = SimpleDirectoryReader(input_files=[file_path])
        documents = reader.load_data()
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return

    print(f"Loaded {len(documents)} document parts.")

    splitter = SentenceSplitter(chunk_size=512)
    nodes = splitter.get_nodes_from_documents(documents)

    print(f"Total chunks: {len(nodes)}")

    print("Generating embeddings and adding to ChromaDB...")
    valid_docs = []
    valid_embeddings = []
    valid_ids = []
    
    for node in nodes:
        # Clean text: collapse whitespace
        cleaned_text = " ".join(node.text.split())
        
        if len(cleaned_text) < 5:
            continue
        
        embedding = embed_model.encode(cleaned_text).tolist()
        
        valid_docs.append(cleaned_text)
        valid_embeddings.append(embedding)
        valid_ids.append(str(uuid.uuid4()))

    if valid_docs:
        print(f"Adding {len(valid_docs)} documents to ChromaDB...")
        collection.add(
            documents=valid_docs,
            embeddings=valid_embeddings,
            ids=valid_ids
        )
        print(f"✅ Successfully added {len(valid_docs)} documents to ChromaDB.")
    else:
        print("No valid content found to ingest.")
