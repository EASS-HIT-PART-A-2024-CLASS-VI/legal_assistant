from typing import List, Type

from llama_index.core import PropertyGraphIndex
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.indices.property_graph import (
    BasePGRetriever,
    LLMSynonymRetriever,
    VectorContextRetriever,
)
from llama_index.embeddings.gemini import GeminiEmbedding
from src.engine.retrievers import synonyms_retriever


class RagRetriever:
    def __init__(
        self,
        kg_index: PropertyGraphIndex,
        embedding_model: BaseEmbedding = GeminiEmbedding(
            model_name="text-embedding-3-small"
        ),
    ):
        self.kg_index = kg_index

    def _get_sub_retrievers(
        self, similarity_top_k_nodes: int
    ) -> List[Type[BasePGRetriever]]:
        return [
            VectorContextRetriever(
                self.graph_store,
                # only needed when the graph store doesn't support vector queries
                # vector_store=index.vector_store,
                embed_model=self.embedding_model,
                # include source chunk text with retrieved paths
                include_text=True,
                # the number of nodes to fetch
                similarity_top_k=similarity_top_k_nodes,
                # the depth of relations to follow after node retrieval
                path_depth=1,
                # can provide any other kwargs for the VectorStoreQuery class
            ),
            LLMSynonymRetriever(
                self.graph_store,
                llm=self.retriever_llm,
                # include source chunk text with retrieved paths
                include_text=True,
                synonym_prompt=synonyms_retriever.prompt,
                output_parsing_fn=synonyms_retriever.parse_fn,
                max_keywords=10,
                # the depth of relations to follow after node retrieval
                path_depth=1,
            ),
        ]

    def query(self, question: str, response_mode: str, similarity_top_k_nodes: int):
        response = self.kg_index.as_query_engine(
            llm=self.retriever_llm,
            sub_retrievers=self._get_sub_retrievers(
                similarity_top_k_nodes=similarity_top_k_nodes
            ),
        ).query(question)
        return response
