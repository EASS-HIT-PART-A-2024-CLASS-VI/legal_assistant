from unittest.mock import Mock, AsyncMock
import pytest
from fastapi import UploadFile
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE
from src.api.cases.consts import SUGGESTED_QUESTION
from src.api.cases.service import get_suggested_questions, CONTENT_TYPE_EXTRACTORS, extract_text_from_file
from src.utils.api_error_response import ApiErrorException

TEST_QUESTION = "example question"
TEST_SUGGESTION = "example suggested question"
TEST_EXTRACTED_TEXT = "Extracted text content"
TEST_UNKNOWN_QUESTION = "non-matching question"


class TestQuestionService:
    @pytest.fixture
    def mock_upload_file(self):
        def _create_mock_file(content_type: str, filename: str) -> Mock:
            mock_file = Mock(spec=UploadFile)
            mock_file.content_type = content_type
            mock_file.filename = filename
            return mock_file

        return _create_mock_file

    @pytest.fixture
    def mock_text_extractor(self):
        mock_extractor = AsyncMock()
        mock_extractor.extract.return_value = TEST_EXTRACTED_TEXT
        return mock_extractor

    def test_get_suggested_questions_when_question_exists(self):
        SUGGESTED_QUESTION[TEST_QUESTION] = TEST_SUGGESTION
        result = get_suggested_questions(TEST_QUESTION)
        assert result == (TEST_SUGGESTION, True)

    def test_get_suggested_questions_when_question_not_exists(self):
        result = get_suggested_questions(TEST_UNKNOWN_QUESTION)
        assert result == (TEST_UNKNOWN_QUESTION, False)

    @pytest.mark.asyncio
    async def test_extract_text_from_pdf_file(self, mock_upload_file, mock_text_extractor):
        mock_file = mock_upload_file("application/pdf", "test.pdf")
        CONTENT_TYPE_EXTRACTORS["application/pdf"] = lambda _: mock_text_extractor

        result = await extract_text_from_file(mock_file)

        assert result == TEST_EXTRACTED_TEXT
        mock_text_extractor.extract.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_text_from_txt_file(self, mock_upload_file, mock_text_extractor):
        mock_file = mock_upload_file("text/plain", "test.txt")
        CONTENT_TYPE_EXTRACTORS["text/plain"] = lambda _: mock_text_extractor

        result = await extract_text_from_file(mock_file)

        assert result == TEST_EXTRACTED_TEXT
        mock_text_extractor.extract.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_text_raises_error_for_unsupported_file_type(self, mock_upload_file):
        mock_file = mock_upload_file("application/unknown", "test.unknown")

        with pytest.raises(ApiErrorException) as exc_info:
            await extract_text_from_file(mock_file)

        assert exc_info.value.error_code == HTTP_415_UNSUPPORTED_MEDIA_TYPE
