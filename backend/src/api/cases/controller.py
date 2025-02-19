import logging
import uuid


from src.api.cases import service
from src.engine.rag_pipeline import RagPipeline
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

async def create_new_case(case_name, files):
    logger.debug(f"uploading files {files}")
    documents = []
    for file in files:
        logger.info(f"starting to process file {file.filename}")
        text = await service.extract_text_from_file(file)
        document = { "text": text , "file_name": file.filename , 'file_type': file.content_type, 'id': uuid.uuid4() }
        documents.append(document)
    logger.info(f'Number of Documents: {len(documents)}')
    rag_pipeline = RagPipeline()
    rag_pipeline.handle(documents=documents, graph_name=case_name)
