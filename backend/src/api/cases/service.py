import logging

from fastapi import UploadFile
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE

from src.utils.api_error_response import ApiErrorException
from src.utils.logger import setup_logging
from src.engine.loaders.file_extractor import (
    DocxExtractor,
    PdfExtractor,
    TxtExtractor,
)
setup_logging()
logger = logging.getLogger(__name__)

CONTENT_TYPE_EXTRACTORS = {
    "application/pdf": PdfExtractor,
    "text/plain": TxtExtractor,
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": DocxExtractor,
}


async def extract_text_from_file(file: UploadFile) -> str:
    content_type = file.content_type
    logger.info(f"Processing file {file.filename} with content type {content_type}")
    if content_type in CONTENT_TYPE_EXTRACTORS:
        extractor = CONTENT_TYPE_EXTRACTORS[content_type](file)
        return await extractor.extract()
    else:
        raise ApiErrorException(error_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE, message="Unsupported file type")