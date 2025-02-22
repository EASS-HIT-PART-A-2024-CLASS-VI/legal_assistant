import logging

from src.utils.logger import setup_logging
from src.utils.rest_client import RestClient

setup_logging()
logger = logging.getLogger(__name__)


class CaseService:
    def __init__(self, fastapi_uri: str):
        self.rest_client = RestClient(base_url=fastapi_uri, headers={})

    def get_names_cases(self):
        logger.info("Getting names")
        endpoint = "/api/v1/cases/list_cases"
        response = self.rest_client.get(endpoint)
        return response

    def answer_question(self, user_question: str, case_name: str, selected_method: str):
        logger.info(f"Asking question for case {case_name}")
        endpoint = f"/api/v1/cases/{case_name}/search"
        payload = {"question": user_question, "response_mod": selected_method}
        response = self.rest_client.post(endpoint, json=payload)
        return response

    def upload_case(self, case_name: str, files):
        logger.info(f"uploaded files - {files}")
        endpoint = "/api/v1/cases/create_new_case"
        payload = {"case_name": case_name}
        response = self.rest_client.post(endpoint, data=payload, files=files)
        return response

    def get_graph(self, case_name: str):
        logger.info(f"Getting graph for case {case_name}")
        endpoint = f"/graph/{case_name}"
        response = self.rest_client.get(endpoint)
        return response

    def get_generate_answer_graph(self, case_name: str, question: str, answer: str):
        logger.info(f"Getting answer graph for case {case_name}")
        endpoint = f"cases/{case_name}/generate_graph"
        payload = {"question": question, "answer": answer}
        response = self.rest_client.post(endpoint, json=payload)
        return response

    def delete_case(self, case_name: str):
        logger.info(f"Deleting case - {case_name}")
        endpoint = f"/graph/{case_name}"
        response = self.rest_client.delete(endpoint)
        return response
