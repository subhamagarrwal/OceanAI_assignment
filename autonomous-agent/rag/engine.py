from llama_index.core import QueryBundle
from llm.groq_client import groq_smart

class RAGQueryEngine:
    def __init__(self, retriever):
        self.retriever = retriever

    def query(self, q):
        bundle = QueryBundle(q)
        retrieved = self.retriever.retrieve(bundle)
        
        context = "\n\n".join([n.node.text for n in retrieved])
        
        final_prompt = f"""
        You are a Test Scenario Generation LLM.
        Based on the Context below, generate a detailed Test Plan in JSON.
        
        CONTEXT:
        {context}

        QUESTION:
        {q}

        OUTPUT REQUIREMENTS:
        Return a JSON object with a key "test_cases" containing a list.
        Each item must have:
        - "id": "TC001"
        - "title": "Short title"
        - "steps": ["Step 1", "Step 2", ...]
        - "expected_result": "Final verification step"
        """
        
        return groq_smart(final_prompt)
