from llama_index.core import Document
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.gemini import Gemini
from src.engine.knowledge_graph import KnowledgeGraphIndex
from src.engine.llm_client_factory import get_client, get_embedding_client
from src.engine.prompts import (
    kg_triplets_extract_template,
    refine_template,
    text_qa_template,
)
from src.env import configuration

class RagPipeline:
    def __init__(self):
        self.llm = Gemini(model="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)
        self.embed_model = GeminiEmbedding(model_name="models/gemini-1.5-flash", api_key=GOOGLE_API_KEY)

    @staticmethod
    def _create_documents(documents):
        rag_documents = []
        for document in documents:
            rag_document = Document(
                text_resource=document["text"],
                metadata={"file_name": document["file_name"], "file_type": document["file_type"], "id": document["id"], "category": "legal"},
                excluded_llm_metadata_keys=["id"],
            )
            rag_documents.append(rag_document)
        return rag_documents

    def handle(self, documents, graph_name):
        self._create_documents(documents)
        knowledge_graph = KnowledgeGraphIndex(
            url=configuration.falkordb_uri,
            graph_name=graph_name,
            embedding_model=get_embedding_client(),
            information_extraction_llm=get_client(),
            text_qa_template=text_qa_template,
            kg_triplets_extract_template=kg_triplets_extract_template,
            refine_template=refine_template,
            max_triplets_per_chunk=10,
            scheme_validation=False,
        )
