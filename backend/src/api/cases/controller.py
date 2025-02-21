import logging

from src.api.cases import service
from src.api.cases.consts import question_template
from src.api.cases.model import RagResponseMod
from src.engine.rag_pipeline import RagPipeline
from src.utils.db_client import FalkorDBClient
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


async def create_new_case(case_name, files):
    logger.debug(f"uploading files {files}")
    documents = []
    for file in files:
        logger.info(f"starting to process file {file.filename}")
        text = await service.extract_text_from_file(file)
        document = {
            "text": text,
            "file_name": file.filename,
            "file_type": file.content_type,
        }
        documents.append(document)
    logger.info(f"Number of Documents: {len(documents)}")
    rag_pipeline = RagPipeline()
    rag_pipeline.handle(documents=documents, graph_name=case_name)


async def list_cases(db_client: FalkorDBClient):
    try:
        logger.info("Listing cases")
        res = await db_client.client.list_graphs()
        logger.debug(f"cases returned - {res}")
        return res
    except Exception as e:
        logger.error(f"Error while listing graphs {e}")
        return [""]


async def search(case_name: str, question: str, respond_mod: RagResponseMod):
    logger.info(f"Getting case - {case_name}")
    rag_pipeline = RagPipeline()
    case = rag_pipeline.get_existing_kg(case_name)
    question, suggested_question_exist = service.get_suggested_questions(question)
    if suggested_question_exist:
        answer = rag_pipeline.query(kg_index=case, question=question, respond_mod=respond_mod)
    else:
        default_formatted_question = question_template.format(user_question=question)
        answer = rag_pipeline.query(kg_index=case, question=default_formatted_question, respond_mod=respond_mod)
    return answer.response
