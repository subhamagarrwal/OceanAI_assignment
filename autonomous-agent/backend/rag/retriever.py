from llama_index.core.retrievers import BaseRetriever
from llama_index.core.vector_stores import VectorStoreQuery
from llama_index.core import QueryBundle
from llama_index.core.schema import NodeWithScore

class PGVectorRetriever(BaseRetriever):
    def __init__(self, vector_store, embed_model, k=3):
        super().__init__()
        self.vector_store = vector_store
        self.embed_model = embed_model
        self.k = k

    def _retrieve(self, query_bundle: QueryBundle):
        q_emb = self.embed_model.encode(query_bundle.query_str).tolist()
        q = VectorStoreQuery(query_embedding=q_emb, similarity_top_k=self.k)
        result = self.vector_store.query(q)

        out = []
        for node, score in zip(result.nodes, result.similarities):
            out.append(NodeWithScore(node=node, score=score))
        return out
