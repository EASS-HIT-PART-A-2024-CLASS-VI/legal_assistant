import logging

from fastapi import UploadFile
from src.api.cases.consts import SUGGESTED_QUESTION
from src.api.cases.model import Node, Relationship, GraphData
from src.engine.loaders.file_extractor import DocxExtractor, PdfExtractor, TxtExtractor
from src.utils.api_error_response import ApiErrorException
from src.utils.logger import setup_logging
from starlette.status import HTTP_415_UNSUPPORTED_MEDIA_TYPE

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


def get_suggested_questions(question: str) -> tuple[str, bool] | str:
    logger.info(f"Getting suggestions for {question}")
    suggested_question_text = SUGGESTED_QUESTION.get(question)
    if suggested_question_text:
        return suggested_question_text, True

    return question, False

def transform_graph_data(raw_data) -> GraphData:
    entities_dict = {}
    relationships = []

    for node_data, relation_data in raw_data:
        node_id = str(node_data["node_id"])
        if node_id not in entities_dict:
            entities_dict[node_id] = Node(
                labels=["ENTITY"],
                id=node_id,
                properties={k: v for k, v in node_data.items() if k != "embedding"}
            )

        relationships.append(
            Relationship(
                relation=relation_data.relation,
                src_node=str(relation_data.src_node),
                dest_node=str(relation_data.dest_node),
            )
        )

    return GraphData(
        relationships=relationships,
        entities=list(entities_dict.values())
    )