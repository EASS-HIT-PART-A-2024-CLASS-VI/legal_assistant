import logging
from typing import List, Optional, Type

from llama_index.core import Document, PromptTemplate, PropertyGraphIndex, Response
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.indices.property_graph import (
    BasePGRetriever,
    LLMSynonymRetriever,
    SchemaLLMPathExtractor,
    VectorContextRetriever,
)
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.graph_stores.falkordb import FalkorDBPropertyGraphStore
from llama_index.llms.gemini import Gemini
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class KnowledgeGraphIndex:
    def __init__(
        self,
        url: str,
        graph_name: str,
        information_extraction_llm,
        text_qa_template: PromptTemplate,
        refine_template: PromptTemplate,
        kg_triplets_extract_template: PromptTemplate,
        max_triplets_per_chunk: int,
        scheme_validation: bool,
        embedding_model: BaseEmbedding,
        documents: Optional[List[Document]] = None,
    ) -> None:
        self.graph_store = self._connect(graph_name=graph_name, url=url)
        self.information_extraction_llm = information_extraction_llm
        self.embedding_model = embedding_model
        self.text_qa_template = text_qa_template
        self.refine_template = refine_template
        self.kg_triplets_extract_template = kg_triplets_extract_template
        self.max_triplets_per_chunk = max_triplets_per_chunk
        self.documents = documents
        self.kg_index = self.get_kg_index()
        self.scheme_validation = scheme_validation
        self.update_kg_docs(documents=documents)

    @staticmethod
    def _connect(graph_name: str, url: str) -> FalkorDBPropertyGraphStore:
        try:
            logger.info(f"Connecting to FalkorDB at {url}, graph: {graph_name}")
            return FalkorDBPropertyGraphStore(url=url, database=graph_name)
        except Exception as e:
            logger.error(f"failed to connect db - {e}")

    def get_kg_index(
        self,
    ) -> Type[PropertyGraphIndex]:
        return PropertyGraphIndex

    def update_kg_docs(
        self,
        documents: List[Document],
    ) -> None:

        from typing import Literal

        entities_scheme = Literal[""]
        relations_scheme = Literal[""]
        kg_validation_schema = {  # <entity_type>: <relation_type>
            "": [],
        }

        kg_extractor = SchemaLLMPathExtractor(
            llm=self.information_extraction_llm,
            extract_prompt=self.kg_triplets_extract_template,
            num_workers=4,
            max_triplets_per_chunk=self.max_triplets_per_chunk,
            possible_entities=entities_scheme,
            possible_relations=relations_scheme,
            kg_validation_schema=kg_validation_schema,
            strict=self.scheme_validation,
        )
        kg_index_kwargs = {
            "documents": documents,
            "llm": self.information_extraction_llm,
            "kg_extractors": [kg_extractor],
            "property_graph_store": self.graph_store,
            "embed_model": self.embedding_model,
            "embed_kg_nodes": True,
            "show_progress": True,
        }
        self.kg_index = self.kg_index.from_documents(**kg_index_kwargs)
