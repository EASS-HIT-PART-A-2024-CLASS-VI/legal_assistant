import pytest
from typing import List, Dict, Any
from llama_index.core import Document

from src.engine.rag_pipeline import RagPipeline


class TestRagPipeline:
    DEFAULT_CATEGORY = "legal"
    EXCLUDED_METADATA = ["id"]

    @pytest.fixture
    def sample_documents_input(self) -> List[Dict[str, str]]:
        return [
            {
                "text": "Sample text 1",
                "file_name": "file1.txt",
                "file_type": "txt",
            },
            {
                "text": "Sample text 2",
                "file_name": "file2.docx",
                "file_type": "docx",
            },
        ]

    @pytest.fixture
    def expected_documents(self, sample_documents_input) -> List[Document]:
        return [
            Document(
                text=doc["text"],
                metadata={
                    "file_name": doc["file_name"],
                    "file_type": doc["file_type"],
                    "category": self.DEFAULT_CATEGORY,
                },
                excluded_llm_metadata_keys=self.EXCLUDED_METADATA,
            )
            for doc in sample_documents_input
        ]

    def _assert_documents_equal(self, result_docs: List[Document],
                                expected_docs: List[Document]) -> None:
        assert len(result_docs) == len(expected_docs)
        for res, exp in zip(result_docs, expected_docs):
            assert res.text == exp.text
            assert res.metadata == exp.metadata
            assert res.excluded_llm_metadata_keys == exp.excluded_llm_metadata_keys

    def test_should_create_documents_successfully(self, sample_documents_input,
                                                  expected_documents):
        result = RagPipeline._create_documents(sample_documents_input)
        self._assert_documents_equal(result, expected_documents)

    def test_should_return_empty_list_for_empty_input(self):
        result = RagPipeline._create_documents([])
        assert result == []
