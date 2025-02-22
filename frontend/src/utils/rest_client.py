import logging

import requests
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class RestClient:
    def __init__(self, base_url: str, timeout=30, headers=None):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout

    def get(self, endpoint, params=None):
        try:
            logger.info(f"getting request from  {endpoint}")
            response = requests.get(f"{self.base_url}/{endpoint}", headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(
                f"HTTP error occurred: {err}",
            )
            return {"error": f"HTTP error occurred: {err}"}
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            return {"error": f"HTTP error occurred: {err}"}

    def post(self, endpoint, data=None, json=None, files=None):
        try:
            logger.info(f"post request to  {endpoint}")
            response = requests.post(
                f"{self.base_url}/{endpoint}", headers=self.headers, data=data, json=json, files=files
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(
                f"HTTP error occurred: {err}",
            )
            return {"error": f"HTTP error occurred: {err}"}
        except Exception as err:
            logger.error(f"An error occurred: {err}")
            return {"error": f"HTTP error occurred: {err}"}

    def put(self, endpoint, data=None, json=None):
        try:
            logger.info(f"put request to  {endpoint}")
            response = requests.put(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                data=data,
                json=json,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(
                f"HTTP error occurred: {err}",
            )
        except Exception as err:
            logger.error(f"An error occurred: {err}")

    def delete(self, endpoint):
        try:
            logger.info(f"delete request to  {endpoint}")
            response = requests.delete(f"{self.base_url}/{endpoint}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            logger.error(
                f"HTTP error occurred: {err}",
            )
        except Exception as err:
            logger.error(f"An error occurred: {err}")
