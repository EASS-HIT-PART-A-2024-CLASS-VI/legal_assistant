import logging

from falkordb.asyncio import FalkorDB
from src.utils.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class FalkorDBClient(metaclass=Singleton):
    def __init__(self, host: str = "localhost", port: int = 6379) -> None:
        self.client = self._connect(host, port)

    def _connect(self, host: str, port: int) -> FalkorDB:
        try:
            logger.info(f"Connecting to FalkorDB at {host}:{port}")
            return FalkorDB(host=host, port=port)
        except Exception as e:
            logger.error(f"Exception - {e}")
            raise

    async def query(self, graph_query: str, graph_name):
        try:
            graph = self.client.select_graph(graph_name)
            logger.info(f"Querying FalkorDB graph - {graph_name}")
            response = await graph.query(graph_query)
            return response.result_set
        except Exception as e:
            logger.error(f"Exception - {e}")
            raise

    async def delete(self, graph_name) -> None:
        try:
            graph = self.client.select_graph(graph_name)
            await graph.delete()
        except Exception as e:
            logger.error(f"Exception - {e}")
