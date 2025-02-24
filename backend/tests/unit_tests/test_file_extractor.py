from unittest.mock import Mock, AsyncMock, patch
import pytest
from src.engine.loaders.file_extractor import PdfExtractor, TxtExtractor, DocxExtractor
from src.utils.api_error_response import ApiErrorException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

MOCK_PDF_PAGE1_TEXT = "First page text."
MOCK_PDF_PAGE2_TEXT = "Second page text."
MOCK_TXT_CONTENT = "Sample text content"
MOCK_DOCX_PARA1 = "First paragraph."
MOCK_DOCX_PARA2 = "Second paragraph."
MOCK_ERROR_MESSAGE = "Mocked exception"


@pytest.fixture
def mock_file():
    mock = Mock()
    mock.file = Mock()
    return mock


@pytest.fixture
def mock_async_file():
    return AsyncMock()


class TestPdfExtractor:
    @pytest.mark.asyncio
    async def test_extract_succeeds_with_multiple_pages(self, mock_file):
        mock_pdf_reader = self._create_mock_pdf_reader([
            MOCK_PDF_PAGE1_TEXT,
            MOCK_PDF_PAGE2_TEXT
        ])

        with patch("src.engine.loaders.file_extractor.PdfReader", return_value=mock_pdf_reader):
            pdf_extractor = PdfExtractor(file=mock_file)
            result = await pdf_extractor.extract()

        assert result == f"{MOCK_PDF_PAGE1_TEXT}{MOCK_PDF_PAGE2_TEXT}"

    @pytest.mark.asyncio
    async def test_extract_returns_empty_string_for_empty_pdf(self, mock_file):
        mock_pdf_reader = self._create_mock_pdf_reader([])

        with patch("src.engine.loaders.file_extractor.PdfReader", return_value=mock_pdf_reader):
            pdf_extractor = PdfExtractor(file=mock_file)
            result = await pdf_extractor.extract()

        assert result == ""

    @pytest.mark.asyncio
    async def test_extract_raises_api_error_on_exception(self, mock_file):
        with patch("src.engine.loaders.file_extractor.PdfReader",
                   side_effect=Exception(MOCK_ERROR_MESSAGE)):
            pdf_extractor = PdfExtractor(file=mock_file)

            with pytest.raises(ApiErrorException) as exc_info:
                await pdf_extractor.extract()

        assert exc_info.value.error_code == HTTP_500_INTERNAL_SERVER_ERROR
        assert f"Error processing PDF file: {MOCK_ERROR_MESSAGE}" in exc_info.value.message

    def _create_mock_pdf_reader(self, page_texts):
        mock_reader = Mock()
        mock_reader.pages = []
        for text in page_texts:
            page = Mock()
            page.extract_text.return_value = text
            mock_reader.pages.append(page)
        return mock_reader


class TestTxtExtractor:
    @pytest.mark.asyncio
    async def test_extract_succeeds_with_text_content(self, mock_async_file):
        mock_async_file.read.return_value = MOCK_TXT_CONTENT.encode()
        txt_extractor = TxtExtractor(file=mock_async_file)

        result = await txt_extractor.extract()

        assert result == MOCK_TXT_CONTENT


class TestDocxExtractor:
    @pytest.mark.asyncio
    async def test_extract_succeeds_with_multiple_paragraphs(self, mock_file):
        mock_document = self._create_mock_docx_document([
            MOCK_DOCX_PARA1,
            MOCK_DOCX_PARA2
        ])

        with patch("src.engine.loaders.file_extractor.DocxDocument", return_value=mock_document):
            docx_extractor = DocxExtractor(file=mock_file)
            result = await docx_extractor.extract()

        assert result == f"{MOCK_DOCX_PARA1}\n{MOCK_DOCX_PARA2}"

    def _create_mock_docx_document(self, paragraph_texts):
        mock_document = Mock()
        mock_document.paragraphs = []
        for text in paragraph_texts:
            paragraph = Mock()
            paragraph.text = text
            mock_document.paragraphs.append(paragraph)
        return mock_document
