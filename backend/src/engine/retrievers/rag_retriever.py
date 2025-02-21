from llama_index.core import PropertyGraphIndex
from llama_index.core.indices.property_graph import (
    LLMSynonymRetriever,
    VectorContextRetriever,
)
from src.engine.retrievers import synonyms_retriever


class RagRetriever:
    def __init__(self, kg_index: PropertyGraphIndex, retriever_llm, embedding_model):
        self.kg_index = kg_index
        self.retriever_llm = retriever_llm
        self.graph_store = kg_index.property_graph_store
        self.embedding_model = embedding_model

    def _get_sub_retrievers(self, similarity_top_k_nodes: int) -> list[VectorContextRetriever | LLMSynonymRetriever]:
        return [
            VectorContextRetriever(
                self.graph_store,
                embed_model=self.embedding_model,
                include_text=True,
                similarity_top_k=similarity_top_k_nodes,
                path_depth=1,
            ),
            LLMSynonymRetriever(
                self.graph_store,
                llm=self.retriever_llm,
                include_text=True,
                synonym_prompt=synonyms_retriever.prompt,
                output_parsing_fn=synonyms_retriever.parse_fn,
                max_keywords=10,
                path_depth=1,
            ),
        ]

    def query(self, question: str, response_mode: str, similarity_top_k_nodes: int = 4):
        response = self.kg_index.as_query_engine(
            llm=self.retriever_llm,
            response_mode=response_mode,
            sub_retrievers=self._get_sub_retrievers(similarity_top_k_nodes=similarity_top_k_nodes),
        ).query(question)
        return response
