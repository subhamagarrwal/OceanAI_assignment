from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter
from sentence_transformers import SentenceTransformer

def ingest_documents(file_path: str, embed_model: SentenceTransformer, vector_store):
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

    print("Generating embeddings...")
    valid_nodes = []
    for node in nodes:
        # Clean text: collapse whitespace
        cleaned_text = " ".join(node.text.split())
        
        if len(cleaned_text) < 5:
            continue
            
        node.text = cleaned_text
        node.embedding = embed_model.encode(cleaned_text).tolist()
        valid_nodes.append(node)

    if valid_nodes:
        print(f"Inserting {len(valid_nodes)} nodes into PGVector...")
        vector_store.add(valid_nodes)
        print("Nodes added to PGVectorStore.")
    else:
        print("No valid content found to ingest.")
