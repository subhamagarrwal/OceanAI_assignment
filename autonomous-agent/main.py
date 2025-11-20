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

    # 3. Interactive Mode
    requirement = input("Enter the requirement: ") or "User login functionality with email and password"
    
    # Step 1: Generate Plan
    test_plan = agent.generate_test_plan(requirement)
    if "error" in test_plan:
        print(test_plan)
        return

    # Save plan immediately
    agent.save_test_plan(test_plan)

    # Step 2: Display options
    test_cases = test_plan.get("test_cases", [])
    print("\n📋 Generated Test Cases:")
    for idx, tc in enumerate(test_cases):
        print(f"{idx + 1}. [{tc.get('id')}] {tc.get('title')}")

    # Step 3: Select
    selection = input("\nEnter the number of the test case to generate code for (or 'all'): ")
    
    selected_cases = []
    if selection.lower() == 'all':
        selected_cases = test_cases
    else:
        try:
            idx = int(selection) - 1
            if 0 <= idx < len(test_cases):
                selected_cases = [test_cases[idx]]
            else:
                print("Invalid selection.")
                return
        except ValueError:
            print("Invalid input.")
            return

    # Step 4: Generate Code
    for tc in selected_cases:
        code = agent.generate_selenium_code(tc)
        agent.save_code(tc.get('id'), code)

    print("\n✅ Done!")

if __name__ == "__main__":
    main()
