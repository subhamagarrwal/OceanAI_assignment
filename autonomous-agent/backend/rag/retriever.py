class ChromaRetriever:
    def __init__(self, collection, embed_model, k=3):
        self.collection = collection
        self.embed_model = embed_model
        self.k = k

    def retrieve(self, query_bundle):
        from llama_index.core.schema import NodeWithScore, TextNode
        
        q_emb = self.embed_model.encode(query_bundle.query_str).tolist()
        
        results = self.collection.query(
            query_embeddings=[q_emb],
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
