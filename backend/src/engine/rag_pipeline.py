from llama_index.core import Document
from src.engine.knowledge_graph import KnowledgeGraphConfig, KnowledgeGraphCreator
from src.engine.llm_client_factory import get_client, get_embedding_client
from src.engine.prompts import (
    kg_triplets_extract_template,
    refine_template,
    text_qa_template,
)
from src.env import configuration


class RagPipeline:
    def __init__(self):
        self.llm = get_client()
        self.embed_model = get_embedding_client()

    @staticmethod
    def _create_documents(documents):
        rag_documents = []
        for document in documents:
            rag_document = Document(
                text=document["text"],
                metadata={
                    "file_name": document["file_name"],
                    "file_type": document["file_type"],
                    "category": "legal",
                },
                excluded_llm_metadata_keys=["id"],
            )
            rag_documents.append(rag_document)
        return rag_documents

    def handle(self, documents, graph_name):
        rag_documents = self._create_documents(documents)
        kg_config = KnowledgeGraphConfig(
            url=configuration.falkordb_uri,
            graph_name=graph_name,
            embedding_model=self.embed_model,
            information_extraction_llm=self.llm,
            text_qa_template=text_qa_template,
            kg_triplets_extract_template=kg_triplets_extract_template,
            refine_template=refine_template,
            max_triplets_per_chunk=10,
            scheme_validation=False,
            documents=rag_documents,
        )
        KnowledgeGraphCreator(kg_config).create_kg()
