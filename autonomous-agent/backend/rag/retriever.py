class ChromaRetriever:
    def __init__(self, collection, k=3):
        """
        Initialize retriever with ChromaDB collection.
        """
        self.collection = collection
        self.k = k

    def retrieve(self, query_bundle):
        from llama_index.core.schema import NodeWithScore, TextNode
        
        # Use ChromaDB's built-in embeddings
        results = self.collection.query(
            query_texts=[query_bundle.query_str],
            n_results=self.k
        )
        
        out = []
        if results and results["documents"] and len(results["documents"]) > 0:
            for i, doc_text in enumerate(results["documents"][0]):
                distance = results["distances"][0][i] if results["distances"] else 0
                similarity = 1 - distance
                
                node = TextNode(text=doc_text)
                out.append(NodeWithScore(node=node, score=similarity))
        
        return out
