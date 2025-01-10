import logging

from src.logger import setup_logging
from utils import status

setup_logging()
logger = logging.getLogger(__name__)


class ApiErrorException(Exception):
    """Encapsulates rest error return code"""

    def __init__(self, message, error_code=status.HTTP_500_INTERNAL_SERVER_ERROR, payload=None, log_message=True, log_stacktrace=True):
        """
        c'tor for ApiErrorException
        :param message: free text string describing the error
        :param error_code: http error code
        :param payload: serializable data object to be attached to the error.
        """
        if payload is None:
            payload = {}
        self.message = message
        if log_message:
            logger.error(f"API Error: {message}", exc_info=log_stacktrace)
        self.error_code = error_code
        self.payload = payload
