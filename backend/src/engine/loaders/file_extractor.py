import logging
from abc import ABC, abstractmethod

from docx import Document as DocxDocument
from fastapi import UploadFile
from pypdf import PdfReader
from src.utils.api_error_response import ApiErrorException
from src.utils.logger import setup_logging
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

setup_logging()
logger = logging.getLogger(__name__)


class FileExtractor(ABC):

    def __init__(self, file: UploadFile):

        self.file = file

    @abstractmethod
    async def extract(self) -> str:
        """
        Abstract method to extract text from the file.
        """


class DocxExtractor(FileExtractor):

    async def extract(self) -> str:
        try:
            logger.info("Processing DOCX file...")
            doc = DocxDocument(self.file.file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise ApiErrorException(
                error_code=HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Error processing DOCX file: {e}",
            )


class TxtExtractor(FileExtractor):
    async def extract(self) -> str:
        try:
            logger.info("Processing text file...")
            content = await self.file.read()
            return content.decode("utf-8")
        except Exception as e:
            raise ApiErrorException(
                error_code=HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Error processing text file: {e}",
            )


class PdfExtractor(FileExtractor):

    async def extract(self) -> str:
        try:
            logger.info("Processing PDF file...")
            pdf_reader = PdfReader(self.file.file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
            return text
        except Exception as e:
            raise ApiErrorException(
                error_code=HTTP_500_INTERNAL_SERVER_ERROR,
                message=f"Error processing PDF file: {e}",
            )
