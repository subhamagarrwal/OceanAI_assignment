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
        You are a Senior QA Automation Architect.
        Based on the Context below, generate a COMPREHENSIVE Test Plan in JSON.
        
        ### CONTEXT
        <documentation>
        {context}
        </documentation>

        ### TASK
        <question>
        {q}
        </question>

        ### OUTPUT REQUIREMENTS
        1. **Quantity**: Generate a minimum of 10 test cases.
        2. **Coverage**: Include Positive, Negative, and Edge cases.
        3. **Format**: Return a JSON object with a key "test_cases" containing a list.
        4. **Structure**: Each item must have:
           - "id": "TC001", "TC002", etc.
           - "title": "Short descriptive title"
           - "description": "Detailed description of what is being tested"
           - "steps": ["Step 1", "Step 2", ...]
           - "expected_result": "Final verification step"
        """
        
        return groq_smart(final_prompt)
