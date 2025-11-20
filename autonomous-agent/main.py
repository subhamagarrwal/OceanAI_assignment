from sentence_transformers import SentenceTransformer
from rag.database import vector_store
from rag.retriever import PGVectorRetriever
from rag.engine import RAGQueryEngine
from core.agent import AutonomousQAAgent

def main():
    # 1. Setup RAG Components
    print("Initializing RAG components...")
    embed_model = SentenceTransformer("all-MiniLM-L6-v2")
    retriever = PGVectorRetriever(vector_store, embed_model)
    rag_engine = RAGQueryEngine(retriever)

    # 2. Initialize Agent
    agent = AutonomousQAAgent(rag_engine)

    # 3. Run
    requirement = "User login functionality with email and password"
    agent.run(requirement, generate_all_tests=False)

if __name__ == "__main__":
    main()
