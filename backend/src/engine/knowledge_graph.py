import logging
from dataclasses import dataclass
from typing import List, Literal, Optional

from llama_index.core import Document, PromptTemplate, PropertyGraphIndex
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.indices.property_graph import SchemaLLMPathExtractor
from llama_index.core.llms import LLM
from llama_index.graph_stores.falkordb import FalkorDBPropertyGraphStore
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@dataclass
class KnowledgeGraphConfig:
    url: str
    graph_name: str
    information_extraction_llm: LLM
    text_qa_template: PromptTemplate
    refine_template: PromptTemplate
    kg_triplets_extract_template: PromptTemplate
    max_triplets_per_chunk: int
    scheme_validation: bool
    embedding_model: BaseEmbedding
    documents: Optional[List[Document]] = None


class KnowledgeGraphIndexBase:
    def __init__(self, config: KnowledgeGraphConfig) -> None:
        self.graph_store = self.connect_to_graph_store(config.graph_name, config.url)
        self.information_extraction_llm = config.information_extraction_llm
        self.embedding_model = config.embedding_model
        self.text_qa_template = config.text_qa_template
        self.refine_template = config.refine_template
        self.kg_triplets_extract_template = config.kg_triplets_extract_template
        self.max_triplets_per_chunk = config.max_triplets_per_chunk
        self.documents = config.documents
        self.scheme_validation = config.scheme_validation

    @staticmethod
    def connect_to_graph_store(graph_name: str, url: str) -> FalkorDBPropertyGraphStore:
        try:
            logger.info(f"Connecting to FalkorDB at {url}, graph: {graph_name}")
            return FalkorDBPropertyGraphStore(url=url, database=graph_name)
        except Exception as e:
            logger.error(f"Failed to connect to the database - {e}")
            raise


class KnowledgeGraphCreator(KnowledgeGraphIndexBase):
    def __init__(self, config: KnowledgeGraphConfig) -> None:
        super().__init__(config)

    def create_kg(self) -> None:
        entities_scheme = Literal[""]
        relations_scheme = Literal[""]
        kg_validation_schema = {"": []}  # <entity_type>: <relation_type>
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
        kg_index_kwargs = {"embed_kg_nodes": True}
        PropertyGraphIndex.from_documents(
            self.documents,
            embed_model=self.embedding_model,
            kg_extractors=[kg_extractor],
            property_graph_store=self.graph_store,
            show_progress=True,
            kwargs=kg_index_kwargs,
        )


class KnowledgeGraphRetriever(KnowledgeGraphIndexBase):
    def __init__(self, config: KnowledgeGraphConfig) -> None:
        super().__init__(config)
        self.retrieve_kg_index()

    def retrieve_kg_index(self):
        return PropertyGraphIndex.from_existing(
            property_graph_store=self.graph_store,
            llm=self.information_extraction_llm,
            embed_model=self.embedding_model,
            embed_kg_nodes=True,
        )
